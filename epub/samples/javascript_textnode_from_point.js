const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
elements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, dt, dd, blockquote, td, th, span, div')
for (const el of elements) {
    const rect = el.getBoundingClientRect();
    const style = window.getComputedStyle(el);

    // 过滤不可见元素：尺寸为0、display:none、visibility:hidden
    const text = el.innerText?.trim();
    if (!text) continue;
    if (el.offsetParent === null) continue; 
    if (rect.width === 0 || rect.height === 0) continue;
    if (style.display === 'none' || style.visibility === 'hidden') continue;

    // 判断是否在视口内（任意部分可见就算）
    //const x = rect.left + rect.width / 2;
    //const y = rect.top + rect.height / 2;
    const x = rect.left
    const y = rect.top
    el_in_view = document.elementFromPoint(x, y);
    if (el_in_view) console.log(el_in_view);
}
