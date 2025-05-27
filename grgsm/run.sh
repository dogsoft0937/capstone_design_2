sudo docker build -f Dockerfile -t grgsm_docker .
sudo docker run -it \
  --net host \
  --privileged \
  -v /dev/bus/usb:/dev/bus/usb \
  grgsm_docker \
  grgsm_livemon_headless --args="serial=3485530" -f 957e6 -g 30
