import difflib
import os
import re


def write_file(filepath: str, data_str: str):
    with open(filepath, "w") as f:
        f.write(data_str)


def read_file(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()


def read_mesh_xml(filename: str) -> str:
    filepath = os.path.join("test_buildings", "mesh_xml", filename)
    return read_file(filepath)


def write_mesh_xml(filename: str, xml_str: str):
    """
    Writes mesh XML file to disk. Used to create unit test mesh XML files.
    """
    filepath = os.path.join("test_buildings", "mesh_xml", filename)
    return write_file(filepath=filepath, data_str=xml_str)


def get_diff(value_str: str, expected_str: str):
    diff_results = difflib.unified_diff(
        value_str.splitlines(keepends=True),
        expected_str.splitlines(keepends=True),
        fromfile="value_str",
        tofile="expected_str")
    
    return [dr for dr in diff_results]


def _overwrite_info_date(xml_str):
    return re.sub(
        '<info date=".+" schemav',
        '<info date="2024-01-01" schemav',
        xml_str)


def _split_shapes(xml_str):
    shapes_index = xml_str.find("<shapes>")
    return xml_str[:shapes_index], xml_str[shapes_index:]


def print_diff_lines(name, diff_lines):
    print("")
    print(f"{name}_DIFF_LENGTH", len(diff_lines))
    print(f"{name}_DIFF_START")
    for dr in diff_lines:
        print(dr, end="")
    print(f"{name}_DIFF_END")


def assert_equal_mesh_xml(mesh_xml_str, expected_mesh_xml_str):
    """
    - The model XML has the following sections:
        - info      Information including date written
                    - I need to ignore this as the date changes
        - label     Information about the shapes, names, number of children, etc
                    - We can diff this separately
                    - If different, a shape has been added or removed, or the
                      number of child objects has changed
        - shapes    Vertex and edge data
                    - If different, vertex and edge data is different (perhaps
                      because the position of something changed)
    """
    info_str, shapes_str = _split_shapes(xml_str=mesh_xml_str)
    info_str = _overwrite_info_date(xml_str=info_str)

    expected_info_str, expected_shapes_str = _split_shapes(
        xml_str=expected_mesh_xml_str)
    expected_info_str = _overwrite_info_date(xml_str=expected_info_str)

    info_diff_lines = get_diff(
        value_str=info_str,
        expected_str=expected_info_str)

    shapes_diff_lines = get_diff(
        value_str=shapes_str,
        expected_str=expected_shapes_str)
    
    if len(info_diff_lines) != 0:
        # There is an info diff
        print_diff_lines(name="INFO", diff_lines=info_diff_lines)
        raise AssertionError("Info is not equal")
    
    if len(shapes_diff_lines) != 0:
        # No info diff, but there is shapes diff
        print_diff_lines(name="SHAPES", diff_lines=shapes_diff_lines)
        raise AssertionError("Shapes are not equal")
    
    # There is no diff - the mesh XML is equal
    return
