import os
import subprocess
import datetime

WWW_DIR = "www"
CURRENT_DIR = WWW_DIR + "/" + "current"
HLS_DIR = WWW_DIR + "/" + "hls"

if __name__ == '__main__':

    if os.path.islink(CURRENT_DIR):
        os.unlink(CURRENT_DIR)

    text = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    path = HLS_DIR + "/" + text
    os.mkdir(path)

    os.symlink(path, CURRENT_DIR)

    playlistLocation = HLS_DIR + "/" + "playlist.m3u8"
    mediaLocation = HLS_DIR + "/" + "segment%05d.ts"

    # TODO LEDで青色にする
    ret = subprocess.call(
        f'gst-launch-1.0 libcamerasrc ! videoconvert ! videoscale ! clockoverlay time-format="%D %H:%M:%S" ! v4l2h264enc ! "video/x-h264,level=(string)4" ! h264parse ! mpegtsmux name=mux ! hlssink max-files=0 target-duration=10 location=${mediaLocation} playlist-location=${playlistLocation} sync=false')

    # TODO LEDで赤色にして、さらにブザーを鳴らす
