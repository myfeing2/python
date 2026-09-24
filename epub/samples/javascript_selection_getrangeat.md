getRangeAt() 是 ‌Selection‌ 对象的方法，用来按索引获取当前选区包含的 ‌Range‌ 对象，通常用 getRangeAt(0) 拿第一个（也是大多数浏览器里唯一的）选区范围。‌

📌 基本用法
javascript
const selection = window.getSelection();
if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    // 拿到 range 后就能操作选中内容了
}
先检查 rangeCount 再调用，否则没选中内容时会报错。‌

🎯 常见应用场景
‌获取选中 HTML‌：用 range.cloneContents() 复制选中片段，再塞进临时 div 取 innerHTML。
‌删除/替换选中内容‌：range.deleteContents() 清空选区，再用 range.insertNode() 插入新节点。
‌文本高亮‌：结合 surroundContents() 把选中内容包进 <span> 或 <strong> 标签，实现标注或加粗。
‌光标定位‌：配合 collapse() 和 addRange() 把光标移到指定位置。‌
⚠️ 注意事项
大多数浏览器一个 Selection 最多只有一个 Range，只有 Firefox 支持多选（Ctrl/Cmd + 点击）。
调用前一定先判断 rangeCount > 0，否则 getRangeAt(0) 会抛错。
anchorNode/focusNode 代表选区的起点和终点，可能跟 Range 的 start/end 方向不同，操作时要留意。‌
