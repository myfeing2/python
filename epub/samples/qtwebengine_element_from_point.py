# 获取当前视口对应的 DOM 元素或节点信息
def get_viewport_node(self):
    js_code = """
    (function() {
        // 返回视口相关信息，例如视口尺寸
        return {
            width: window.innerWidth,
            height: window.innerHeight,
            // 也可以返回视口顶部的元素等
            topElement: document.elementFromPoint(window.innerWidth/2, 0)?.tagName || null
        };
    })()
    """
    self.view.page().runJavaScript(js_code, self.on_viewport_result)

def on_viewport_result(self, result):
    print(result)  # {'width': 1920, 'height': 1080, 'topElement': 'DIV'}

'''
document.elementFromPoint(x, y) 是浏览器原生 API，用来‌获取视口内指定坐标点上最顶层的那个 DOM 元素‌。‌

基本用法
javascript
const el = document.elementFromPoint(100, 200);
传入的 x、y 是‌相对于当前视口左上角的 CSS 像素坐标‌（也就是 clientX / clientY 那套），不是页面文档坐标。
坐标超出视口范围（负数或大于 window.innerWidth / innerHeight）会返回 null。
如果坐标点没有元素，返回根元素 <html>。‌
常见应用场景
‌模拟点击‌：拿到坐标上的元素后，直接调用 .click()，或用 MouseEvent 构造事件再 dispatchEvent，实现自动化点击。
‌检测元素覆盖‌：取目标元素中心点坐标，调用 elementFromPoint，如果返回的不是目标元素，说明它被其他元素挡住了。
‌鼠标悬浮热区检测‌：在 mousemove 里用 e.clientX / e.clientY 实时获取鼠标下的元素。‌
容易踩的坑
坐标没对齐视口是返回 null 或错误元素的最常见原因。如果你手头是文档坐标，先减去滚动偏移再传：docX - window.scrollX、docY - window.scrollY。‌

‌pointer-events: none 的元素‌：视觉上还在，但 elementFromPoint 会直接跳过它，返回底下的元素。
‌iframe 场景‌：必须要在对应 iframe 的 contentDocument 上调用，不能在顶层 document 查子 frame 里的元素。
‌DOM 刚修改后立刻调用‌：可能拿到旧结果，稳妥做法是包一层 requestAnimationFrame 再查。
‌返回结果受层叠顺序影响‌：多个元素重叠时，它只返回最上面那个（z-index 最高的）。如果想拿全部层叠元素，可以用 document.elementsFromPoint(x, y)，它会返回从顶到底的数组。‌
高频调用的性能建议
鼠标移动每秒触发 60+ 次，频繁调用 elementFromPoint 叠加 DOM 遍历容易掉帧。别盲目节流/防抖，更实用的做法是：‌只在坐标变化超过 2px 时才重新查询‌，其余时间复用上一次结果。‌
'''
    
