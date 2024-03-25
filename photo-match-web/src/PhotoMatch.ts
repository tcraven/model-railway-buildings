import { Mesh, MeshStandardMaterial, PerspectiveCamera, Scene } from 'three';
import { CameraTransform, Line, PhotoMatchShape, PhotoMatchShapesDict, ShapeEdge, ShapeEdgeLine, ShapeMesh, ShapeMeshesDict } from './types';
import { BoxGeometry } from './geometry/BoxGeometry';
import { HouseGeometry } from './geometry/HouseGeometry';
import { RoofGeometry } from './geometry/RoofGeometry';
import { NelderMead } from './NelderMead';
import { RectGeometry } from './geometry/RectGeometry';
import { Station } from './photo-match-shapes/Station';
import { PlatformShelter } from './photo-match-shapes/PlatformShelter';

const getPhotoMatchShapesBySceneId = (): PhotoMatchShapesDict => {
    return {
        '1': Station.getPhotoMatchShapes(),
        '2': PlatformShelter.getPhotoMatchShapes()
    };
};

const applyTransformToCamera = (
    cameraTransform: CameraTransform,
    camera: PerspectiveCamera,
    cameraAspect: number
) => {    
    camera.aspect = cameraAspect;
    camera.fov = cameraTransform.fov; 
    const position = cameraTransform.position;
    camera.position.set(position.x, position.y, position.z);
    const rotation = cameraTransform.rotation;
    camera.rotation.set(rotation.x, rotation.y, rotation.z);
    camera.updateMatrix();
    camera.updateMatrixWorld();
    camera.updateProjectionMatrix();
};

const getShapeEdgeLines = (
    shapeMeshes: ShapeMesh[],
    camera: PerspectiveCamera,
    photoMatchLines: Line[]
): ShapeEdgeLine[] => {
    type MatchEdgesDict = { [ shapeId: number ]: { [ edgeId: number ]: number } };

    // Create match edges dict from photo match lines for faster lookup below
    const matchEdgesDict: MatchEdgesDict = {};
    for (const photoMatchLine of photoMatchLines) {
        const shapeId = photoMatchLine.matchingShapeId;
        const edgeId = photoMatchLine.matchingEdgeId;
        if (!matchEdgesDict[shapeId]) {
            matchEdgesDict[shapeId] = {};
        }
        matchEdgesDict[shapeId][edgeId] = photoMatchLine.id;
    }
    
    const shapeEdgeLines: ShapeEdgeLine[] = [];
    for (const shapeMesh of shapeMeshes) {
        const shapeId = shapeMesh.id;        
        for (let i = 0; i < shapeMesh.geometry.pmEdges.length; i++) {
            const matchEdgesOfShapeDict = matchEdgesDict[shapeId] || {};
            let photoMatchLineId = matchEdgesOfShapeDict[i];
            if (photoMatchLineId === undefined) {
                photoMatchLineId = -1;
            };
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
                photoMatchLineId: photoMatchLineId,
                v0: { x: p0.x, y: p0.y },
                v1: { x: p1.x, y: p1.y }
            });
        }

    }
    return shapeEdgeLines;
};

