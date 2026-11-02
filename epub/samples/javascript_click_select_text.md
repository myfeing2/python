实现“点击文本后自动选中”，核心就是‌在点击事件里用 Range + Selection 把目标元素的内容圈起来‌。给你直接可用的代码方案：

javascript
// 绑定到任意元素，点击后选中其全部文本
function selectText(e) {
  const el = e.target;
  const range = document.createRange();
  range.selectNodeContents(el); // 选中元素内的文本内容（不含标签本身）
  const selection = window.getSelection();
  selection.removeAllRanges();   // 先清空已有选区，否则可能叠加失效
  selection.addRange(range);
}

// 使用方式（以 div 为例）
document.querySelectorAll('.selectable').forEach(el => {
  el.addEventListener('click', selectText);
});
📌 关键点说明
‌selectNodeContents(el) 与 selectNode(el) 的区别‌：前者只选中元素内的文本和子节点内容，不含标签本身，更符合“选中文字”的预期；后者会把整个元素连同标签一起选中。‌‌

‌必须 removeAllRanges() 再 addRange()‌：否则新选区和旧选区叠加，会导致选中不生效或显示异常。‌‌

‌如果目标是 <input> 或 <textarea>‌：不需要用 Range，直接用原生的 select() 方法即可：‌‌

javascript
document.getElementById('myInput').addEventListener('focus', function() {
  this.select();
});
‌旧版 IE 兼容‌（IE 9 以下）：用 document.body.createTextRange() 和 moveToElementText() 代替：‌‌
javascript
if (document.body.createTextRange) {
  const textRange = document.body.createTextRange();
  textRange.moveToElementText(el);
  textRange.select();
}
⚠️ ‌注意‌：如果点击的元素内部有嵌套子元素（如 <span>、<br>），e.target 可能指向的是子元素而不是你绑定事件的元素。此时建议改用 e.currentTarget 来确保选中的是整个绑定元素的内容。‌‌

🎯 实际场景示例
给一个完整的 HTML 示例，直接复制就能跑：

html
<!DOCTYPE html>
<html lang="zh-CN">
<body>
  <style>
.selectable { cursor: pointer; padding: 8px; border: 1px solid #ccc; }
  </style>

  <div class="selectable">点击这段文字试试，会被自动选中</div>
  <div class="selectable">第二段也能选中</div>

  <input type="text" value="点击输入框自动全选" id="myInput">

  <script>
    // 普通元素：点击选中内容
    document.querySelectorAll('.selectable').forEach(el => {
      el.addEventListener('click', function(e) {
        const range = document.createRange();
        range.selectNodeContents(this);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
      });
    });

    // 输入框：点击自动全选
    document.getElementById('myInput').addEventListener('focus', function() {
      this.select();
    });
  </script>
</body>
</html>
如果需要‌选中后自动复制‌，可以在 addRange 之后加一句 document.execCommand('copy')（旧方法）或使用 navigator.clipboard.writeText(selection.toString())（新方法）。‌‌
