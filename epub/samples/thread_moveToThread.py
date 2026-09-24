'''
这个报错的意思是：你的 TtsTask 类在 __init__ 里没有调用父类的初始化方法。moveToThread 要求对象必须是 QObject 的子类，而 PySide6 在创建对象时会通过 libshiboken 检查父类 __init__ 是否被正确调用，没调就会抛这个 RuntimeError。

原因
TtsTask 继承自 QObject，但你在 __init__ 里可能写了自定义逻辑，却忘了调用 super().__init__()。ShiBoken（PySide6 的底层绑定）需要在对象创建时就完成 C++ 层的初始化，这一步没做，moveToThread 就无法正常绑定线程。‌

python
class TtsTask(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)  # 这一行必须加上
        # 你自己的初始化代码
排查步骤
‌确认继承关系‌：TtsTask 必须直接或间接继承自 QObject，不能是普通 Python 类。
‌检查 __init__ 里的 super().__init__()‌：如果没写，补上；如果写了，检查是否被条件分支跳过，或者参数传递是否错误（比如 parent 没传对）。
‌确认没有重复调用‌：不要在 __init__ 里再次调用 moveToThread 或 start()，这些操作应在对象完全构造后再进行。‌
代码示例
python
'''

from PySide6.QtCore import QObject, QThread

class TtsTask(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)  # 必须调用
        self._running = False

    def do_work(self):
        # 耗时操作
        pass

# 使用
thread = QThread()
task = TtsTask()
task.moveToThread(thread)
thread.started.connect(task.do_work)
thread.start()

'''
其他注意事项
如果你用 moveToThread 管理耗时任务，注意线程里不要直接操作 UI 控件，否则会崩溃。
如果对象在线程结束后被删除，后续再访问也会出现类似 Internal C++ object already deleted 的错误，记得在线程结束时清理信号连接。‌
这类问题通常就是父类初始化没调用导致的，补上 super().__init__() 后一般就能解决。如果还报错，检查下是不是 TtsTask 的 __init__ 里有逻辑提前 return 了。
'''
