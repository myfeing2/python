function getFirstVisibleElement(selector = '*') {
  const elements = Array.from(document.querySelectorAll(selector));
  
  // 按文档绝对位置排序（从上到下）
  elements.sort((a, b) => {
    const aTop = a.getBoundingClientRect().top + window.scrollY;
    const bTop = b.getBoundingClientRect().top + window.scrollY;
    return aTop - bTop;
  });

  const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
  const viewportWidth = window.innerWidth || document.documentElement.clientWidth;

  for (const el of elements) {
    const rect = el.getBoundingClientRect();
    const style = window.getComputedStyle(el);

    // 过滤不可见元素：尺寸为0、display:none、visibility:hidden
    if (rect.width === 0 || rect.height === 0) continue;
    if (style.display === 'none' || style.visibility === 'hidden') continue;

    // 判断是否在视口内（任意部分可见就算）
    const isInViewport = (
      rect.top < viewportHeight && rect.bottom > 0 &&
      rect.left < viewportWidth && rect.right > 0
    );

    if (isInViewport) return el;
  }
  
  return null; // 视口内没有可见元素
}

要获取视口内第一个元素，核心思路是用 getBoundingClientRect() 获取每个元素相对视口的位置，再筛选出符合可见条件的元素。
使用示例‌：传入一个元素数组，按 DOM 顺序排列，返回第一个完整出现在视口内的元素。
function getFirstElementInViewport(elements) {
  const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
  const viewportHeight = window.innerHeight || document.documentElement.clientHeight;

  for (const el of elements) {
    const rect = el.getBoundingClientRect();
    const isInViewport = (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= viewportHeight &&
      rect.right <= viewportWidth
    );
    if (isInViewport) {
      return el;
    }
  }
  return null; // 没有元素在视口内
}
