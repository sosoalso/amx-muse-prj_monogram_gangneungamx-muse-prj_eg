from mojo import context

from config import CAM_IP_LIST, TP_01, TP_PORT_CAM
from lib.button import add_button
from lib.lib_tp import (
    tp_set_button,
    tp_set_button_in_range,
    tp_set_button_text_unicode,
    tp_show_popup,
)
from lib.simpleurlrequests import url_get

# ---------------------------------------------------------------------------- #


class PanaCam:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.is_fast = False
        self.last_recall_preset = 0

    def toggle_speed(self):
        self.is_fast = not self.is_fast

    def set_speed(self, speed):
        self.is_fast = speed is True

    def get_speed(self):
        return 24 if self.is_fast else 12

    def get_tilt_speed(self):
        return 24 if self.is_fast else 12

    def get_pan_speed(self):
        return 24 if self.is_fast else 12

    def get_zoom_speed(self):
        return 24 if self.is_fast else 12

    # ---------------------------------------------------------------------------- #
    def move_up(self):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23T{50+self.get_speed():02d}&res=1")

    def move_down(self):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23T{50-self.get_speed():02d}&res=1")

    def move_left(self):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23P{50-self.get_speed():02d}&res=1")

    def move_right(self):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23P{50+self.get_speed():02d}&res=1")

    def move_stop(self):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23PTS5050&res=1")

    def zoom_in(self):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23Z&res=1")

    def zoom_out(self):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23Z{50+self.get_zoom_speed():02d}&res=1")

    def zoom_stop(self):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23Z{50-self.get_zoom_speed():02d}&res=1")

    def recall_preset(self, preset_no):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23R{preset_no:02d}&res=1")
        self.last_recall_preset = preset_no

    def store_preset(self, preset_no):
        url_get(f"http://{self.ip_address}/cgi-bin/aw_ptz?cmd=%23M{preset_no:02d}&res=1")


# ---------------------------------------------------------------------------- #
NUM_CAM = 2
cam_instance_list = [PanaCam(ip) for ip in CAM_IP_LIST]
# ---------------------------------------------------------------------------- #


