// definition file for the page content structures and other interfaces

interface NotebookLayer {
  pageName: 'Notebook';
}

interface CellLayer {
  pageName: 'Cell';
  content: {
    cellId: string;
  };
}

// discriminated union type, TypeScript will infer the correct type from pageName value. Will show an error if provided with an unknown pageName.
export type SideDashboardLayer = NotebookLayer | CellLayer;

export interface SideDashboardState {
  navigationState: SideDashboardLayer[];
  timeWindow: string;
  refreshBoolean: boolean;
}

// for ThemeReducer
export interface ThemeState {
  isThemeLight: boolean;
}

// for ToCReducer
export type LocationData = {
  location_count: { [key: string]: number };
  total_count: number;
} | null;

export interface ToCState {
  refreshBoolean: boolean;
  displayDashboard: boolean;
  hasNotebookId: boolean;
  locationData: LocationData;
}
