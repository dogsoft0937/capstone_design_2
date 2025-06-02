from scapy.utils import wrpcap
from scapy.all import *

# GSMTAP 헤더를 위한 scapy 정의 (수동 정의)
class GSMTAP(Packet):
    name = "GSMTAP"
    fields_desc = [
        ByteField("version", 0x02),
        ByteField("hdr_len", 0x0c),
        ByteField("type", 0x01),  # 0x01: GSMTAP_TYPE_UM
        ByteField("timeslot", 0x00),
        ShortField("arfcn", 63),
        ByteField("signal_dbm", 0),
        ByteField("snr_db", 31),
        ByteField("frame_number", 0),  # optional
        ByteField("sub_type", 0),
        ByteField("antenna", 0),
        ByteField("sub_slot", 0),
        ByteField("res", 0)
    ]

bind_layers(GSMTAP, Raw)

# Location Update Request payload (실제 GSM L3 메시지 바이트 값)
location_update_req = bytes.fromhex(
    "05213008919705090121f130"
)
# 이건 아래 구성 기준:
# 05 21   = Location Updating Request (MM)
# 30 08   = Length, skip
# 91 97 05 09 01 21 f1 = IMSI "901700000050912"
# 30      = Classmark
# ... 등등

pkt = GSMTAP(arfcn=63, timeslot=0, snr_db=31) / Raw(location_update_req)
wrpcap("/root/location_update.pcap", [pkt])

print("[*] location_update.pcap 생성 완료.")
