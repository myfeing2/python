用 textContent 就能直接拿到元素自身的全部文本（包含子元素的），但要“不含子元素”就得分两步：先拿到自己的文本节点，再看有没有。

‌核心思路：遍历 childNodes，只统计 nodeType === 3（文本节点）且 trim() 后不为空的内容。‌

javascript
function hasOwnText(element) {
  for (let i = 0; i < element.childNodes.length; i++) {
    const node = element.childNodes[i];
    if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() !== '') {
      return true;
    }
  }
  return false;
}
关键点说明
childNodes 会包含文本节点和元素节点，children 只包含元素节点，所以这里必须用 childNodes。
Node.TEXT_NODE 的值是 3，用来过滤出真正的文本节点，跳过子元素。
trim() 是为了排除纯空白文本（如换行、缩进），那些不算“有字”。‌‌
如果你想顺便拿到这段文本
javascript
function getOwnText(element) {
  let text = '';
  for (let i = 0; i < element.childNodes.length; i++) {
    const node = element.childNodes[i];
    if (node.nodeType === Node.TEXT_NODE) {
      text += node.textContent;
    }
  }
  return text.trim();
}
注意：textContent 会连子元素的文本一起返回，innerText 也是，所以不能直接用它们来判断“自身文本”。‌‌
