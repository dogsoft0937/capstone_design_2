# 📡 GSM 단말 초기 등록 절차 분석 보고서

## 🗂 개요

본 분석은 실제 USIM 단말을 사용하여 오픈소스 Osmocom 기지국에 접속하는 과정을 Wireshark로 캡처하고, 해당 `.pcapng` 파일을 기반으로 **GSM 프로토콜 계층의 초기 접속 흐름**을 분석한 것입니다.  
핵심 목표는 **RR, MM, CC** 프로토콜 메시지를 포착하고, **IMSI 식별 → TMSI 재할당 → 회선 종료**까지의 절차를 확인하는 것입니다.

---

## 🔍 환경 정보

- **단말**: 실제 USIM 폰
- **기지국 구성**: osmo-bsc, osmo-msc, osmo-hlr 등
- **프로토콜 필터**:  
  `sctp.port == 2905 || gsm_a`  
- **캡처 인터페이스**: `lo` (Loopback)

---

## 📑 분석된 주요 메시지 흐름

| No. | Protocol | 설명 |
|-----|----------|------|
| 1 | **BSSAP - Location Updating Request** | 단말이 최초로 네트워크에 위치 등록 요청을 전송 |
| 2 | **DTAP - Identity Request** | 네트워크가 단말의 IMSI 요청 |
| 3 | **DTAP - Identity Response** | 단말이 IMSI(국제 이동 가입자 번호)를 전송 |
| 4 | **DTAP - Location Updating Accept** | 네트워크가 위치 등록을 승인 |
| 5 | **DTAP - TMSI Reallocation Complete** | 단말이 임시 식별자(TMSI) 재할당을 완료함 |
| 6 | **BSSMAP - Clear Command** | MSC가 회선을 종료 요청 |
| 7 | **BSSMAP - Clear Complete** | BSC가 종료 수락 |
| 8 | **SCCP - RLSD / RLC** | 세션 해제 완료 (Release / Confirm) |

---

## 📌 핵심 설명 포인트

### ✅ 1. 단말 식별 절차 (IMSI → TMSI)
- `Identity Request/Response`에서 단말은 평문으로 IMSI를 전송
- 이후 `TMSI Reallocation`을 통해 단말은 임시 식별자로 전환됨 → **식별 보호**

### ✅ 2. 위치 등록 절차 (Location Update)
- `Location Updating Request` 및 `Accept` 메시지로 위치 갱신 완료
- 이는 **MM 계층의 핵심 절차**

### ✅ 3. 회선 정리 (Clear Command)
- 위치 등록 후 회선은 자동으로 `Clear Command` → `Clear Complete` → `RLSD/RLC` 흐름으로 정리됨
- 이는 **BSSAP 및 SCCP 계층**에서 이루어짐

---

## 🔬 계층별 프로토콜 요약

| 계층 | 주요 메시지 | 설명 |
|------|-------------|------|
| **RR (Radio Resource)** | Channel Request, Immediate Assignment (이번 세션엔 미포착) | 무선 채널 연결 |
| **MM (Mobility Management)** | Identity, Location Update, TMSI | 단말 인증 및 위치 등록 |
| **CC (Call Control)** | Setup, Alerting, Release (이번 세션엔 없음) | 통화 절차 제어 |
| **BSSAP** | Location Update, Clear Command 등 | BSC ↔ MSC 고수준 제어 |
| **SCCP** | RLSD, RLC | 세션 연결/해제 |

---

## 🎯 결론 및 다음 단계

- 본 캡처에서 단말은 정상적으로 기지국에 등록되었으며, **IMSI 등록 → TMSI 재할당 → 회선 정리**의 절차가 모두 완료됨
- **통화(Call Setup)** 시도는 없었기에 CC 계층 메시지는 확인되지 않음
- **다음 단계**: 실제 음성 통화를 시도하여 `Setup`, `Connect`, `Release` 흐름 추가 캡처

---

## 🧩 참고 자료

- Wireshark Display Filter:  
  `sctp.port == 2905 || gsm_a || dtap || bssap`
- Decode As: SCTP Port 2905 → **M3UA**
- Osmocom 공식 문서: https://osmocom.org

---