# GSM 네트워크 가이드 라인
이 문서는 GSM 네트워크를 구축하기 위한 가이드라인입니다. \
우분투 22.04.5 LTS를 기준으로 작성되었습니다. \
**설치된 Osmocom 스택 버전은 다음과 같습니다.**
- `OsmoHLR` : 1.9.1 \
- `OsmoSTP` : 2.1.0.63-64c8 \
- `OsmoMGW` : 1.14.0.29-2fded 
- `OsmoBSC` : 1.13.0.9-2b718 
- `OsmoMSC` : 1.13.0.7-86cda 
- `OsmoTRX-UHD` : 1.7.1.1-a0e1b 
- `OsmoBTS-TRX` : 1.9.02-d4bb8 
- `libosmocore` : 1.11.0.24-ece60

## 1. 필수 빌드 의존성 설치
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
  libortp-dev libdahdi-dev dahdi-linux\
  dahdi-source libsqlite3-dev libboost-dev \
```
## Osmocom 스택
### 1.libosmocore 설치
```bash
git clone https://gitea.osmocom.org/osmocom/libosmocore
cd libosmocore
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 2. libosmo-netif 설치
```bash
git clone https://gitea.osmocom.org/osmocom/libosmo-netif
cd libosmo-netif
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 3. libosmo-abis 설치
```bash
git clone https://gitea.osmocom.org/osmocom/libosmo-abis
cd libosmo-abis
autoreconf -fi
./configure --prefix=/usr/local --disable-dahdi
make -j$(nproc)
sudo make install
sudo ldconfig -i

```

### 4. libosmo-sigtran 설치
```bash
git clone https://gitea.osmocom.org/osmocom/libosmo-sigtran
cd libosmo-sigtran
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 5. OsmoSTP
```bash
libosmo-sigtran을 설치하면 포함되어 있습니다.
osmo-stp -V -> 버전 확인
```

### 6. OsmoHLR 설치
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-hlr
cd osmo-hlr
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```


### 7. OsmoMGW 설치
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-mgw
cd osmo-mgw
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 8. OsmoBSC 설치

```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-bsc
cd osmo-bsc
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 9. OsmoMSC 설치
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-msc
cd osmo-msc
autoreconf -fi
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 10. OsmoTRX-UHD 설치
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-trx
cd osmo-trx
autoreconf -fi
./configure --prefix=/usr/local --with-uhd 
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 11. OsmoBTS-TRX 설치
```bash
git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-bts
cd osmo-bts
autoreconf -fi
./configure --prefix=/usr/local --enable-sysmobts --enable-trx --enable-shared
make -j$(nproc)
sudo make install
sudo ldconfig
```