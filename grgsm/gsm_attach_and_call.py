import socket
import time

# === 실험 파라미터 ===
GSMTAP_IP = "127.0.0.1"
GSMTAP_PORT = 4729
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

IMSI_TBCD = bytes.fromhex("21436587")        # IMSI: 12345678 (TBCD)
SRES = bytes.fromhex("9ACDA837")             # 고정 SRES
DISPLAYER_TBCD = bytes.fromhex("1020930864F0")  # 전화번호: 01023980460 (TBCD)

# === GSMTAP 패킷 래퍼 ===
def wrap_gsmtap(payload: bytes) -> bytes:
    # Dummy GSMTAP header: 16 bytes
    hdr = bytes.fromhex("01" * 16)  # GSMTAP type = 0x01 (Um interface)
    return hdr + payload

# === Location Update Request ===
def make_location_update_req():
    msg_type = b'\x08'  # Location Updating Request
    identity_type = b'\x01'  # IMSI
    identity = bytes([len(IMSI_TBCD)]) + IMSI_TBCD
    mm_payload = msg_type + identity_type + identity
    return wrap_gsmtap(mm_payload)

# === Authentication Response ===
def make_auth_response():
    msg_type = b'\x0b'
    return wrap_gsmtap(msg_type + SRES)

# === Call Setup (발신 번호 숨기고 수신 번호만 넣음) ===
def make_call_setup():
    dtap_setup = b'\x05'  # Setup
    bearer_cap = b'\x04\x03\x80\x90\xa3'  # 기본 오디오
    called_party = b'\x5e' + bytes([len(DISPLAYER_TBCD) + 1]) + b'\x91' + DISPLAYER_TBCD
    payload = dtap_setup + bearer_cap + called_party
    return wrap_gsmtap(payload)

# === 전송 함수 ===
def send_packet(pkt: bytes, delay: float = 1.0):
    sock.sendto(pkt, (GSMTAP_IP, GSMTAP_PORT))
    time.sleep(delay)

# === 전체 실행 흐름 ===
def main():
    print("[*] Sending Location Update Request...")
    send_packet(make_location_update_req())

    print("[*] Sending Authentication Response...")
    send_packet(make_auth_response())

    print("[*] Sending Call Setup to 01023980460...")
    send_packet(make_call_setup())

    print("[✓] Done. Check displayerPhone for incoming call.")

if __name__ == "__main__":
    main()
