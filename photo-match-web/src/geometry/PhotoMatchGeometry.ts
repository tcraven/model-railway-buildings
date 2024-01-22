import { BufferGeometry, Float32BufferAttribute, Vector3 } from 'three';

/**
 * Base class for photo match geometry objects that are Three BufferGeometry
 * objects that have defined vertices, edges and faces, and have
 * photo match edges (pmEdges) to be used for photo matching.
 */
export class PhotoMatchGeometry extends BufferGeometry {
    
    pmEdges: any[] = [];
    vertices: any[] = [];
    indices: any[] = [];
    normals: any[] = [];
    uvs: any[] = [];
    uniqueVertices: any[] = [];
    vertexCount = 0;

    addEdge(i0: number, i1: number): void {
        const v0 = new Vector3(
            this.uniqueVertices[i0 * 3],
            this.uniqueVertices[i0 * 3 + 1],
            this.uniqueVertices[i0 * 3 + 2]);

        const v1 = new Vector3(
            this.uniqueVertices[i1 * 3],
            this.uniqueVertices[i1 * 3 + 1],
            this.uniqueVertices[i1 * 3 + 2]);

        this.pmEdges.push([ v0, v1 ]);
    }

    addFace(i0: number, i1: number, i2: number): void {
        this.indices.push(
            this.vertexCount + 0,
            this.vertexCount + 1,
            this.vertexCount + 2);

        this.vertexCount += 3;
        
        const v0 = new Vector3(
            this.uniqueVertices[i0 * 3],
            this.uniqueVertices[i0 * 3 + 1],
            this.uniqueVertices[i0 * 3 + 2]);

        const v1 = new Vector3(
            this.uniqueVertices[i1 * 3],
            this.uniqueVertices[i1 * 3 + 1],
            this.uniqueVertices[i1 * 3 + 2]);

        const v2 = new Vector3(
            this.uniqueVertices[i2 * 3],
            this.uniqueVertices[i2 * 3 + 1],
            this.uniqueVertices[i2 * 3 + 2]);
        
        this.vertices.push(
            v0.x, v0.y, v0.z,
            v1.x, v1.y, v1.z,
            v2.x, v2.y, v2.z
        );
    
        const normal = new Vector3().crossVectors(
            new Vector3().subVectors(v1, v0),
            new Vector3().subVectors(v2, v0)
        ).normalize();
    
        this.normals.push(
            normal.x, normal.y, normal.z,
            normal.x, normal.y, normal.z,
            normal.x, normal.y, normal.z
        );
    
        this.uvs.push(
            0, 0,
            1, 0,
            1, 1
        );
    }

    createGeometry(): void {
        this.setIndex(this.indices);
        this.setAttribute('position', new Float32BufferAttribute(this.vertices, 3));
        this.setAttribute('normal', new Float32BufferAttribute(this.normals, 3));
        this.setAttribute('uv', new Float32BufferAttribute(this.uvs, 2));
    }
}
