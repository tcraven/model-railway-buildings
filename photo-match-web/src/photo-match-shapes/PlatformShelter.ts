import { PhotoMatchShape } from '../types';

const getPhotoMatchShapes = (): PhotoMatchShape[] => {
    // Platform is 15 mm above ground
    // Estimated l x w: 182 x 32
    return [
        {
            // Platform shelter
            id: 1,
            position: { x: 0, y: 0, z: 0 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'house',
            params: {
                length: 182,
                width: 32,
                height: 50,
                roofHeight: 8
            }
        },
        {
            // Platform shelter roof
            id: 2,
            position: { x: 0, y: 50, z: 0 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'roof',
            params: {
                length: 182,
                width: 32,
                roofHeight: 8,
                roofThickness: 1.7,
                overhangSide: 3,
                overhangLeft: 3,
                overhangRight: 3
            }
        },
        {
            // Platform
            id: 3,
            position: { x: 0, y: 0, z: -32 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'box',
            params: {
                length: 282,
                width: 32,
                height: 15
            }
        },
        {
            // Door 1
            id: 4,
            position: { x: -91.2, y: 30.25, z: -0.5 },  // 0
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 11,  // 13
                width: 30.5
            }
        },
        {
            // Window set 1
            id: 5,
            position: { x: 0, y: 38, z: -16.2 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 182,
                width: 14
            }
        },
        {
            // Window 1 (right)
            // TO DO: Are all windows 7 x 14 ?
            id: 6,
            position: { x: 91.2, y: 37.25, z: -1.75 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0.5 * Math.PI },
            typeName: 'rect',
            params: {
                length: 7,
                width: 14
            }
        },
        {
            // Window 2 (front right)  76
            id: 7,
            position: { x: 76, y: 38, z: -16.2 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 7,
                width: 14
            }
        },
        {
            // Window 3 (front left 1)
            id: 8,
            position: { x: -55, y: 38, z: -16.2 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 7,
                width: 14
            }
        },
        {
            // Window 4 (front left 2)
            id: 9,
            position: { x: -72, y: 38, z: -16.2 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 7,
                width: 14
            }
        },
        {
            // Door set 1
            id: 10,
            position: { x: 30.5, y: 30.25, z: -16.2 },
            rotation: { x: 0.5 * Math.PI, y: 0, z: 0 },
            typeName: 'rect',
            params: {
                length: 55,
                width: 30.5
            }
        },
        {
            // Chimney
            id: 11,
            position: { x: -61, y: 0, z: 17 },
            rotation: { x: 0, y: 0, z: 0 },
            typeName: 'box',
            params: {
                length: 8,
                width: 5,
                height: 65.5
            }
        }


        // Door set is 55 wide
        // Door is 13 wide
        // - Three windows are equally spaced and take up the remaining space
        // => 55 - 13 = 42
        // 42 / 3 = 14  --  this is double the width of small windows
        // - Window height looks to be a bit larger, perhaps 15
        //      - A bit lower, aligned with the top of the door
        // - Windows have cross frames with 1/3 2/3 vertical split
    ];
};

export const PlatformShelter = {
    getPhotoMatchShapes
};
