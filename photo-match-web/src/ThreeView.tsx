import { FunctionComponent, ReactElement, useEffect, useRef } from 'react';
import { Canvas, useLoader, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { CameraMode, CameraTransform, CssTransform, Dimensions, Rect } from './types';
import { getRectStyle } from './utils';
import { PerspectiveCamera } from 'three';

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
                ...getRectStyle(props.photoRect, props.containerDimensions),
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
    return (
        <mesh>
            <directionalLight position={[1, 1, 1]} intensity={2} />
            <directionalLight position={[-1, -1, -1]} intensity={3}/>
            <directionalLight position={[0, -1, 0]} intensity={2}/>
            <primitive
                object={result.scene}
                scale={[1, 1, 1]}  // Use millimeter units to match the GLTF
                rotation={[-Math.PI / 2, 0, 0]}
            />

            { props.cameraMode === CameraMode.ORBIT &&
                <OrbitControls
                    ref={orbitControlsRef}
                    enabled={props.isOrbitEnabled}
                />
            }
            <gridHelper args={[50 * 10, 50]} />
            <axesHelper args={[200]} />
        </mesh>
        
    );
};
