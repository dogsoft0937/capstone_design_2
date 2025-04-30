# 📡 GSM 네트워크 구축 가이드 (Ubuntu 22.04.5 기준)

본 문서는 Ubuntu 22.04.5 LTS 환경에서 **Osmocom 스택을 기반으로 2G GSM 기지국**을 구성하기 위한 상세 설치 가이드입니다.  
모든 컴포넌트는 **로컬에서 실행되며**, USRP SDR + 실제 USIM 단말을 통한 테스트를 목적으로 작성되었습니다.

---

## 🧩 설치 환경 및 버전

| 컴포넌트 | 버전 | Git 커밋 해시 (선택)
|----------|-------| ----- |
| OsmoHLR | 1.9.1 |
| OsmoSTP | 2.1.0.63-64c8 |
| OsmoMGW | 1.14.0.29-2fded |
| OsmoBSC | 1.13.0.9-2b718 |
| OsmoMSC | 1.13.0.7-86cda |
| OsmoTRX-UHD | 1.7.1.1-a0e1b |
| OsmoBTS-TRX | 1.9.02-d4bb8 |
| libosmocore | 1.11.0.24-ece60 |
| libosmo-abis | 11.3.0 | d2e8ce53... |
| libosmo-netif | 15.0.0 | 1b4044d7... |
| libosmo-sigtran | 11.0.0 | 64c8e3b9...|

---
## ✅ 설치 순서 개요

| 순서 | 구성 요소 | 역할 요약 |
|------|-----------|-----------|
| 1 | libosmocore | 공통 기반 라이브러리 |
| 2 | libosmo-netif | 네트워크 통신 처리 |
| 3 | libosmo-abis | BTS ↔ BSC 간 Abis 처리 |
| 4 | libosmo-sigtran | SIGTRAN 계층 (SCCP, M3UA 등) 처리 |
| 5 | osmo-stp | SIGTRAN 라우터 (STP 역할) |
| 6 | osmo-hlr | 가입자 DB (IMSI, 키, 번호) 관리 |
| 7 | osmo-mgw | RTP 기반 음성 게이트웨이 |
| 8 | osmo-bsc | Base Station Controller |
| 9 | osmo-msc | Mobile Switching Center |
| 10 | osmo-trx | SDR RF 트랜시버 (UHD 기반) |
| 11 | osmo-bts | BTS 자체 제어 소프트웨어 |

---
## ✅ 1. 필수 빌드 의존성 설치

다음 패키지들은 모든 Osmocom 구성 요소의 컴파일 및 실행에 필요합니다.

```bash
sudo apt-get update
sudo apt-get install -y \
  build-essential git autoconf automake libtool pkg-config \
  libsctp-dev libssl-dev libdbi-dev libgnutls28-dev \
  libnl-3-dev libnl-route-3-dev libpcap-dev \
  libusb-1.0-0-dev fftw3-dev libuhd-dev uhd-host \
  libtalloc-dev libsctp-dev shtool \
  git-core make gcc gnutls-dev \
  libmnl-dev liburing-dev libpcsclite-dev libpcsclite1 \
  libortp-dev libdahdi-dev dahdi-linux \
  dahdi-source libsqlite3-dev libboost-dev 
```
## Osmocom 스택
### 1. `libosmocore`
> Osmocom 전반에서 사용하는 공통 유틸리티, 로깅, 타이머 기능 포함
```bash
git clone https://gitea.osmocom.org/osmocom/libosmocore
cd libosmocore
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 2. `libosmo-netif`
> Osmocom 컴포넌트 간의 메시지 전송을 위한 네트워크 프레임워크
```bash
git clone https://gitea.osmocom.org/osmocom/libosmo-netif
cd libosmo-netif
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 3. `libosmo-abis`
> BTS와 BSC 간의 Abis 인터페이스 프로토콜 구현 
```bash
git clone https://gitea.osmocom.org/osmocom/libosmo-abis
cd libosmo-abis
autoreconf -fi
./configure --prefix=/usr/local --disable-dahdi
make -j$(nproc)
sudo make install
sudo ldconfig

```

### 4. `libosmo-sigtran`
> SCCP/M3UA 등 SIGTRAN 기반 통신 계층 구현 (BSC <-> MSC 연결용)
```bash
git clone https://gitea.osmocom.org/osmocom/libosmo-sigtran
cd libosmo-sigtran
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 5. `OsmoSTP`
> SIGTRAN 메시지의 라우팅 역할을 수행하는 Signaling Transfer Point\
(libosmo-sigtran을 설치하면 자동 포함됨)
```bash
osmo-stp -V -> #설치 및 빌드 확인
```

### 6. `OsmoHLR`
> 가입자 DB(HSS처럼 IMSI, 키, 전화번호 저장) – 단말 인증, TMSI 배정 등 처리
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-hlr
cd osmo-hlr
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```


### 7. `OsmoMGW`
> RTP 기반 음성 경로를 설정하고 오디오 데이터를 전달하는 Media Gateway \
(통화 연결 시 필요)
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-mgw
cd osmo-mgw
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 8. `OsmoBSC`
> Base Station Controller \
BTS 제어, TRX 할당, MSC와의 연결을 관리함
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-bsc
cd osmo-bsc
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 9. `OsmoMSC`
> 단말의 위치 등록, 인증, 통화 제어 등을 수행하는 핵심 교환기
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-msc
cd osmo-msc
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 10. `OsmoTRX-UHD`
> USRP SDR를 통해 실제 전파 송수신을 담당하는 RF 트랜시버
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-trx
cd osmo-trx
autoreconf -fi
./configure --prefix=/usr/local --with-uhd 
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 11. `OsmoBTS-TRX`
> BTS 자체의 무선 계층 제어 소프트웨어 \
`osmo-trx`와 연동하여 무선 통신 직접 처리
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-bts
cd osmo-bts
autoreconf -fi
./configure --prefix=/usr/local --enable-sysmobts --enable-trx --enable-shared
make -j$(nproc)
sudo make install
sudo ldconfig
```

## ▶️ 실행 순서 요약

```bash
osmo-hlr -c ./config/osmo-hlr.cfg
osmo-stp -c ./config/osmo-stp.cfg
osmo-bsc -c ./config/osmo-bsc.cfg
osmo-msc -c ./config/osmo-msc.cfg
sudo osmo-trx-uhd -c ./config/osmo-trx-uhd.cfg
sudo osmo-bts-trx -c ./config/osmo-bts-trx.cfg