# from audiomixer import ui_mixer_01
from mojo import context

from cam import ui_cam_01
from config import TP_01
from lib.button import add_button_set_debug_flag
from lib.lib_tp import tp_set_debug_flag
from lib.lib_yeoul import set_log_level
from lib.uimenu import UIMenu
from relay import ui_relay_01
from vidmtx import ui_vidmtx_01
from vidprj import ui_vidprj_01_01, ui_vidprj_02_01
from vidrec import ui_vidrec_01

# from vidswt import ui_vidswt_01

# ---------------------------------------------------------------------------- #
set_log_level("debug")
add_button_set_debug_flag(True, True)
tp_set_debug_flag(True, True, True, True, True, True)
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    ui_menu_01 = UIMenu(TP_01)  # [v]
    # ---------------------------------------------------------------------------- #
    ui_vidrec_01.add_tp()  # [v]
    ui_vidrec_01.add_evt()  # [v]
    ui_cam_01.add_tp_cam()  # [v]
    ui_cam_01.add_evt_cam()  # [v]
    # ---------------------------------------------------------------------------- #
    # ui_mixer_01.add_tp()  # [v]
    # ui_mixer_01.add_evt()  # [v]
    # ---------------------------------------------------------------------------- #
    ui_vidmtx_01.add_tp()  # [v]
    ui_vidmtx_01.add_evt()  # [v]
    # ---------------------------------------------------------------------------- #
    ui_vidprj_01_01.add_tp()  # [v]
    ui_vidprj_01_01.add_evt()  # [v]
    ui_vidprj_02_01.add_tp()  # [v]
    ui_vidprj_02_01.add_evt()  # [v]
    # ---------------------------------------------------------------------------- #
    # ui_vidswt_01.add_tp()  # [v]
    # ui_vidswt_01.add_evt()  # [v]
    # ---------------------------------------------------------------------------- #
    ui_relay_01.add_tp()  # [v]
    ui_relay_01.add_evt()  # [v]
    # ---------------------------------------------------------------------------- #
    context.run(globals())
