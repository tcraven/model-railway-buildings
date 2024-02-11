import { PerspectiveCamera, Ray, Vector3 } from 'three';
import {
    BasicLine,
    CameraOrbitTransform,
    CameraTransform,
    Data,
    Dimensions,
    DimensionsStyle,
    Line,
    LineEndpoint,
    LinePointPerpDistInfo,
    Photo,
    Rect,
    RectStyle,
    Scene,
    ShapeEdgeLine,
    Vector2D,
    Vector3D
} from './types';

const getDimensionsStyle = (dimensions: Dimensions): DimensionsStyle => {
    return {
        width: dimensions.width + 'px',
        height: dimensions.height + 'px'
    }
};

const getDistanceSquared = (a: Vector2D, b: Vector2D): number => {
    const dx = a.x - b.x;
    const dy = a.y - b.y;
    return dx * dx + dy * dy;
};

const getFileUrl = (filename: string): string => {
    return `http://localhost:5007/file/${filename}`;
}

const getClickedLineEndpoint = (mousePosition: Vector2D, lines: Line[]): LineEndpoint | null  => {
    const endpointRadiusSq = 0.00006;  // TO DO: Convert to pixels?
    for (const line of lines) {
        const d20 = Utils.getDistanceSquared(mousePosition, line.v0);
        if (d20 < endpointRadiusSq) {
            return { id: line.id, endpointIndex: 0 };
        }
        const d21 = Utils.getDistanceSquared(mousePosition, line.v1);
        if (d21 < endpointRadiusSq) {
            return { id: line.id, endpointIndex: 1 };
        }
    }
    return null;
};

const getClickedShapeEdgeLine = (mousePosition: Vector2D, lines: ShapeEdgeLine[]): ShapeEdgeLine | null => {
    const maxPerpDistSq = 0.00006;
    for (const line of lines) {
        const pdi = getLinePointPerpDistInfo(line as BasicLine, mousePosition);
        if (pdi.isOnLine && pdi.perpDistSq <= maxPerpDistSq) {
            return line;
        }
    }
    return null;
};

const getClickedLineId = (mousePosition: Vector2D, lines: Line[]): number | null => {
    const maxPerpDistSq = 0.00006;
    for (const line of lines) {
        const pdi = getLinePointPerpDistInfo(line as BasicLine, mousePosition);
        if (pdi.isOnLine && pdi.perpDistSq <= maxPerpDistSq) {
            return line.id;
        }
    }
    return null;
};

const getLinePointPerpDistInfo = (line: BasicLine, point: Vector2D): LinePointPerpDistInfo => {
    const lx = line.v1.x - line.v0.x;
    const ly = line.v1.y - line.v0.y;
    const A = point.x - line.v0.x;
    const B = point.y - line.v0.y;
    const ld = lx * lx + ly * ly;
    const s = (ly * A - lx * B) / ld;
    const t = (B + lx * s) / ly;
    const perpDistSq = s * s * ld;
    const isOnLine = (t >= 0) && (t <= 1);
    return {
        t: t,
        isOnLine: isOnLine,
        perpDistSq: perpDistSq
    };
};

const getPhoto = (scene: Scene): Photo => {
    const photoId = getPhotoId(scene);
    const photo = scene.photos.find(p => p.id === photoId);
    if (!photo) {
        throw Error();
    }
    return photo;
};

const getPhotoId = (scene: Scene): number => {
    return scene._uiData.photoId;
};

const getRectStyle = (rect: Rect, containerDimensions: Dimensions): RectStyle => {
    return {
        left: (0.5 * containerDimensions.width + rect.x - 0.5 * rect.width) + 'px',
        top: (0.5 * containerDimensions.height - rect.y - 0.5 * rect.height) + 'px',
        width: rect.width + 'px',
        height: rect.height + 'px'
    };
};

const getScaledRect = (rect: Rect, scale: number): Rect => {
    return {
        x: scale * rect.x,
        y: scale * rect.y,
        width: scale * rect.width,
        height: scale * rect.height
    };
};

