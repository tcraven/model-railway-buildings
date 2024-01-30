import { Mesh, Vector3 } from 'three';
import { PhotoMatchGeometry } from './geometry/PhotoMatchGeometry';

export type Data = {
    _metadata: {
        version: number
        isReady: boolean
    },
    _uiData: {
        sceneId: number
    },
    scenes: Scene[]
};

export type Scene = {
    _uiData: {
        photoId: number
    }
    id: number
    name: string,
    photos: Photo[]
};

export type Photo = {
    _uiData: {
        photoOpacity: number
        linesOpacity: number
        modelOpacity: number
        controlMode: string
        viewTransform: ViewTransform
        lineId: number | null
        cameraTransform: CameraTransform
    },
    id: number,
    name: string,
    width: number,
    height: number,
    filename: string,
    lines: Line[]
};


export const CameraMode = {
    FREE: 'FREE',
    ORBIT: 'ORBIT'
};

export type CameraTransform = {
    fov: number,
    position: Vector3D,
    rotation: Vector3D
};

export const ControlMode = {
    PAN_ZOOM_2D: 'PAN_ZOOM_2D',
    EDIT_LINES: 'EDIT_LINES',
    ORBIT_3D: 'ORBIT_3D'
};

export type CssTransform = {
    x: number,
    y: number,
    scale: number
};

export type DimensionsStyle = {
    width: string,
    height: string
};

export type Dimensions = {
    width: number,
    height: number
};

export type Line = {
    id: number
    v0: Vector2D
    v1: Vector2D
    matchingShapeId: number
    matchingEdgeId: number
};

export type LineEndpoint = {
    id: number
    endpointIndex: number
};

export type LinePointPerpDistInfo = {
    t: number
    isOnLine: boolean
    perpDistSq: number
};

export type PhotoImage = {
    width: number,
    height: number,
    url: string
};

export type Rect = {
    x: number,
    y: number,
    width: number,
    height: number
};

export type RectStyle = {
    left: string,
    top: string,
    width: string,
    height: string
};

export type Vector2D = {
    x: number
    y: number
};

export type Vector3D = {
    x: number,
    y: number,
    z: number
};

export type ViewTransform = {
    x: number,
    y: number,
    scale: number
};

export type PhotoMatchShape = {
    id: number,
    position: Vector3D,
    rotation: Vector3D,
    typeName: 'house' | 'roof',
    params: any
};

export type ShapeEdge = {
    // shapeId: number
    // edgeId: number
    v0: Vector3
    v1: Vector3
};

export type ShapeEdgeLine = {
    shapeId: number
    edgeId: number
    photoMatchLineId: number
    v0: Vector2D
    v1: Vector2D
};

export type ShapeMesh = {
    id: number
    geometry: PhotoMatchGeometry
    mesh: Mesh
};
