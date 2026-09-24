点击元素后自动选中它的文本，核心思路是用 e.target 拿到被点的元素，再用 Range + window.getSelection() 把内容框选出来。给你一个直接能用的版本：

html
<div onclick="selectText(event)">点击我选中这段文字</div>

<script>
function selectText(e) {
  const el = e.target;
  const range = document.createRange();
  range.selectNodeContents(el); // 只选内容，不含标签本身
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
}
</script>
几个关键点帮你避坑：

‌用 selectNodeContents 而不是 selectNode‌：前者只选中元素内部的文本和子节点，不含外层标签，更符合“选中文本”的预期。
‌兼容处理 e.target‌：现代浏览器直接用 e.target 就行，老 IE 才需要回退到 e.srcElement。
‌点击子元素时的陷阱‌：如果 <div> 里面还有 <input>、<button> 这类可交互子元素，e.target 会指向子元素而不是容器，这时可以向上查找：e.target.closest('div')。‌‌
如果你是在列表里点击某个按钮，想拿到对应列表项的文本，那就换一套思路——用 closest() 找到共同的父容器，再用 querySelector() 定位目标元素：

javascript
document.querySelectorAll('.list-item button').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const item = e.target.closest('.list-item');
    const title = item.querySelector('.title').textContent;
    console.log(title);
  });
});
这里 textContent 拿的是纯文本，不会带 HTML 标签，性能也比 innerText 好。‌‌

补充两个小提醒：

移动端 Safari 下记得加 user-select: text，否则可能选不中。‌‌

如果页面上有很多可点击选中的元素，建议用事件委托（在父容器上绑定一次监听），别给每个元素单独绑，性能和代码可维护性都好很多