import { FunctionComponent, ReactElement, useEffect, useRef } from 'react';
import { Canvas, Object3DNode, extend, useLoader, useThree } from '@react-three/fiber';
import { Edges, OrbitControls, OrthographicCamera } from '@react-three/drei';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { CameraMode, CameraTransform, CssTransform, Dimensions, Rect, PhotoMatchShape } from './types';
import { Utils } from './Utils';
import { PerspectiveCamera } from 'three';
import { HouseGeometry } from './geometry/HouseGeometry';
import { RoofGeometry } from './geometry/RoofGeometry';

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
    cameraMode: string,
    cameraTransform: CameraTransform
};

export const ThreeView: FunctionComponent<ThreeViewProps> = (props): ReactElement => {
    return (
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
            />
        </Canvas>
    );
};

type SceneMeshProps = {
    isOrbitEnabled: boolean
    cameraMode: string,
    cameraTransform: CameraTransform
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
        camera.fov = props.cameraTransform.fov; 
        const position = props.cameraTransform.position;
        camera.position.set(position.x, position.y, position.z);
        const rotation = props.cameraTransform.rotation;
        camera.rotation.set(rotation.x, rotation.y, rotation.z);
        camera.updateProjectionMatrix();
    },
    [ props.cameraMode ]);

    const gltfLoader: any = GLTFLoader;
    const result = useLoader(gltfLoader, 'mesh.gltf');

    // Data only (doesn't contain references or computed values)
    const shapes: PhotoMatchShape[] = [
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

            {shapes.map((shape) => {
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
