核心思路是‌遍历页面里所有“可能承载文字”的元素，再筛出当前视口内可见的那些‌，而不是只匹配 <p> 标签。‌‌

推荐下面这个通用方案，可以直接在浏览器控制台跑：

javascript
// 1. 选出一个有代表性的“文本容器”集合（涵盖 p、标题、列表、引用等）
const candidates = [...document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, dd, dt, blockquote, pre, figcaption, td, th, span, div')];

// 2. 过滤出“看起来像文本块”且“至少有一部分在视口内”的元素
const visibleTexts = candidates
.filter(el => {
    // 语义层：跳过空白、纯装饰性元素
    const text = el.textContent.trim();
    if (!text) return false;
    if (el.children.length > 0 && el.textContent.length < 20) return false; // 太短且带子元素，多半是容器不是内容

    // 视觉层：判断是否在视口内
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom > 0 &&
           rect.left < window.innerWidth && rect.right > 0;
  })
.map(el => el.textContent.trim());

console.log([...new Set(visibleTexts)]); // 去重后输出
关键点说明
‌判断视口‌：用 getBoundingClientRect() 获取元素相对视口的位置，再跟 window.innerWidth / innerHeight 比较，就能知道它当前是否可见。
‌筛选文本‌：textContent 会包含隐藏元素和 script/style 里的内容，所以不能直接拿它当结果；上面的写法用“元素类型 + 文本长度”做了粗筛。
‌只拿“可见文本”更简单‌：如果你只是想快速抓当前屏的文字，不追求精准，可以直接用 document.body.innerText——它天然忽略隐藏元素，返回渲染后用户能看到的文本。‌‌
⚠️ 注意
innerText 受 CSS 影响，会触发浏览器重算布局；大量调用时性能不如 textContent。
如果页面有自定义滚动容器（比如某个 overflow: auto 的 div），window.innerHeight 判断的是整个窗口，不适用于那个容器内部的可见性判断。‌‌
想更精准地监控“元素进入视口”这个动作（比如做懒加载），推荐用 IntersectionObserver，它异步执行不卡主线程，比手动监听 scroll 更高效。‌‌