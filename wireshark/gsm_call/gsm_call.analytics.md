
# 📞 GSM Call Flow 분석 보고서 (패킷 번호 기반)

이 문서는 Wireshark를 통해 캡처된 패킷 흐름을 기반으로, GSM 2G 환경에서 실제 단말 간의 Call Setup 및 Release 흐름을 분석한 자료입니다.  
**실험에서 캡처한 pcap에 포함된 Call Control 패킷들을 No 순서에 따라 설명합니다.**

---

## 📑 Call Signaling 단계별 설명

### 1️⃣ Call Setup 시작

- **No. 6887 ~ 6888**  
  `DTAP (CC) Setup` → 발신 단말이 통화 요청 시작  
  `Call Proceeding` → 네트워크가 통화 요청을 수락하고 처리 중임을 응답

---

### 2️⃣ 채널 할당 및 수신자 호출

- **No. 6890 ~ 6902**  
  `Paging Request` → 수신 단말 호출  
  `Assignment Request` / `Assignment Complete` → 전용 채널 할당 완료

---

### 3️⃣ 수신자 벨 울림 및 통화 수락

- **No. 10216 ~ 14603**  
  `Alerting` → 수신 단말이 벨 울리기 시작  
  `Connect` / `Connect Acknowledge` → 수신 단말이 통화 수락, 발신 단말이 수락 확인

---

### 4️⃣ 통화 종료

- **No. 26633 ~ 61380**  
  `Disconnect` → 단말 또는 네트워크 측 통화 종료 요청  
  `Release` / `Release Complete` → 자원 회수 및 세션 종료

---

### 5️⃣ Clear Command 처리

- **No. 62062 ~ 이후**  
  `Clear Command` → BSC가 세션을 완전히 종료  
  `Clear Complete` / `RLSD`, `RLC` → SCCP 계층에서 연결 종료 확인

---

## ✅ 종합 분석 요약

| 단계 | 주요 메시지 | 패킷 번호 |
|------|-------------|-----------|
| Call Setup 시작 | Setup, Call Proceeding | 6887 ~ 6888 |
| 채널 할당 / 페이징 | Paging, Assignment | 6890 ~ 6902 |
| 수신자 응답 | Alerting, Connect | 10216 ~ 14603 |
| 통화 종료 | Disconnect, Release | 26633 ~ 61380 |
| 세션 해제 | Clear Command ~ RLC | 62062 ~ 이후 |


---
# ✅ 계층별 GSM 시그널링 포착 결과

## 🟡 1. RR (Radio Resource) 계층

- **포착 여부**: ✅

- **근거 메시지**:
  - `Assignment Request`, `Assignment Complete` (채널 할당)
  - `Paging Request`, `Paging Response`

- **역할**:
  - 무선 채널 설정
  - TCH (Traffic Channel) 할당
  - 단말 식별 및 호출(Paging)

---

## 🔵 2. MM (Mobility Management) 계층

- **포착 여부**: ✅

- **근거 메시지**:
  - `CM Service Request` (Call 시작 전 단말 인증 요청)

- **비고**:
  - Location Updating 메시지는 본 캡처에서 사용되지 않았으나,
    `CM Service Request`는 MM 계층에 해당합니다.

- **역할**:
  - 단말 인증 및 식별(IMSI, TMSI)
  - 위치 등록
  - 서비스 접근 요청 제어

---

## 🔴 3. CC (Call Control) 계층

- **포착 여부**: ✅

- **근거 메시지**:
  - `Setup`, `Call Proceeding`, `Alerting`, `Connect`
  - `Disconnect`, `Release`, `Clear Command`, `Clear Complete`

- **역할**:
  - Call Setup → 통화 연결 → 종료 흐름 제어
  - 통화 시 상태 전이 관리

---
