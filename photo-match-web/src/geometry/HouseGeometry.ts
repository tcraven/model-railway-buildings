import { PhotoMatchGeometry } from './PhotoMatchGeometry';

type HouseGeometryParameters = {
    length: number,
    width: number,
    height: number,
    roofHeight: number
};

class HouseGeometry extends PhotoMatchGeometry {

    constructor(parameters: HouseGeometryParameters) {

        super();

        const l = parameters.length;
        const w = parameters.width;
        const h = parameters.height;
        const rh = parameters.roofHeight;

        // Vertices
        this.uniqueVertices = [
            // Floor 0-3
            -0.5 * l,   0,  -0.5 * w,
             0.5 * l,   0,  -0.5 * w,
             0.5 * l,   0,   0.5 * w,
            -0.5 * l,   0,   0.5 * w,

            // Ceiling 4-7
            -0.5 * l,   h,  -0.5 * w,
             0.5 * l,   h,  -0.5 * w,
             0.5 * l,   h,   0.5 * w,
            -0.5 * l,   h,   0.5 * w,

            // Roof ridge 8-9
            -0.5 * l,   h + rh,     0,
             0.5 * l,   h + rh,     0

            // // Floor 0-3
            // 0, 0, 0,
            // l, 0, 0,
            // l, 0, w,
            // 0, 0, w,

            // // Ceiling 4-7
            // 0, h, 0,
            // l, h, 0,
            // l, h, w,
            // 0, h, w,

            // // Roof ridge 8-9
            // 0, h + rh, 0.5 * w,
            // l, h + rh, 0.5 * w
        ];

        // Faces

        // Bottom
        this.addFace(0, 1, 2);
        this.addFace(0, 2, 3);

        // Front XY +Z
        this.addFace(3, 6, 7);
        this.addFace(2, 6, 3);

        // Front roof XY +Z
        this.addFace(6, 8, 7);
        this.addFace(6, 9, 8);

        // Back XY -Z
        this.addFace(0, 4, 5);
        this.addFace(0, 5, 1);

        // Back roof XY -Z
        this.addFace(4, 9, 5);
        this.addFace(4, 8, 9);

        // Right ZY +X
        this.addFace(1, 5, 2);
        this.addFace(2, 5, 6);

        // Right roof ZY +X
        this.addFace(6, 5, 9);

        // Left ZY -X
        this.addFace(0, 3, 7);
        this.addFace(0, 7, 4);

        // Left roof ZY -X
        this.addFace(4, 7, 8);

        // Edges

        // Floor edges
        this.addEdge(0, 1);
        this.addEdge(1, 2);
        this.addEdge(2, 3);
        this.addEdge(3, 0);
        
        // Ceiling edges
        this.addEdge(4, 5);
        this.addEdge(5, 6);
        this.addEdge(6, 7);
        this.addEdge(7, 4);
        
        // Wall edges
        this.addEdge(0, 4);
        this.addEdge(1, 5);
        this.addEdge(2, 6);
        this.addEdge(3, 7);

        // Roof edges
        this.addEdge(4, 8);
        this.addEdge(7, 8);
        this.addEdge(5, 9);
        this.addEdge(6, 9);

        // Roof ridge
        this.addEdge(8, 9);

        // Create the Three.js geometry from the vertices, edges and faces
        this.createGeometry();
    }

}

export { HouseGeometry };
