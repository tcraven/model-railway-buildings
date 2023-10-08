import { FunctionComponent, ReactElement, useRef, useState } from 'react';
import useResizeObserver from '@react-hook/resize-observer';
import { CameraMode, CameraTransform, ControlMode, Dimensions, LineEndpoint, Rect, Vector2D } from './types';
import { getDimensionsStyle, getDistanceSquared, getFileUrl, getPhoto, getScaledRect, getScene } from './utils';
import { Controls } from './Controls';
import { LinesView } from './LinesView';
import { Overview } from './Overview';
import { Photo } from './Photo';
import { ThreeView } from './ThreeView';
import { useData } from './DataContext';

export const PanZoomContainer: FunctionComponent = (): ReactElement => {

    const overviewSizeRatio = 0.2;

    const panZoomElementRef = useRef<HTMLDivElement | null>(null);
    const mouseDownPositionPixelsRef = useRef<Vector2D | null>(null);

    // Line endpoint that is being dragged
    const [ draggedLineEndpoint, setDraggedLineEndpoint ] = useState<LineEndpoint | null>(null);

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
    useResizeObserver(panZoomElementRef, (entry) => {
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

    const getMousePositionPixels = (event: React.MouseEvent): Vector2D => {
        const el: any = panZoomElementRef.current;
        const rect = el.getBoundingClientRect();
        return {
            x: event.pageX - rect.x - 0.5 * containerDimensions.width,
            y: 0.5 * containerDimensions.height + rect.y - event.pageY
        };
    };

    const getMousePosition = (event: React.MouseEvent): Vector2D => {
        // Get the normalized mouse position in the image
        // in the range -1 < x < 1 and -1 < y < 1
        const positionPixels = getMousePositionPixels(event);
        const vpr = getViewPhotoRect();
        return {
            x: 2 * (positionPixels.x - vpr.x) / vpr.width,
            y: 2 * (positionPixels.y - vpr.y) / vpr.height
        };
    };

    const panView = (event: React.MouseEvent) => {
        const dx = -2 * event.movementX / containerDimensions.width;
        const dy = 2 * event.movementY / containerDimensions.height;
        updateViewTransform(dx, dy, 1);
    };

    const zoomView = (event: React.WheelEvent) => {
        const k = 0.002;
        const ds = 1 + k * event.deltaY;
        updateViewTransform(0, 0, ds);  
    };

    const onMouseDown = (event: React.MouseEvent) => {
        mouseDownPositionPixelsRef.current = getMousePositionPixels(event);
        if (controlMode === ControlMode.EDIT_LINES) {
            // Set the line endpoint that will be dragged, if the mouse is over
            // a line endpoint
            const position = getMousePosition(event);
            const lineEndpoint = getLineEndpoint(position);
            if (lineEndpoint) {
                setDraggedLineEndpoint(lineEndpoint);
            }
        }
    };

    const onMouseMove = (event: React.MouseEvent) => {
        if (controlMode === ControlMode.PAN_ZOOM_2D) {
            if (event.buttons === 1) {
                panView(event);
            }
        }
        if (controlMode === ControlMode.EDIT_LINES) {
            if (event.buttons === 1) {
                if (draggedLineEndpoint) {
                    // Update the position of the line endpoint that is being dragged
                    dispatch({
                        action: 'setLineEndpointPosition',
                        lineEndpoint: draggedLineEndpoint,
                        position: getMousePosition(event)
                    });
                }
                else {
                    // The user is dragging without a line endpoint being dragged,
                    // so pan the view
                    panView(event);
                }
            }
        }
    };

    const onMouseUp = (event: React.MouseEvent) => {
        if (mouseDownPositionPixelsRef.current === null) {
            return;
        }
        try {
            const mousePositionPixels = getMousePositionPixels(event);
            const distanceSq = getDistanceSquared(mousePositionPixels, mouseDownPositionPixelsRef.current);
            if (distanceSq < 4) {
                // The mouse moved fewer than two pixels since mouse down, so
                // this is a click
                onClick(event);
            }
            if (controlMode === ControlMode.EDIT_LINES) {
                // Set the line endpoint being dragged to null
                setDraggedLineEndpoint(null);
            }
        }
        finally {
            mouseDownPositionPixelsRef.current = null;
        }
    };

    const onClick = (event: React.MouseEvent) => {
        const position = getMousePosition(event);
        const displayX = Number(position.x.toFixed(4));
        const displayY = Number(position.y.toFixed(4));
        console.log(`{ x: ${displayX}, y: ${displayY} }`);
    };

    const onWheelCapture = (event: React.WheelEvent) => {
        if ([ ControlMode.PAN_ZOOM_2D, ControlMode.EDIT_LINES ].includes(controlMode)) {
            zoomView(event);          
        }
    };

    const getLineEndpoint = (mousePosition: Vector2D): LineEndpoint | null  => {
        const endpointRadiusSq = 0.00006;  // TO DO: Convert to pixels?
        for (const line of photo.lines) {
            const d20 = getDistanceSquared(mousePosition, line.v0);
            if (d20 < endpointRadiusSq) {
                return { id: line.id, endpointIndex: 0 };
            }
            const d21 = getDistanceSquared(mousePosition, line.v1);
            if (d21 < endpointRadiusSq) {
                return { id: line.id, endpointIndex: 1 };
            }
        }
        return null;
    };

    return (
        <div className="pm-pan-zoom-container">
            <div
                className="pm-pan-zoom"
                ref={panZoomElementRef}
                onMouseMove={onMouseMove}
                onWheelCapture={onWheelCapture}
                onMouseDown={onMouseDown}
                onMouseUp={onMouseUp}
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
