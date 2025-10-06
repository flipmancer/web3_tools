import re

def parse_func_signatures(filename="./opcode"):
    """
    Extracts unique 4-byte function selectors from a file.

    Args:
        filename (str): Path to the opcode file.

    Returns:
        set[str]: Unique function selector hex strings.
    """
    with open(filename, "r") as f:
        data = f.read()

    # Regex to capture PUSH4 function selectors (hex after PUSH4)
    selectors = re.findall(r'PUSH4\s+0x([0-9a-fA-F]{8})', data)

    # Only unique function selectors
    selectors_set = set()
    for sel in selectors:
        selectors_set.add(sel)

    return selectors_set

if __name__ == "__main__":
    """
    Example: 
        signatures = parse_func_signatures("./example-opcode_file")
    """

