FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install gr-gsm
RUN apt-get -y install uhd-host
RUN /usr/lib/uhd/utils/uhd_images_downloader.py
RUN apt-get -y install gnuradio python3 python3-pip libuhd-dev libfftw3-dev
RUN pip3 install scapy
CMD grgsm_livemon_headless -h; /bin/bash