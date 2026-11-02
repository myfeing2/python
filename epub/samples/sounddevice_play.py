import sounddevice as sd
import numpy as np

fs = 44100  # 采样率
f = 440     # 频率, Hz
seconds = 3 # 持续时间秒
t = np.linspace(0, seconds, int(fs*seconds), endpoint=False)
data = np.sin(2 * np.pi * f * t)
sd.play(data, samplerate=fs)
sd.wait()  # 等待直到数据播放完成