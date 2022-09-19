
import RPi.GPIO as GPIO
import subprocess
import time



led = 7
switch = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

file = f"{time.localtime().tm_mday}_{time.localtime().tm_hour}.{time.localtime().tm_min}"

process = subprocess.Popen([f"ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 records/{file}.mkv"], stdin=subprocess.PIPE, shell=True,)


time.sleep(2)

cur_time = time.localtime().tm_sec

GPIO.output(led, True)

print(GPIO.input(switch))

while GPIO.input(switch) == 1:
  time.sleep(0.01)
process.stdin.write("q".encode())
process.stdin.close()



#   if abs(cur_time - time.localtime().tm_sec) > 5:
#     process.stdin.write("q".encode())
#     process.stdin.close()
    # break

GPIO.output(led, False)
GPIO.cleanup()
print("This is the end!!!")




# ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 output.mkv
