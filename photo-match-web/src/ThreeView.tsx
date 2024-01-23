import { FunctionComponent, ReactElement, useCallback, useEffect, useRef, useState } from 'react';
import { Canvas, Object3DNode, extend, useLoader, useThree } from '@react-three/fiber';
import { Edges, OrbitControls, OrthographicCamera } from '@react-three/drei';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { CameraMode, CameraTransform, CssTransform, Dimensions, Rect, PhotoMatchShape, ShapeEdge, ShapeEdgeLine, Line } from './types';
import { Utils } from './Utils';
import { Mesh, MeshStandardMaterial, PerspectiveCamera, Scene } from 'three';
import { HouseGeometry } from './geometry/HouseGeometry';
import { RoofGeometry } from './geometry/RoofGeometry';
import { ThreeLinesView } from './ThreeLinesView';
import { PhotoMatchGeometry } from './geometry/PhotoMatchGeometry';
import { useData } from './DataContext';

extend({ HouseGeometry, RoofGeometry });

// type DictById<T> = { [shapeId: number]: T };
type ShapeMesh = {
    id: number
    geometry: PhotoMatchGeometry
    mesh: Mesh
};

const getShapeMeshes = (shapes: PhotoMatchShape[]): ShapeMesh[] => {
    // Get the data for each shape by constructing the geometry objects
    const shapeMeshes: ShapeMesh[] = [];

    const scene = new Scene();

    for (const shape of shapes) {
        let geometry = null;
        if (shape.typeName === 'house') {
            geometry = new HouseGeometry(shape.params);
        }
        if (shape.typeName === 'roof') {
            geometry = new RoofGeometry(shape.params);
        }
        if (geometry === null) {
            throw 'unknown geometry type';
        }

        // Create a mesh with position and rotation
        const mesh = new Mesh(geometry, new MeshStandardMaterial());
        scene.add(mesh);
        mesh.position.set(shape.position.x, shape.position.y, shape.position.z);
        mesh.rotation.set(shape.rotation.x, shape.rotation.y, shape.rotation.z);
        mesh.updateMatrix();
        mesh.updateMatrixWorld();

        shapeMeshes.push({
            id: shape.id,
            geometry: geometry,
            mesh: mesh
        });
    }
    // debugger;
    return shapeMeshes;
};

const getShapeEdgeLines = (
    shapeMeshes: ShapeMesh[],
    camera: PerspectiveCamera,
    photoMatchLines: Line[]
) => {
    type MatchEdgesDict = { [ shapeId: number ]: { [ edgeId: number ]: true } };
    
    // Create match edges dict from photo match lines for faster lookup below
    const matchEdgesDict: MatchEdgesDict = {};
    for (const photoMatchLine of photoMatchLines) {
        const shapeId = photoMatchLine.matchingShapeId;
        const edgeId = photoMatchLine.matchingEdgeId;
        if (!matchEdgesDict[shapeId]) {
            matchEdgesDict[shapeId] = {};
        }
        matchEdgesDict[shapeId][edgeId] = true;
    }
    
    const shapeEdgeLines: ShapeEdgeLine[] = [];
    for (const shapeMesh of shapeMeshes) {
        // Do not render edges if the shape is not included in the matches dict
        const shapeId = shapeMesh.id;
        if (!matchEdgesDict[shapeId]) {
            continue;
        }
        
        for (let i = 0; i < shapeMesh.geometry.pmEdges.length; i++) {
            // Do not render edge if it is not included in the matches dict
            if (!matchEdgesDict[shapeId][i]) {
                continue;
            }

            const pmEdge: ShapeEdge = shapeMesh.geometry.pmEdges[i];
            
            const v0 = pmEdge.v0.clone().applyMatrix4(shapeMesh.mesh.matrixWorld);            
            const p0 = v0
                .clone()
                .applyMatrix4(camera.matrixWorldInverse)
                .applyMatrix4(camera.projectionMatrix);
            
            const v1 = pmEdge.v1.clone().applyMatrix4(shapeMesh.mesh.matrixWorld);
            const p1 = v1
                .clone()
                .applyMatrix4(camera.matrixWorldInverse)
                .applyMatrix4(camera.projectionMatrix);

            shapeEdgeLines.push({
                shapeId: shapeId,
                edgeId: i,
                v0: { x: p0.x, y: p0.y },
                v1: { x: p1.x, y: p1.y }
            });
        }

    }
    return shapeEdgeLines;
};

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
    cameraMode: string,
    cameraTransform: CameraTransform
};


