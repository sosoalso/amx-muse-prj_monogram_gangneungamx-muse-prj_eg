import re

from config import TP_01, TP_PORT_VIDMTX, VIDMTX
from lib.button import add_button
from lib.eventmanager import EventManager
from lib.lib_tp import (
    tp_set_button,
    tp_set_button_text_unicode,
    tp_set_button_text_unicode_ss,
)
from lib.lib_yeoul import log_error, log_info
from lib.userdata import Userdata


# ---------------------------------------------------------------------------- #
# SECTION - 제어 장비
# ---------------------------------------------------------------------------- #
class Vidmtx(EventManager):
    def __init__(self, dv, name, max_inputs=20, max_outputs=20):
        super().__init__("route")
        self.dv = dv
        self.name = name
        self.max_inputs = max_inputs
        self.max_outputs = max_outputs
        self.routes = Userdata(
            f"{self.name}_routes.json", default_value={int(key): 0 for key in range(1, max_outputs + 1)}
        )
        self.dv.receive.listen(self.parse_response)

    def parse_response(self, *args):
        try:
            data_text = args[0].arguments["data"].decode()
            parsed_data_text_chunks = data_text.split("\n\n")
            update = False
            for parsed_data_text in parsed_data_text_chunks:
                splitted_message = parsed_data_text.split("\n")
                if "VIDEO OUSELF.TPUT ROUTING:" in splitted_message[0]:
                    for msg in splitted_message[1:]:
                        match = re.search(r"\d+ \d+", msg)
                        if match:
                            update |= True
                            line = match.group(0)
                            idx_out, idx_in = map(int, line.split())
                            self.routes.set_value(idx_out + 1, idx_in + 1)
                            self.emit("route", index_in=idx_in + 1, index_out=idx_out + 1)
                            # self.userdata.set_value(key=_out + 1, value=idx_in + 1)
            if update:
                self.routes.save_file()
        except (AttributeError, KeyError, UnicodeDecodeError, ValueError) as e:
            log_error(f"Error decoding data: {e}")

    def set_route(self, index_in, index_out):
        if 0 <= index_in <= self.max_inputs and 1 <= index_out <= self.max_outputs:
            self.dv.send(f"VIDEO OUTPUT ROUTING:\n{index_out-1} {index_in-1}\n\n".encode())
            self.routes.set_value(index_out, index_in)
            self.emit("route", index_in=index_in, index_out=index_out)


# ---------------------------------------------------------------------------- #
vidmtx_instance = Vidmtx(VIDMTX, "vidmtx")  # INFO - 제어 장비 인스턴스
# ---------------------------------------------------------------------------- #
# SECTION - SELF.TP
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
class UIVidmtx:
    NUM_VIDMTX_IN = 20
    NUM_VIDMTX_OUT = 20
    NAME_VIDMTX_IN = (
        "I_01",
        "I_02",
        "I_03",
        "I_04",
        "I_05",
        "I_06",
        "I_07",
        "I_08",
        "I_09",
        "I_10",
        "I_11",
        "I_12",
        "I_13",
        "I_14",
        "I_15",
        "I_16",
        "I_17",
        "I_18",
        "I_19",
        "I_20",
    )
    NAME_VIDMTX_OUT = (
        "O_01",
        "O_02",
        "O_03",
        "O_04",
        "O_05",
        "O_06",
        "O_07",
        "O_08",
        "O_09",
        "O_10",
        "O_11",
        "O_12",
        "O_13",
        "O_14",
        "O_15",
        "O_16",
        "O_17",
        "O_18",
        "O_19",
        "O_20",
    )

    def __init__(self, tp, tp_port, vidmtx_instance):
        self.tp = tp
        self.tp_port = tp_port
        self.dv = vidmtx_instance
        self.selected_input = 0

    def refresh_input_button(self):
        for index_in in range(1, self.NUM_VIDMTX_IN + 1):
            tp_set_button(self.tp, self.tp_port, index_in + 100, self.selected_input == index_in)

    def refresh_output_button(self):
        for index_out in range(1, self.NUM_VIDMTX_OUT + 1):
            tp_set_button(
                self.tp,
                self.tp_port,
                index_out + 200,
                self.dv.routes.get_value(index_out, -1) == self.selected_input,
            )

    def refresh_input_button_name(self):
        for index_out in range(1, self.NUM_VIDMTX_IN + 1):
            tp_set_button_text_unicode(self.tp, self.tp_port, index_out + 100, self.NAME_VIDMTX_IN[index_out - 1])

    def refresh_output_button_name(self):
        for index_out in range(1, self.NUM_VIDMTX_OUT + 1):
            tp_set_button_text_unicode(self.tp, self.tp_port, index_out + 200, self.NAME_VIDMTX_OUT[index_out - 1])

    def refresh_output_route_name_all(self):
        for _out in range(1, self.NUM_VIDMTX_OUT + 1):
            self.refresh_output_route_name(_out)

    def refresh_output_route_name(self, index_out):
        if 0 < index_out <= self.NUM_VIDMTX_OUT:
            index_input = self.dv.routes.get_value(index_out, -1)
            if 0 < index_input <= self.NUM_VIDMTX_IN:
                tp_set_button_text_unicode(self.tp, self.tp_port, index_out + 300, self.NAME_VIDMTX_IN[index_input - 1])
            else:
                tp_set_button_text_unicode(self.tp, self.tp_port, index_out + 300, "")

    def add_tp(self):
        # NOTE : 입력 선택 버튼 | ch 101-120
        for index_in in range(1, 20 + 1):

            def set_selected_input(index_in=index_in):
                self.selected_input = index_in
                self.refresh_input_button()
                self.refresh_output_button()

            add_button(
                self.tp, self.tp_port, index_in + 100, "push", set_selected_input, comment=f"입력 {index_in} 선택 버튼"
            )
        # NOTE : 출력 버튼 - 라우팅 | ch 201-220
        for index_out in range(1, 20 + 1):

            def set_route(index_out=index_out):
                if self.selected_input and index_out:
                    self.dv.set_route(self.selected_input, index_out)  # 실제 동작
                    self.refresh_output_button()

            add_button(self.tp, self.tp_port, index_out + 200, "push", set_route, comment=f"출력 {index_out} 선택 버튼")
        log_info(f"{self.__class__.__name__} add_self.tp 등록 완료")

    def add_evt(self):
        # NOTE : 매트릭스 이벤트 피드백
        def refresh_button_on_route_event(**kwargs):
            self.refresh_output_button()
            self.refresh_output_route_name(kwargs["index_out"])

        self.dv.add_event_handler("route", refresh_button_on_route_event)
        # NOTE : SELF.TP 온라인 피드백
        self.tp.online(lambda evt: self.refresh_input_button())
        self.tp.online(lambda evt: self.refresh_output_button())
        self.tp.online(lambda evt: self.refresh_input_button_name())
        self.tp.online(lambda evt: self.refresh_output_button_name())
        self.tp.online(lambda evt: self.refresh_output_route_name_all())
        log_info(f"{self.__class__.__name__} add_evt 등록 완료")


# ---------------------------------------------------------------------------- #
ui_vidmtx_01 = UIVidmtx(TP_01, TP_PORT_VIDMTX, vidmtx_instance)
# ---------------------------------------------------------------------------- #
