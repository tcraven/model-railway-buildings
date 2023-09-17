export const CameraMode = {
    FREE: 'FREE',
    ORBIT: 'ORBIT'
};

export type Vector3D = {
    x: number,
    y: number,
    z: number
};

export type CameraTransform = {
    fov: number,
    position: Vector3D,
    rotation: Vector3D
};

export const ControlMode = {
    PAN_ZOOM_2D: 'PAN_ZOOM_2D',
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

export type ViewTransform = {
    x: number,
    y: number,
    scale: number
};
