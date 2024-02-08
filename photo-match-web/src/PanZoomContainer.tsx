import { FunctionComponent, ReactElement, useCallback, useEffect, useRef, useState } from 'react';
import useResizeObserver from '@react-hook/resize-observer';
import { BasicLine, CameraMode, CameraTransform, ControlMode, Dimensions, DrawNewLineInfo, LineEndpoint, Rect, ShapeMode, Vector2D } from './types';
import { Controls } from './Controls';
import { useData } from './DataContext';
import { LinesView } from './LinesView';
import { Overview } from './Overview';
import { Photo } from './Photo';
import { ThreeView } from './ThreeView';
import { Utils } from './Utils';
import { PhotoMatch } from './PhotoMatch';
import Button from '@mui/material/Button';


export const PanZoomContainer: FunctionComponent = (): ReactElement => {

    const overviewSizeRatio = 0.2;

    const panZoomElementRef = useRef<HTMLDivElement | null>(null);
    const mouseDownPositionPixelsRef = useRef<Vector2D | null>(null);

    // Line endpoint that is being dragged
    const [ draggedLineEndpoint, setDraggedLineEndpoint ] = useState<LineEndpoint | null>(null);

    const { data, dispatch } = useData();
    const scene = Utils.getScene(data);
    const photo = Utils.getPhoto(scene);

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

    const [ drawNewLineInfo, setDrawNewLineInfo ] = useState<DrawNewLineInfo | null>(null);

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

    // In order to listen for key presses, we need to attach a listener
    // to the HTML document itself, so we do it with an effect that
    // removes the listener when this component is destroyed.
    // The callback uses useCallback and is updated whenever dispatch or
    // photo is updated
    const onDocumentKeyDown = useCallback(
        (event: KeyboardEvent) => {
            if (event.key === 'q') {
                const shapeMode = photo._uiData.shapeMode;
                const newShapeMode = (shapeMode === ShapeMode.SHAPES) ?
                    ShapeMode.MODELS : ShapeMode.SHAPES;

                dispatch({
                    action: 'setShapeMode',
                    shapeMode: newShapeMode
                });
            }
        },
        [ dispatch, photo ]
    );

    useEffect(
        () => {
            document.addEventListener('keydown', onDocumentKeyDown);
            return () => {
                document.removeEventListener('keydown', onDocumentKeyDown);
            };
        },
        [ onDocumentKeyDown ]
    );

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
        return Utils.getScaledRect(getPhotoRect(), overviewSizeRatio);
    };

    const getOverviewViewRect = (): Rect => {
        return Utils.getScaledRect(getViewRect(), overviewSizeRatio);
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

    const orbit3dView = (event: React.MouseEvent) => {
        const dx = -2 * event.movementX / containerDimensions.width;
        const dy = 2 * event.movementY / containerDimensions.height;
        const SPEED = 30;
        const ct = photo._uiData.cameraTransform;

        const newCameraTransform = {
            fov: ct.fov,
            position: {
                x: ct.position.x + SPEED * dx,
                y: ct.position.y + SPEED * dy,
                z: ct.position.z  // + SPEED * dy
            },
            rotation: {
                x: ct.rotation.x,  // + dx,
                y: ct.rotation.y,  // + dx,
                z: ct.rotation.z   // + dx,
            }
        };

        dispatch({
            action: 'setCameraTransform',
            cameraTransform: newCameraTransform
        });
    };

    const zoomView = (event: React.WheelEvent) => {
        const k = 0.002;
        const ds = 1 + k * event.deltaY;
        updateViewTransform(0, 0, ds);  
    };

    const zoom3dView = (event: React.WheelEvent) => {
        console.log('zoom3dView');
    };

    const onMouseDown = (event: React.MouseEvent) => {
        mouseDownPositionPixelsRef.current = getMousePositionPixels(event);
        if (controlMode === ControlMode.EDIT_LINES) {
            // Set the line endpoint that will be dragged, if the mouse is over
            // a line endpoint
            const mousePosition = getMousePosition(event);
            const lineEndpoint = Utils.getClickedLineEndpoint(mousePosition, photo.lines);
            if (lineEndpoint) {
                setDraggedLineEndpoint(lineEndpoint);
            }
        }
    };

    const onMouseMove = (event: React.MouseEvent) => {
        const isDragging = (
            event.buttons === 1 &&
            mouseDownPositionPixelsRef.current !== null
        );

        if (controlMode === ControlMode.PAN_ZOOM_2D) {
            if (isDragging) {
                panView(event);
            }
        }

        if (controlMode === ControlMode.EDIT_LINES) {
            if (isDragging) {
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
            else {
                // If the button is not pressed and there is a new line drawing
                // in progress, update the position of the new line v1 endpoint
                if (drawNewLineInfo !== null) {
                    setDrawNewLineInfo({
                        ...drawNewLineInfo,
                        v1: getMousePosition(event)
                    });
                }
            }
        }

        if (controlMode === ControlMode.ORBIT_3D) {
            if (isDragging) {
                orbit3dView(event);
            }
        }
    };

    const onMouseUp = (event: React.MouseEvent) => {
        if (mouseDownPositionPixelsRef.current === null) {
            return;
        }
        try {
            const mousePositionPixels = getMousePositionPixels(event);
            const distanceSq = Utils.getDistanceSquared(mousePositionPixels, mouseDownPositionPixelsRef.current);
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
        const mousePosition = getMousePosition(event);
        const displayX = Number(mousePosition.x.toFixed(4));
        const displayY = Number(mousePosition.y.toFixed(4));
        console.log(`{ x: ${displayX}, y: ${displayY} }`);

        if (controlMode === ControlMode.EDIT_LINES) {
            let newLineId: number | null = null;
            const clickedLineEndpoint = Utils.getClickedLineEndpoint(mousePosition, photo.lines);
            if (clickedLineEndpoint) {
                newLineId = clickedLineEndpoint.id;
            }
            else {
                newLineId = Utils.getClickedLineId(mousePosition, photo.lines);
            }

            if (newLineId !== null) {
                // If the line is already selected, deselect it
                if (photo._uiData.lineId === newLineId) {
                    newLineId = null;
                }
                console.log('WWW', newLineId);
                dispatch({
                    action: 'setLineId',
                    lineId: newLineId
                });
            }
            else {
                // No line was clicked, so deselect the current line if necessary
                if (photo._uiData.lineId !== null) {
                    dispatch({
                        action: 'setLineId',
                        lineId: null
                    });
                }
                else {
                    // No line was clicked, and no line was deselected. Draw
                    // a new line.
                    const mousePosition = getMousePosition(event);

                    // If there is no new line drawing in progress, start the
                    // new line
                    if (drawNewLineInfo === null) {
                        setDrawNewLineInfo({
                            v0: mousePosition,
                            v1: mousePosition
                        });
                    }
                    else {
                        // If there is a new line drawing in progress, finish the
                        // new line and set the new line drawing object to null
                        dispatch({
                            action: 'addPhotoMatchLine',
                            v0: drawNewLineInfo.v0,
                            v1: mousePosition
                        });
                        setDrawNewLineInfo(null);
                    }

                }
            }

            
        }

        if (controlMode == ControlMode.ORBIT_3D) {
            const photoRect = getPhotoRect();
            const cameraAspect = photoRect.width / photoRect.height;
            const camera = PhotoMatch.getPerspectiveCamera(
                photo._uiData.cameraTransform,
                cameraAspect);

            const _shapes = PhotoMatch.getPhotoMatchShapes();
            const _shapeMeshes = PhotoMatch.getShapeMeshes(_shapes);
            const edgeLines = PhotoMatch.getShapeEdgeLines(_shapeMeshes, camera, photo.lines);
            let clickedEdgeLine = Utils.getClickedShapeEdgeLine(mousePosition, edgeLines);
            console.log('RRR', clickedEdgeLine);
            if (clickedEdgeLine !== null) {
                // If the line is already selected, deselect it
                if (
                    photo._uiData.selectedShapeId === clickedEdgeLine.shapeId &&
                    photo._uiData.selectedEdgeId === clickedEdgeLine.edgeId
                ) {
                    clickedEdgeLine = null;
                }
                const newShapeId = clickedEdgeLine ? clickedEdgeLine.shapeId : null;
                const newEdgeId = clickedEdgeLine ? clickedEdgeLine.edgeId : null;
                dispatch({
                    action: 'setShapeEdgeIds',
                    shapeId: newShapeId,
                    edgeId: newEdgeId
                });
            }
            else {
                // No line was clicked, so deselect the current line if necessary
                if (photo._uiData.selectedShapeId !== null) {
                    dispatch({
                        action: 'setShapeEdgeIds',
                        shapeId: null,
                        edgeId: null
                    });
                }
            }
        }
    };

    const onWheelCapture = (event: React.WheelEvent) => {
        if ([ ControlMode.PAN_ZOOM_2D, ControlMode.EDIT_LINES ].includes(controlMode)) {
            zoomView(event);          
        }
        if (controlMode === ControlMode.ORBIT_3D) {
            zoom3dView(event);
        }
    };

    const optimizeCameraTransform = () => {
        const photoRect = getPhotoRect();
        const cameraAspect = photoRect.width / photoRect.height;
        const newCameraTransform = PhotoMatch.getOptimalCameraTransform(
            photo._uiData.cameraTransform,
            cameraAspect,
            photo.lines
        );
        dispatch({
            action: 'setCameraTransform',
            cameraTransform: newCameraTransform
        });
    };

    const linkSelectedPhotoMatchLineAndShapeEdge = () => {
        const lineId = photo._uiData.lineId;
        const shapeId = photo._uiData.selectedShapeId;
        const edgeId = photo._uiData.selectedEdgeId;
        if (lineId === null || shapeId === null || edgeId === null) {
            return;
        }
        dispatch({
            action: 'linkPhotoMatchLineAndShapeEdge',
            lineId: lineId,
            shapeId: shapeId,
            edgeId: edgeId
        });
    };

    const unlinkSelectedPhotoMatchLine = () => {
        const lineId = photo._uiData.lineId;
        if (lineId === null) {
            return;
        }
        dispatch({
            action: 'linkPhotoMatchLineAndShapeEdge',
            lineId: lineId,
            shapeId: -1,
            edgeId: -1
        });
    };

    const deleteSelectedPhotoMatchLine = () => {
        const lineId = photo._uiData.lineId;
        if (lineId === null) {
            return;
        }
        dispatch({
            action: 'deletePhotoMatchLine',
            lineId: lineId
        });
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
                        ...Utils.getDimensionsStyle(containerDimensions)
                    }}
                >
                    <Photo
                        containerDimensions={containerDimensions}
                        boundary={getViewPhotoRect()}
                        opacity={photoOpacity}
                        imageUrl={Utils.getFileUrl(photo.filename)}
                    />
                    <LinesView
                        containerDimensions={containerDimensions}
                        photoRect={getPhotoRect()}
                        cssTransform={getCssTransform()}
                        drawNewLineInfo={drawNewLineInfo}
                    />
                    <ThreeView
                        containerDimensions={containerDimensions}
                        photoRect={getPhotoRect()}
                        cssTransform={getCssTransform()}
                        cameraMode={cameraMode}
                        isOrbitEnabled={controlMode === ControlMode.ORBIT_3D}
                        opacity={modelOpacity}
                    />
                    <Overview
                        dimensions={getOverviewDimensions()}
                        photoRect={getOverviewPhotoRect()}
                        viewRect={getOverviewViewRect()}
                        photoImageUrl={Utils.getFileUrl(photo.filename)}
                    />
                </div>
            </div>
            <div className="pm-controls-container">
                <Controls
                    deleteEdge={deleteSelectedPhotoMatchLine}
                    linkEdge={linkSelectedPhotoMatchLineAndShapeEdge}
                    unlinkEdge={unlinkSelectedPhotoMatchLine}
                    optimizeCameraTransform={optimizeCameraTransform}
                />
            </div>
        </div>
    );
};
