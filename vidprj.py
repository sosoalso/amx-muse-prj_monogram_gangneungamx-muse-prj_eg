from mojo import context

from config import TP_01, VIDPRJ_LIST
from lib.button import add_button
from lib.eventmanager import EventManager
from lib.lib_tp import tp_set_button
from lib.lib_yeoul import log_info
from lib.scheduler import Scheduler


# ---------------------------------------------------------------------------- #
# SECTION - 제어 장비
# ---------------------------------------------------------------------------- #
class PJLink(EventManager):
    def __init__(self, dv, name="PJLink"):
        super().__init__("power", "poweron", "poweroff", "mute", "muted", "unmuted", "poll")
        self.dv = dv
        self.name = name
        self.power = False
        self.mute = False
        self.source = "0"
        self.poll = Scheduler(name=self.name + " poll")
        self.dv.receive.listen(self.parse_response)
        self.dv.connect()
        self.start_poll()

    def start_poll(self, *args):
        def query_power():
            self.dv.send("%1POWR ?\r".encode())

        def query_mute():
            self.dv.send("%1AVMT ?\r".encode())

        self.poll.set_timeout(lambda: self.poll.set_interval(query_power, 10.0), 1.0)
        self.poll.set_timeout(lambda: self.poll.set_interval(query_mute, 10.0), 2.0)

    def parse_response(self, *args):
        if not args or not hasattr(args[0], "arguments") or "data" not in args[0].arguments:
            context.log.error(f"수신 응답은 잘못된 형식입니다. {args=}")
        else:
            try:
                data_text = args[0].arguments["data"].decode("utf-8")
                response = data_text.split("\r")[0]
                if "%1POWR=" in response:
                    res = response.partition("=")[2]
                    if res == "1":
                        self.power = True
                    elif res == "0":
                        self.power = False
                    self.emit("power", value=self.power, this=self)
                elif "%1AVMT=" in response:
                    res = response.partition("=")[2]
                    if res == "31":
                        self.mute = True
                    elif res == "30":
                        self.mute = False
                    self.emit("mute", value=self.mute, this=self)
            except (AttributeError, KeyError, UnicodeDecodeError) as e:
                context.log.error(f"PJLink {self.name=} Error decoding data: {e}")

    def set_power(self, value):
        self.dv.send("%1POWR 1\r".encode() if value else "%1POWR 0\r".encode())
        self.power = value
        self.emit("power", value=value, this=self)

    def power_on(self):
        self.set_power(True)

    def power_off(self):
        self.set_power(False)

    def set_mute(self, value):
        self.dv.send("%1AVMT 31\r".encode() if value else "%1AVMT 30\r".encode())
        self.mute = value
        self.emit("mute", value=value, this=self)

    def mute_on(self):
        self.set_mute(True)

    def mute_off(self):
        self.set_mute(False)


# ---------------------------------------------------------------------------- #
vidprj_instance_list = tuple(PJLink(d, name=f"vidprj_0{i}") for i, d in enumerate(VIDPRJ_LIST))
# ---------------------------------------------------------------------------- #
# SECTION - TP
# ---------------------------------------------------------------------------- #
TP_PORT_VIDPRJ = 4


class UIVidprj:
    def __init__(self, tp, tp_port, vidprj_instance, vidprj_index=0):
        self.tp = tp
        self.tp_port = tp_port
        self.dv = vidprj_instance
        self.vidprj_index = vidprj_index
        # ---------------------------------------------------------------------------- #
        self.POWER_ON_BUTTON = 10 + self.vidprj_index
        self.POWER_OFF_BUTTON = 20 + self.vidprj_index
        self.UNMUTE_BUTTON = 30 + self.vidprj_index
        self.MUTE_BUTTON = 40 + self.vidprj_index

    def add_event_handlers(self):
        self.dv.on("power", self.refresh_vidprj_power_button)
        self.dv.on("mute", self.refresh_vidprj_mute_button)

    def refresh_vidprj_power_button(self, *args, **kwargs):
        tp_set_button(self.tp, self.tp_port, self.POWER_ON_BUTTON, self.dv.power)
        tp_set_button(self.tp, self.tp_port, self.POWER_OFF_BUTTON, not self.dv.power)

    def refresh_vidprj_mute_button(self, *args, **kwargs):
        tp_set_button(self.tp, self.tp_port, self.UNMUTE_BUTTON, not self.dv.mute)
        tp_set_button(self.tp, self.tp_port, self.MUTE_BUTTON, self.dv.mute)

    def add_tp(self):
        add_button(
            self.tp,
            self.tp_port,
            self.POWER_ON_BUTTON,
            "push",
            self.dv.power_on,
            comment=f"비디오 프로젝터 {self.vidprj_index}번 전원 켜기 버튼",
        )
        add_button(
            self.tp,
            self.tp_port,
            self.POWER_OFF_BUTTON,
            "push",
            self.dv.power_off,
            comment=f"비디오 프로젝터 {self.vidprj_index}번 전원 끄기 버튼",
        )
        add_button(
            self.tp,
            self.tp_port,
            self.UNMUTE_BUTTON,
            "push",
            self.dv.mute_off,
            comment=f"비디오 프로젝터 {self.vidprj_index}번 뮤트 해제 버튼",
        )
        add_button(
            self.tp,
            self.tp_port,
            self.MUTE_BUTTON,
            "push",
            self.dv.mute_on,
            comment=f"비디오 프로젝터 {self.vidprj_index}번 뮤트 버튼",
        )
        log_info(f"{self.__class__.__name__} add_tp 등록 완료")

    def add_evt(self):
        # NOTE : 비디오 프로젝터 이벤트 피드백
        self.dv.on("power", self.refresh_vidprj_power_button)
        self.dv.on("mute", self.refresh_vidprj_mute_button)
        # NOTE : TP 온라인 피드백
        self.tp.online(lambda evt: self.refresh_vidprj_power_button())
        self.tp.online(lambda evt: self.refresh_vidprj_mute_button())
        # ---------------------------------------------------------------------------- #
        log_info(f"{self.__class__.__name__} add_evt 등록 완료")


# ---------------------------------------------------------------------------- #
ui_vidprj_01_01 = UIVidprj(TP_01, TP_PORT_VIDPRJ, vidprj_instance_list[0], 1)
ui_vidprj_02_01 = UIVidprj(TP_01, TP_PORT_VIDPRJ, vidprj_instance_list[1], 2)
# ---------------------------------------------------------------------------- #