// Data only (doesn't contain references or computed values)
const _shapes: PhotoMatchShape[] = [
    {
        id: 1,
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'house',
        params: {
            length: 170,
            width: 69,
            height: 48,
            roofHeight: 22
        }
    },
    {
        id: 2,
        position: { x: 0, y: 48, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'roof',
        params: {
            length: 170,
            width: 69,
            roofHeight: 22,
            roofThickness: 3,
            overhangSide: 5,
            overhangLeft: 0,
            overhangRight: 5
        }
    },
    {
        id: 3,
        position: { x: -114, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'house',
        params: {
            length: 58,
            width: 69,
            height: 81,
            roofHeight: 22
        }
    },
    {
        id: 4,
        position: { x: -114, y: 81, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'roof',
        params: {
            length: 58,
            width: 69,
            roofHeight: 22,
            roofThickness: 3,
            overhangSide: 5,
            overhangLeft: 34.5,
            overhangRight: 5
        }
    },
    {
        id: 5,
        position: { x: -177.5, y: 0, z: -34.5 },
        rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
        typeName: 'house',
        params: {
            length: 156,
            width: 69,
            height: 81,
            roofHeight: 22
        }
    },
    {
        id: 6,
        position: { x: -177.5, y: 81, z: -34.5 },
        rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
        typeName: 'roof',
        params: {
            length: 156,
            width: 69,
            roofHeight: 22,
            roofThickness: 3,
            overhangSide: 5,
            overhangLeft: 5,
            overhangRight: 5
        }
    },
    {
        id: 7,
        position: { x: -220, y: 0, z: -34.5 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'house',
        params: {
            length: 16,
            width: 36,
            height: 32,
            roofHeight: 14
        }
    },
    {
        id: 8,
        position: { x: -220, y: 32, z: -34.5 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'roof',
        params: {
            length: 16,
            width: 36,
            roofHeight: 14,
            roofThickness: 3,
            overhangSide: 3,
            overhangLeft: 3,
            overhangRight: 0
        }
    },
    {
        id: 9,
        position: { x: -122.5, y: 0, z: -70.5 },
        rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
        typeName: 'house',
        params: {
            length: 72,
            width: 53,
            height: 81,
            roofHeight: 17
        }
    },
    {
        id: 10,
        position: { x: -122.5, y: 81, z: -70.5 },
        rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
        typeName: 'roof',
        params: {
            length: 72,
            width: 53,
            roofHeight: 17,
            roofThickness: 3,
            overhangSide: 5,
            overhangLeft: 40,
            overhangRight: 5
        }
    }
];

// TO DO: Recalculate when shapes change
const _shapeMeshes: ShapeMesh[] = getShapeMeshes(_shapes);


export const ThreeView: FunctionComponent<ThreeViewProps> = (props): ReactElement => {

    const { data, dispatch } = useData();
    const scene = Utils.getScene(data);
    const photo = Utils.getPhoto(scene);
    const photoMatchLines = photo.lines;

    const shapes = _shapes;
    const shapeMeshes = _shapeMeshes;

    // TO DO: Recalculate when camera parameters change
    // const shapeEdgeLines: ShapeEdgeLine[] = getShapeEdgeLines(shapeEdges);
    // I need a useCallback and pass it down into the mesh to get the camera
    // params: onCameraParamsUpdate. This callback updates the shapeEdgeLines
    // which sends new props to ThreeLinesView
    const [ shapeEdgeLines, setShapeEdgeLines ] = useState<ShapeEdgeLine[]>([]);

    const onCameraUpdate = useCallback(
        (camera: PerspectiveCamera) => {
            // console.log('QQQ', camera.position.x);
            const shapeEdgeLines: ShapeEdgeLine[] = getShapeEdgeLines(
                shapeMeshes, camera, photoMatchLines);

            setShapeEdgeLines(shapeEdgeLines);
        },
        []
    );

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
                    cameraTransform={props.cameraTransform}
                    shapes={shapes}
                    onCameraUpdate={onCameraUpdate}
                />
            </Canvas>

            <ThreeLinesView
                containerDimensions={props.containerDimensions}
                photoRect={props.photoRect}
                cssTransform={props.cssTransform}
                shapeEdgeLines={shapeEdgeLines}
            />
        </>
    );
};

type SceneMeshProps = {
    isOrbitEnabled: boolean
    cameraMode: string,
    cameraTransform: CameraTransform
    shapes: PhotoMatchShape[],
    onCameraUpdate: any
};

const SceneMesh = (props: SceneMeshProps): ReactElement => {
    const orbitControlsRef = useRef<any>(null);
    const state = useThree();

    // When props.cameraMode changes, update the
    // camera transform so that the camera shows the correct position
    // and rotation.
    // When in CameraMode.ORBIT, the OrbitControls component overrides the
    // camera transform with one that has the correct position but looks at
    // the origin.
    // When in CameraMode.FREE, the camera is positioned and rotated exactly
    // according to the transform.
    useEffect(() => {
        const camera = state.camera as PerspectiveCamera;
        camera.far = 100000;
        camera.fov = props.cameraTransform.fov; 
        const position = props.cameraTransform.position;
        camera.position.set(position.x, position.y, position.z);
        const rotation = props.cameraTransform.rotation;
        camera.rotation.set(rotation.x, rotation.y, rotation.z);
        camera.updateProjectionMatrix();

        // console.log('QQQ', camera);
        props.onCameraUpdate(camera);
    },
    [ props.cameraMode ]);

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

            { props.cameraMode === CameraMode.ORBIT &&
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
            }

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
