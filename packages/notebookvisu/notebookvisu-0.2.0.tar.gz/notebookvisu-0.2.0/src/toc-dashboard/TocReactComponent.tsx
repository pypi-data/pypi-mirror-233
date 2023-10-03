import React from 'react';

const computeTransparency = (value: number, total: number): number => {
  const transparency: number = (3 * value) / total + 0.05;

  return Math.min(1, transparency);
};

interface ITocComponentProps {
  data: [number | null | undefined, number | null | undefined] | null;
  cellId: string;
}

const TocReactComponent = ({
  data,
  cellId
}: ITocComponentProps): JSX.Element => {
  // const getCurrentTime = (): string => {
  //   return new Date().toISOString().slice(17, 21);
  // };

  return (
    <>
      {data && data[0] && data[1] ? (
        <div
          className="dashboard-toc-react-component"
          style={{
            backgroundColor: `rgba(21, 92, 144, ${computeTransparency(
              data[0],
              data[1]
            )})`
          }}
        >
          <span className="dashboard-toc-react-text">
            {data[0] + '/' + data[1]}
          </span>
        </div>
      ) : (
        <div className="dashboard-toc-react-component"></div>
      )}
    </>
  );
};

export default TocReactComponent;
