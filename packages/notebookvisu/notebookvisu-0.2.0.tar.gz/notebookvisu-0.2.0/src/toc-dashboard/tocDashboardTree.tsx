import React, { useEffect, useState, useRef } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';
import { NotebookPanel } from '@jupyterlab/notebook';
import { INotebookHeading } from '../utils/headings';
import { TocDashboardItem } from './tocDashboardItem';
import { Signal } from '@lumino/signaling';
import { TocDashboardPanel } from './tocDashboardPanel';
import { ItemRenderer } from '../utils/interfaces';
import { ToolbarComponent } from './generator/toolbar_generator';
import { BACKEND_API_URL, Selectors } from '../utils/constants';
import { areListsEqual, hashCellList } from '../utils/utils';
import { LocationData } from '../redux/types';

interface ITOCTreeProps {
  title: string;
  headings: INotebookHeading[];
  entryClicked?: Signal<TocDashboardPanel, TocDashboardItem>;
  itemRenderer: ItemRenderer;
  Toolbar: ToolbarComponent | null;
  notebookPanel: NotebookPanel;
}

const TocDashboardTree: React.FC<ITOCTreeProps> = props => {
  const notebookCells = useRef<string[] | null | undefined>(null);
  // to abort ongoing API requests
  const fetchToCDataController = useRef<AbortController | undefined>();

  const refreshRequired = useSelector(
    (state: RootState) => state.tocdashboard.refreshBoolean
  );

  const shouldDisplayDashboardRedux = useSelector(
    (state: RootState) => state.tocdashboard.displayDashboard
  );

  const [locationData, setLocationData] = useState<LocationData>(null);

  // only fetch again when the list of cells actuall changed or when a refresh is requested
  useEffect(() => {
    // console.log('fetcTOCData()');
    fetchToCData();

    // cleanup callback function to abort ongoing requests and clear data
    return () => {
      abortController(
        notebookCells.current
          ? 'Aborted from useEffect with cells : ' +
              notebookCells.current.join(',')
          : 'Aborted from useEffect with no cells'
      );
      // console.log('locationData to null');
      setLocationData(null);
    };
  }, [notebookCells.current, refreshRequired]);

  ////////////////////////////////////////////////////////////////

  // update the list of notebook cells every time there is a potential change
  useEffect(() => {
    updateCellList();
  }, [props.headings, props.title, props.notebookPanel]);

  const abortController = (reason: string) => {
    // console.log('ABORT STARTED');
    if (fetchToCDataController.current) {
      fetchToCDataController.current.signal;
      fetchToCDataController.current.abort(reason);
    }
  };

  // const currentRequestId = useRef<number>(0);

  const fetchToCData = async (): Promise<void> => {
    abortController(
      notebookCells.current
        ? 'Aborted from fetchToCData with cells : ' +
            notebookCells.current.join(',')
        : 'Aborted from fetchToCData with no cells'
    );

    const notebookId = props.notebookPanel.model?.getMetadata(
      Selectors.notebookId
    );
    // only fetch if there is a notebook id, and there are cells
    if (!notebookId || !notebookCells.current) {
      return;
    }

    fetchToCDataController.current = new AbortController();
    const signal = fetchToCDataController.current.signal;

    try {
      // console.log('fetch() call ...');
      const response = await fetch(
        `${BACKEND_API_URL}/dashboard/toc/${notebookId}?hashedList=${hashCellList(
          notebookCells.current
        )}`,
        { signal: signal }
      );

      if (!signal.aborted) {
        // if (currentNumber === currentRequestId.current) {
        if (response.ok) {
          const data = await response.json();
          // process the response data and handle the different scenarios
          if (data.status === 'not_found') {
            // no entry found in the Notebook table for the notebook id
            // console.log('Notebook not registered');
          } else if (data.status === 'hash_mismatch') {
            // hash mismatch between the URL parameter and the notebook table entry
            // console.log('Cell list mismatch with the registered notebook');
          } else if (data.status === 'success') {
            // // console.log(
            //   'Location data fetched : ',
            //   data.data,
            //   '\nSignal : ',
            //   signal,
            //   '\nReason : ',
            //   signal.reason
            // );
            setLocationData(data.data);
            return;
          }
        } else {
          // console.log('Error:', response.status);
        }
      } else {
        // console.log(signal.reason);
      }
    } catch (error) {
      // console.log(
      //   'Toc Fetch Error:',
      //   error,
      //   '\nAborted when cells : ',
      //   signal.reason
      // );
    } finally {
      // reset the controller to allow new API calls
      fetchToCDataController.current = undefined;
    }
    // if it didn't fetch, set the fetched data to null
    setLocationData(null);
  };

  const updateCellList = (): boolean => {
    const cells = props.notebookPanel.model?.cells;
    if (cells) {
      const cellList = Array.from(cells).map(c => c.id);

      if (!areListsEqual(cellList, notebookCells.current)) {
        // console.log('UPDATE : Cell list changed : ', {
        //   new: cellList,
        //   old: notebookCells.current
        // });
        notebookCells.current = cellList;
        return true;
      } else {
        // console.log('UPDATE : Cell list unchanged : ', { current: cellList });
      }
    } else {
      notebookCells.current = null;
    }
    return false;
  };

  const aggregateCollapsedData = (): { [key: string]: number } => {
    // const haveCellsChanged = updateCellList();
    // if (!haveCellsChanged) {
    //   return {};
    // }

    const uncollapsedIds: string[] = props.headings.map(
      heading => heading.cellRef.model.id
    );
    const uniqueUncollapsedIds: string[] = [...new Set(uncollapsedIds)];

    const dict: { [key: string]: number } = {};
    const currentCells = notebookCells.current;
    if (currentCells && locationData) {
      const mapping: number[] = uniqueUncollapsedIds.map(id =>
        currentCells.indexOf(id)
      );

      dict['total_count'] = locationData.total_count;

      // adapt the boundaries
      mapping[0] = 0;
      mapping.push(currentCells.length - 1);

      for (let i = 0; i < uniqueUncollapsedIds.length; i++) {
        const start = mapping[i];
        const end = mapping[i + 1];
        let total = 0;
        if (start === -1) {
          // not found
          total = 0;
        } else {
          for (let j = start; j < end; j++) {
            total += locationData.location_count[currentCells[j]] || 0;
          }
        }
        dict[uniqueUncollapsedIds[i]] = total;
      }
    }

    return dict;
  };

  const renderedCells = new Set<string>();
  const aggregatedData = aggregateCollapsedData();

  return (
    <div className="dashboard-TableOfContents">
      <div className="dashboard-stack-panel-header">{props.title}</div>
      {props.Toolbar && <props.Toolbar />}
      <ul className="dashboard-TableOfContents-content">
        {props.headings.map((el, index) => {
          const cellId = el.cellRef.model.id;
          const isFirstCellOccurrence = !renderedCells.has(cellId);

          if (isFirstCellOccurrence) {
            renderedCells.add(cellId);
          }
          return (
            <TocDashboardItem
              heading={el}
              headings={props.headings}
              entryClicked={props.entryClicked}
              itemRenderer={props.itemRenderer}
              // only display the dashboard component when not disabled with redux, when it's the first cell occurrence and when there is data
              addReactComponent={shouldDisplayDashboardRedux && !!locationData}
              isFirstCellOccurrence={isFirstCellOccurrence}
              tocDashboardData={[
                aggregatedData[cellId],
                aggregatedData['total_count']
              ]}
              key={`${el.text}-${el.level}-${index++}`}
            />
          );
        })}
      </ul>
    </div>
  );
};

export default TocDashboardTree;
