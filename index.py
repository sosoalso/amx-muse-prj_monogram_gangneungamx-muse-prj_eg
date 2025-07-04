from mojo import context

# from audiomixer import ui_mixer_01
from cam import ui_cam_01  # [v]
from config import TP_01
from lib.lib_tp import tp_set_debug_flag
from lib.lib_yeoul import set_log_level
from lib.uimenu import UIMenu
from relay import ui_relay_01  # [v]
from vidmtx import ui_vidmtx_01  # [v]
from vidprj import ui_vidprj_01_01, ui_vidprj_02_01  # [v]
from vidrec import ui_vidrec_01  # [v]
from vidswt import ui_vidswt_01  # [v]

# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
set_log_level("debug")
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
    ui_vidprj_01_01.add_tp()
    ui_vidprj_01_01.add_evt()
    ui_vidprj_02_01.add_tp()
    ui_vidprj_02_01.add_evt()
    # ---------------------------------------------------------------------------- #
    ui_vidswt_01.add_tp()  # [v]
    ui_vidswt_01.add_evt()  # [v]
    # ---------------------------------------------------------------------------- #
    ui_relay_01.add_tp()
    ui_relay_01.add_evt()
    # ---------------------------------------------------------------------------- #
    context.run(globals())
