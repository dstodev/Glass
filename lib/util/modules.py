import importlib
import os
import pathlib


def import_from_path(path: str, verbose=False) -> str:
    modules = [str(f.relative_to(".")).replace(os.sep, ".")[:-3] for f in pathlib.Path(path).rglob("*.py")]
    for module in modules:
        importlib.import_module(module)

    if verbose:
        path_sep = str(pathlib.Path(path))
        path_mod = path_sep.replace(os.sep, ".")
        print("Loaded modules", f"(.{os.sep}{path_sep}):", ", ".join([m.replace(f"{path_mod}.", "") for m in modules]))

    return "test"
