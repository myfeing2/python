获取被点击元素的文本，核心是 ‌在事件回调里通过 event.target 拿到实际点击的 DOM 元素，再用 .textContent 或 .innerText 取值‌。下面按使用场景给你几种写法：

🎯 原生 JS：直接获取被点击元素自身文本
适用于点击的是 <button>、<div>、<p> 这类元素本身。

js
document.querySelectorAll('.your-class').forEach(el => {
  el.addEventListener('click', function(e) {
    // 方式1：用 e.target（实际触发事件的元素）
    console.log('target文本:', e.target.textContent);

    // 方式2：用 this（当前绑定事件的元素）
    console.log('this文本:', this.textContent);
  });
});
‌关于 this 的坑‌：回调用 function(){} 时，this 指向绑定事件的元素；如果用‌箭头函数‌，this 会丢失，此时只能用 e.target。‌‌

🧩 事件委托：动态元素或大量同类元素
如果元素是动态加载的，或者数量很多，建议在父容器上监听：

js
document.getElementById('parent').addEventListener('click', function(e) {
  const target = e.target.closest('.your-class'); // 向上查找匹配的元素
  if (target) {
    console.log('委托获取文本:', target.textContent);
  }
});
closest() 会从 e.target 自身开始向上匹配，能安全处理点击到子元素（如 <span>、图标）的情况。‌‌

🔍 区分 e.target 和 e.currentTarget
e.target：‌实际被点击‌的那个最深层元素（比如 <span> 里的文字节点）。
e.currentTarget 或 this：‌绑定监听器‌的那个元素（比如父级 <li>）。
如果点击 <li> 里的 <span>，e.target 是 <span>，e.currentTarget 是 <li>，两者不同。‌‌

💡 取文本用 textContent 还是 innerText
‌textContent‌：返回所有子节点的纯文本，不包含 HTML 标签，兼容性最好，推荐优先用。
‌innerText‌：也返回纯文本，但会受 CSS 影响（比如 display:none 的文本取不到），性能略差。
‌innerHTML‌：会包含 HTML 标签，如无特殊需求不建议用来取纯文本。‌‌
🔧 jQuery 写法（普通函数才能用 this）
js
$('.your-class').on('click', function() {
  console.log('jQuery文本:', $(this).text().trim()); // 注意：这里必须用普通函数
});
‌关键坑‌：jQuery 回调里如果用‌箭头函数‌，this 会指向外层作用域（如 window），拿不到当前元素，必须用 function(){}。‌‌

🚫 常见错误写法
js
// ❌ 箭头函数里用 this，拿不到元素
el.addEventListener('click', () => {
  console.log(this.textContent); // this 不指向元素
});

// ❌ 直接读 e.target.value（按钮没有 value 属性）
el.addEventListener('click', (e) => {
  console.log(e.target.value); // 返回 undefined
});
补充一点：如果点击目标内部还有嵌套元素（比如 <button><svg><path></path></svg></button>），e.target 可能落到 <path> 上，此时用 e.target.closest('button') 能稳定拿到按钮本身再取文本。‌‌