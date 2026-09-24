"""this is a demo of sherpa0-onnx"""

import sherpa_onnx
import sounddevice as sd
import onnxruntime as ort

print(ort.__version__)
print(ort.get_available_providers())  # 比如 ['CPUExecutionProvider']
sess = ort.InferenceSession("kokoro-multi-lang-v1_1/model.onnx", \
    providers=['CPUExecutionProvider'])

config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig( \
            model="kokoro-multi-lang-v1_1/model.onnx", \
            voices="kokoro-multi-lang-v1_1/voices.bin", \
            tokens="kokoro-multi-lang-v1_1/tokens.txt", \
            data_dir="kokoro-multi-lang-v1_1/espeak-ng-data", \
            lexicon="kokoro-multi-lang-v1_1/lexicon-zh.txt, \
               kokoro-multi-lang-v1_1/lexicon-us-en.txt",\
        ),
        num_threads=1,
    ),
)

#if not config.validate():
#    raise ValueError("Please check your config")

tts = sherpa_onnx.OfflineTts(config)
TEXT = "This model supports both Chinese and English. \
    小米的核心价值观是什么？答案是真诚热爱！有困难，\
    请拨打110 或者18601200909。I am learning 机器学习. \
    我在研究 machine learning。What do you think \
    中英文说的如何呢?今天是 2025年6月18号."
audio = tts.generate(text=TEXT,
                     sid=0,
                     speed=1.0)

sd.play(audio.samples, samplerate=audio.sample_rate)
sd.wait()
