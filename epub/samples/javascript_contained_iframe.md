要检查网页里有没有 <iframe>，核心思路就是‌在页面加载后用 document.querySelectorAll('iframe') 去查找，看返回的集合长度是否为 0‌。以下是几种常用做法：

🔍 基础检查
javascript
// 检查是否存在 iframe
const iframes = document.querySelectorAll('iframe');
if (iframes.length > 0) {
    console.log('页面包含 ' + iframes.length + ' 个 iframe');
} else {
    console.log('页面没有 iframe');
}
这段代码会找出页面里所有 <iframe> 元素，数量大于 0 就说明有。如果想要更精细的控制，可以配合 <u>querySelector</u> 按 id、class 或属性精确定位。‌‌

🧰 进阶用法
‌检查是否加载完成‌：用 load 事件判断 iframe 内容是否渲染完毕，再执行后续操作。
javascript
const iframe = document.getElementById('myIframe');
iframe.addEventListener('load', function() {
    console.log('iframe 已加载完成');
});

2. &zwnj;**获取 iframe 的 URL**&zwnj;：遍历所有 iframe，读取其 `src` 属性或内部页面的地址。注意&zwnj;**跨域页面受同源策略限制，无法直接读取内部 URL**&zwnj;，这种情况要用 `<u>postMessage</u>` 通信。
```javascript
const iframes = document.querySelectorAll('iframe');
iframes.forEach(iframe => {
    console.log('iframe 地址:', iframe.src);
});
```‌‌:ml-citation{ref="13" appearance="aggregated" data="citationList"}

3. &zwnj;**判断当前页面是否被嵌入 iframe**&zwnj;：如果想知道自己页面是不是被别的网站嵌在 iframe 里，可以用 `window.self === window.top` 判断。
```javascript
if (window.self === window.top) {
    console.log('当前页面是顶级窗口，未被嵌入');
} else {
    console.log('当前页面被嵌入在 iframe 中');
}
```‌‌:ml-citation{ref="4" appearance="aggregated" data="citationList"}

### ⚠️ 注意
- 如果 iframe 是&zwnj;**动态创建**&zwnj;的，检查时要等它插入 DOM 后再查，否则可能漏掉。
- 跨域 iframe 的内容无法直接访问，但元素本身（标签、属性）始终可以检查，不受同源策略影响。‌‌:ml-citation{ref="14,18" appearance="aggregated" data="citationList"}
