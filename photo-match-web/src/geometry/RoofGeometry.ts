import { PhotoMatchGeometry } from './PhotoMatchGeometry';

type RoofGeometryParameters = {
    length: number,
    width: number,
    roofHeight: number,
    roofThickness: number,
    overhangSide: number,
    overhangLeft: number,
    overhangRight: number
};

class RoofGeometry extends PhotoMatchGeometry {

    constructor(parameters: RoofGeometryParameters) {

        super();

        const l = parameters.length;
        const w = parameters.width;
        const rh = parameters.roofHeight;
        const rt = parameters.roofThickness;
        const os = parameters.overhangSide;
        const ol = parameters.overhangLeft;
        const or = parameters.overhangRight;

        // Vertices
        // Three.js uses x, z, y coordinates

        const xl = -0.5 * l - ol;
        const xr = 0.5 * l + or;
        const Py = 0;
        const Pz = rh;
        const Qy = 0.5 * w + os;
        const Qz = -2 * rh * os / w;

        this.uniqueVertices = [
            // Right vertices 0-5
            xr, Pz, Py,
            xr, Qz, Qy,
            xr, Qz + rt, Qy,
            xr, Pz + rt, Py,
            xr, Qz + rt, -Qy,
            xr, Qz, -Qy,

            // Left vertices 6-11
            xl, Pz, Py,
            xl, Qz, Qy,
            xl, Qz + rt, Qy,
            xl, Pz + rt, Py,
            xl, Qz + rt, -Qy,
            xl, Qz, -Qy
        ];

        // Faces

        // Right
        this.addFace(0, 2, 1);
        this.addFace(0, 3, 2);
        this.addFace(0, 4, 3);
        this.addFace(0, 5, 4);

        // Left
        this.addFace(6, 7, 8);
        this.addFace(6, 8, 9);
        this.addFace(6, 9, 10);
        this.addFace(6, 10, 11);

        // Front
        this.addFace(5, 11, 10);
        this.addFace(5, 10, 4);

        // Back
        this.addFace(1, 8, 7);
        this.addFace(1, 2, 8);

        // Bottom front
        this.addFace(0, 6, 11);
        this.addFace(0, 11, 5);

        // Bottom back
        this.addFace(0, 1, 7);
        this.addFace(0, 7, 6);

        // Top front
        this.addFace(3, 4, 10);
        this.addFace(3, 10, 9);

        // Top back
        this.addFace(2, 3, 8);
        this.addFace(3, 9, 8);

        // Edges

        // Right
        this.addEdge(0, 1);
        this.addEdge(1, 2);
        this.addEdge(2, 3);
        this.addEdge(3, 4);
        this.addEdge(4, 5);
        this.addEdge(5, 0);

        // Left
        this.addEdge(6, 7);
        this.addEdge(7, 8);
        this.addEdge(8, 9);
        this.addEdge(9, 10);
        this.addEdge(10, 11);
        this.addEdge(11, 6);

        // Front
        this.addEdge(4, 10);
        this.addEdge(5, 11);

        // Back
        this.addEdge(1, 7);
        this.addEdge(2, 8);

        // Top
        this.addEdge(3, 9);

        // Bottom
        this.addEdge(0, 6);

        // Create the Three.js geometry from the vertices, edges and faces
        this.createGeometry();
    }

}

export { RoofGeometry };
