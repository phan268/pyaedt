import os
import sys

from System.Windows.Forms import MessageBox
from System.Windows.Forms import MessageBoxButtons
from System.Windows.Forms import MessageBoxIcon

is_linux = os.name == "posix"
# is_windows = not is_linux


def set_linux_environment(oDesktop):
    if is_linux:
        edt_root = os.path.normpath(oDesktop.GetExeDir())
        version = oDesktop.GetVersion()[2:6].replace(".", "")
        os.environ["ANSYSEM_ROOT{}".format(version)] = edt_root
        ld_library_path_dirs_to_add = [
            "{}/commonfiles/CPython/3_7/linx64/Release/python/lib".format(edt_root),
            "{}/commonfiles/CPython/3_10/linx64/Release/python/lib".format(edt_root),
            "{}/common/mono/Linux64/lib64".format(edt_root),
            "{}/Delcross".format(edt_root),
            "{}".format(edt_root),
        ]
        os.environ["LD_LIBRARY_PATH"] = ":".join(ld_library_path_dirs_to_add) + ":" + os.getenv("LD_LIBRARY_PATH", "")


def check_file(oDesktop, file_path):
    if not os.path.isfile(file_path):
        show_error(
            oDesktop,
            '"{}" does not exist. Please click on the "Install PyAEDT" button in the Automation ribbon.'.format(
                file_path
            ),
        )


def show_error(oDesktop, msg):
    oDesktop.AddMessage("", "", 2, str(msg))
    MessageBox.Show(str(msg), "Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
    sys.exit()
