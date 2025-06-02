```bash
sudo docker build -f Dockerfile -t grgsm_docker .
sudo docker run -it \
  --net host \
  --privileged \
  -v /dev/bus/usb:/dev/bus/usb \
  grgsm_docker
```


### ***SDR 장치는 모두 USB 3.0포트를 사용해야 했습니다.***
### 도커 컨테이너 안에서 입력
```bash
grgsm_livemon_headless --args="serial=3485530" -f 947.6e6 -g 35 -s 2e6
```
