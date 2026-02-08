from fastmcp import FastMCP
mcp = FastMCP("arith")

def _as_number(x):
    """Accept ints/floats or numeric strings; raise clean errors otherwise"""
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        return float(x.strip())
    raise TypeError(f"Expected a number (int/float/string), got {type(x).__name__}")

@mcp.tool()
def add(a: str, b: str) -> float:
    """Add two numbers together"""
    return _as_number(a) + _as_number(b)

@mcp.tool()
def subtract(a: str, b: str) -> float:
    """Subtract b from a"""
    return _as_number(a) - _as_number(b)

@mcp.tool()
def multiply(a: str, b: str) -> float:
    """Multiply two numbers"""
    return _as_number(a) * _as_number(b)

@mcp.tool()
def divide(a: str, b: str) -> float:
    """Divide a by b"""
    num_a = _as_number(a)
    num_b = _as_number(b)
    if num_b == 0:
        raise ValueError("Cannot divide by zero")
    return num_a / num_b

@mcp.tool()
def power(base: str, exponent: str) -> float:
    """Raise base to the power of exponent"""
    return _as_number(base) ** _as_number(exponent)

# Run the server
if __name__ == "__main__":
    mcp.run()