from mojo import context

from config import TP_01, TP_PORT_VIDREC, VIDREC
from lib.button import add_button
from lib.eventmanager import EventManager
from lib.lib_tp import tp_set_button


# ---------------------------------------------------------------------------- #
# SECTION - 제어 장비
# ---------------------------------------------------------------------------- #
class Vidrec(EventManager):
    def __init__(self, dv):
        super().__init__("transport")
        self.dv = dv
        self.transport = 0
        self.init()

    def init(self):
        self.dv.receive.listen(self.parse_response)

    def send(self, cmd):
        self.dv.send(f"{cmd}\r\n")

    def record(self):
        self.send("record")
        self.transport = "record"
        self.emit("transport", transport=self.transport, this=self)

    def stop(self):
        self.send("stop")
        self.transport = "stopped"
        self.emit("transport", transport=self.transport, this=self)

    def play(self):
        self.send("play")
        self.transport = "play"
        self.emit("transport", transport=self.transport, this=self)

    def track_prev(self):
        self.send("goto: clip id: -1")

    def track_next(self):
        self.send("goto: clip id: +1")

    def track_start(self):
        self.send("goto: clip: start")

    def track_end(self):
        self.send("goto: clip: end")

    def parse_response(self, *args):
        try:
            if not args or not hasattr(args[0], "arguments") or "data" not in args[0].arguments:
                return
            data_text = args[0].arguments["data"].decode("utf-8")
            while "\r\n" in data_text:
                response = data_text.split("\r\n", 1)
                if "status: " in response:
                    if "record" in response[7:]:
                        self.transport = "record"
                    elif "stopped" in response[7:]:
                        self.transport = "stopped"
                    elif "preview" in response[7:]:
                        self.transport = "preview"
                    elif "play" in response[7:]:
                        self.transport = "play"
                    else:
                        pass  # Add appropriate handling here if needed
            self.emit("transport", transport=self.transport, this=self)
        except (AttributeError, KeyError, UnicodeDecodeError) as e:
            context.log.debug(f"Error decoding data: {e}")


vidrec_instance = Vidrec(VIDREC)
# ---------------------------------------------------------------------------- #


class UIVidrec:
    RECORD_BUTTON = 1
    STOP_BUTTON = 2
    TRACK_NEXT_BUTTON = 3
    TRACK_PREV_BUTTON = 4
    PLAY_BUTTON = 5

    def __init__(self, tp, tp_port, dv_instance):
        self.tp = tp
        self.tp_port = tp_port
        self.dv = dv_instance
        self.transport = "stopped"

    def refresh_transport_button(self, **kwargs):
        transport = kwargs.get("transport")
        tp_set_button(self.tp, self.tp_port, self.RECORD_BUTTON, transport == "record")
        tp_set_button(self.tp, self.tp_port, self.STOP_BUTTON, transport == "stopped")
        # tp_set_button(self.tp, self.tp_port, self.PLAY_BUTTON, transport == "play")

    def add_tp(self):
        add_button(self.tp, self.tp_port, self.RECORD_BUTTON, "push", self.dv.record)
        add_button(self.tp, self.tp_port, self.STOP_BUTTON, "push", self.dv.stop)
        # add_button(self.tp, self.tp_port, self.PLAY_BUTTON, "push", self.dv.play)
        # add_button(self.tp, self.tp_port, self.PLAY_BUTTON, "push", lambda: self.dv.emit("transport", transport="play", this=self.dv))
        add_button(self.tp, self.tp_port, self.TRACK_NEXT_BUTTON, "push", self.dv.track_next)
        add_button(self.tp, self.tp_port, self.TRACK_PREV_BUTTON, "push", self.dv.track_prev)

    def add_evt(self):
        self.dv.on("transport", self.refresh_transport_button)


# ---------------------------------------------------------------------------- #
ui_vidrec_01 = UIVidrec(TP_01, TP_PORT_VIDREC, vidrec_instance)
# ---------------------------------------------------------------------------- #