const getScene = (data: Data): Scene => {
    const sceneId = getSceneId(data);
    const scene = data.scenes.find(s => s.id === sceneId);
    if (!scene) {
        throw Error();
    }
    return scene;
};

const getSceneId = (data: Data): number => {
    return data._uiData.sceneId;
};

const isReady = (data: Data): boolean => {
    return data._metadata.isReady;
};

const toTuple = (val: Vector3D): [number, number, number] => {
    return [ val.x, val.y, val.z ];
}

const clamp = (val: number, min: number, max: number): number => {
    return Math.min(Math.max(val, min), max);
};

const wrapAngle = (angle: number): number => {
    const TWO_PI = 2 * Math.PI;
    if (angle < 0) {
        return TWO_PI + angle % TWO_PI;
    }
    if (angle > TWO_PI) {
        return angle % TWO_PI;
    }
    return angle;
};

// Camera object used for orbit calculation
const cc = new PerspectiveCamera();

const calculateCameraTransformFromOrbit = (cameraOrbitTransform: CameraOrbitTransform): CameraTransform => {
    const newCot = cameraOrbitTransform;
    const rCosPhi = newCot.radius * Math.cos(newCot.phi);
    const position = {
        x: newCot.centerPosition.x + rCosPhi * Math.sin(newCot.theta),
        y: newCot.centerPosition.y + newCot.radius * Math.sin(newCot.phi),
        z: newCot.centerPosition.z + rCosPhi * Math.cos(newCot.theta)
    };
    // Use the Three JS camera lookAt function to calculate the camera
    // rotation
    cc.position.set(position.x, position.y, position.z);
    cc.lookAt(
        newCot.centerPosition.x,
        newCot.centerPosition.y,
        newCot.centerPosition.z
    );
    const rotation = {
        x: cc.rotation.x,
        y: cc.rotation.y,
        z: cc.rotation.z
    };
    const newCameraTransform = {
        fov: newCot.fov,
        position: position,
        rotation: rotation
    };
    return newCameraTransform;
};

const calculateCameraOrbitFromTransform = (cameraTransform: CameraTransform): CameraOrbitTransform => {
    const ct = cameraTransform;
    cc.position.set(ct.position.x, ct.position.y, ct.position.z);
    cc.rotation.set(ct.rotation.x, ct.rotation.y, ct.rotation.z);
    cc.updateMatrix();
    cc.updateMatrixWorld();
    const cDirection = new Vector3();
    cc.getWorldDirection(cDirection);
    cDirection.normalize();
    const ray = new Ray(cc.position, cDirection);
    // Choose the radius to be the distance from the camera to the
    // origin
    const radius = cc.position.distanceTo(new Vector3(0, 0, 0));
    // Find the orbit center position by moving radius units from
    // the camera position in the camera direction
    const centerPos = new Vector3();
    ray.at(radius, centerPos);
    // Calculate the orbit angles from the camera position and the
    // orbit center position
    const phi = Math.asin((ct.position.y - centerPos.y) / radius);
    const rCosPhi = radius * Math.cos(phi);
    const theta = Math.atan2(
        (ct.position.x - centerPos.x) / rCosPhi,
        (ct.position.z - centerPos.z) / rCosPhi
    );

    const cot = {
        fov: ct.fov,
        centerPosition: {
            x: centerPos.x,
            y: centerPos.y,
            z: centerPos.z
        },
        radius: radius,
        theta: theta,
        phi: phi
    };
    return cot;
};

export const Utils = {
    calculateCameraOrbitFromTransform,
    calculateCameraTransformFromOrbit,
    clamp,
    getClickedLineEndpoint,
    getClickedLineId,
    getClickedShapeEdgeLine,
    getDimensionsStyle,
    getDistanceSquared,
    getFileUrl,
    getLinePointPerpDistInfo,
    getPhoto,
    getPhotoId,
    getRectStyle,
    getScaledRect,
    getScene,
    getSceneId,
    isReady,
    toTuple,
    wrapAngle
};
