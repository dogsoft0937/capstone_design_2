FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    git build-essential autoconf libtool pkg-config \
    libusb-1.0-0-dev libfftw3-dev libuhd-dev uhd-host \
    python3-pip libncurses5-dev libpcsclite-dev \
    libtalloc-dev telnet net-tools libsctp-dev \
    libgnutls28-dev sudo

# 편의상 bash alias, vim 등도 추가
RUN apt install -y vim tmux less htop iputils-ping

# 작업 디렉토리
WORKDIR /root

RUN apt install -y libmnl-dev

RUN git clone https://gitea.osmocom.org/osmocom/libosmocore.git && \
    cd libosmocore && \
    git checkout 1.5.0 && \
    autoreconf -fi && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    ldconfig

WORKDIR /root

RUN git clone https://gitea.osmocom.org/cellular-infrastructure/osmo-trx.git && \
    cd osmo-trx && \
    git checkout 1.3.0 && \
    autoreconf -fi && \
    ./configure --prefix=/usr/local --with-uhd && \
    make -j$(nproc) && \
    make install && \
    ldconfig

WORKDIR /root

RUN git clone https://github.com/osmocom/osmocom-bb.git && \
    cd osmocom-bb && \
    git checkout 38c4f729

WORKDIR /root/osmocom-bb/src/host/layer23

RUN autoreconf -fi && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    ldconfig

WORKDIR /root

COPY ./osmo-trx-uhd.cfg /root/osmo-trx-uhd.cfg
COPY ./mobile.cfg /root/mobile.cfg

CMD ["/bin/bash"]
