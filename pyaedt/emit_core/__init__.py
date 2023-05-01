from importlib import import_module
import os
import sys

EMIT_API_PYTHON = None

delcross_python_path = os.environ.get("ANSYS_DELCROSS_PYTHON_PATH")
if delcross_python_path:
    sys.path.append(delcross_python_path)


def emit_api_python():
    """
    Get the Emit backend API.

    The backend API is available once a pyaedt.Emit() object has been created. An Exception is raised if this method is called before a pyaedt.Emit() object has been created.
    """
    if not EMIT_API_PYTHON:
        raise Exception("A pyaedt.Emit() object must be initialized before using the EMIT API.")
    return EMIT_API_PYTHON


# need this as a function so that it can be set
# for the correct aedt version that the user is running
def _set_api(aedt_version):
    numeric_version = int(aedt_version[-3:])
    desktop_path = os.environ.get(aedt_version)
    if desktop_path and numeric_version > 231:
        path = os.path.join(desktop_path, "Delcross")
        sys.path.insert(0, path)
        global EMIT_API_PYTHON
        EMIT_API_PYTHON = import_module("EmitApiPython")
