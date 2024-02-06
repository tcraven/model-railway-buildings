import { PhotoMatchGeometry } from './PhotoMatchGeometry';

type RectGeometryParameters = {
    length: number,
    width: number
};

class RectGeometry extends PhotoMatchGeometry {

    constructor(parameters: RectGeometryParameters) {

        super();

        const l = parameters.length;
        const w = parameters.width;

        // Vertices
        this.uniqueVertices = [
            // Floor 0-3
            -0.5 * l,   0,  -0.5 * w,
             0.5 * l,   0,  -0.5 * w,
             0.5 * l,   0,   0.5 * w,
            -0.5 * l,   0,   0.5 * w
        ];

        // Faces

        // Top
        this.addFace(0, 2, 1);
        this.addFace(0, 3, 2);

        // Edges

        this.addEdge(0, 1);
        this.addEdge(1, 2);
        this.addEdge(2, 3);
        this.addEdge(3, 0);

        // Create the Three.js geometry from the vertices, edges and faces
        this.createGeometry();
    }

}

export { RectGeometry };
