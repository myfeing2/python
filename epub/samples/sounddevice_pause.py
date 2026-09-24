import sounddevice as sd
import numpy as np
import time

class AudioPlayer:
    def __init__(self):
        self.current_frame = 0  # 记录当前播放到哪一帧（暂停的核心：自己维护进度）
        self.data = None         # 音频数据（形状：[总帧数, 通道数]）
        self.fs = 44100          # 采样率
        self.stream = None
        self.is_playing = False

    def _audio_callback(self, outdata, frames, time_info, status):
        """音频回调函数：声卡需要数据时自动调用，不能阻塞、不能做耗时操作"""
        if status:
            print(f"音频状态警告: {status}", flush=True)
        
        if self.data is None:
            outdata[:] = 0
            return

        # 从当前暂停/播放位置取数据
        end_frame = self.current_frame + frames
        chunksize = min(len(self.data) - self.current_frame, frames)
        outdata[:chunksize] = self.data[self.current_frame : self.current_frame + chunksize]
        
        # 如果数据不够填满缓冲区，剩余部分填0并停止播放
        if chunksize < frames:
            outdata[chunksize:] = 0
            raise sd.CallbackStop()  # 播放到末尾，自动终止流
        
        self.current_frame += chunksize

    def load_audio(self, data: np.ndarray, samplerate: int = 44100):
        """加载音频数据：data形状必须为 [帧数, 通道数]，dtype用float32"""
        # 单声道自动转二维，适配outdata格式
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        self.data = data.astype(np.float32)
        self.fs = samplerate
        self.current_frame = 0

    def play(self):
        """开始/继续播放"""
        if self.data is None:
            print("请先加载音频数据", flush=True)
            return
        
        # 如果已有流先关闭，避免冲突
        if self.stream is not None:
            self.stream.close()
        
        # 创建输出流
        self.stream = sd.OutputStream(
            samplerate=self.fs,
            channels=self.data.shape[1],
            callback=self._audio_callback,
            dtype=np.float32
        )
        self.stream.start()
        self.is_playing = True
        print("▶️ 开始播放", flush=True)

    def pause(self):
        """暂停播放"""
        if self.stream is not None and self.is_playing:
            self.stream.stop()  # 仅停止声卡输出，不会重置current_frame
            self.is_playing = False
            print("⏸️  已暂停", flush=True)

    def resume(self):
        """从暂停位置继续播放"""
        if self.stream is not None and not self.is_playing:
            self.stream.start()
            self.is_playing = True
            print("▶️  继续播放", flush=True)

    def stop(self):
        """停止播放并重置进度到开头"""
        if self.stream is not None:
            self.stream.close()
            self.stream = None
        self.current_frame = 0
        self.is_playing = False
        print("⏹️  已停止，回到开头", flush=True)

# ------------------- 测试用例 -------------------
if __name__ == "__main__":
    # 1. 先生成一段5秒的440Hz正弦波测试音频（也可以用soundfile读wav/mp3）
    duration = 5  # 秒
    frequency = 440  # A音
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    test_audio = 0.3 * np.sin(2 * np.pi * frequency * t)  # 0.3控制音量避免爆音

    # 2. 初始化播放器并加载音频
    player = AudioPlayer()
    player.load_audio(test_audio, samplerate=fs)

    # 3. 模拟播放、暂停、继续、停止流程
    player.play()
    time.sleep(2)  # 播放2秒

    player.pause()
    time.sleep(1)  # 暂停1秒

    player.resume()
    time.sleep(3)  # 继续播放到结束（剩余3秒）

    player.stop()

    # --- 如果要播放本地wav文件，替换test_audio部分即可：
    # import soundfile as sf
    # data, fs = sf.read("你的音频文件.wav", dtype='float32')
    # player.load_audio(data, samplerate=fs)

