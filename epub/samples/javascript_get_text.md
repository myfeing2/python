获取元素文本值，最推荐用 textContent，它性能好、兼容性强，而且拿到的就是纯文本，不带 HTML 标签。‌

javascript
// 获取元素
const element = document.getElementById('myElement');
// 获取文本值
const text = element.textContent;
console.log(text);
三种方式的区别
‌textContent‌：获取元素及其所有后代的纯文本，不受 CSS 影响，隐藏的文本也能拿到，性能最好，W3C 标准，推荐优先使用。
‌innerText‌：只获取用户可见的文本，会受 CSS 影响（比如 display: none 的内容拿不到），性能稍差，适合需要精确匹配用户看到内容的场景。
‌innerHTML‌：返回包括 HTML 标签在内的全部内容，适合需要操作 HTML 结构的场景，但可能有 XSS 安全风险，不建议仅用来取文本。‌
表单元素特殊处理
如果是 <input>、<textarea> 这类表单元素，需要用 value 属性获取用户输入的内容，而不是 textContent。‌

javascript
const inputValue = document.getElementById('myInput').value;
⚠️ 需要注意：如果获取的是隐藏元素（display: none），innerText 会返回空字符串，但 textContent 仍能正常获取；如果用 jQuery，可以用 $('#myElement').text() 快速获取文本。‌