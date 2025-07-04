import threading

import PyATEMMax

from lib.eventmanager import EventManager


class AtemHandler(EventManager):
    def __init__(self, ip):
        super().__init__(
            "connected", "disconnected", "pgm_switched", "pvw_switched", "switch_pgm", "switch_pvw", "cut", "auto"
        )
        self.ip = ip
        self._thread_switcher = None
        self.init()

    # ---------------------------------------------------------------------------- #
    def init(self):
        self._thread_switcher = threading.Thread(target=self._handle_thread_switcher, daemon=True)
        self._thread_switcher.start()

    def _handle_thread_switcher(self):
        switcher = PyATEMMax.ATEMMax()

        def on_received(params):
            # context.log.info(f"on_received {params}")
            if params["cmd"] == "PrgI":
                idx_in = switcher.programInput[0].videoSource.value
                self.emit("pgm_switched", idx_in=idx_in)
            elif params["cmd"] == "PrvI":
                idx_in = switcher.previewInput[0].videoSource.value
                self.emit("pvw_switched", idx_in=idx_in)

        # ---------------------------------------------------------------------------- #
        # switcher.registerEvent(switcher.atem.events.connectAttempt, on_connect_attempt)
        # switcher.registerEvent(switcher.atem.events.connect, on_connected)
        # switcher.registerEvent(switcher.atem.events.disconnect, on_disconnected)
        # switcher.registerEvent(switcher.atem.events.warning, on_warning)
        switcher.registerEvent(switcher.atem.events.receive, on_received)

        # ---------------------------------------------------------------------------- #
        def on_switch_pgm(idx_in):
            # context.log.info(f"on_switch_pgm {idx_in}")
            self.emit("pgm_switched", idx_in=idx_in)
            switcher.setProgramInputVideoSource(0, idx_in)

        def on_switch_pvw(idx_in):
            # context.log.info(f"on_switch_pvw {idx_in}")
            self.emit("pvw_switched", idx_in=idx_in)
            switcher.setPreviewInputVideoSource(0, idx_in)

        def on_switch_cut():
            switcher.execCutME(0)

        def on_switch_auto():
            switcher.execAutoME(0)

        self.on("switch_pgm", on_switch_pgm)
        self.on("switch_pvw", on_switch_pvw)
        self.on("cut", on_switch_cut)
        self.on("auto", on_switch_auto)
        # ---------------------------------------------------------------------------- #
        switcher.connect(self.ip)
        # ---------------------------------------------------------------------------- #
