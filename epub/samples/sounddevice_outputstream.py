import sounddevice as sd
import numpy as np‌

fs = 44100
data, _ = sf.read("test.wav", always_2d=True)
current_frame = 0

def callback(outdata, frames, time, status):
    global current_frame
    chunksize = min(len(data) - current_frame, frames)
    outdata[:chunksize] = data[current_frame:current_frame + chunksize]
    if chunksize < frames:
        outdata[chunksize:] = 0
        raise sd.CallbackStop()
    current_frame += chunksize

stream = sd.OutputStream(samplerate=fs, channels=data.shape, callback=callback)
with stream:
    event.wait()  # 等待播放完成
‌
'''
### 关键参数

- &zwnj;**samplerate**&zwnj;：采样率，比如 CD 音质的 `44100` Hz。
- &zwnj;**channels**&zwnj;：声道数，单声道填 `1`，立体声填 `2`。
- &zwnj;**dtype**&zwnj;：数据类型，常用 `'float32'` 或 `'int16'`，默认是 `'float32'`。
- &zwnj;**blocksize**&zwnj;：每次回调处理的帧数，值越小延迟越低，但 CPU 占用越高。
- &zwnj;**device**&zwnj;：指定输出设备，用 `sd.query_devices()` 查看设备列表。
- &zwnj;**latency**&zwnj;：延迟设置，可以填 `'low'` 或 `'high'`。‌

### 常见坑与建议

- &zwnj;**回调里 `outdata` 是缓冲区视图**&zwnj;，直接用 `outdata[:] = data` 赋值，别重新赋值。
- &zwnj;**数据形状要匹配**&zwnj;：写进 `outdata` 的数据形状必须和它一致，否则会报错或出杂音。
- &zwnj;**流记得关闭**&zwnj;：用 `with` 语句或手动 `stop()` + `close()`，避免资源泄漏。
- &zwnj;**别把 `OutputStream` 当局部变量**&zwnj;：如果在函数里创建后不保存引用，Python 垃圾回收可能把它提前释放，导致程序崩溃（Bus Error 或 Segfault）。把它存成实例属性或全局变量。‌

> 如果程序出现诡异的崩溃或音频突然中断，先检查 `OutputStream` 对象是否被意外回收了。‌
'''
