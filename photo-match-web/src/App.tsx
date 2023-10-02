import { FunctionComponent, ReactElement, useState } from 'react';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import './App.css';
import CssBaseline from '@mui/material/CssBaseline';
import LinearProgress from '@mui/material/LinearProgress';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { DataProvider, useData } from './DataContext';
import { PanZoomContainer } from './PanZoomContainer';
import { PhotoList } from './PhotoList';
import { isReady } from './utils';

const darkTheme = createTheme({ palette: { mode: 'dark' } });

const App: FunctionComponent = (): ReactElement => {
    return (
        <ThemeProvider theme={darkTheme}>
            <CssBaseline />
            <DataProvider>
                <Container />
            </DataProvider>
        </ThemeProvider>
    );
};

const Container: FunctionComponent = (): ReactElement => {
    const { data } = useData();

    if (!isReady(data)) {
        return (
            <div className="pm-app">
                <div className="pm-app-loader">
                    <LinearProgress />
                </div>
            </div>
        );
    }

    return (
        <div className="pm-app">
            <PhotoList />
            <PanZoomContainer />
        </div>
    );
};

export default App;
