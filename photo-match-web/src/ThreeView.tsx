import { FunctionComponent, ReactElement, useCallback, useEffect, useRef, useState } from 'react';
import { Canvas, Object3DNode, extend, useLoader, useThree } from '@react-three/fiber';
import { Edges, OrbitControls, OrthographicCamera } from '@react-three/drei';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { CameraMode, CameraTransform, CssTransform, Dimensions, Rect, PhotoMatchShape, ShapeEdge, ShapeEdgeLine, Line, ShapeMesh } from './types';
import { Utils } from './Utils';
import { Mesh, MeshStandardMaterial, PerspectiveCamera, Scene } from 'three';
import { HouseGeometry } from './geometry/HouseGeometry';
import { RoofGeometry } from './geometry/RoofGeometry';
import { ThreeLinesView } from './ThreeLinesView';
import { PhotoMatchGeometry } from './geometry/PhotoMatchGeometry';
import { useData } from './DataContext';
import { PhotoMatch } from './PhotoMatch';

extend({ HouseGeometry, RoofGeometry });

declare module '@react-three/fiber' {
    interface ThreeElements {
        houseGeometry: Object3DNode<HouseGeometry, typeof HouseGeometry>
        roofGeometry: Object3DNode<RoofGeometry, typeof RoofGeometry>
    }
}

type ThreeViewProps = {
    containerDimensions: Dimensions,
    photoRect: Rect,
    cssTransform: CssTransform,
    isOrbitEnabled: boolean,
    opacity: number,
    cameraMode: string
};

const _shapes = PhotoMatch.photoMatchShapes;
const _shapeMeshes = PhotoMatch.getShapeMeshes(_shapes);

export const ThreeView: FunctionComponent<ThreeViewProps> = (props): ReactElement => {

    const { data, dispatch } = useData();
    const scene = Utils.getScene(data);
    const photo = Utils.getPhoto(scene);
    const photoMatchLines = photo.lines;

    const shapes = _shapes;
    const shapeMeshes = _shapeMeshes;

    const cameraTransform = photo._uiData.cameraTransform;

    const [ shapeEdgeLines, setShapeEdgeLines ] = useState<ShapeEdgeLine[]>([]);

    const [ camera, setCamera ] = useState<PerspectiveCamera | null>(null);

    const onCameraUpdate = useCallback(
        (newCamera: PerspectiveCamera) => {
            setCamera(newCamera);
        },
        []
    );

    useEffect(
        () => {
            if (camera === null) {
                return;
            }

            const shapeEdgeLines: ShapeEdgeLine[] = PhotoMatch.getShapeEdgeLines(
                shapeMeshes, camera, photoMatchLines);
            
            setShapeEdgeLines(shapeEdgeLines);
        },
        [ camera, shapeMeshes, photoMatchLines ]
    );

    const cameraAspect = props.photoRect.width / props.photoRect.height;

    return (
        <>
            <Canvas
                className="pm-three-view"
                // Make the canvas ignore parent CSS transforms when resizing
                // itself to fit its container. See:
                // https://github.com/pmndrs/react-three-fiber/blob/master/packages/fiber/src/web/Canvas.tsx#L21C18-L21C18
                // https://www.npmjs.com/package/react-use-measure#api
                resize={{ offsetSize: true }}
                style={{
                    ...Utils.getRectStyle(props.photoRect, props.containerDimensions),
                    transform: `translate(${props.cssTransform.x}px, ${-props.cssTransform.y}px) scale(${props.cssTransform.scale})`,
                    opacity: props.opacity
                }}
            >
                <SceneMesh
                    isOrbitEnabled={props.isOrbitEnabled}
                    cameraMode={props.cameraMode}
                    shapes={shapes}
                    cameraAspect={cameraAspect}
                    cameraTransform={cameraTransform}
                    onCameraUpdate={onCameraUpdate}
                />
            </Canvas>

            <ThreeLinesView
                containerDimensions={props.containerDimensions}
                photoRect={props.photoRect}
                cssTransform={props.cssTransform}
                shapeEdgeLines={shapeEdgeLines}
                selectedPhotoMatchLineId={photo._uiData.lineId}
                selectedShapeId={photo._uiData.selectedShapeId}
                selectedEdgeId={photo._uiData.selectedEdgeId}
            />
        </>
    );
};

type SceneMeshProps = {
    isOrbitEnabled: boolean
    cameraMode: string
    cameraTransform: CameraTransform
    shapes: PhotoMatchShape[]
    onCameraUpdate: any
    cameraAspect: number
};

const SceneMesh = (props: SceneMeshProps): ReactElement => {
    const state = useThree();

    useEffect(
        () => {
            const camera = state.camera as PerspectiveCamera;
            camera.far = 10000;
            camera.aspect = props.cameraAspect;
            camera.fov = props.cameraTransform.fov; 
            const position = props.cameraTransform.position;
            camera.position.set(position.x, position.y, position.z);
            const rotation = props.cameraTransform.rotation;
            camera.rotation.set(rotation.x, rotation.y, rotation.z);
            camera.updateMatrix();
            camera.updateMatrixWorld();
            camera.updateProjectionMatrix();
            // Clone the camera object to ensure that it doesn't get changed
            // by Three.js after it is returned from this function!
            const cameraClone = camera.clone();
            props.onCameraUpdate(cameraClone);
        },
        [ props.cameraTransform ]
    );

    const gltfLoader: any = GLTFLoader;
    const result = useLoader(gltfLoader, 'mesh.gltf');

    return (
        <mesh>
            <directionalLight position={[1, 1, 1]} intensity={2} />
            <directionalLight position={[-1, -1, -1]} intensity={3}/>
            <directionalLight position={[0, -1, 0]} intensity={2}/>
            <primitive
                object={result.scene}
                scale={[1, 1, 1]}  // Use millimeter units to match the GLTF
                rotation={[-Math.PI / 2, 0, 0]}
                position={[200, 0, 0]}
            />

            {props.shapes.map((shape) => {
                return (
                    <mesh
                        key={shape.id}
                        position={Utils.toTuple(shape.position)}
                        rotation={Utils.toTuple(shape.rotation)}
                    >
                    { shape.typeName === 'house' &&
                        <houseGeometry args={[shape.params]} />
                    }
                    { shape.typeName === 'roof' &&
                        <roofGeometry args={[shape.params]} />
                    }
                        <meshStandardMaterial
                            args={[{
                                polygonOffset: true,
                                polygonOffsetFactor: 1, // shape.id,
                                polygonOffsetUnits: 1,
                            }]}
                        />
                        <Edges />
                    </mesh>
                );
            })}

            {/* {props.cameraMode === CameraMode.ORBIT &&
                <OrbitControls
                    ref={orbitControlsRef}
                    enabled={props.isOrbitEnabled}
                    // enableDamping={false}
                    onChange={(e) => {
                        // props.onCameraUpdate(orbitControlsRef.current.object);
                        if (!e) {
                            return;
                        }
                        const camera = e.target.object as PerspectiveCamera;
                        camera.updateMatrix();
                        camera.updateMatrixWorld();
                        camera.updateProjectionMatrix();
                        props.onCameraUpdate(camera);
                    }}
                />
            } */}

            {/* <OrthographicCamera
                makeDefault
                zoom={1}
                near={1}
                far={2000}
                position={[0, 0, 200]}
            /> */}

            <gridHelper args={[50 * 10, 50]} position={[0, -0.4, 0]} />
            <axesHelper args={[200]} position={[-0.1, -0.1, -0.1]} />
        </mesh>
        
    );
};
