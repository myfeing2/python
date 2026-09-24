'''
可以用 ‌finished_callback 参数‌来侦测播放结束，这是 sounddevice 官方提供的机制。‌

具体做法是在创建 OutputStream 时传入 finished_callback，当音频数据全部播完、流停止时，这个回调会被自动调用。常见搭配 threading.Event 来阻塞主线程等待播放完成：

python
'''

import sounddevice as sd
import soundfile as sf
import threading

event = threading.Event()
data, fs = sf.read("test.wav", always_2d=True)
current_frame = 0

def callback(outdata, frames, time, status):
    global current_frame
    if status:
        print(status)
    chunksize = min(len(data) - current_frame, frames)
    outdata[:chunksize] = data[current_frame:current_frame + chunksize]
    if chunksize < frames:
        outdata[chunksize:] = 0
        raise sd.CallbackStop()  # 数据播完，停止回调
    current_frame += chunksize

stream = sd.OutputStream(
    samplerate=fs,
    channels=data.shape,
    callback=callback,
    finished_callback=event.set  # 播放结束时触发
)‌

with stream:
    event.wait()  # 阻塞直到播放完成

'''
📌 关键点
‌finished_callback 触发时机‌：当流因 CallbackStop 被抛出、或数据全部处理完毕后触发，表示播放真正结束。
‌CallbackStop 的作用‌：在回调里数据不足一帧时抛出它，通知 sounddevice 停止拉取数据，随后 finished_callback 会被调用。
‌用 Event 同步‌：event.wait() 会一直阻塞，直到 finished_callback 执行 event.set()，这样就能准确知道播放结束，不会提前退出程序。‌
⚠️ 需要注意
如果用 sd.play() + sd.wait() 的简单方式，sd.wait() 本身就会阻塞到播放完成，不需要额外侦测。
如果播放过程中出现 output underflow 提示，通常是回调处理太慢导致，可以在 OutputStream 里加 blocksize 参数缓解，但这和侦测结束无关。
如果音频数据来自实时流（非文件），判断“结束”需要自己定义条件，比如检测到静音持续一段时间，finished_callback 这种方式就不适用了。‌
'''
