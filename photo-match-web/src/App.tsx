import { FunctionComponent, ReactElement } from 'react';
import './App.css';
import { PanZoomContainer } from './PanZoomContainer';


const App: FunctionComponent = (): ReactElement => {
    return (
        <div className="pm-app">
            <PanZoomContainer />
        </div>
    );
}

export default App;
