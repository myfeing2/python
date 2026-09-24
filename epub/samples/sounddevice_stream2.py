import sounddevice as sd
import numpy as np

# 生成一秒钟的随机噪音
fs = 44100  # 采样率
data = np.random.uniform(-1, 1, fs)

data = np.asarray(data, dtype="float32")

# 创建输出流
stream = sd.OutputStream(samplerate=fs, channels=1)

# 启动输出流并播放数据
with stream:
    stream.write(data)