from config import (
    RELAY_MIC_01_DOWN,
    RELAY_MIC_01_STOP,
    RELAY_MIC_01_UP,
    RELAY_MIC_02_DOWN,
    RELAY_MIC_02_STOP,
    RELAY_MIC_02_UP,
    RELAY_PDU,
    TP_01,
    TP_PORT_RELAY,
)
from lib.button import add_button
from lib.lib_tp import tp_set_button
from lib.lib_yeoul import pulse

# ---------------------------------------------------------------------------- #
# PDU


class UIRelay:
    INDEX_PDU_ON = 51
    INDEX_PDU_OFF = 52
    INDEX_MIC_01_UP = 111
    INDEX_MIC_01_STOP = 112
    INDEX_MIC_01_DOWN = 113
    INDEX_MIC_02_UP = 114
    INDEX_MIC_02_STOP = 115
    INDEX_MIC_02_DOWN = 116

    def __init__(self, tp, tp_port):
        self.tp = tp
        self.tp_port = tp_port

    def set_relay(self, relay, state):
        relay.state.value = state

    def pulse_relay(self, relay, duration=0.5):

        def relay_off(relay=relay):
            self.set_relay(relay, False)

        @pulse(off_method=relay_off, duration=duration)
        def relay_on(relay=relay):
            self.set_relay(relay, True)

        relay_on()

    def add_tp(self):
        add_button(self.tp, self.tp_port, self.INDEX_PDU_ON, "hold_2.0", lambda: self.set_relay(RELAY_PDU, True))
        add_button(self.tp, self.tp_port, self.INDEX_PDU_OFF, "hold_2.0", lambda: self.set_relay(RELAY_PDU, False))
        add_button(self.tp, self.tp_port, self.INDEX_MIC_01_UP, "push", lambda: self.pulse_relay(RELAY_MIC_01_UP))
        add_button(self.tp, self.tp_port, self.INDEX_MIC_01_STOP, "push", lambda: self.pulse_relay(RELAY_MIC_01_STOP))
        add_button(self.tp, self.tp_port, self.INDEX_MIC_01_DOWN, "push", lambda: self.pulse_relay(RELAY_MIC_01_DOWN))
        add_button(self.tp, self.tp_port, self.INDEX_MIC_02_UP, "push", lambda: self.pulse_relay(RELAY_MIC_02_UP))
        add_button(self.tp, self.tp_port, self.INDEX_MIC_02_STOP, "push", lambda: self.pulse_relay(RELAY_MIC_02_STOP))
        add_button(self.tp, self.tp_port, self.INDEX_MIC_02_DOWN, "push", lambda: self.pulse_relay(RELAY_MIC_02_DOWN))

    def refresh_pdu_button(self, *args):
        state = RELAY_PDU.state.value
        tp_set_button(self.tp, self.tp_port, 51, state)
        tp_set_button(self.tp, self.tp_port, 52, not state)

    def add_evt(self):
        RELAY_PDU.state.watch(self.refresh_pdu_button)
        self.tp.online(self.refresh_pdu_button)


# ---------------------------------------------------------------------------- #
ui_relay_01 = UIRelay(TP_01, TP_PORT_RELAY)  # TP_01, TP_PORT_RELAY
# ---------------------------------------------------------------------------- #
