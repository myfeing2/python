在 JS 里获取点击的元素，最标准的方式是 event.target，它始终指向你真正点到的那个最内层元素。‌‌

javascript
document.addEventListener('click', function (event) {
  console.log(event.target); // 点击哪个元素，这里就输出哪个
});
区分 target 和 currentTarget
‌event.target‌：实际被点击的元素（“谁被点”）。
‌event.currentTarget‌：事件监听器绑定的元素（“谁绑的”）。
在事件委托里两者经常不一样：给父容器绑监听，点里面的子元素，target 是子元素，currentTarget 是父容器。‌‌

javascript
document.getElementById('list').addEventListener('click', function (event) {
  console.log('target:', event.target);         // 可能是 li，也可能是 li 里的 span 或文本
  console.log('currentTarget:', event.currentTarget); // 总是 list
});
实际开发中的推荐写法
‌事件委托 + closest() 向上查找‌：点列表项时，目标可能是 li 里的子标签或文本节点，用 closest() 更稳妥。
javascript
const list = document.getElementById('list');
list.addEventListener('click', function (event) {
  const clickedLi = event.target.closest('li');
  if (clickedLi) {
    console.log('点击的列表项:', clickedLi.textContent);
  }
});
```‌‌:ml-citation{ref="1,7" appearance="aggregated" data="citationList"}

‌排除文本节点‌：点纯文字时 target 可能是 #text 节点，可先检查 nodeType 再操作。
javascript
if (event.target.nodeType === Node.ELEMENT_NODE) {
  console.log(event.target);
}
```‌‌:ml-citation{ref="1,7" appearance="aggregated" data="citationList"}

‌jQuery 里用 $(this)‌：在 .on('click', function(){...}) 回调里，this 指向被点击的元素本身。‌‌
注意：onclick="func(this)" 里 this 指向当前元素；但普通函数调用时 this 是 window 或 undefined，推荐直接用 addEventListener 或 event.target。‌‌

获取一组元素中被点击的索引
用 querySelectorAll 拿到元素集合后，用 indexOf 定位：

javascript
const items = document.querySelectorAll('.item');
let lastIndex = null;

items.forEach(node => {
  node.addEventListener('click', function () {
    lastIndex = [...items].indexOf(this);
    console.log('点击索引:', lastIndex);
  });
});
其他常用属性
拿到 event.target 后，可以继续读取：

event.target.id — 元素 ID
event.target.className — class 名
event.target.innerHTML — 内部 HTML
event.target.dataset.id — 自定义 data-* 属性
简单说：‌用 event.target 拿真正点击的元素，用 closest() 向上找你要操作的那个节点，动态列表优先用事件委托。