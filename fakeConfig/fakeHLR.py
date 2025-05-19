import socket
from colorama import init, Fore, Style

init(autoreset=True)

HOST = '127.0.0.1'
PORT = 8787

def decode_imsi(tbcd: bytes) -> str:
    imsi_digits = ''
    for byte in tbcd:
        low = byte & 0x0F
        high = (byte & 0xF0) >> 4
        if low < 0x0A:
            imsi_digits += str(low)
        if high < 0x0A:
            imsi_digits += str(high)
    return imsi_digits

def handle_client(conn, addr):
    print(f"{Fore.GREEN}[+] MSC와 연결됨: {addr}{Style.RESET_ALL}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            print(f"{Fore.YELLOW}[RX] MSC -> HLR: {data.hex()}{Style.RESET_ALL}")

            if data.startswith(b'\x00\x01\xfe\x00'):
                # 초기 요청
                response = bytes.fromhex('020101020810112233445566770304aabbccdd')
                print(f"{Fore.CYAN}[TX] HLR -> MSC: {response.hex()}{Style.RESET_ALL}")
                conn.sendall(response)

            elif data.startswith(b'\x00\x12\xee'):
                # AUTH REQ - IMSI + RAND + SRES
                imsi_raw = data[7:15]
                rand = data[15:19]
                sres = data[19:25]

                imsi = decode_imsi(imsi_raw) if imsi_raw else "UNKNOWN"

                print(f"{Fore.GREEN}[+] IMSI : {imsi}")
                print(f"[+] RAND : {rand.hex()}")
                print(f"[+] SRES : {sres.hex()}{Style.RESET_ALL}")

                response = bytes.fromhex('020101020810112233445566770304aabbccdd')
                print(f"{Fore.CYAN}[TX] HLR -> MSC: {response.hex()}{Style.RESET_ALL}")
                conn.sendall(response)

    except Exception as e:
        print(f"{Fore.RED}[-] 오류 발생: {e}{Style.RESET_ALL}")
    finally:
        conn.close()
        print(f"{Fore.RED}[-] MSC와 연결 종료됨, 재대기 중...{Style.RESET_ALL}")

def start_fake_hlr():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"{Fore.BLUE}[+] 가짜 HLR 서버 실행 중... ({HOST}:{PORT}){Style.RESET_ALL}")

        while True:
            conn, addr = server.accept()
            handle_client(conn, addr)

if __name__ == '__main__':
    start_fake_hlr()
