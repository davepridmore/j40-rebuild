# Auto-load the J40 reference model when FreeCAD starts.
# Installed under the user's FreeCAD Mod directory.

from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui


ROOT = Path("/Users/davidpridmore/IdeaProjects/J40")
LOADER_MACRO = ROOT / "data" / "manual" / "cad" / "j40_reference_model" / "freecad" / "J40ReferenceModelAutoUpdate.FCMacro"


def run_j40_loader():
    if not LOADER_MACRO.exists():
        App.Console.PrintError(f"J40 loader macro not found: {LOADER_MACRO}\n")
        return
    namespace = {"__file__": str(LOADER_MACRO)}
    code = LOADER_MACRO.read_text(encoding="ascii")
    exec(compile(code, str(LOADER_MACRO), "exec"), namespace, namespace)


def run_j40_loader_once():
    if getattr(App, "J40AutoLoaderStarted", False):
        return
    App.J40AutoLoaderStarted = True
    run_j40_loader()


class J40AutoLoaderWorkbench(Workbench):
    MenuText = "J40 Auto Loader"
    ToolTip = "Load the J40 reference CAD model"

    def Initialize(self):
        return

    def Activated(self):
        run_j40_loader()

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(J40AutoLoaderWorkbench())

try:
    from PySide6 import QtCore
except Exception:
    try:
        from PySide2 import QtCore
    except Exception:
        QtCore = None


if QtCore is not None:
    QtCore.QTimer.singleShot(2500, run_j40_loader_once)
else:
    run_j40_loader_once()
