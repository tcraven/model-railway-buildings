import { FunctionComponent, ReactElement, useRef, useState } from 'react';
import useResizeObserver from '@react-hook/resize-observer';
import { CameraMode, CameraTransform, ControlMode, Dimensions, Rect } from './types';
import { getDimensionsStyle, getFileUrl, getPhoto, getScaledRect, getScene } from './utils';
import { Controls } from './Controls';
import { LinesView } from './LinesView';
import { Overview } from './Overview';
import { Photo } from './Photo';
import { ThreeView } from './ThreeView';
import { useData } from './DataContext';

export const PanZoomContainer: FunctionComponent = (): ReactElement => {

    const overviewSizeRatio = 0.2;

    const ref = useRef(null);

    const { data, dispatch } = useData();
    const scene = getScene(data);
    const photo = getPhoto(scene);

    // Width and height of the container, used to calculate positions and
    // sizes of child elements
    const [containerDimensions, setContainerDimensions] = useState<Dimensions>({
        width: 0,
        height: 0
    });

    const controlMode = photo._uiData.controlMode;
    const photoOpacity = photo._uiData.photoOpacity;
    const modelOpacity = photo._uiData.modelOpacity;
    
    const [ cameraMode, setCameraMode ] = useState<string>(CameraMode.FREE);
    const [ cameraTransform, setCameraTransform ] = useState<CameraTransform>({
        fov: 50,
        position: { x: 200, y: 100, z: 400 },
        rotation: { x: -0.44497866312686412, y: 0.4516334410795318, z: 0.10867903971378184 }
    });

    // Position and scale of the view (considering the photo image to be
    // fixed size, and the view a float window that moves around on top of
    // the photo image).
    // The origin is the center of the photo image.
    // Coordinates go from (-1, -1) to (1, 1)
    const viewTransform = photo._uiData.viewTransform;

    // Update the container dimensions when the container resizes
    useResizeObserver(ref, (entry) => {
        setContainerDimensions({
            width: entry.contentRect.width,
            height: entry.contentRect.height
        });
    });

    // Gets a rect for the photo image, scaled to fit exactly inside
    // the container (how it would be sized if zoom level is 1)
    const getPhotoRect = (): Rect => {
        const scale = Math.min(
            containerDimensions.height / photo.height,
            containerDimensions.width / photo.width
        );
        const w = scale * photo.width;
        const h = scale * photo.height;
        return {
            x: 0,
            y: 0,
            width: w,
            height: h
        };
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
        };
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

    const getCssTransform = (): { x: number; y: number; scale: number; } => {
        const vr = getViewRect();
        const pr = getPhotoRect();
        const scale = Math.max(pr.width / vr.width, pr.height / vr.height);
        return {
            x: scale * -vr.x,
            y: scale * -vr.y,
            scale: scale
        };
    };

    const getOverviewDimensions = (): Dimensions => {
        return {
            width: overviewSizeRatio * containerDimensions.width,
            height: overviewSizeRatio * containerDimensions.height
        };
    };

    const getOverviewPhotoRect = (): Rect => {
        return getScaledRect(getPhotoRect(), overviewSizeRatio);
    };

    const getOverviewViewRect = (): Rect => {
        return getScaledRect(getViewRect(), overviewSizeRatio);
    };

    const updateViewTransform = (dx: number, dy: number, ds: number): void => {
        let nx = viewTransform.x + dx * viewTransform.scale;
        let ny = viewTransform.y + dy * viewTransform.scale;
        let ns = viewTransform.scale * ds;

        // Scale bounds
        const SCALE_MIN = 0.1;
        const SCALE_MAX = 1;
        if (ns > SCALE_MAX) { ns = SCALE_MAX; }
        if (ns < SCALE_MIN) { ns = SCALE_MIN; }

        // Position bounds
        const L = 1 - ns;
        if (nx < -L) { nx = -L; }
        if (nx > L) { nx = L; }
        if (ny < -L) { ny = -L; }
        if (ny > L) { ny = L; }

        dispatch({
            action: 'setViewTransform',
            viewTransform: {
                x: nx,
                y: ny,
                scale: ns
            }
        });
    };

    const onMouseMove = (event: React.MouseEvent) => {
        if (controlMode !== ControlMode.PAN_ZOOM_2D) {
            return;
        }
        if (event.buttons === 1) {
            const dx = -2 * event.movementX / containerDimensions.width;
            const dy = 2 * event.movementY / containerDimensions.height;
            updateViewTransform(dx, dy, 1);
        }
    };

    const onClick = (event: React.MouseEvent) => {
        const el: any = ref.current;
        const rect = el.getBoundingClientRect();
        const cx = event.pageX - rect.x - 0.5 * containerDimensions.width;
        const cy = 0.5 * containerDimensions.height + rect.y - event.pageY;
        const vpr = getViewPhotoRect();
        // (x, y) is the normalized mouse position in the image
        // in the range -1 < x < 1 and -1 < y < 1
        const x = 2 * (cx - vpr.x) / vpr.width;
        const y = 2 * (cy - vpr.y) / vpr.height;

        console.log(`{ x: ${Number(x.toFixed(4))}, y: ${Number(y.toFixed(4))} }`);
    };

    const onWheelCapture = (event: React.WheelEvent) => {
        if (controlMode !== ControlMode.PAN_ZOOM_2D) {
            return;
        }
        const k = 0.002;
        const ds = 1 + k * event.deltaY;
        updateViewTransform(0, 0, ds);
    };

    return (
        <div className="pm-pan-zoom-container">
            <div
                className="pm-pan-zoom"
                ref={ref}
                onMouseMove={onMouseMove}
                onWheelCapture={onWheelCapture}
                onClick={onClick}
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
                        opacity={photoOpacity}
                        imageUrl={getFileUrl(photo.filename)}
                    />
                    <LinesView
                        containerDimensions={containerDimensions}
                        photoRect={getPhotoRect()}
                        cssTransform={getCssTransform()}
                    />
                    <ThreeView
                        containerDimensions={containerDimensions}
                        photoRect={getPhotoRect()}
                        cssTransform={getCssTransform()}
                        cameraMode={cameraMode}
                        isOrbitEnabled={controlMode === ControlMode.ORBIT_3D}
                        opacity={modelOpacity}
                        cameraTransform={cameraTransform}
                    />
                    <Overview
                        dimensions={getOverviewDimensions()}
                        photoRect={getOverviewPhotoRect()}
                        viewRect={getOverviewViewRect()}
                        photoImageUrl={getFileUrl(photo.filename)}
                    />
                </div>
            </div>
            <div className="pm-controls-container">
                <Controls
                    cameraMode={cameraMode}
                    setCameraMode={setCameraMode}
                />
            </div>
        </div>
    );
};
