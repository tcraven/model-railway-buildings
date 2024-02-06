import { PhotoMatchGeometry } from './PhotoMatchGeometry';

type BoxGeometryParameters = {
    length: number,
    width: number,
    height: number
};

class BoxGeometry extends PhotoMatchGeometry {

    constructor(parameters: BoxGeometryParameters) {

        super();

        const l = parameters.length;
        const w = parameters.width;
        const h = parameters.height;

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
            -0.5 * l,   h,   0.5 * w
        ];

        // Faces

        // Bottom
        this.addFace(0, 1, 2);
        this.addFace(0, 2, 3);

        // Front XY +Z
        this.addFace(3, 6, 7);
        this.addFace(2, 6, 3);

        // Back XY -Z
        this.addFace(0, 4, 5);
        this.addFace(0, 5, 1);

        // Right ZY +X
        this.addFace(1, 5, 2);
        this.addFace(2, 5, 6);

        // Left ZY -X
        this.addFace(0, 3, 7);
        this.addFace(0, 7, 4);

        // Top
        this.addFace(4, 6, 5);
        this.addFace(4, 7, 6);

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

        // Create the Three.js geometry from the vertices, edges and faces
        this.createGeometry();
    }

}

export { BoxGeometry };
