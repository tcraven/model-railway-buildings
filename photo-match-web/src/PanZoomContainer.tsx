import { FunctionComponent, MouseEventHandler, ReactElement, useRef, useState } from 'react';
import useResizeObserver from '@react-hook/resize-observer';
import { ControlMode, Dimensions, Rect, ViewTransform } from './types';
import { getDimensionsStyle, getScaledRect } from './utils';
import { Controls } from './Controls';
import { Lines } from './Lines';
import { Overview } from './Overview';
import { Photo } from './Photo';
import { ThreeView } from './ThreeView';

export const PanZoomContainer: FunctionComponent<{}> = (): ReactElement => {

    const overviewSizeRatio = 0.2;

    const photoImageDimensions: Dimensions = {
        width: 598,
        height: 412 // 600
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

    const [controlMode, setControlMode] = useState<string>(
        ControlMode.PAN_ZOOM_2D);

    // Position and scale of the view (considering the photo image to be
    // fixed size, and the view a float window that moves around on top of
    // the photo image).
    // The origin is the center of the photo image.
    // Coordinates go from (-1, -1) to (1, 1)
    const [viewTransform, setViewTransform] = useState<ViewTransform>({
        x: 0,
        y: 0,
        scale: 1
    });

    // Gets a rect for the photo image, scaled to fit exactly inside
    // the container (how it would be sized if zoom level is 1)
    const getPhotoRect = (): Rect => {
        const scale = Math.min(
            containerDimensions.height / photoImageDimensions.height,
            containerDimensions.width / photoImageDimensions.width
        );
        const w = scale * photoImageDimensions.width;
        const h = scale * photoImageDimensions.height;
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

        setViewTransform({
            x: nx,
            y: ny,
            scale: ns
        });
    };

    const getViewTransformXYfromClientXY = (clientX: number, clientY: number): { x: number; y: number; } => {
        const vpx = clientX - 0.5 * containerDimensions.width;
        const vpy = 0.5 * containerDimensions.height - clientY;
        const vr = getViewRect();
        const pr = getPhotoRect();
        const scale = Math.max(pr.width / vr.width, pr.height / vr.height);
        const vtx = 2 * vpx / scale / containerDimensions.width;
        const vty = 2 * vpy / scale / containerDimensions.height;
        return {
            x: vtx,
            y: vty
        };
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

    const onWheelCapture = (event: React.WheelEvent) => {
        if (controlMode !== ControlMode.PAN_ZOOM_2D) {
            return;
        }
        const k = 0.002;
        const ds = 1 + k * event.deltaY;
        updateViewTransform(0, 0, ds);
    };

    return (
        <div
            ref={ref}
            className="pm-pan-zoom-container"
            onMouseMove={onMouseMove}
            onWheelCapture={onWheelCapture}
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
                    containerDimensions={containerDimensions}
                    photoRect={getPhotoRect()}
                    cssTransform={getCssTransform()}
                    isOrbitEnabled={controlMode === ControlMode.ORBIT_3D}
                />
                <Lines
                    boundary={getPhotoRect()}
                />
                <Overview
                    dimensions={getOverviewDimensions()}
                    photoRect={getOverviewPhotoRect()}
                    viewRect={getOverviewViewRect()}
                />
                <Controls
                    controlMode={controlMode}
                    setControlMode={setControlMode}
                />
            </div>
        </div>
    );
};
