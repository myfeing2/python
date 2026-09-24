'''
在 sherpa_onnx 里做 TTS 多线程，核心思路是‌用一个 OfflineTts 实例，配合 Python 的 ThreadPoolExecutor 并发调用 generate()‌。有个关键点：OfflineTts 实例本身不是线程安全的，但它的 generate() 方法是线程安全的，所以多线程共享同一个 TTS 实例是可行的，这也是官方推荐的做法。‌

🔧 基础多线程实现
‌创建 TTS 引擎‌：配置好模型和 num_threads（这是单个推理任务内部使用的线程数）。
‌用线程池并发调用‌：把要合成的文本列表提交给线程池，每个任务调用 tts.generate()。‌
python
'''

import sherpa_onnx
import soundfile as sf
from concurrent.futures import ThreadPoolExecutor
import os

# 1. 配置 TTS 引擎（num_threads 是单次推理的线程数）
config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(
            model="./model.onnx",
            tokens="./tokens.txt",
            data_dir="./espeak-ng-data",
        )
    ),
    num_threads=2,  # 单次推理用 2 线程，通常 2-4 个最佳 
)‌

tts = sherpa_onnx.OfflineTts(config)

# 2. 多线程并发合成
texts = ["你好", "Hello world", "测试多线程", "TTS 并发"]

def synthesize(text, output_path):
    audio = tts.generate(text, sid=0, speed=1.0)  # 线程安全 
    sf.write(output_path, audio.samples, audio.sample_rate)
    return output_path‌

# 用线程池并发执行，max_workers 根据 CPU 核心数调整
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(synthesize, t, f"output_{i}.wav") for i, t in enumerate(texts)]
    for future in futures:
        print(future.result())

'''
⚙️ 线程数怎么配
‌num_threads（单任务内）‌：控制单个 generate() 调用内部的推理并行度，一般 ‌2-4 个‌效果最好，调太高反而可能因线程切换变慢。
‌max_workers（并发任务数）‌：控制同时合成几个文本，建议根据 CPU 核心数和任务类型调整。有个经验公式：线程数 = min(物理核心数 × 1.2（CPU密集）, 并发请求数 × 0.8（IO密集）)。‌
python
'''

# 简单粗暴的自动配置
num_workers = max(1, int(os.cpu_count() * 0.75))  # 参考公式 
‌
### 🚀 进阶：异步 + 多线程
'''
如果要做成服务，可以把 `ThreadPoolExecutor` 和 `asyncio` 结合，避免阻塞事件循环：‌

python
'''

import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def async_tts(text):
    loop = asyncio.get_event_loop()
    # 把同步的 generate 丢到线程池执行，不阻塞主线程
    audio = await loop.run_in_executor(executor, tts.generate, text)
    return audio

# 用法示例
async def main():
    tasks = [async_tts(t) for t in texts]
    results = await asyncio.gather(*tasks)
    # 处理 results...

asyncio.run(main())

'''
⚠️ 注意事项
‌共享实例‌：多个线程共用一个 OfflineTts 实例没问题，generate() 是线程安全的；但别在多个线程里同时创建/销毁实例。
‌内存占用‌：线程越多内存占用越高，如果模型较大（比如 Kokoro），建议控制并发数，避免内存溢出。
‌模型选择‌：如果主要是中文场景，用 vits-zh 这类中文模型；如果是中英混合，用 kokoro-multi-lang 效果更好。
‌输出文件‌：多线程同时写文件时，注意文件路径别重复，否则会互相覆盖。‌
'''
