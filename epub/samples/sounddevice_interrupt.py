import sounddevice as sd
import soundfile as sf
import threading
import sys

def play_audio(file_path):
    try:
        data, fs = sf.read(file_path, dtype='float32')
        sd.play(data, fs)
        sd.wait()  # 阻塞直到播放结束
    except sd.PortAudioError:
        pass  # 忽略因停止导致的错误

# 启动播放线程
t = threading.Thread(target=play_audio, args=('test.wav',))
t.daemon = True  # 主程序退出时线程自动终止
t.start()

try:
    while t.is_alive():
        t.join(timeout=0.1)  # 每0.1秒检查一次，允许响应 KeyboardInterrupt
except KeyboardInterrupt:
    sd.stop()  # 立即停止音频播放
    print("\n播放已中断")
    sys.exit(0)
