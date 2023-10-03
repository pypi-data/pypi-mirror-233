import React, { useEffect, useState, useRef } from 'react';
import { NotebookPanel } from '@jupyterlab/notebook';
import NoNotebookPlaceholder from '../toc-dashboard/NoNotebookPlaceholder';
import { Provider } from 'react-redux';
import PageRouter from './PageRouter';
import { store } from '../redux/store';
import SidebarPlaceholder from './SidebarPlaceholder';
import { BACKEND_API_URL, Selectors } from '../utils/constants';
import { hashCellList } from '../utils/utils';
import Loader from './components/placeholder/Loader';

interface IDashboardProps {
  panel: NotebookPanel | null;
  cellIds: string[] | null;
}

const DashboardComponent = (props: IDashboardProps): JSX.Element => {
  const [isChecking, setIsChecking] = useState<boolean>(true);
  const [invalidity, setInvalidity] = useState<null | string>(null);
  const [hasValidNotebookId, setHasValidNotebookId] = useState<
    string | null | undefined
  >(null);
  // to abort ongoing API requests
  const fetchDataController = useRef<AbortController | undefined>();

  useEffect(() => {
    const fetchData = async () => {
      if (fetchDataController.current) {
        fetchDataController.current.abort();
      }

      let validNotebookId = null;
      let invalidityReason: string | null = 'No Notebook';
      if (props.panel && props.panel.model) {
        setIsChecking(true);
        // only fetch when the panel has finished building
        if (props.panel.context.isReady) {
          invalidityReason = 'Fetching Error';
          const notebookId = props.panel.model.getMetadata(
            Selectors.notebookId
          );

          try {
            fetchDataController.current = new AbortController();
            const signal = fetchDataController.current.signal;

            if (notebookId) {
              const response = await fetch(
                `${BACKEND_API_URL}/dashboard/check/${notebookId}?hashedList=${hashCellList(
                  props.cellIds
                )}`,
                { signal: signal }
              );

              if (!signal.aborted) {
                if (response.ok) {
                  const data = await response.json();
                  if (data.status === 'not_found') {
                    // no entry found in the Notebook table for the notebook id
                    invalidityReason = 'Notebook not Registered';
                  } else if (data.status === 'hash_mismatch') {
                    // hash mismatch between the URL parameter and the notebook table entry
                    invalidityReason = 'Mismatch with the Registered Notebook';
                  } else if (data.status === 'success') {
                    invalidityReason = null;
                    validNotebookId = notebookId;
                  }
                }
              }
            } else {
              invalidityReason = 'Untagged Notebook';
            }
          } catch (error) {
            console.log('(Check your connexion) ' + error);
          } finally {
            // reset the controller to allow new API calls
            fetchDataController.current = undefined;
            setIsChecking(false);
          }
        }
      }
      setInvalidity(invalidityReason);
      setHasValidNotebookId(validNotebookId);
    };

    // call the async fetch method
    fetchData();

    return () => {
      // clean up callback function
      if (fetchDataController.current) {
        fetchDataController.current.abort();
      }
    };
  }, [props.panel, props.cellIds]);

  return (
    <>
      {props.panel ? (
        <>
          {isChecking ? (
            <Loader />
          ) : (
            <>
              {invalidity ? (
                <SidebarPlaceholder title={invalidity} />
              ) : (
                <Provider store={store}>
                  <PageRouter
                    notebookId={hasValidNotebookId as string}
                    notebookName={props.panel.sessionContext.name}
                  />
                </Provider>
              )}
            </>
          )}
        </>
      ) : (
        <NoNotebookPlaceholder title={'Side Panel Dashboard'} />
      )}
    </>
  );
};

export default DashboardComponent;
