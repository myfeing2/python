from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

def traverse_dom(view):
    # 遍历所有 div 元素，并获取它们的 id 和 class
    script = """
    (function() {
        var results = [];
        var elements = document.querySelectorAll('div');
        for (var i = 0; i < elements.length; i++) {
            results.push({
                id: elements[i].id,
                className: elements[i].className,
                text: elements[i].textContent.substring(0, 50)  // 取前50字符
            });
        }
        return JSON.stringify(results);
    })();
    """
    
    def callback(result):
        import json
        data = json.loads(result)
        for item in data:
            print(f"ID: {item['id']}, Class: {item['className']}, Text: {item['text'][:20]}...")
    
    view.page().runJavaScript(script, callback)

# 使用示例
app = QApplication([])
view = QWebEngineView()
view.load(QUrl("https://example.com"))
view.loadFinished.connect(lambda: traverse_dom(view))  # 页面加载完成后执行
view.show()
app.exec()

#========================

def get_dom_tree(view):
    script = """
    (function() {
        function walk(node, depth) {
            var result = {tag: node.tagName, depth: depth, children: []};
            for (var i = 0; i < node.children.length; i++) {
                result.children.push(walk(node.children[i], depth + 1));
            }
            return result;
        }
        return JSON.stringify(walk(document.body, 0));
    })();
    """
    
    def callback(result):
        import json
        def print_tree(node, level=0):
            print("  " * level + node['tag'])
            for child in node['children']:
                print_tree(child, level + 1)
        
        data = json.loads(result)
        print_tree(data)
    
    view.page().runJavaScript(script, callback)

#====================

def find_elements_by_condition(view):
    # 查找所有包含特定文本或属性的元素
    script = """
    (function() {
        var results = [];
        // 例：查找所有带 href 属性的链接
        var links = document.querySelectorAll('a[href]');
        for (var i = 0; i < links.length; i++) {
            results.push({
                tag: 'a',
                href: links[i].href,
                text: links[i].textContent.trim()
            });
        }
        return JSON.stringify(results);
    })();
    """
    view.page().runJavaScript(script, lambda result: print(result))

'''
⚠️ 注意事项
‌必须等页面加载完成‌：在 loadFinished 信号触发后再执行 JS，否则 DOM 可能还未就绪。
‌结果通过回调返回‌：runJavaScript() 的返回值是异步的，必须在回调函数中处理结果。
‌JS 与 Python 的数据传递‌：JS 对象需要先 JSON.stringify() 才能正确传递到 Python 端。[5]
‌执行时机‌：如果页面有动态加载内容（如 AJAX），可能需要等待额外的时间或监听特定事件。
'''
