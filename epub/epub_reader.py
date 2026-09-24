"""this is a demo of sherpa-onnx"""

import numpy as np
import librosa
import sherpa_onnx
import sounddevice as sd

from PySide6.QtCore import QObject, Signal, Slot

config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        matcha=sherpa_onnx.OfflineTtsMatchaModelConfig(
            acoustic_model="matcha-icefall-zh-en/model-steps-3.onnx",
            vocoder="vocos-16khz-univ.onnx",
            lexicon="matcha-icefall-zh-en/lexicon.txt",
            tokens="matcha-icefall-zh-en/tokens.txt",
            data_dir="matcha-icefall-zh-en/espeak-ng-data",
        ),
        num_threads=2,
        debug=True, # set it False to disable debug output
    ),
    max_num_sentences=1,
    rule_fsts="matcha-icefall-zh-en/phone-zh.fst,matcha-icefall-zh-en/date-zh.fst,matcha-icefall-zh-en/number-zh.fst",
)
#if not config.validate():
#    raise ValueError("Please check your config")
tts = sherpa_onnx.OfflineTts(config)

class TtsTask(QObject):
    consumed = Signal()
    finished = Signal()
    
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.is_generated = False
        self._pause = False
        self.text = ""
        self.audio_data = None
        self.stream = None

    def play(self):
        if self.is_generated and self.stream:
            self.stream.start() # 继续播放
        
    def stop(self):
        self.is_running = False
        if self.stream:
            self.stream.close() # 播放完毕关闭流
        self.finished.emit()

    def pause(self):
        if not self._pause:
            if self.stream and self.stream.active:
                self._pause = True
                self.stream.stop() # 暂停播放
        else:
            if self.stream and not self.stream.active:
                self._pause = False
                self.stream.start() # 继续播放

    def new_text_arrival(self, text:str):
        self.text = text
        self.is_generated = False
        if self.stream:
            self.stream.close() # 播放完毕关闭流

    def callback(self, outdata, frames, time, status):
        """音频回调函数：声卡需要数据时自动调用，不能阻塞、不能做耗时操作"""
        if status:
            print(f"音频状态警告: {status}", flush=True)
        
        if self.audio_data is None:
            outdata[:] = 0
            return

        chunksize = min(len(self.audio_data) - self.current_frame, frames)
        outdata[:chunksize] = self.audio_data[self.current_frame:self.current_frame + chunksize]
        if chunksize < frames:
            outdata[chunksize:] = 0
            self.consumed.emit()
            raise sd.CallbackStop()
        self.current_frame += chunksize

    @Slot()
    def run(self):
        self.is_running = True
        self.is_generated = True
        while self.is_running:
            if not self.is_generated:
                try:
                    self.current_frame = 0
                    audio = tts.generate(self.text, sid=0, speed=1.0)
                    data = np.asarray(audio.samples, dtype="float32")
                    self.audio_data = librosa.resample(data, orig_sr=audio.sample_rate, target_sr=48000)
                    if self.audio_data.ndim == 1:
                        self.audio_data = self.audio_data.reshape(-1, 1)
                    self.stream = sd.OutputStream(samplerate=48000, channels=1, dtype='float32', callback=self.callback)
                    self.stream.start() # 继续播放
                    self.is_generated = True
                except sd.PortAudioError:
                    pass
