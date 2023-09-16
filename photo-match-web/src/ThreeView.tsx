import { FunctionComponent, ReactElement, useEffect } from 'react';
import { Canvas, useLoader, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { CssTransform, Dimensions, Rect } from './types';
import { getRectStyle } from './utils';

type ThreeViewProps = {
    containerDimensions: Dimensions,
    photoRect: Rect,
    cssTransform: CssTransform,
    isOrbitEnabled: boolean
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
                opacity: 0.8
            }}
        >
            <TomBox/>
            <OrbitControls enabled={props.isOrbitEnabled} />
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
