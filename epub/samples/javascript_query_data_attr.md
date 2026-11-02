在 JavaScript 里按自定义属性值查找元素，核心就是用 ‌CSS 属性选择器‌配合 querySelector 和 querySelectorAll 这两个方法。‌

‌查找第一个匹配的元素‌：用 document.querySelector('[data-custom="value"]')，返回第一个匹配的 Element 对象，找不到时返回 null。
‌查找所有匹配的元素‌：用 document.querySelectorAll('[data-custom="value"]')，返回一个 NodeList，可以用 forEach 遍历。‌
具体用法
‌精确匹配属性值‌

javascript
// 查找 data-id 为 "123" 的元素
const element = document.querySelector('[data-id="123"]');

// 查找所有 data-role 为 "admin" 的元素
const allAdmins = document.querySelectorAll('[data-role="admin"]');
‌只匹配某个属性存在‌（不关心值）

javascript
// 查找所有带 data-target-id 属性的 div
const divs = document.querySelectorAll('div[data-target-id]');
‌组合标签、类名等更精确地筛选‌

javascript
// 查找 div 标签中 data-id 为 "legacy" 的元素
const legacyDivs = document.querySelectorAll('div[data-id="legacy"]');

// 在某个父容器内查找
const container = document.getElementById('task_id');
const sign = container.querySelector('input[id-sign="lnglat"]');
‌按属性值的部分匹配‌

javascript
// 查找 data-name 值包含 "cat" 的元素
document.querySelectorAll('[data-name*="cat"]');

// 查找 data-name 值以 "cat" 开头的元素
document.querySelectorAll('[data-name^="cat"]');
关键注意事项
‌属性名格式‌：选择器里必须用完整的属性名，比如 [data-target-id]，不能用驼峰写法。
‌批量匹配多个值‌：querySelectorAll 不支持直接传数组或多值选择器。要查找多个值（比如 data-name 为 "cat" 和 "dog" 的元素），需要循环每个值单独查，再用 Set 去重合并。
‌动态内容‌：如果元素是后来动态加载的，要等 DOM 就绪或元素添加后再执行查询。
‌性能‌：在很大的 DOM 里用复杂属性选择器会有开销，性能敏感时可以结合 id 或 class 缩小范围，并缓存查询结果。‌
拿到元素后怎么取自定义属性的值
‌推荐用 dataset‌：专门处理 data-* 属性，data-user-name 会映射为 element.dataset.userName，更简洁可读。
‌通用方法 getAttribute()‌：可以读任何属性，但要写完整属性名，如 element.getAttribute('data-id')。‌
javascript
const el = document.querySelector('[data-id="legacy"]');
if (el) {
  console.log(el.dataset.id);        // 输出 "legacy"
  console.log(el.getAttribute('data-id')); // 输出 "legacy"
}
注意：如果 querySelector 找不到元素会返回 null，直接访问 dataset 会报错，使用前一定要做存在性检查。‌
