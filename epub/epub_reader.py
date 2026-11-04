"""this is a demo of sherpa-onnx"""

import json
import numpy as np
import librosa
import sherpa_onnx
import sounddevice as sd

from PySide6.QtCore import QObject, Signal, Slot

class TtsObject:
    def __init__(self):
        self.config = None
        self.tts = None
        self.acoustic_model = ""
        self.vocoder = ""
        self.lexicon = ""
        self.tokens = ""
        self.data_dir = ""
        self.num_threads = 2
        self.debug = True
        self.max_num_sentences = 1
        self.rule_fsts = ""

    def loadConfig(self, config_path="tts_matcha.json"):
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
            self.acoustic_model = config_data.get("acoustic_model", "")
            self.vocoder = config_data.get("vocoder", "")
            self.lexicon = config_data.get("lexicon", "")
            self.tokens = config_data.get("tokens", "")
            self.data_dir = config_data.get("data_dir", "")
            self.num_threads = config_data.get("num_threads", 2)
            self.debug = config_data.get("debug", True)
            self.max_num_sentences = config_data.get("max_num_sentences", 1)
            self.rule_fsts = config_data.get("rule_fsts", "")

    def initialize(self, model):
        match model:
            case "matcha":
                self.loadConfig()
                self.config = sherpa_onnx.OfflineTtsConfig(
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
                self.tts = sherpa_onnx.OfflineTts(self.config)
            case _:
                raise ValueError(f"Unsupported model: {model}")

class TtsTask(QObject):
    consumed = Signal()
    finished = Signal()
    
    def __init__(self):
        super().__init__()
        self.tts_object = TtsObject()
        self.tts_object.initialize("matcha")
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
        #self.is_generated = True
        while self.is_running:
            if not self.is_generated:
                try:
                    self.current_frame = 0
                    if self.text.strip() != "":
                        audio = self.tts_object.tts.generate(self.text, sid=0, speed=1.0)
                        self.audio_data = np.asarray(audio.samples, dtype="float32")
                        # for librosa resample, it may cause audio distortion, so we use the original sample rate
                        # this work on linux, but on Windows, it may cause audio distortion, so we use the original sample rate
                        # self.audio_data = librosa.resample(data, orig_sr=audio.sample_rate, target_sr=48000)
                        if self.audio_data.ndim == 1:
                            self.audio_data = self.audio_data.reshape(-1, 1)
                        self.stream = sd.OutputStream(samplerate=audio.sample_rate, channels=1, dtype='float32', callback=self.callback)
                        self.stream.start() # 继续播放
                        self.is_generated = True
                except sd.PortAudioError:
                    pass
