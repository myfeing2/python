获取 iframe 里的文本，核心就一句话：‌先拿到 iframe 的 contentDocument（或 contentWindow.document），再读里面的 body 内容‌。但能不能直接读，取决于 iframe 和当前页面是不是同源。

同源情况下（协议、域名、端口一致）
直接用 contentDocument 或 contentWindow.document 访问内部 DOM，这是最常用的方式。‌‌

javascript
var iframe = document.getElementById('myIframe');
// 等 iframe 加载完成再操作
iframe.onload = function() {
    var doc = iframe.contentDocument || iframe.contentWindow.document;
    var text = doc.body.innerText;      // 纯文本
    // 或者拿 HTML：doc.body.innerHTML
    console.log(text);
};
‌contentWindow‌ 获取 iframe 的 window 对象，再通过 .document 访问文档。
‌contentDocument‌ 直接返回 iframe 里的 document 对象，两者等效，但 contentDocument 在 IE8 及以下不支持，contentWindow 兼容性更好。‌‌
建议监听 iframe 的 load 事件再操作，否则可能拿到空的 document。‌‌

跨域情况下（不同源）
同源策略会阻止直接访问 DOM，浏览器会抛 SecurityError。唯一标准做法是用 ‌postMessage‌ 进行消息通信。‌‌

父页面发送消息：

javascript
iframe.contentWindow.postMessage({ type: 'getText' }, 'https://子页面域名');
iframe 内部页面监听并返回内容：

javascript
window.addEventListener('message', function(event) {
    // 务必校验来源
    if (event.origin !== 'https://父页面域名') return;
    if (event.data.type === 'getText') {
        event.source.postMessage({ text: document.body.innerText }, event.origin);
    }
});
父页面接收回传内容：

javascript
window.addEventListener('message', function(event) {
    if (event.origin !== 'https://子页面域名') return;
    console.log(event.data.text);
});
跨域时 postMessage 的第二个参数务必指定确切的目标源，不要用 '*'，否则有安全风险。‌‌

补充说明
‌获取元素的方式‌：拿到 document 后，可以用 getElementById、querySelector 等标准 DOM 方法继续定位具体元素。
‌老浏览器兼容‌：早期 IE 用 document.frames["iframeName"].document 获取，现代浏览器统一用 contentWindow 即可。
‌如果 iframe 是动态创建的‌：需要先 appendChild 到页面，再等 load 事件后操作。‌‌
