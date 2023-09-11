import React from 'react';
import {
    useRef,
    useState    
} from 'react';
import {
    FunctionComponent,
    ReactElement
} from 'react';
import useResizeObserver from '@react-hook/resize-observer';
import './App.css';

type RectStyle = {
    left: string,
    top: string,
    width: string,
    height: string
};

type DimensionsStyle = {
    width: string,
    height: string
};

type Dimensions = {
    width: number,
    height: number
};

type Rect = {
    x: number,
    y: number,
    width: number,
    height: number
};

type ViewTransform = {
    x: number,
    y: number,
    scale: number
};

const getDimensionsStyle = (dimensions: Dimensions): DimensionsStyle => {
    return {
        width: dimensions.width + 'px',
        height: dimensions.height + 'px'
    }
};

const getRectStyle = (rect: Rect, containerDimensions: Dimensions): RectStyle => {
    return {
        left: (0.5 * containerDimensions.width + rect.x - 0.5 * rect.width) + 'px',
        top: (0.5 * containerDimensions.height - rect.y - 0.5 * rect.height) + 'px',
        width: rect.width + 'px',
        height: rect.height + 'px'
    };
};

type PhotoProps = {
    containerDimensions: Dimensions,
    boundary: Rect
};
const Photo: FunctionComponent<PhotoProps> = (props): ReactElement => {
    return (
        <img
            className="pm-photo-img"
            src="photo-1.jpg"
            style={{
                ...getRectStyle(props.boundary, props.containerDimensions)
            }}
        />
    );
};


type ThreeViewProps = {
    boundary: Rect
};
const ThreeView: FunctionComponent<ThreeViewProps> = (props): ReactElement => {
    return (
        <div
            className="pm-three-view"
            style={{}}
        >
            ThreeView
        </div>
    );
};

type LinesProps = {
    boundary: Rect
};
const Lines: FunctionComponent<LinesProps> = (props): ReactElement => {
    return (
        <div
            className="pm-lines"
            style={{}}
        >
            Lines
        </div>
    );
};

type OverviewProps = {
    dimensions: Dimensions,
    photoRect: Rect,
    viewRect: Rect
};
const Overview: FunctionComponent<OverviewProps> = (props): ReactElement => {
    return (
        <div
            className="pm-overview"
            style={{
                ...getDimensionsStyle(props.dimensions)
            }}
        >
            <img
                className="pm-photo"
                src="photo-1.jpg"
                style={{
                    ...getRectStyle(props.photoRect, props.dimensions)
                }}
            />
            <div
                className="pm-view"
                style={{
                    ...getRectStyle(props.viewRect, props.dimensions)
                }}
            />
        </div>
    );
};


const Controls: FunctionComponent<{}> = (): ReactElement => {
    return (
        <div className="pm-controls">
            <button className="pm-button">A</button>
            <button className="pm-button">B</button>
            <button className="pm-button">C</button>
            <button className="pm-button">D</button>
            <button className="pm-button">E</button>
        </div>
    );
};


const PanZoomContainer: FunctionComponent<{}> = (): ReactElement => {
    
    const overviewSizeRatio = 0.2;

    const photoImageDimensions: Dimensions = {
        width: 598,  // 800,
        height: 412  // 600
    };

    // Width and height of the container, used to calculate positions and
    // sizes of child elements
    const [containerDimensions, setContainerDimensions] = useState<Dimensions>({
        width: 0,
        height: 0
    });

    // Update the container dimensions when the container resizes
    const ref = useRef(null);
    useResizeObserver(ref, (entry) => {
        setContainerDimensions({
            width: entry.contentRect.width,
            height: entry.contentRect.height
        });
    });

    // Returns the scale that fits the photo image into the container
    // (centered either vertically or horizonatally)
    const getImageFillScale = (): number => {
        return Math.min(
            containerDimensions.height / photoImageDimensions.height,
            containerDimensions.width / photoImageDimensions.width
        );
    };

    const getBoundedViewTransform = (vt: ViewTransform): ViewTransform => {
        const w = vt.scale * containerDimensions.width;
        const h = vt.scale * containerDimensions.height;
        const x = 0.5 * containerDimensions.width * vt.x;
        const y = 0.5 * containerDimensions.height * vt.y;
        const scale = getImageFillScale();
        const pw = scale * photoImageDimensions.width;
        const ph = scale * photoImageDimensions.height;
        console.log(vt, w / pw, h / ph);
        return vt;
    }

    // Position and scale of the view (considering the photo image to be
    // fixed size, and the view a float window that moves around on top of
    // the photo image).
    // The origin is the center of the photo image.
    // Coordinates go from (-1, -1) to (1, 1)
    const [viewTransform, setViewTransform] = useState<ViewTransform>({
        x: 0.0,
        y: 0.0,
        scale: 0.8
    });

    // Gets a rect for the photo image, scaled to fit exactly inside
    // the container (how it would be sized if zoom level is 1)
    const getPhotoRect = (): Rect => {
        const scale = getImageFillScale();
        const w = scale * photoImageDimensions.width;
        const h = scale * photoImageDimensions.height;
        const x = 0;
        const y = 0;
        return {
            x: x,
            y: y,
            width: w,
            height: h
        }
    };

    // Gets a rect for the view photo - the scaled photo that is much
    // larger than the container if the user is zoomed in
    const getViewPhotoRect = (): Rect => {
        const vr = getViewRect();
        const pr = getPhotoRect();
        const scale = Math.max(pr.width / vr.width, pr.height / vr.height);
        return {
            x: scale * -vr.x,
            y: scale * -vr.y,
            width: scale * pr.width,
            height: scale * pr.height
        };
    };

    const getOverviewDimensions = (): Dimensions => {
        return {
            width: overviewSizeRatio * containerDimensions.width,
            height: overviewSizeRatio * containerDimensions.height
        }
    };

    const getScaledRect = (rect: Rect, scale: number): Rect => {
        return {
            x: scale * rect.x,
            y: scale * rect.y,
            width: scale * rect.width,
            height: scale * rect.height
        }
    };

    const getOverviewPhotoRect = (): Rect => {
        return getScaledRect(getPhotoRect(), overviewSizeRatio);
    };

    // Get the view rect that represents the view area for the
    // current view transform
    const getViewRect = (): Rect => {
        const w = viewTransform.scale * containerDimensions.width;
        const h = viewTransform.scale * containerDimensions.height;
        const x = 0.5 * containerDimensions.width * viewTransform.x;
        const y = 0.5 * containerDimensions.height * viewTransform.y;
        return {
            x: x,
            y: y,
            width: w,
            height: h
        }
    };

    const getOverviewViewRect = (): Rect => {
        return getScaledRect(getViewRect(), overviewSizeRatio);
    };

    return (
        <div
            ref={ref}
            className="pm-pan-zoom-container"
        >
            <div
                className="pm-inner"
                style={{
                    ...getDimensionsStyle(containerDimensions)
                }}
            >
                <Photo
                    containerDimensions={containerDimensions}
                    boundary={getViewPhotoRect()}
                />
                <ThreeView
                    boundary={getPhotoRect()}
                />
                <Lines
                    boundary={getPhotoRect()}
                />
                <Overview
                    dimensions={getOverviewDimensions()}
                    photoRect={getOverviewPhotoRect()}
                    viewRect={getOverviewViewRect()}
                />
                <Controls />
            </div>
        </div>
    );
};


const App: FunctionComponent = (): ReactElement => {
    return (
        <div className="pm-app">
            <PanZoomContainer />
        </div>
    );
}

export default App;
