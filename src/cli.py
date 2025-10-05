import asyncio
import importlib
import inspect
import pkgutil
import typer
from typing import Any

app = typer.Typer(help="🧩 Web3 Tools – Run any module interactively.")

def list_modules(package_name: str):
    """List available submodules inside a given package."""
    package = importlib.import_module(package_name)
    return [name for _, name, _ in pkgutil.iter_modules(package.__path__)]

def list_functions(module):
    """Return all callable functions (excluding private ones)."""
    return [name for name, obj in inspect.getmembers(module, inspect.isfunction) if not name.startswith("_")]

@app.command()
def run(
    package: str = typer.Option(..., "--package", "-p", help="Module type (e.g., parsers or decoders)"),
    module: str = typer.Option(..., "--module", "-m", help="Module name inside the package"),
    function: str = typer.Option(..., "--function", "-f", help="Function to run"),
    args: str = typer.Option(None, "--args", "-a", help="Arguments to pass to the function"),
    ):
    """
    Run a specific function from a given module interactively.
    """
    try:
        mod = importlib.import_module(f"{package}.{module}")
        func = getattr(mod, function)
    except (ImportError, AttributeError) as e:
        typer.echo(f"[!] Could not load {package}.{module}.{function} — {e}")
        raise typer.Exit(1)

    typer.echo(f"✅ Running {package}.{module}.{function}({",".join(args)})")
    try:
        args = args.split(" ") if args else []
        if asyncio.iscoroutinefunction(func):
            result = asyncio.run(func(*args))
        else:
            result = func(*args)

        typer.echo(f"\n📤 Result:\n{result}")
    except Exception as e:
        typer.echo(f"[!] Error while running function: {e}")

@app.command()
def menu():
    """Interactive menu to choose a module and function."""
    import inquirer  # pip install inquirer
    packages = ["parsers", "decoders"]
    pkg_choice = inquirer.list_input("Select package", choices=packages)
    modules = list_modules(f"{pkg_choice}")
    mod_choice = inquirer.list_input("Select module", choices=modules)
    module = importlib.import_module(f"{pkg_choice}.{mod_choice}")
    functions = list_functions(module)
    func_choice = inquirer.list_input("Select function", choices=functions)
    args_input = inquirer.text("Enter args (space-separated or leave empty)") or ""
    args = args_input.split(" ") if args_input else []

    typer.echo(f"\nRunning: {pkg_choice}.{mod_choice}.{func_choice}({args})\n")
    func = getattr(module, func_choice)
    try:
        if asyncio.iscoroutinefunction(func):
            result = asyncio.run(func(*args))
        else:
            result = func(*args)
        typer.echo(f"📤 Result:\n{result}")
    except Exception as e:
        typer.echo(f"[!] Error: {e}")

if __name__ == "__main__":
    """
    Run via direct cli call: 
        `python cli.py run -p parsers -m parse_opcode -f parse_func_signatures -a parsers/example-opcode_file`
         python cli.py run -p decoders -m decode_signatures -f decode_func_signatures -a "a9059cbb db006a75"
    OR
    Run via interactive menu:
        `python cli.py menu` 
    """
    app()