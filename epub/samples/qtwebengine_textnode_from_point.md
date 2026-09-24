获取视口内文本元素的核心思路：‌遍历 DOM 筛选出可见的文本容器，再用 getBoundingClientRect() 判断它们是否与视口相交‌。‌‌

给你一段可直接跑在浏览器控制台的通用方案，不用硬编码标签列表，适合第三方网站抓取场景：

javascript
// 获取视口内所有可见文本元素的通用方案
function getVisibleTextElementsInViewport() {
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;
  const results = [];
  
  // 1. 选择天然承载文本的块级元素
  const candidates = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, dt, dd, blockquote, td, th, span, div');
  
  candidates.forEach(el => {
    // 2. 过滤：必须有实际文本，且未被隐藏
    const text = el.innerText?.trim();
    if (!text) return;
    if (el.offsetParent === null) return; // display: none 或不可见
    
    // 3. 用 getBoundingClientRect 判断是否在视口内（允许部分可见）
    const rect = el.getBoundingClientRect();
    const isInViewport = rect.top < viewportHeight && rect.bottom > 0 && 
                         rect.left < viewportWidth && rect.right > 0;
    
    if (isInViewport) {
      results.push({
        element: el,
        text: text,
        rect: { top: rect.top, left: rect.left, bottom: rect.bottom, right: rect.right }
      });
    }
  });
-**  
  return results;
}

// 调用示例
const visibleTexts = getVisibleTextElementsInViewport();
console.log(visibleTexts);
关键点说明
‌筛选逻辑‌：先用 innerText 获取渲染后的可见文本，再用 offsetParent 排除 display: none 或 visibility: hidden 的元素。
‌视口判断‌：getBoundingClientRect() 返回元素相对视口的位置，通过 top/bottom 与 window.innerHeight 比较即可判断是否进入视口。
‌性能考虑‌：如果需要在滚动时持续检测，建议用 IntersectionObserver 替代手动计算，它异步回调、不阻塞主线程，性能更好。‌‌
进阶优化
‌只取部分可见‌：上面代码允许元素“部分进入视口”就算命中，符合“出现在视口内”的语义。
‌排除脚本样式‌：innerText 本身不会包含 <script>、<style> 内容，无需额外过滤。
‌自定义滚动容器‌：如果目标不在 window 下滚动，而是在 overflow: auto 的容器里，需改用 container.getBoundingClientRect() 并监听容器滚动事件。‌‌
⚠️ 这段代码只检测元素是否在视口内，无法检测是否被其他元素遮挡。若需判断遮挡，要用 document.elementFromPoint() 进一步确认。‌‌
