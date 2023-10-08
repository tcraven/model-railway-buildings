import {
    Data,
    Dimensions,
    DimensionsStyle,
    Photo,
    Rect,
    RectStyle,
    Scene,
    Vector2D
} from './types';

export const getDimensionsStyle = (dimensions: Dimensions): DimensionsStyle => {
    return {
        width: dimensions.width + 'px',
        height: dimensions.height + 'px'
    }
};

export const getRectStyle = (rect: Rect, containerDimensions: Dimensions): RectStyle => {
    return {
        left: (0.5 * containerDimensions.width + rect.x - 0.5 * rect.width) + 'px',
        top: (0.5 * containerDimensions.height - rect.y - 0.5 * rect.height) + 'px',
        width: rect.width + 'px',
        height: rect.height + 'px'
    };
};

export const getScaledRect = (rect: Rect, scale: number): Rect => {
    return {
        x: scale * rect.x,
        y: scale * rect.y,
        width: scale * rect.width,
        height: scale * rect.height
    };
};

export const getFileUrl = (filename: string): string => {
    return `http://localhost:5007/file/${filename}`;
}

export const isReady = (data: Data): boolean => {
    return data._metadata.isReady;
};

export const getSceneId = (data: Data): number => {
    return data._uiData.sceneId;
};

export const getScene = (data: Data): Scene => {
    const sceneId = getSceneId(data);
    const scene = data.scenes.find(s => s.id === sceneId);
    if (!scene) {
        throw Error();
    }
    return scene;
};

export const getPhotoId = (scene: Scene): number => {
    return scene._uiData.photoId;
};

export const getPhoto = (scene: Scene): Photo => {
    const photoId = getPhotoId(scene);
    const photo = scene.photos.find(p => p.id === photoId);
    if (!photo) {
        throw Error();
    }
    return photo;
};

export const getDistanceSquared = (a: Vector2D, b: Vector2D): number => {
    const dx = a.x - b.x;
    const dy = a.y - b.y;
    return dx * dx + dy * dy;
};
