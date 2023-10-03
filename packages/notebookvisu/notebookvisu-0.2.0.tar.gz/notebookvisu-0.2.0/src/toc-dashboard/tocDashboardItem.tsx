import React from 'react';
import { INotebookHeading } from '../utils/headings';
import { Signal } from '@lumino/signaling';
import { TocDashboardPanel } from './tocDashboardPanel';
import { ItemRenderer } from '../utils/interfaces';
import TocReactComponent from './TocReactComponent';

interface ITocDashboardItemProps {
  heading: INotebookHeading;

  headings: INotebookHeading[];

  entryClicked?: Signal<TocDashboardPanel, TocDashboardItem>;

  itemRenderer: ItemRenderer;

  addReactComponent: boolean;

  isFirstCellOccurrence: boolean;

  tocDashboardData: [number | null | undefined, number | null | undefined];
}

export class TocDashboardItem extends React.Component<ITocDashboardItemProps> {
  render() {
    const {
      heading,
      headings,
      addReactComponent,
      isFirstCellOccurrence,
      tocDashboardData
    } = this.props;

    // create an onClick handler for the TOC item
    // that scrolls the anchor into view.
    const onClick = (event: React.SyntheticEvent<HTMLSpanElement>) => {
      event.preventDefault();
      event.stopPropagation();
      this.props.entryClicked?.emit(this);
      heading.onClick();
    };

    const content = this.props.itemRenderer(heading, headings);
    if (!content) {
      return null;
    }
    return (
      <li
        className="dashboard-tocItem"
        onClick={onClick}
        onContextMenu={(event: React.SyntheticEvent<HTMLSpanElement>) => {
          this.props.entryClicked?.emit(this);
          heading.onClick();
        }}
      >
        {content}
        {addReactComponent && (
          <TocReactComponent
            cellId={heading.cellRef.model.id}
            data={isFirstCellOccurrence ? tocDashboardData : null}
          />
        )}
      </li>
    );
  }
}

export default TocDashboardItem;
