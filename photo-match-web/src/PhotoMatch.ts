import { Mesh, MeshStandardMaterial, PerspectiveCamera, Scene } from 'three';
import { CameraTransform, Line, PhotoMatchShape, ShapeEdge, ShapeEdgeLine, ShapeMesh } from './types';
import { HouseGeometry } from './geometry/HouseGeometry';
import { RoofGeometry } from './geometry/RoofGeometry';
import { NelderMead } from './NelderMead';
import { Camera } from '@react-three/fiber';

// Data only (doesn't contain references or computed values)
const photoMatchShapes: PhotoMatchShape[] = [
    {
        id: 1,
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'house',
        params: {
            length: 170,
            width: 69,
            height: 48,
            roofHeight: 22
        }
    },
    {
        id: 2,
        position: { x: 0, y: 48, z: 0 },
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
        id: 3,
        position: { x: -114, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'house',
        params: {
            length: 58,
            width: 69,
            height: 81,
            roofHeight: 22
        }
    },
    {
        id: 4,
        position: { x: -114, y: 81, z: 0 },
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
    // TO DO: It appears that the main house is rotated 3.6 degrees and so is
    // not at a right angle to the rest of the station. Verify that this is
    // correct for the other photos!
    // 0.52 * Math.PI = 93.6 degrees
    // - I will use this position for photo matching but not for the model,
    //   since getting everything to line up will be much harder if I include
    //   this strange angle!
    {
        id: 5,
        position: { x: -177.5, y: 0, z: -34.5 },
        rotation: { x: 0, y: 0.50 * Math.PI, z: 0 },
        typeName: 'house',
        params: {
            length: 156,
            width: 69,
            height: 81,
            roofHeight: 22
        }
    },
    {
        id: 6,
        position: { x: -177.5, y: 81, z: -34.5 },
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
        id: 7,
        position: { x: -220, y: 0, z: -34.5 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'house',
        params: {
            length: 16,
            width: 36,
            height: 32,
            roofHeight: 14
        }
    },
    {
        id: 8,
        position: { x: -220, y: 32, z: -34.5 },
        rotation: { x: 0, y: 0, z: 0 },
        typeName: 'roof',
        params: {
            length: 16,
            width: 36,
            roofHeight: 14,
            roofThickness: 3,
            overhangSide: 3,
            overhangLeft: 3,
            overhangRight: 0
        }
    },
    {
        id: 9,
        position: { x: -122.5, y: 0, z: -70.5 },
        rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
        typeName: 'house',
        params: {
            length: 72,
            width: 53,
            height: 81,
            roofHeight: 17
        }
    },
    {
        id: 10,
        position: { x: -122.5, y: 81, z: -70.5 },
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
    }
];

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
        if (geometry === null) {
            throw 'unknown geometry type';
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

const getOptimalCameraTransform = (
    initialCameraTransform: CameraTransform,
    cameraAspect: number,
    photoMatchLines: Line[]
): CameraTransform => {
    const shapes = photoMatchShapes;
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
        for (const seLine of shapeEdgeLines) {
            if (seLine.photoMatchLineId === -1) {
                continue;
            }
            const pmLine = pmLinesById[seLine.photoMatchLineId];
            d += getSquaredDistancePointToLine(pmLine.v0.x, pmLine.v0.y, seLine.v0.x, seLine.v0.y, seLine.v1.x, seLine.v1.y);
            d += getSquaredDistancePointToLine(pmLine.v1.x, pmLine.v1.y, seLine.v0.x, seLine.v0.y, seLine.v1.x, seLine.v1.y);
        }
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

    return newCameraTransform;
};


export const PhotoMatch = {
    applyTransformToCamera,
    getShapeEdgeLines,
    getOptimalCameraTransform,
    getPerspectiveCamera,
    getShapeMeshes,
    photoMatchShapes
};
