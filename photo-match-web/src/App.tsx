import { FunctionComponent, ReactElement, useState } from 'react';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import './App.css';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { PanZoomContainer } from './PanZoomContainer';
import { PhotoImage } from './types';
import { PhotoList } from './PhotoList';

const darkTheme = createTheme({ palette: { mode: 'dark' } });

const App: FunctionComponent = (): ReactElement => {

    const photoImages: PhotoImage[] = [
        {
            width: 598,
            height: 412,
            url: 'photo-1.jpg'
        },
        {
            width: 598,
            height: 439,
            url: 'photo-2.jpg'
        },
        {
            width: 598,
            height: 376,
            url: 'photo-3.jpg'
        }
    ];
    const photoImage: PhotoImage = photoImages[2];

    const [ photoIndex, setPhotoIndex ] = useState<number>(0);

    const getPhotoImage = (): PhotoImage => {
        return photoImages[photoIndex];
    };

    return (
        <ThemeProvider theme={darkTheme}>
            <CssBaseline />
            <div className="pm-app">
                <PhotoList
                    photoImages={photoImages}
                    photoIndex={photoIndex}
                    setPhotoIndex={setPhotoIndex}
                />
                <PanZoomContainer
                    key={photoIndex}  // Forces full refresh?
                    photoImage={getPhotoImage()}
                />
            </div>
        </ThemeProvider>
    );
}

export default App;