class UICam:
    BTN_CAM_SELECT = [111, 112]
    BTN_UP = 101
    BTN_DOWN = 102
    BTN_LEFT = 103
    BTN_RIGHT = 104
    BTN_ZOOM_IN = 105
    BTN_ZOOM_OUT = 106
    BTN_TOGGLE_SPEED = 107

    def __init__(self, tp, tp_port, cam_instance_list):
        self.tp = tp
        self.tp_port = tp_port
        self.cam_list = cam_instance_list
        self.selected_cam = 0
        self.last_recall_preset = 0

    def select_cam(self, selected_cam):
        self.selected_cam = selected_cam
        self.refresh_cam_select_button()
        self.refresh_preset_button()
        self.refresh_speed_button()

    def refresh_cam_select_button(self):
        for index, btn in enumerate(self.BTN_CAM_SELECT):
            tp_set_button(self.tp, self.tp_port, btn, self.selected_cam == index + 1)

    def refresh_preset_button(self):
        context.log.info(f"refresh_preset_button: selected_cam={self.selected_cam}")
        if 1 <= self.selected_cam <= NUM_CAM:
            tp_set_button_in_range(
                self.tp, self.tp_port, 1, 10, cam_instance_list[self.selected_cam - 1].last_recall_preset
            )
        else:
            tp_set_button_in_range(self.tp, self.tp_port, 1, 10, False)

    def refresh_speed_button(self):
        if 1 <= self.selected_cam <= NUM_CAM:
            tp_set_button(
                self.tp, self.tp_port, self.BTN_TOGGLE_SPEED, cam_instance_list[self.selected_cam - 1].is_fast
            )
        else:
            tp_set_button(self.tp, self.tp_port, self.BTN_TOGGLE_SPEED, False)

    def refresh_cam_all_button(self):
        self.refresh_cam_select_button()
        self.refresh_preset_button()
        self.refresh_speed_button()

    def show_cam_popup(self, idx_cam, idx_preset):
        tp_set_button_text_unicode(self.tp, 1, 51, f"{idx_cam}번 카메라 {idx_preset}번 프리셋이 저장되었습니다.")
        tp_show_popup(self.tp, "popup_notification")

    # ---------------------------------------------------------------------------- #
    def add_tp_cam(self):
        def select_cam(idx_cam):  # 기본 매개변수로 idx_cam 캡처
            self.selected_cam = idx_cam + 1
            self.refresh_cam_select_button()
            self.refresh_preset_button()
            self.refresh_speed_button()

        def recall_preset(idx_preset):
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].recall_preset(idx_preset)
                self.refresh_preset_button()

        def store_preset(idx_preset):
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].store_preset(idx_preset)
                self.show_cam_popup(self.selected_cam, idx_preset)

        def move_up():
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].move_up()

        def stop_move():
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].move_stop()

        def move_down():
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].move_down()

        def move_left():
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].move_left()

        def move_right():
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].move_right()

        def zoom_in():
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].zoom_in()

        def zoom_out():
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].zoom_out()

        def stop_zoom():
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].zoom_stop()

        def toggle_speed():
            if 1 <= self.selected_cam <= NUM_CAM:
                self.cam_list[self.selected_cam - 1].toggle_speed()
            self.refresh_speed_button()

        # ---------------------------------------------------------------------------- #
        # NOTE : 카메라 선택 버튼 | ch 111-113
        for idx_cam, btn in enumerate(self.BTN_CAM_SELECT):
            add_button(self.tp, self.tp_port, btn, "push", lambda idx_cam=idx_cam: select_cam(idx_cam))
        # NOTE : 카메라 프리셋 버튼 | ch 1-10
        for idx_preset in range(1, 10 + 1):
            preset_button = add_button(
                self.tp, self.tp_port, idx_preset, "release", lambda idx_preset=idx_preset: recall_preset(idx_preset)
            )
            preset_button.on("hold_1.5", store_preset)
        # NOTE : 카메라 각종 버튼 | ch 101-107
        up_button = add_button(self.tp, self.tp_port, self.BTN_UP, "push", move_up, comment="카메라 상 버튼")
        up_button.on("release", stop_move)
        down_button = add_button(self.tp, self.tp_port, self.BTN_DOWN, "push", move_down, comment="카메라 하 버튼")
        down_button.on("release", stop_move)
        left_button = add_button(self.tp, self.tp_port, self.BTN_LEFT, "push", move_left, comment="카메라 좌 버튼")
        left_button.on("release", stop_move)
        right_button = add_button(self.tp, self.tp_port, self.BTN_RIGHT, "push", move_right, comment="카메라 우 버튼")
        right_button.on("release", stop_move)
        zoom_in_button = add_button(
            self.tp, self.tp_port, self.BTN_ZOOM_IN, "push", zoom_in, comment="카메라 줌인 버튼"
        )
        zoom_in_button.on("release", stop_zoom)
        zoom_out_button = add_button(
            self.tp, self.tp_port, self.BTN_ZOOM_OUT, "push", zoom_out, comment="카메라 줌 아웃 버튼"
        )
        zoom_out_button.on("release", stop_zoom)
        add_button(
            self.tp, self.tp_port, self.BTN_TOGGLE_SPEED, "push", toggle_speed, comment="카메라 스피드 토글 버튼"
        )
        context.log.info("add_tp_cam 등록 완료")

    def add_evt_cam(self):
        self.tp.online(lambda evt: self.refresh_cam_select_button())
        self.tp.online(lambda evt: self.refresh_preset_button())
        context.log.info("add_evt_cam 등록 완료")


# ---------------------------------------------------------------------------- #
ui_cam_01 = UICam(TP_01, TP_PORT_CAM, cam_instance_list)
# ---------------------------------------------------------------------------- #
