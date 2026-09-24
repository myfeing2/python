'''
这个问题是典型的‌数据类型不匹配‌：tts.generate 返回的是 float64 数组，而 sounddevice 的 OutputStream 默认或你指定的是 float32。直接把 float64 数据喂给 float32 的流就会报这个 TypeError。

‌解决办法是在写入前把音频数据转成 float32‌，最直接的方式是用 NumPy 的 astype：


python
'''

import numpy as np
import sounddevice as sd

# 假设 tts 和 text 已就绪
audio = tts.generate(text)  # 返回 float64 数组

# 关键：转换为 float32
audio_float32 = np.asarray(audio, dtype=np.float32)

# 写入流（确保 samplerate 与 tts 输出一致）
with sd.OutputStream(samplerate=tts.sample_rate, channels=1, dtype='float32') as stream:
    stream.write(audio_float32)

'''
几个容易踩的坑

‌采样率必须匹配‌：OutputStream 的 samplerate 要设成 tts.sample_rate（或你模型的实际采样率），否则声音会变调或报错。
‌检查 tts.generate 的返回类型‌：有的版本会返回元组（如 (samples, sample_rate)），先确认一下你的返回值结构。如果是元组，取 audio = result 再转换。
‌确认输出流的数据类型‌：如果你创建流时没指定 dtype，sounddevice 默认可能是 float32，所以把数据统一成 float32 是最稳妥的。
‌一次性写入 vs 流式写入‌：上面是先把整段音频生成完再写入。如果你用 tts.generate_streaming 做流式合成，每一块返回的数据也要同样转成 float32 再 write。‌
备选方案
如果 astype 之后仍有问题，可以显式指定流的 dtype='float32'，或者在创建流时用 dtype='float64'（但很多音频设备不支持 float64，所以还是建议转成 float32 更通用）。

顺带一提：sounddevice 对浮点音频的期望范围是 [-1.0, 1.0]，如果合成结果超出这个范围，播放时可能削波失真，必要时可以做归一化处理。‌
'''
