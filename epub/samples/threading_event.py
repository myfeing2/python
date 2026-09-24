'''
threading.Event 是 Python 中用于‌线程间通信和同步‌的简单机制，通过一个内部标志位（flag）来协调多个线程的执行顺序。‌

核心原理
Event 内部维护一个布尔标志，初始为 False。线程调用 wait() 时会阻塞，直到其他线程调用 set() 将标志置为 True 才会被唤醒。‌

常用方法
表格
方法	作用
set()	将标志设为 True，唤醒所有等待的线程
clear()	将标志重置为 False
wait(timeout=None)	阻塞直到标志为 True，超时则返回 False
is_set()	检查标志是否为 True，不阻塞
典型应用场景
‌启动信号‌：主线程控制多个子线程同时开始工作
‌任务完成通知‌：一个线程完成任务后通知其他线程继续
‌线程优雅停止‌：通过 is_set() 轮询让子线程安全退出
‌暂停/恢复‌：配合 clear() 和 set() 实现任务暂停与继续‌
基本使用示例
python
'''

import threading
import time

# 创建事件对象
event = threading.Event()

def worker():
    print("等待启动信号...")
    event.wait()  # 阻塞等待
    print("开始工作!")

def controller():
    time.sleep(2)
    event.set()  # 触发信号

t1 = threading.Thread(target=worker)
t2 = threading.Thread(target=controller)
t1.start()
t2.start()

'''
注意事项
‌不存储信号‌：若事件已被 set()，之后调用 wait() 会立即返回，不会阻塞。
‌一次性通知‌：set() 后需 clear() 才能再次使用，适合"一次性信号"场景。
‌set() 可重复调用‌：多次调用不会产生额外效果，但也不会报错。
‌适合"开关"场景‌：Event 只传递 True/False，不传递具体数据，比 Lock 更轻量高效。‌
与 Lock 的区别
‌Event‌：用于线程间‌同步‌（按顺序执行），不涉及共享资源访问，效率更高。
‌Lock‌：用于‌互斥‌，保护共享资源不被多个线程同时修改。‌
需要注意的是，wait() 必须搭配 set() 使用，否则线程会一直阻塞；如果业务逻辑中有长阻塞调用（如 socket.recv()），应改用带超时版本并轮询检查 Event，避免响应延迟。‌
'''
