要在 DOM 里用 JavaScript 选中当前光标位置的下一个单词，核心思路是先拿到光标位置，再用 Selection 和 Range 按单词粒度去扩展选区。这里直接给出可用的实现方法。‌‌

基本实现：基于光标位置选中下一个单词
javascript
function selectNextWord() {
  const sel = window.getSelection();
  if (!sel.rangeCount) return;

  const range = sel.getRangeAt(0);
  range.collapse(false); // 折叠到光标终点位置

  // 先向后扩展一个单词，覆盖绝大多数情况
  sel.modify('extend', 'forward', 'word');
}
这段代码先用 collapse(false) 把选区折叠到光标终点，再用 modify('extend', 'forward', 'word') 向前扩展一个单词粒度。‌‌

进阶处理：跨节点和边界情况
modify('word') 在遇到跨节点文本或 URL 等特殊字符时可能不准确，这时需要手动遍历文本节点来补齐。思路是：先从光标处取到单词片段，如果这个片段正好落在文本节点边界，就继续读取相邻文本节点，把完整单词拼接起来。‌‌

javascript
function getFullWordAtCursor() {
  const sel = window.getSelection();
  if (!sel.rangeCount) return '';

  const range = sel.getRangeAt(0);
  range.collapse(false);
  let node = range.startContainer;
  let offset = range.startOffset;

  // 只在文本节点上处理
  if (!node || node.nodeType !== Node.TEXT_NODE) return '';

  const data = node.textContent;
  if (offset >= data.length) offset = data.length - 1;

  // 跳过空白字符
  if (/\s/.test(data[offset])) return '';

  // 向前后扫描，找出当前单词片段
  let start = offset, end = offset;
  while (start > 0 && !/\s/.test(data[start - 1])) start--;
  while (end < data.length - 1 && !/\s/.test(data[end + 1])) end++;

  let word = data.substring(start, end + 1);

  // 如果单词片段在节点边界，需要跨节点补全
  if (end === data.length - 1) {
    let next = node.nextSibling;
    while (next && next.nodeType !== Node.TEXT_NODE) next = next.nextSibling;
    if (next) {
      let i = 0;
      while (i < next.textContent.length && !/\s/.test(next.textContent[i])) {
        word += next.textContent[i++];
      }
    }
  }
  return word;
}
拿到完整单词后，再用 setBaseAndExtent() 精确设置选区，就能选中下一个单词了。‌‌

不同场景的注意事项
‌可编辑 div 和普通文本‌：上面代码都适用，核心是拿 Selection 和 Range 对象。
‌input / textarea‌：不能用 Selection，要用 selectionStart / selectionEnd 加 setSelectionRange() 来定位和选中。
‌兼容性‌：selection.modify() 在现代浏览器基本可用；如果遇到兼容问题，就退回手动遍历文本节点的方案。‌‌
需要注意：selectionchange 事件在拖拽选中时会频繁触发，如果在这个事件里做自动选中，要加防抖或条件判断，避免性能问题