const walker = document.createTreeWalker(
  document.body,      // root：遍历的根节点
  NodeFilter.SHOW_ELEMENT,  // whatToShow：要看的节点类型（位掩码）
  {                    // filter：可选，自定义过滤规则
    acceptNode(node) {
      return node.classList.contains('highlight')
        ? NodeFilter.FILTER_ACCEPT
        : NodeFilter.FILTER_SKIP;
    }
  },
  false                // entityReferenceExpansion：现代浏览器基本忽略
);

/*
  🔍 关键概念
‌whatToShow 位掩码‌：控制要暴露的节点类型。默认只显示元素节点，可以用 NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT 组合来同时处理元素和文本。
‌过滤器三种返回值‌：
FILTER_ACCEPT（1）：接受该节点，包含在结果中
FILTER_REJECT（2）：拒绝该节点‌及其所有子节点‌
FILTER_SKIP（3）：跳过该节点，但‌继续遍历其子节点‌
‌游标式遍历‌：通过 nextNode() / previousNode() 在节点间移动，而不是一次性返回所有节点，可以随时中断。‌‌
*/

/*
  收集所有可见文本节点‌（跳过隐藏元素）：‌‌
*/

const walker = document.createTreeWalker(
  document.body,
  NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
  {
    acceptNode(node) {
      if (node.nodeType === Node.ELEMENT_NODE) {
        const style = window.getComputedStyle(node);
        if (style.display === 'none' || style.visibility === 'hidden') {
          return NodeFilter.FILTER_REJECT; // 跳过整个子树
        }
      }
      return NodeFilter.FILTER_ACCEPT;
    }
  }
);

const textNodes = [];
let current;
while (current = walker.nextNode()) {
  if (current.nodeType === Node.TEXT_NODE && current.textContent.trim()) {
    textNodes.push(current.textContent.trim());
  }
}

/*
  查找特定元素‌（如所有带 data-role 且未禁用的按钮）：‌‌
*/

const walker = document.createTreeWalker(
  document.body,
  NodeFilter.SHOW_ELEMENT,
  {
    acceptNode(node) {
      return node.matches('button:not([disabled]):is([data-role])')
        ? NodeFilter.FILTER_ACCEPT
        : NodeFilter.FILTER_SKIP;
    }
  }
);

/*⚠️ 注意事项
‌不要用 className.includes() 代替 classList.contains()‌，会误匹配 class="button" 之类的情况。
‌不要在 acceptNode 里做高开销操作‌（如 getComputedStyle），每个节点都会调用它，建议缓存结果。
‌不要用异步操作或修改 DOM‌，TreeWalker 不支持异步回调，修改结构可能导致跳过或重复遍历。
‌注意 currentNode 属性‌：可以手动赋值来“跳转”到任意兼容节点，实现非线性遍历；节点被移出 DOM 后需自行判断是否仍在文档中（node.isConnected）。‌‌
*/
