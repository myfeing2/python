'''
用 OutputStream 播放音频时，判断结束有几种常用方式，最推荐用 finished_callback 配合事件或标志位来捕获结束时机。‌

✅ 推荐方案：finished_callback + threading.Event
这是官方示例里的标准做法，能明确知道流已经完整播完。‌

python
'''

import sounddevice as sd
import soundfile as sf
import threading

data, fs = sf.read("test.wav", always_2d=True)
current_frame = 0
event = threading.Event()

def callback(outdata, frames, time, status):
    global current_frame
    if status:
        print(status)
    chunksize = min(len(data) - current_frame, frames)
    outdata[:chunksize] = data[current_frame:current_frame + chunksize]
    if chunksize < frames:
        outdata[chunksize:] = 0
        raise sd.CallbackStop()  # 数据播完，主动停止
    current_frame += chunksize

def finished_callback():
    print("播放结束")
    event.set()  # 通知主线程

stream = sd.OutputStream(samplerate=fs, channels=data.shape,
                         callback=callback, finished_callback=finished_callback)
with stream:
    event.wait()  # 阻塞直到播放结束
‌

'''
### ⚠️ 几个关键点

- `finished_callback` 会在流正常结束或被停止时自动调用，是判断播放完成最可靠的入口。
- 在 `callback` 里，当数据全部写入后要手动 `raise sd.CallbackStop()` 来终止流，否则不会触发 `finished_callback`。
- 如果不介意轮询，也可以用 `stream.active` 属性判断：`while stream.active: pass`，但它不如事件精准，且会空转占 CPU。‌

### 🛠️ 备选方案：`sd.play()` + `sd.wait()`

如果不需要流式处理，直接用 `sd.play()` 播放整个音频，然后 `sd.wait()` 会阻塞到播放完成，更简单。‌

python
'''

import sounddevice as sd
import soundfile as sf

data, fs = sf.read("test.wav")
sd.play(data, samplerate=fs)
sd.wait()  # 播放结束后返回
print("播放结束")
