import { FunctionComponent, ReactElement, useEffect } from 'react';
import { Canvas, useLoader, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { CssTransform, Dimensions, Rect } from './types';
import { getRectStyle } from './utils';

type ThreeViewProps = {
    containerDimensions: Dimensions,
    photoRect: Rect,
    viewRect: Rect,
    viewPhotoRect: Rect,
    cssTransform: CssTransform,
    isOrbitEnabled: boolean
};

export const ThreeView: FunctionComponent<ThreeViewProps> = (props): ReactElement => {
    // const vr = props.viewRect;
    // const pr = props.photoRect;
    // const vpr = props.viewPhotoRect;
    // const scale = Math.max(pr.width / vr.width, pr.height / vr.height);
    // const canvasRect: Rect = {
    //     x: props.viewPhotoRect.x,
    //     y: props.viewPhotoRect.y,
    //     width: props.photoRect.width,
    //     height: props.photoRect.height
    // };
    const canvasRect = props.photoRect;
    return (
        <Canvas
            className="pm-three-view"
            style={{
                ...getRectStyle(canvasRect, props.containerDimensions),
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
