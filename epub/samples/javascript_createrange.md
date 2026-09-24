document.createRange() 是浏览器提供的原生方法，用来创建一个 ‌Range 对象‌，代表文档中的一个连续区域（可以是一段文本、一个节点或跨节点的内容）。这个对象本身不选中任何内容，需要通过 setStart() 和 setEnd() 等方法来指定边界。

🎯 核心用法
‌创建 Range‌：直接调用 document.createRange() 即可，不需要传参数。
‌设置边界‌：
range.setStart(node, offset) 设置起点，offset 在文本节点里是字符偏移，在元素节点里是子节点索引。
range.setEnd(node, offset) 设置终点，规则同上。
也可以用快捷方法：selectNode(el) 选中整个元素，selectNodeContents(el) 只选中元素内部内容。
‌应用到选区‌：要把 Range 显示成高亮或供用户操作，需要配合 window.getSelection()：
js
const sel = window.getSelection();
sel.removeAllRanges();  // 清空现有选区
sel.addRange(range);    // 添加你的 Range
‌操作内容‌：拿到 Range 后可以做这些事：
cloneContents()：复制范围内的 DOM 片段（含标签）。
deleteContents()：删除范围内的内容。
extractContents()：移除并返回范围内的内容，方便插入到别处。
insertNode(node)：在范围起点插入新节点。
surroundContents(node)：用新节点包裹范围内容。
⚠️ 注意点
document.createRange() 是 DOM2 标准方法，现代浏览器都支持；但 ‌IE 8 及以下不支持‌，只能用 document.body.createTextRange() 代替。
如果 Range 的起点和终点落在同一个位置（collapsed 为 true），它就相当于一个光标，可以用来插入内容或移动焦点。
一次只能显示一个 Range 的高亮，多选（Ctrl 多选）在多数浏览器中受限，不建议依赖。‌
🔍 适用场景
富文本编辑器里的加粗、高亮、插入链接等操作。
自定义文本选择、提取或格式化。
跨节点操作文本（比如选中一个段落里的部分文字并包裹标签）。
如果需要把 Range 存到服务器（比如保存用户高亮位置），不能直接存对象，需要把起点和终点节点转成选择器（如 XPath 或 CSS 选择器），下次再通过选择器找回节点重新创建 Range。‌