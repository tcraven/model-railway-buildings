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
        },
        {
            width: 1400,
            height: 1050,
            url: 'photo-4.jpg'
        },
        {
            width: 598,
            height: 413,
            url: 'photo-5.jpg'
        },
        {
            width: 3840,
            height: 2160,
            url: 'photo-6.png'
        },
        {
            width: 3034,
            height: 2334,
            url: 'photo-7.png'
        },
        {
            width: 598,
            height: 402,
            url: 'photo-8.jpg'
        },
        {
            width: 598,
            height: 436,
            url: 'photo-9.jpg'
        },
        {
            width: 1400,
            height: 1050,
            url: 'photo-10.jpg'
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
