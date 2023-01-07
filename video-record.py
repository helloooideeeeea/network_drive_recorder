import os
import subprocess
import datetime
from constants import *


if __name__ == '__main__':

    if os.path.islink(CURRENT_DIR):
        os.unlink(CURRENT_DIR)

    text = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    path = HLS_DIR + "/" + text
    os.mkdir(path)

    os.symlink(os.path.abspath(path), CURRENT_DIR)

    playlistLocation = os.path.abspath(CURRENT_DIR + "/" + PLAYLIST_FILENAME)
    mediaLocation = os.path.abspath(CURRENT_DIR + "/" + "segment%05d.ts")

    # TODO LEDで青色にする
    ret = subprocess.run(
        f"/usr/bin/gst-launch-1.0 libcamerasrc ! videoconvert ! videoscale ! clockoverlay time-format='%D %H:%M:%S' ! v4l2h264enc ! 'video/x-h264,level=(string)4' ! h264parse ! mpegtsmux name=mux ! hlssink max-files=0 target-duration=10 location={mediaLocation} playlist-location={playlistLocation} sync=false", shell=True)

    # TODO LEDで赤色にして、さらにブザーを鳴らす
