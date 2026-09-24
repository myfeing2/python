'''
用 sd.stop() 只能停止播放，要实现“暂停后再继续”，需要改用 sd.OutputStream 配合 stream.stop() 和 stream.start()。‌‌‌

sd.play() 这类便捷函数不支持暂停恢复，只能整体停止。要暂停播放，得用更底层的流对象来控制：

python
'''

import sounddevice as sd
import numpy as np

# 生成一段测试音频
data = sd.playrec(np.random.randn(44100), samplerate=48000, channels=1)  # 示意，实际用你已有的音频数据
sd.wait()

print("stream start...")
data = np.asarray(data, dtype="float32")
stream = sd.OutputStream(samplerate=48000, channels=1)

stream.start()
stream.write(data)  # 写入音频数据

# 暂停播放
stream.stop()

# 从暂停处继续播放
stream.start()

# 播放完毕关闭流
stream.close()

'''
stream.stop() 暂停播放，但不会关闭流，之后可以随时恢复。
stream.start() 从暂停位置继续播放。
不再需要播放时，调用 stream.close() 释放资源。‌‌
⚠️ 注意：stream.stop() 是暂停而不是终止，音频数据还保留在缓冲区里，可以继续播放；如果只是想结束播放，直接调 sd.stop() 即可。‌‌
'''

