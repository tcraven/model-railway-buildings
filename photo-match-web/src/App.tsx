import React from 'react';
import { useEffect, useRef, useState } from 'react';
import { FunctionComponent, ReactElement } from 'react';
import useResizeObserver from '@react-hook/resize-observer';
import { Canvas, useThree, useLoader } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import './App.css';

const ControlMode = {
    PAN_ZOOM_2D: 'PAN_ZOOM_2D',
    ORBIT_3D: 'ORBIT_3D'
};

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

type CssTransform = {
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
            alt=""
            style={{
                ...getRectStyle(props.boundary, props.containerDimensions)
            }}
        />
    );
};


const TomBox = () => {
    const state = useThree();
    useEffect(() => {
        state.camera.position.set(100, 50, 200);
        state.camera.lookAt(0, 0, 0);
        state.camera.updateProjectionMatrix();
        console.log('XXX', state);
    }, []);
    const gltfLoader: any = GLTFLoader;
    const result = useLoader(gltfLoader, 'mesh.gltf');
    // Use millimeter units to match the GLTF
    return (
        <mesh>
            <directionalLight position={[1, 1, 1]} intensity={2} />
            <directionalLight position={[-1, -1, -1]} intensity={3}/>
            <directionalLight position={[0, -1, 0]} intensity={2}/>
            <primitive
                object={result.scene}
                scale={[1, 1, 1]}
                rotation={[-Math.PI / 2, 0, 0]}
            />
        </mesh>
    );
};

type ThreeViewProps = {
    containerDimensions: Dimensions,
    boundary: Rect,
    cssTransform: CssTransform,
    isOrbitEnabled: boolean
};
const ThreeView: FunctionComponent<ThreeViewProps> = (props): ReactElement => {
    return (
        <Canvas
            className="pm-three-view"
            style={{
                ...getRectStyle(props.boundary, props.containerDimensions),
                transform: `translate(${props.cssTransform.x}px, ${-props.cssTransform.y}px) scale(${props.cssTransform.scale})`,
                opacity: 0.8
            }}
        >
            <TomBox/>
            {props.isOrbitEnabled ? (<OrbitControls />) : null}
            <axesHelper args={[200]} />
            <gridHelper args={[50 * 10, 50]} />
        </Canvas>
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
                alt=""
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

type UpdateViewTransformFn = (dx: number, dy: number, ds: number) => void;
type ControlsProps = {
    controlMode: string,
    setControlMode: (controlMode: string) => void
};
const Controls: FunctionComponent<ControlsProps> = (props): ReactElement => {
    return (
        <div className="pm-controls">
            <button
                className="pm-button"
                onClick={() => {
                    props.setControlMode(
                        (props.controlMode === ControlMode.ORBIT_3D) ?
                        ControlMode.PAN_ZOOM_2D : ControlMode.ORBIT_3D
                    );
                }}
            >
                {props.controlMode}
            </button>
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

    const [controlMode, setControlMode] = useState<string>(
        ControlMode.PAN_ZOOM_2D);

    // Position and scale of the view (considering the photo image to be
    // fixed size, and the view a float window that moves around on top of
    // the photo image).
    // The origin is the center of the photo image.
    // Coordinates go from (-1, -1) to (1, 1)
    const [viewTransform, setViewTransform] = useState<ViewTransform>({
        x: 0.0,
        y: 0.0,
        scale: 1.0
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

    const getCssTransform = (): { x: number, y: number, scale: number } => {
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

    const getViewTransformXYfromClientXY = (clientX: number, clientY: number): { x: number, y: number } => {
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
        }
    }

    return (
        <div
            ref={ref}
            className="pm-pan-zoom-container"
            onMouseMove={(e) => {
                if (controlMode !== ControlMode.PAN_ZOOM_2D) {
                    return;
                }
                if (e.buttons === 1) {
                    const dx = -2 * e.movementX / containerDimensions.width;
                    const dy = 2 * e.movementY / containerDimensions.height;
                    updateViewTransform(dx, dy, 1);
                }
            }}
            onWheelCapture={(e) => {
                if (controlMode !== ControlMode.PAN_ZOOM_2D) {
                    return;
                }
                const k =  0.002;
                const ds = 1 + k * e.deltaY;
                updateViewTransform(0, 0, ds);
            }}
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
                    boundary={getPhotoRect()}
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


const App: FunctionComponent = (): ReactElement => {
    return (
        <div className="pm-app">
            <PanZoomContainer />
        </div>
    );
}

export default App;
