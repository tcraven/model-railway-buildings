import { Mesh, MeshStandardMaterial, PerspectiveCamera, Scene } from 'three';
import { CameraTransform, Line, PhotoMatchShape, ShapeEdge, ShapeEdgeLine, ShapeMesh } from './types';
import { BoxGeometry } from './geometry/BoxGeometry';
import { HouseGeometry } from './geometry/HouseGeometry';
import { RoofGeometry } from './geometry/RoofGeometry';
import { NelderMead } from './NelderMead';
import { RectGeometry } from './geometry/RectGeometry';


const getPhotoMatchShapes = (): PhotoMatchShape[] => {
    // Calculate shapes from parameters?

    // Platform is 15 mm above ground

    return [
        {
            // Waiting room
            id: 1,
            position: { x: 0, y: 0, z: 0 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'house',
            params: {
                length: 170,
                width: 69,
                height: 52,
                roofHeight: 22
            }
        },
        {
            // Waiting room roof
            id: 2,
            position: { x: 0, y: 52, z: 0 },
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
            // Side house
            id: 3,
            position: { x: -114, y: 0, z: 0 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'house',
            params: {
                length: 58,
                width: 69,
                height: 85,
                roofHeight: 22
            }
        },
        {
            // Side house roof
            id: 4,
            position: { x: -114, y: 85, z: 0 },
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
            // Main house
            id: 5,
            position: { x: -177.5, y: 0, z: -38 }, // z: -34.5
            rotation: { x: 0, y: 0.50 * Math.PI, z: 0 },
            typeName: 'house',
            params: {
                length: 156,
                width: 69,
                height: 85,
                roofHeight: 22
            }
        },
        {
            // Main house roof
            id: 6,
            position: { x: -177.5, y: 85, z: -38 },
            rotation: { x: 0, y: 0.50 * Math.PI, z: 0 },
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
            // Main house porch
            id: 7,
            position: { x: -220, y: 0, z: -38 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'house',
            params: {
                length: 15,  // 16
                width: 34,  // 36
                height: 36.5,  // 32
                roofHeight: 13.5
            }
        },
        {
            // Main house porch roof
            id: 8,
            position: { x: -220, y: 36.5, z: -38 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'roof',
            params: {
                length: 16,
                width: 34,
                roofHeight: 13.5,
                roofThickness: 2.5,
                overhangSide: 4,
                overhangLeft: 4,
                overhangRight: 0
            }
        },
        {
            // Back house
            id: 9,
            position: { x: -122.5, y: 0, z: -70.5 },
            rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
            typeName: 'house',
            params: {
                length: 72,
                width: 53,
                height: 85,
                roofHeight: 17
            }
        },
        {
            // Back house roof
            id: 10,
            position: { x: -122.5, y: 85, z: -70.5 },
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
        },
        {
            // Waiting room platform
            id: 11,
            position: { x: 0, y: 0, z: 77 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'box',
            params: {
                length: 170,
                width: 85,
                height: 15
            }
        },
        {
            // Waiting room window set
            id: 12,
            position: { x: 0, y: 34.5, z: 34.7 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 156,
                width: 22
            }
        },
        {
            // Waiting room window 1
            id: 13,
            position: { x: -46.5, y: 34.5, z: 34.7 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 11,
                width: 22
            }
        },
        {
            // Waiting room window 2
            id: 14,
            position: { x: -19.5, y: 34.5, z: 34.7 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 11,
                width: 22
            }
        },
        {
            // Waiting room window 3
            id: 15,
            position: { x: 28.5, y: 34.5, z: 34.7 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 11,
                width: 22
            }
        },
        {
            // Waiting room window 4
            id: 16,
            position: { x: 49.5, y: 34.5, z: 34.7 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 11,
                width: 22
            }
        },
        {
            // Waiting room door 1
            id: 17,
            position: { x: -72, y: 30.25, z: 34.9 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 13,
                width: 30.5
            }
        },
        {
            // Waiting room door 2
            id: 18,
            position: { x: 5, y: 30.25, z: 34.9 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 13,
                width: 30.5
            }
        },
        {
            // Waiting room door 3
            id: 19,
            position: { x: 72.5, y: 30.25, z: 34.9 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 13,
                width: 30.5
            }
        },
        {
            // Side house window 1
            id: 20,
            position: { x: -98.75, y: 34.5, z: 34.7 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 11.5,
                width: 22
            }
        },
        {
            // Side house window 2
            id: 21,
            position: { x: -125, y: 34.5, z: 34.7 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 11.5,
                width: 22
            }
        },
        {
            // Side house window 3
            id: 22,
            position: { x: -113.5, y: 71.5, z: 34.7 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 13,
                width: 20
            }
        },
        {
            // Main house window 1
            id: 23,
            position: { x: -161.75, y: 34.5, z: 40.2 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 10,
                width: 22
            }
        },
        {
            // Main house window 2
            id: 24,
            position: { x: -193, y: 34.5, z: 40.2 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 10,
                width: 22
            }
        },
        {
            // Main house arch window
            id: 25,
            position: { x: -177.5, y: 69.5, z: 40.2 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 9,
                width: 13
            }
        },
        {
            // Main house window set 1
            id: 26,
            position: { x: -212.1, y: 69, z: -38 }, // z: -37
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 102,
                width: 22
            }
        },
        {
            // Main house window 3
            id: 27,
            position: { x: -212.1, y: 69, z: 6 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 14,
                width: 22
            }
        },
        {
            // Main house window 4
            id: 28,
            position: { x: -212.1, y: 69, z: -38 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 10.5,
                width: 22
            }
        },
        {
            // Main house window 5
            id: 29,
            position: { x: -212.1, y: 69, z: -82 }, // 71.5 ?
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 14,
                width: 22
            }
        },
        {
            // Main house window 6
            id: 30,
            position: { x: -212.1, y: 28.5, z: 6 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 14,
                width: 22
            }
        },
        {
            // Main house window 7
            id: 31,
            position: { x: -212.1, y: 28.5, z: -82 }, // 71.5 ?
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 14,
                width: 22
            }
        },
        {
            // Main house porch door
            id: 32,
            position: { x: -227.7, y: 20.5, z: -38 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 13,
                width: 28
            }
        },
        {
            // Main house porch arch
            id: 33,
            position: { x: -227.7, y: 38.25, z: -38 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 13,
                width: 6.5
            }
        }
    ];
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
    initialCameraTransform: CameraTransform,
    cameraAspect: number,
    photoMatchLines: Line[]
): CameraTransform => {
    const shapes = getPhotoMatchShapes();
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
    getPhotoMatchShapes,
    getShapeMeshes
};
