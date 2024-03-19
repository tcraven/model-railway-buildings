import re
from decimal import Decimal
from cadquery import exporters, Workplane


Vertex = tuple[float, float]
VertexLoops = dict[int, list[Vertex]]


def _get_path_edges(path_strings: list[str]) -> list[str]:
    # return [p.strip()[1:].split(" L") for p in path_strings]

    # => "M43.0,33.0 L25.0,33.0 "
    # [['43.0,-33.0', '43.0,-15.0'], ...]

    path_edges = []
    for ps in path_strings:
        point_strings = ps.strip()[1:].split(" L")
        for i in range(len(point_strings)):
            if i == 0:
                continue
            path_edges.append([
                point_strings[i - 1],
                point_strings[i]
            ])

    return path_edges


def get_panel_vertex_loops(workplane: Workplane) -> VertexLoops:
    # Export CadQuery panel sketch to SVG using top down view
    svg_str = exporters.svg.getSVG(
        shape=exporters.utils.toCompound(workplane),
        opts={
            "width": 300,
            "height": 300,
            "marginLeft": 10,
            "marginTop": 10,
            "projectionDir": (0, 0, -1),  # Top
            "showAxes": False,
            "showHidden": False
        }
    )

    # print("XXX")
    # print(svg_str)
 
    # Get the <path /> elements from the SVG string
    # <path d="M43.0,33.0 L25.0,33.0 " />
    # => "M43.0,33.0 L25.0,33.0 "
    path_strings = re.findall("<path d=\"(.+)\"", svg_str)

    # [['43.0,-33.0', '43.0,-15.0'], ...]
    path_edges = _get_path_edges(path_strings=path_strings)

    vertex_index = 0
    vertices_dict = {}
    for pe in path_edges:
        for j in [0, 1]:
            pe[j] = _format_vertex_str(vertex_str=pe[j])
            if pe[j] not in vertices_dict:
                vertices_dict[pe[j]] = vertex_index
                vertex_index += 1

    vertices_by_index = {
        vertex_index: vertex_str
        for vertex_str, vertex_index in vertices_dict.items()
    }

    # print("XXX-2")
    # for xx in sorted(vertices_dict.keys()):
    #     print(xx)
    
    edges = []
    for pe in path_edges:
        edges.append([vertices_dict[pe[0]], vertices_dict[pe[1]]])
    
    vertex_neighbors: dict[int, list[int]] = {}
    for edge in edges:
        if edge[0] not in vertex_neighbors:
            vertex_neighbors[edge[0]] = []
        vertex_neighbors[edge[0]].append(edge[1])
        if edge[1] not in vertex_neighbors:
            vertex_neighbors[edge[1]] = []
        vertex_neighbors[edge[1]].append(edge[0])

    # print("XXX")
    # for vi, v in vertices_by_index.items():
    #     print(vi, v)
    # print(edges)
    # print(vertex_neighbors)

    # Create loops
    loop_dict = {}
    loop_index = 0
    filtered_edges = [edge for edge in edges]
    edge = filtered_edges[0]
    neighbors = []
    while True:
        # Add edges to loop
        j = 0
        while True:
            if j == 0:
                loop_dict[edge[0]] = loop_index
                loop_dict[edge[1]] = loop_index
                neighbors = vertex_neighbors[edge[1]]
            
            j += 1
            
            # If both neighbors are already in the loop, then stop
            if neighbors[0] in loop_dict and neighbors[1] in loop_dict:
                break
            if neighbors[0] not in loop_dict:
                loop_dict[neighbors[0]] = loop_index
                neighbors = vertex_neighbors[neighbors[0]]
            else:
                loop_dict[neighbors[1]] = loop_index
                neighbors = vertex_neighbors[neighbors[1]]
        
        # Get filtered edges (edges that don't already belong to a loop)
        filtered_edges = [edge for edge in edges if edge[0] not in loop_dict]
        
        # Stop if all edges have been processed
        if len(filtered_edges) == 0:
            break

        # Choose the next starting edge
        edge = filtered_edges[0]
        loop_index += 1

    loops: VertexLoops = {}
    for vertex, loop_index in loop_dict.items():
        if loop_index not in loops:
            loops[loop_index] = []
        loops[loop_index].append(_vertex_tuple(vertices_by_index[vertex]))

    # print(loops)

    return loops


def get_width_height(
        panel_vertices: VertexLoops
) -> tuple[float, float, float, float]:
    # Get width and height
    xs = []
    ys = []
    for vertices in panel_vertices.values():
        xs.extend([v[0] for v in vertices])
        ys.extend([v[1] for v in vertices])

    # print("XXX")
    # print(xs)
    # print(ys)

    center_offset_x = 0.5 * (min(xs) + max(xs))
    center_offset_y = 0.5 * (min(ys) + max(ys))
    
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)

    return width, height, center_offset_x, center_offset_y


def _format_vertex_str(vertex_str: str) -> str:
    # '41.62,-31.62' => '41.62,-31.62'
    # '31.619999999999997,-16.62' => '31.62,-16.62'
    # Note: the "+ 0" ensures that we never see -0.0, only 0.0

    vertex_list = []
    for x in vertex_str.split(","):
        # print(x)
        # xf = str(round(float(x), 4) + 0)
        xd = Decimal(x)
        xf = f"{xd:.8f}"
        if xf == "-0.00000000":
            xf = "0.00000000"
        # print(xf)
        vertex_list.append(xf)

    return ",".join(vertex_list)
    # return ",".join([str(round(float(x), 4) + 0) for x in vertex_str.split(",")])


def _vertex_tuple(vertex_str: str) -> Vertex:
    x, y = vertex_str.split(",")
    return (float(x), float(y))
