一、核心 API（记忆 3 个步骤）

新建观察者
const io = new IntersectionObserver(callback, options)
告诉它要观察谁
io.observe(DOM元素)  可多次调用，一个实例可同时观察 N 个节点
用完收回
io.unobserve(元素) 或 io.disconnect()

callback 会被传入两个形参：
entries – 本次发生变化的 IntersectionObserverEntry 数组
observer – 当前观察者实例，可用于 unobserve
entry 上最常用的 3 个字段

isIntersecting 布尔值 – 是否「可  见」
intersectionRatio 0-1 – 可见比例
target – 被观察的 DOM 节点

options 3 选 1 均可省

root        默认 null（= 视口），也可指定祖先滚动容器
rootMargin  扩大/缩小触发范围，写法同 CSS margin（"50px 0"）
threshold   触发阈值，默认 0（刚碰到就触发），可写数组 [0, 0.5, 1]


二、4 个常见真实场景与可直接粘贴的示例

图片懒加载（最经典）

<img class="lazy" src="placeholder.png" data-src="real.jpg" width="400">
<img class="lazy" src="placeholder.png" data-src="real2.jpg" width="400">
<script>
const io = new IntersectionObserver((entries, ob) => {
  entries.forEach(en => {
    if (en.isIntersecting) {               // 进入视口
      const img = en.target;
      img.src = img.dataset.src;           // 换真实地址
      ob.unobserve(img);                   // 立即取消监听
    }
  });
}, { rootMargin: '100px' });               // 提前 100px 开始加载

document.querySelectorAll('img.lazy').forEach(el => io.observe(el));
</script>


无限滚动（触底加载下一页）

<ul id="list"></ul>
<li id="sentinel">加载中…</li>
<script>
let page = 1;
const io = new IntersectionObserver(([entry]) => {
  if (entry.isIntersecting) {              // 底部元素完全可见
    loadMore();                            // 请求接口
  }
}, { threshold: 1 });

function loadMore() {
  fetch(`/api/list?page=${page++}`)
    .then(r => r.json())
    .then(arr => {
      const ul = document.getElementById('list');
      arr.forEach(d => ul.insertAdjacentHTML('beforeend', `<li>${d}</li>`));
    });
}
io.observe(document.getElementById('sentinel'));
</script>


元素出现即播放动画（一次性）

css代码：

.fadeIn { opacity: 0; transform: translateY(20px); transition: .6s }
.fadeIn.show { opacity: 1; transform: translateY(0) }

<div class="fadeIn">Hello</div>
<div class="fadeIn">World</div>
<script>
const io = new IntersectionObserver((entries, ob) => {
  entries.forEach(en => {
    if (en.isIntersecting) {
      en.target.classList.add('show');
      ob.unobserve(en.target);             // 动画只需一次
    }
  });
}, { threshold: .3 });                    // 30% 可见就触发
document.querySelectorAll('.fadeIn').forEach(el => io.observe(el));
</script>


广告/组件「曝光埋点」

const io = new IntersectionObserver((entries, ob) => {
  entries.forEach(en => {
    if (en.isIntersecting && en.intersectionRatio >= 1) {
      // 整卡完全可见，只发一次
      gtag('event', 'ad_impression', { element: en.target.dataset.id });
      ob.unobserve(en.target);
    }
  });
}, { threshold: 1 });

document.querySelectorAll('.ad-card').forEach(card => io.observe(card));

三、易踩小坑 & 性能提示

观察器实例可以复用，不要给每个元素 new 一个
回调里不要做重计算/同步 IO，必要时用 requestIdleCallback 延后
节点移除后记得 unobserve，SPA 切换页时记得 disconnect() 防止泄漏
旧版浏览器（IE）需加载 polyfill（github.com/w3c/IntersectionObserver）
若滚动容器不是 window，记得把 root 指向那个「可滚动祖先」



作者：旺仔牛仔QQ糖
链接：https://juejin.cn/post/7562359784278360106
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
