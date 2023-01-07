from flask import Flask, render_template, request, redirect, flash, url_for, make_response
import logging, os, re, shutil
from constants import *
from util import *
from urllib.parse import quote

app = Flask(__name__, static_url_path="/" + WWW_DIR, static_folder=WWW_DIR, template_folder='templates')
app.logger.setLevel(logging.DEBUG)


@app.route('/')
def index():
    sorted_files = sorted([file for file in os.listdir(HLS_DIR) if re.match(r'[0-9]{13}', file)], reverse=True)
    play_list_files_map = [(date_dir, HLS_DIR_NAME + "/" + date_dir + "/" + PLAYLIST_FILENAME) for date_dir in
                           sorted_files if
                           os.path.exists(os.path.abspath(os.path.join(HLS_DIR, date_dir)) + "/" + PLAYLIST_FILENAME)]
    return render_template('index.html', play_list_files_map=play_list_files_map)


@app.route('/<date_dir>/video_download')
def video_download(date_dir):

    shot_datetime = date_parse(date_dir)

    zip_path = shutil.make_archive('tmp/' + date_dir, format='zip',
                                   root_dir=os.path.abspath(os.path.join(HLS_DIR, date_dir)))
    res = make_response()
    res.headers['Content-type'] = 'application/octect-stream'
    res.headers['Content-Disposition'] = "attachment; filename*=UTF-8''" + quote(shot_datetime.strftime("%Y年%m月%d日%H時%M分")) + ".zip"
    res.data = open(zip_path, "rb").read()
    os.remove(zip_path)
    return res


@app.route('/<date_dir>/video_delete')
def video_delete(date_dir):
    shutil.rmtree(os.path.abspath(os.path.join(HLS_DIR, date_dir)))
    # flash("%sを削除しました。".format(date_parse(date_dir).strftime("%Y年%m月%d日%H時%M分")), "success")
    return redirect(url_for('index'))

# jinja methodの定義
app.jinja_env.globals.update(
    date_format=date_format
)