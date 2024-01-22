import {
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

const getClickedLineId = (mousePosition: Vector2D, lines: Line[]): number | null => {
    const maxPerpDistSq = 0.00006;
    for (const line of lines) {
        const pdi = getLinePointPerpDistInfo(line, mousePosition);
        if (pdi.isOnLine && pdi.perpDistSq <= maxPerpDistSq) {
            return line.id;
        }
    }
    return null;
};

const getLinePointPerpDistInfo = (line: Line, point: Vector2D): LinePointPerpDistInfo => {
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

export const Utils = {
    getClickedLineEndpoint,
    getClickedLineId,
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
    toTuple
};
