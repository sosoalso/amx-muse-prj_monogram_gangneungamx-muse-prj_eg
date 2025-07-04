from atemhandler import AtemHandler
from config import TP_01, TP_PORT_VIDSWT
from lib.button import add_button
from lib.lib_tp import tp_set_button

# ---------------------------------------------------------------------------- #
vidswt_instance = AtemHandler(ip="10.20.0.88")
# ---------------------------------------------------------------------------- #


class UIVidswt:
    INDEX_PVW_BUTTONS = [101, 102, 103, 104, 105]
    INDEX_PGM_BUTTONS = [201, 202, 203, 204, 205]
    CUT_BUTTON = 50
    AUTO_BUTTON = 51

    def __init__(self, dv, tp, tp_port):
        self.dv = dv
        self.tp = tp
        self.tp_port = tp_port

    def add_tp(self):
        for idx, button in enumerate(self.INDEX_PVW_BUTTONS):
            add_button(self.tp, self.tp_port, button, "push", lambda idx_in=idx: self.dv.emit("switch_pvw", idx_in))
        for idx, button in enumerate(self.INDEX_PGM_BUTTONS):
            add_button(self.tp, self.tp_port, button, "push", lambda idx_in=idx: self.dv.emit("switch_pgm", idx_in))
        add_button(self.tp, self.tp_port, 50, "push", lambda: self.dv.emit("cut"))
        add_button(self.tp, self.tp_port, 51, "push", lambda: self.dv.emit("auto"))

    def add_evt(self):
        def on_pgm_switched(*args, **kwargs):
            idx_in = kwargs.get("idx_in", -1)
            print(kwargs)
            for idx, button in enumerate(self.INDEX_PGM_BUTTONS):
                tp_set_button(self.tp, self.tp_port, button, idx == idx_in)

        def on_pvw_switched(*args, **kwargs):
            idx_in = kwargs.get("idx_in", -1)
            for idx, button in enumerate(self.INDEX_PVW_BUTTONS):
                tp_set_button(self.tp, self.tp_port, button, idx == idx_in)

        self.dv.on("pgm_switched", on_pgm_switched)
        self.dv.on("pvw_switched", on_pvw_switched)


# ---------------------------------------------------------------------------- #
ui_vidswt_01 = UIVidswt(vidswt_instance, TP_01, TP_PORT_VIDSWT)
# ---------------------------------------------------------------------------- #