const getShapeMeshesBySceneId = (shapesBySceneId: PhotoMatchShapesDict): ShapeMeshesDict => {
    const shapeMeshesBySceneId: ShapeMeshesDict = {};
    for (const sceneId of Object.keys(shapesBySceneId)) {
        shapeMeshesBySceneId[sceneId] = getShapeMeshes(shapesBySceneId[sceneId]);
    }
    return shapeMeshesBySceneId;
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
        if (shape.typeName === 'box') {
            geometry = new BoxGeometry(shape.params);
        }
        if (shape.typeName === 'rect') {
            geometry = new RectGeometry(shape.params);
        }
        if (geometry === null) {
            throw new Error('unknown geometry type');
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
    return shapeMeshes;
};

// Gets the squared perpendicular distance from the point (px, py) to
// the line defined by the points (x0, y0) and (x1, y1)
const getSquaredDistancePointToLine = (
    px: number,
    py: number,
    x0: number,
    y0: number,
    x1: number,
    y1: number
): number => {
    const xa = x1 - x0;
    const ya = y1 - y0;
    const dd = xa * (y0 - py) - (x0 - px) * ya;
    return dd * dd / (xa * xa + ya * ya);
};

const cameraTransformToArray = (cameraTransform: CameraTransform): number[] => {
    return [
        cameraTransform.fov,
        cameraTransform.position.x,
        cameraTransform.position.y,
        cameraTransform.position.z,
        cameraTransform.rotation.x,
        cameraTransform.rotation.y,
        cameraTransform.rotation.z
    ];
};

const arrayToCameraTransform = (cameraTransformArray: number[]): CameraTransform => {
    return {
        fov: cameraTransformArray[0],
        position: {
            x: cameraTransformArray[1],
            y: cameraTransformArray[2],
            z: cameraTransformArray[3]
        },
        rotation: {
            x: cameraTransformArray[4],
            y: cameraTransformArray[5],
            z: cameraTransformArray[6]
        }
    };
};

const getPerspectiveCamera = (cameraTransform: CameraTransform, cameraAspect: number): PerspectiveCamera => {
    const camera = new PerspectiveCamera();
    applyTransformToCamera(cameraTransform, camera, cameraAspect);
    return camera;
};

const getConstraintError = (x: number, min: number, max: number): number => {
    if (x < min) {
        return (min - x) * (min - x);
    }
    if (x > max) {
        return (x - max) * (x - max);
    }
    return 0;
};

const getOptimalCameraTransform = (
    sceneId: number,
    initialCameraTransform: CameraTransform,
    cameraAspect: number,
    photoMatchLines: Line[]
): CameraTransform => {
    const shapes = getPhotoMatchShapesBySceneId()[sceneId.toString()];
    const shapeMeshes = getShapeMeshes(shapes);
    const camera = new PerspectiveCamera();

    const pmLinesById: { [ id: number ]: Line } = {};
    for (const pmLine of photoMatchLines) {
        pmLinesById[pmLine.id] = pmLine;
    }

    console.log('QQQ initialCameraTransform', initialCameraTransform);

    const cameraTransformArray0: number[] = cameraTransformToArray(initialCameraTransform);

    const fn = (cameraTransformArray: number[]): number => {
        const cameraTransform: CameraTransform = arrayToCameraTransform(cameraTransformArray);
        applyTransformToCamera(cameraTransform, camera, cameraAspect);
        const shapeEdgeLines = getShapeEdgeLines(shapeMeshes, camera, photoMatchLines);
        let d = 0;
        // Add the squared distances between each shape edge line and its
        // corresponding photo match line
        for (const seLine of shapeEdgeLines) {
            if (seLine.photoMatchLineId === -1) {
                continue;
            }
            const pmLine = pmLinesById[seLine.photoMatchLineId];
            d += getSquaredDistancePointToLine(pmLine.v0.x, pmLine.v0.y, seLine.v0.x, seLine.v0.y, seLine.v1.x, seLine.v1.y);
            d += getSquaredDistancePointToLine(pmLine.v1.x, pmLine.v1.y, seLine.v0.x, seLine.v0.y, seLine.v1.x, seLine.v1.y);
        }

        // Add errors to keep the values constrained
        const MIN_LENGTH = -2000;
        const MAX_LENGTH = 2000;
        const MIN_ANGLE = -2.1 * Math.PI;
        const MAX_ANGLE = 2.1 * Math.PI;

        d += getConstraintError(cameraTransform.fov, 10, 60);
        d += getConstraintError(cameraTransform.position.x, MIN_LENGTH, MAX_LENGTH);
        d += getConstraintError(cameraTransform.position.y, MIN_LENGTH, MAX_LENGTH);
        d += getConstraintError(cameraTransform.position.z, MIN_LENGTH, MAX_LENGTH);
        d += getConstraintError(cameraTransform.rotation.x, MIN_ANGLE, MAX_ANGLE);
        d += getConstraintError(cameraTransform.rotation.z, MIN_ANGLE, MAX_ANGLE);
        d += getConstraintError(cameraTransform.rotation.z, MIN_ANGLE, MAX_ANGLE);

        return d;
    };

    const result = NelderMead.optimize(
        fn,
        cameraTransformArray0,
        {
            maxIterations: 7 * 200 * 10,
            minErrorDelta: 1e-9
        });

    const newCameraTransform = arrayToCameraTransform(result.x);
    console.log('QQQ result', result);
    console.log('QQQ newCameraTransform', newCameraTransform);

    const MAX_ERROR = 0.01;
    if (result.fx > MAX_ERROR) {
        console.log('Error: Camera transform did not converge');
        return initialCameraTransform;
    }

    return newCameraTransform;
};


export const PhotoMatch = {
    applyTransformToCamera,
    getShapeEdgeLines,
    getOptimalCameraTransform,
    getPerspectiveCamera,
    // getPhotoMatchShapes,
    getPhotoMatchShapesBySceneId,
    getShapeMeshes,
    getShapeMeshesBySceneId
};
