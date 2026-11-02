document.elementFromPoint(x, y) 是浏览器原生 API，用来获取当前视口指定坐标处‌最顶层‌的元素。‌‌

📌 基本用法
直接传入相对于视口左上角的 ‌CSS 像素坐标‌，返回该点最上层的 DOM 元素：

javascript
const el = document.elementFromPoint(100, 200);
获取鼠标点击位置的元素：

javascript
document.addEventListener('click', (e) => {
  const el = document.elementFromPoint(e.clientX, e.clientY);
  console.log(el);
});
```‌‌:ml-citation{ref="2,11" appearance="aggregated" data="citationList"}

### ⚠️ 常见坑点
1. &zwnj;**坐标必须是视口坐标**&zwnj;：只认 `clientX/clientY` 这类相对可视区域左上角的值，不接受文档坐标（`pageX/pageY`）或滚动偏移后的坐标。
2. &zwnj;**坐标越界返回 null**&zwnj;：传入负数或超出视口宽高（`window.innerWidth/innerHeight`）的坐标会返回 `null`。
3. &zwnj;**受 `pointer-events` 影响**&zwnj;：如果目标元素或其祖先设置了 `pointer-events: none`，即使视觉可见也会被跳过。
4. &zwnj;**`visibility: hidden` 不参与命中**&zwnj;：虽然占布局，但会被忽略；`display: none` 的元素完全不参与渲染。
5. &zwnj;**DOM 未就绪时调用会失败**&zwnj;：建议在 `DOMContentLoaded` 之后或包一层 `requestAnimationFrame` 再查。‌‌:ml-citation{ref="2,3" appearance="aggregated" data="citationList"}

### 🔍 实际场景处理
1. &zwnj;**获取滚动后文档坐标的元素**&zwnj;：先减去滚动偏移再调用。
   ```javascript
   const viewportX = docX - window.scrollX;
   const viewportY = docY - window.scrollY;
   const el = document.elementFromPoint(viewportX, viewportY);
‌跨 iframe 调用‌：必须在目标 iframe 的 contentDocument 上调用，坐标要减去 iframe 的偏移。
javascript
const rect = iframe.getBoundingClientRect();
const relX = x - rect.left;
const relY = y - rect.top;
const el = iframe.contentDocument.elementFromPoint(relX, relY);
‌移动端 touch 事件‌：用 touches.clientX/Y 或 changedTouches 都行，但要注意 iOS Safari 缩放时坐标可能滞后。
‌高频调用性能‌：不要节流或防抖，而是按坐标变化阈值触发（如 Δx > 2px 才调用），缓存上次结果。‌‌
🔄 和 elementsFromPoint 的区别
document.elementsFromPoint(x, y) 返回‌所有‌命中元素的数组（从顶层到底层），适合需要遍历判断的情况；elementFromPoint 只返回最顶层那一个。 现代浏览器基本都支持 elementsFromPoint，但 IE 不支持。‌‌

动态内容（Canvas 绘制、WebGL 渲染、clip-path 裁剪区域）不适合用这个方法，需要回归到几何计算或底层渲染 API 的拾取逻辑。‌‌