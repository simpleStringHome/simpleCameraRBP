import subprocess
import time

from flask import Flask, render_template, redirect, url_for

process = None
recording = False

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', recording=recording)

@app.route('/start')
def start():
    global process, recording
    file = f"records/{time.localtime().tm_mday}.{time.localtime().tm_hour}.{time.localtime().tm_min}.mkv"
    p1 = subprocess.run(["rm", "-f", file])
    process = subprocess.Popen([f"ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 {file}"], stdin=subprocess.PIPE, shell=True,)
    recording = True
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global process, recording
    process.stdin.write("q".encode())
    process.stdin.close()
    recording = False
    return redirect(url_for('index'))
