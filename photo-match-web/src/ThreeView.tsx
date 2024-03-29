import { FunctionComponent, ReactElement, useCallback, useEffect, useState } from 'react';
import { Canvas, Object3DNode, extend, useLoader, useThree } from '@react-three/fiber';
import { Edges } from '@react-three/drei';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { CameraTransform, CssTransform, Dimensions, Rect, PhotoMatchShape, ShapeEdgeLine, ShapeMode, PhotoMatchShapesDict, ShapeMeshesDict } from './types';
import { Utils } from './Utils';
import { PerspectiveCamera } from 'three';
import { BoxGeometry as PmBoxGeometry } from './geometry/BoxGeometry';
import { HouseGeometry } from './geometry/HouseGeometry';
import { RectGeometry } from './geometry/RectGeometry';
import { RoofGeometry } from './geometry/RoofGeometry';
import { ThreeLinesView } from './ThreeLinesView';
import { useData } from './DataContext';
import { PhotoMatch } from './PhotoMatch';

extend({ PmBoxGeometry, HouseGeometry, RectGeometry, RoofGeometry });

declare module '@react-three/fiber' {
    interface ThreeElements {
        pmBoxGeometry: Object3DNode<PmBoxGeometry, typeof PmBoxGeometry>
        houseGeometry: Object3DNode<HouseGeometry, typeof HouseGeometry>
        rectGeometry: Object3DNode<RectGeometry, typeof RectGeometry>
        roofGeometry: Object3DNode<RoofGeometry, typeof RoofGeometry>
    }
}

type ThreeViewProps = {
    containerDimensions: Dimensions
    photoRect: Rect
    cssTransform: CssTransform
    isOrbitEnabled: boolean
    opacity: number
    refreshCounter: number
};

const _shapesBySceneId: PhotoMatchShapesDict = PhotoMatch.getPhotoMatchShapesBySceneId();
const _shapeMeshesBySceneId: ShapeMeshesDict = PhotoMatch.getShapeMeshesBySceneId(_shapesBySceneId);

export const ThreeView: FunctionComponent<ThreeViewProps> = (props): ReactElement => {

    const { data } = useData();
    const scene = Utils.getScene(data);
    const photo = Utils.getPhoto(scene);
    const photoMatchLines = photo.lines;

    const sceneId = data._uiData.sceneId;
    const shapes = _shapesBySceneId[sceneId.toString()];
    const shapeMeshes = _shapeMeshesBySceneId[sceneId.toString()];

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
                    shapes={shapes}
                    cameraAspect={cameraAspect}
                    cameraTransform={cameraTransform}
                    onCameraUpdate={onCameraUpdate}
                    shapeMode={photo._uiData.shapeMode}
                    refreshCounter={props.refreshCounter}
                    meshFilename={scene.meshFilename}
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
                linesOpacity={photo._uiData.linesOpacity}
            />
        </>
    );
};

type SceneMeshProps = {
    isOrbitEnabled: boolean
    cameraTransform: CameraTransform
    shapes: PhotoMatchShape[]
    onCameraUpdate: any
    cameraAspect: number
    shapeMode: string
    refreshCounter: number
    meshFilename: string
};

const SceneMesh = (props: SceneMeshProps): ReactElement => {
    const state = useThree();
    const threeCamera = state.camera;
    const { cameraAspect, cameraTransform, onCameraUpdate, meshFilename } = props;

    useEffect(
        () => {
            const camera = threeCamera as PerspectiveCamera;
            camera.far = 10000;
            camera.aspect = cameraAspect;
            camera.fov = cameraTransform.fov; 
            const position = cameraTransform.position;
            camera.position.set(position.x, position.y, position.z);
            const rotation = cameraTransform.rotation;
            camera.rotation.set(rotation.x, rotation.y, rotation.z);
            camera.updateMatrix();
            camera.updateMatrixWorld();
            camera.updateProjectionMatrix();
            // Clone the camera object to ensure that it doesn't get changed
            // by Three.js after it is returned from this function!
            const cameraClone = camera.clone();
            onCameraUpdate(cameraClone);
        },
        [ threeCamera, cameraTransform, cameraAspect, onCameraUpdate ]
    );

    const gltfLoader: any = GLTFLoader;

    // console.log('XXX', props.refreshCounter);
    const meshUrl = Utils.getFileUrl(meshFilename) + '?v=' + props.refreshCounter;
    const result = useLoader(gltfLoader, meshUrl);

    return (
        <mesh>
            <directionalLight position={[1, 1, 1]} intensity={2} />
            <directionalLight position={[-1, -1, -1]} intensity={3}/>
            <directionalLight position={[0, -1, 0]} intensity={2}/>

            {(props.shapeMode === ShapeMode.MODELS) && 
                <primitive
                    object={result.scene}
                    scale={[1, 1, 1]}  // Use millimeter units to match the GLTF
                    rotation={[-0.5 * Math.PI, 0, 0]}
                    position={[0, 0, 0]}
                />
            }

            {(props.shapeMode === ShapeMode.SHAPES) && props.shapes.map((shape) => {
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
                    { shape.typeName === 'box' &&
                        <pmBoxGeometry args={[shape.params]} />
                    }
                    { shape.typeName === 'rect' &&
                        <rectGeometry args={[shape.params]} />
                    }
                        <meshStandardMaterial
                            args={[{
                                // transparent: true,
                                // opacity: 1.0,
                                polygonOffset: true,
                                polygonOffsetFactor: 1, // shape.id,
                                polygonOffsetUnits: 1,
                            }]}
                        />
                        <Edges />
                    </mesh>
                );
            })}

            <gridHelper args={[50 * 10, 50]} position={[0, -0.4, 0]} />
            <axesHelper args={[200]} position={[-0.1, -0.1, -0.1]} />
        </mesh>
        
    );
};
