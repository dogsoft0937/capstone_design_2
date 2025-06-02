# FROM ubuntu:18.04

# RUN apt-get update
# RUN apt-get -y upgrade
# RUN apt-get -y install gr-gsm
# RUN apt-get -y install uhd-host
# RUN /usr/lib/uhd/utils/uhd_images_downloader.py
# RUN apt-get -y install gnuradio python3 python3-pip libuhd-dev libfftw3-dev
# RUN pip3 install scapy
# COPY location_update.py /root/location_update.py
# CMD grgsm_livemon_headless -h; /bin/bash
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/usr/local/lib/python3/dist-packages:$PYTHONPATH
ENV LANG=en_US.UTF-8

RUN apt-get update && apt-get install -y locales && locale-gen en_US.UTF-8

# 필수 패키지
RUN apt-get install -y \
    gnuradio python3 python3-pip libuhd-dev libfftw3-dev \
    git cmake libboost-all-dev libgmp-dev swig liblog4cpp5-dev \
    doxygen gnuradio-dev uhd-host pkg-config libtalloc-dev \ 
    libpcsclite-dev libusb-1.0 gnutls-dev libsctp-dev \
    liborc-0.4-dev gr-osmosdr

# UHD 이미지 다운로드
RUN test -f /usr/lib/uhd/utils/uhd_images_downloader.py && /usr/lib/uhd/utils/uhd_images_downloader.py || true


WORKDIR /root
RUN git clone https://gitea.osmocom.org/osmocom/libosmocore.git && \
    cd libosmocore && \
    git checkout 1.4.0 && \
    autoreconf -fi && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    ldconfig


WORKDIR /root
RUN git clone https://github.com/ptrkrysik/gr-gsm.git && \
    cd gr-gsm && mkdir build && cd build && \
    cmake .. && make -j$(nproc) && make install && ldconfig

# grgsm 바이너리 링크
RUN ln -s /usr/local/bin/grgsm_transmitter /usr/bin/grgsm_transmitter || true

# Python 패키지
RUN pip3 install scapy==2.4.5 cryptography==3.3.2

RUN apt-get install -y avahi-daemon
# 테스트 스크립트 복사
COPY location_update.py /root/location_update.py
COPY send_pcap.py /root/send_pcap.py

RUN echo '#!/bin/bash\n\
mkdir -p /var/run/dbus\n\
dbus-daemon --system --fork\n\
sleep 1\n\
avahi-daemon --no-drop-root --daemonize\n\
python3 /root/location_update.py\n\
python3 /root/send_pcap.py\n' > /root/start.sh && chmod +x /root/start.sh

# 기본 실행 명령
CMD ["/root/start.sh"]
