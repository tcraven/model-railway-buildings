import { PhotoMatchShape } from '../types';

const getPhotoMatchShapes = (): PhotoMatchShape[] => {
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
                length: 16,  // 15
                width: 34,  // 34
                height: 35.5,  // 36.5
                roofHeight: 13.5
            }
        },
        {
            // Main house porch roof
            id: 8,
            position: { x: -220, y: 35.5, z: -38 },
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
            position: { x: -228.2, y: 20.5, z: -38 },
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
            position: { x: -228.2, y: 38.75, z: -38 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 13,
                width: 6.5
            }
        },
        {
            // Waiting room chimney 1
            id: 34,
            position: { x: -9, y: 49, z: 0 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'box',
            params: {
                length: 8,
                width: 11,
                height: 40
            }
        },
        {
            // Waiting room chimney 2
            id: 35,
            position: { x: 81.5, y: 49, z: 0 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'box',
            params: {
                length: 6,
                width: 9,
                height: 40
            }
        },
        {
            // Side house chimney
            id: 36,
            position: { x: -142, y: 81, z: 0 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'box',
            params: {
                length: 8,
                width: 11,
                height: 40
            }
        },
        {
            // Back house chimney
            id: 37,
            position: { x: -101, y: 71, z: -79.25 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'box',
            params: {
                length: 7.5,
                width: 10,
                height: 40
            }
        },
        {
            // z: -38
            // z-distance from center: 72.5
            // Main house chimney 1
            // z: 34.5
            id: 38,
            position: { x: -177.5, y: 82, z: 34.5 },
            rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
            typeName: 'box',
            params: {
                length: 7,  // 7
                width: 10.5,  // 10.5
                height: 40
            }
        },
        {
            // Main house chimney 2
            // z: -110.5
            id: 39,
            position: { x: -177.5, y: 82, z: -110.5 },
            rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
            typeName: 'box',
            params: {
                length: 7,
                width: 10.5,
                height: 40
            }
        },
        {
            // Main house chimney 1 base (temporary experiment)
            id: 40,
            position: { x: -177.5, y: 75, z: 34.5 },
            rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
            typeName: 'box',
            params: {
                length: 8,  // 7
                width: 11.5,  // 10.5
                height: 40
            }
        },
        {
            // Main house chimney 1 top layer 1 (temporary experiment)
            id: 41,
            position: { x: -177.5, y: 122, z: 34.5 },
            rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
            typeName: 'box',
            params: {
                length: 8,  // 7
                width: 11.5,  // 10.5
                height: 1
            }
        },
        {
            // Main house chimney 1 top layer 2 (temporary experiment)
            id: 42,
            position: { x: -177.5, y: 123, z: 34.5 },
            rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
            typeName: 'box',
            params: {
                length: 10,  // 7
                width: 13.5,  // 10.5
                height: 2
            }
        },
        {
            // Main house chimney 1 top layer 3 (temporary experiment)
            id: 43,
            position: { x: -177.5, y: 125, z: 34.5 },
            rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
            typeName: 'box',
            params: {
                length: 8,  // 7
                width: 11.5,  // 10.5
                height: 1
            }
        },
        {
            // Main house chimney 1 top layer 4 (temporary experiment)
            id: 44,
            position: { x: -177.5, y: 126, z: 34.5 },
            rotation: { x: 0, y: 0.5 * Math.PI, z: 0 },
            typeName: 'box',
            params: {
                length: 7,  // 7
                width: 10.5,  // 10.5
                height: 1 
            }
        }

    ];
};

export const Station = {
    getPhotoMatchShapes
};
