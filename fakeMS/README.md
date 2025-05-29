### 도커 빌드
```bash
sudo docker build -t osmobb .
```
### 도커실행
```bash
sudo docker run -it --rm \
   --net host \
   --privileged \
   -v /dev/bus/usb:/dev/bus/usb \
   --name osmobb \
   osmocombb:latest /bin/bash
```
### 도커 백그라운드 실행
```bash
sudo docker run -d --net host --privileged -v /dev/bus/usb:/dev/bus/usb --name osmobb osmocombb:latest tail -f /dev/null
```
### 다른 창으로 접근
```bash
sudo docker exec -it osmobb /bin/bash
```