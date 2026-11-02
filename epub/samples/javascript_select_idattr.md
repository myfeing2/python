用 document.querySelectorAll('[id]') 就能直接选中所有定义了 id 属性的元素，返回的是一个 NodeList，可以遍历或转成数组操作。‌‌

javascript
// 获取所有带 id 的元素
const elementsWithId = document.querySelectorAll('[id]');

// 转成数组后用 filter 进一步筛选
const filtered = Array.from(elementsWithId).filter(el => {
  // 比如只保留 id 非空的
  return el.id !== '';
});
如果想排除 id 为空的元素，CSS 选择器可以这样写：

javascript
const nonEmptyIdElements = document.querySelectorAll('[id]:not([id=""])');

const divsWithId = document.querySelectorAll('div[id]');
这会返回所有带 id 属性的 <div> 元素（NodeList），遍历时直接 forEach 就行。‌‌

用 querySelectorAll 选中有 id 的 <div> 和 <p>，再用 filter 过滤即可，核心就两行：

js
const elements = [...document.querySelectorAll('div[id], p[id]')];
const filtered = elements.filter(el => el.id !== '要排除的id');
🎯 实现思路
‌选中目标元素‌：document.querySelectorAll('div[id], p[id]') 会同时选出带 id 属性的 <div> 和 <p>，返回的是 NodeList，用 [...] 或 Array.from() 转成数组才能用 filter。
‌过滤条件‌：filter 遍历数组，回调里判断 el.id 是否满足你的条件（比如不等于某个值、匹配前缀等），返回 true 就保留。‌‌


几种常见过滤场景
‌只保留 id 非空‌：用 [id]:not([id=""]) 选择器直接搞定，或配合 filter 判断 el.id !== ''。
‌按 id 前缀过滤‌：用 [id^="prefix"]，比如 document.querySelectorAll('[id^="item-"]')。
‌按 id 精确值过滤‌：用 [id="exactId"]。
‌按 id 模式（正则）过滤‌：CSS 选择器不支持正则，需要先 querySelectorAll 初步筛选，再用 filter 和正则二次过滤。‌‌
javascript
// 以 feed_item_ 开头且以数字结尾的 id
const items = [...document.querySelectorAll('[id^="feed_item_"]')]
.filter(el => el.id.match(/\d+$/));
注意事项
直接用 [id] 会匹配到空 id（id=""）和重复 id，HTML 规范里 id 应该唯一，但实际页面可能有意外情况，筛选时留意一下。‌‌
