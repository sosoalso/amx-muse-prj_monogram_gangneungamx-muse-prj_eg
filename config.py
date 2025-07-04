from lib.lib_yeoul import get_device
from lib.networkmanager import TcpClient

# ---------------------------------------------------------------------------- #
IDEVICE = get_device("idevice")
RELAY = IDEVICE.relay
RELAY_PDU = IDEVICE.relay[0]
RELAY_MIC_01_UP = IDEVICE.relay[2]
RELAY_MIC_01_STOP = IDEVICE.relay[3]
RELAY_MIC_01_DOWN = IDEVICE.relay[4]
RELAY_MIC_02_UP = IDEVICE.relay[5]
RELAY_MIC_02_STOP = IDEVICE.relay[6]
RELAY_MIC_02_DOWN = IDEVICE.relay[7]
# ---------------------------------------------------------------------------- #
TP_01 = get_device("AMX-11001")
TP_LIST = [TP_01]
TP_PORT_RELAY = 2
TP_PORT_VIDREC = 14
TP_PORT_CAM = 5
TP_PORT_MIXER = 15
TP_PORT_VIDSWT = 10
TP_PORT_VIDMTX = 3

# ---------------------------------------------------------------------------- #
MIXER = TcpClient(name="mixer", ip="192.168.0.41", port=9990, buffer_size=2048)
VIDMTX = TcpClient(name="vidmtx", ip="192.168.0.41", port=9990, buffer_size=2048)
CAM_IP_LIST = ["111.111.111.111", "111.111.111.112"]
VIDPRJ_01 = TcpClient(name="vidprj_01", ip="192.168.0.51", port=4352)
VIDPRJ_02 = TcpClient(name="vidprj_02", ip="192.168.0.52", port=4352)
VIDPRJ_LIST = [VIDPRJ_01, VIDPRJ_02]
VIDREC = TcpClient(name="vidrec", ip="192.168.0.43", port=9993)
# YAMAHA_PORT = 49280
MIXER = TcpClient(name="mier", ip="192.168.1.111", port=49280)


# ---------------------------------------------------------------------------- #
def init_tcp_client_connect():
    VIDMTX.connect()
    VIDPRJ_01.connect()
    VIDPRJ_02.connect()
    VIDREC.connect()


# ---------------------------------------------------------------------------- #
