判断一个节点是否为文本节点，最可靠的方法是检查它的 nodeType 属性是否等于 3。‌‌

javascript
// 判断单个节点是否是文本节点
function isTextNode(node) {
    return node.nodeType === 3;
}

// 使用示例：检查某个元素下是否包含文本节点
const container = document.getElementById('container');
const hasTextNode = Array.from(container.childNodes).some(node => node.nodeType === 3);
📝 关键要点
‌标准判断方式‌：使用 nodeType === 3 判断文本节点，兼容性最好，跨 iframe 也稳定。
‌辅助验证‌：可以结合 nodeName === "#text" 双重确认，调试时更直观。
‌注意事项‌：元素节点 nodeType 为 1，注释节点为 8；用 childNodes 获取子节点时会包含文本节点（比如换行、空格），这点需要留意。‌‌
想获取元素下的纯文本，可以用 textContent；但要注意，空格和换行符也会生成文本节点，不是空白内容就不算。

在 JavaScript 中，获取文本节点（Text Node）的内容主要有以下几种方式，具体取决于你是在操作‌纯文本节点对象‌，还是想从‌元素节点‌中提取文本。

1. 直接操作文本节点对象
如果你已经通过 childNodes、firstChild 等方式获取到了一个具体的文本节点对象（其 nodeType === 3），可以使用以下属性获取内容：

‌nodeValue‌：这是最标准的方法，用于获取或设置节点的值。对于文本节点，它返回包含的字符串。
‌data‌：这是 CharacterData 接口提供的属性，功能与 nodeValue 完全相同，通常更语义化地表示“数据”。
‌wholeText‌：如果相邻的文本节点被合并或分割，此属性可以返回逻辑上相连的所有文本内容（较少用，主要用于处理复杂的 DOM 结构）。
javascript
// 假设有一个元素 <p id="demo">Hello World</p>
const p = document.getElementById('demo');
const textNode = p.firstChild; // 获取第一个子节点（即文本节点）

if (textNode.nodeType === 3) {
    console.log(textNode.nodeValue); // 输出: "Hello World"
    console.log(textNode.data);      // 输出: "Hello World"
}
2. 从元素节点获取文本内容
如果你拥有一个元素节点（如 div, span），并想获取其内部的所有文本，通常不直接遍历子节点，而是使用以下属性：

‌textContent‌（✅ ‌推荐‌）：

获取元素及其所有后代节点的‌纯文本内容‌。
‌优点‌：性能好（不触发布局重算），安全（不解析 HTML，防 XSS），符合 W3C 标准。
‌注意‌：它会保留源码中的空格和换行符。
‌innerText‌：

获取用户‌视觉上可见‌的文本内容。
‌特点‌：受 CSS 样式影响（如 display: none 的元素文本不会被获取），会自动折叠空白符，可能触发布局重算（性能略低）。
‌场景‌：当你需要模拟用户复制粘贴看到的文本时使用。
‌innerHTML‌：

获取包含 HTML 标签的字符串。
‌注意‌：如果你只需要文本，‌不要‌使用它，因为它包含标签且存在 XSS 风险。
javascript
const container = document.getElementById('container');

// 推荐方式：获取纯文本
const text = container.textContent; 
console.log(text);

// 特定场景：获取可见文本
const visibleText = container.innerText;
console.log(visibleText);
3. 精确筛选直接子级文本节点
如果你想忽略子元素中的文本，只获取‌直接属于当前元素‌的文本节点（例如处理混合内容 <p>Hello <b>World</b>!</p> 中的 "Hello " 和 "!"），可以结合 childNodes 和 nodeType 进行过滤：

javascript
const p = document.querySelector('p');
// 过滤出所有直接子节点中的文本节点
const directTextNodes = Array.from(p.childNodes).filter(node => node.nodeType === 3);

// 提取内容并拼接（通常需要 trim 去除换行和缩进带来的空白）
const result = directTextNodes.map(node => node.nodeValue.trim()).join('');
console.log(result); // 输出: "Hello!" (假设中间<b>标签隔开了)
总结建议
表格
场景	推荐方法	说明
‌通用获取元素文本‌	element.textContent	性能最好，最安全，标准做法。
‌获取用户可见文本‌	element.innerText	考虑 CSS 隐藏状态，贴近用户视觉。
‌操作具体文本节点‌	node.nodeValue 或 node.data	当你已持有 Text 节点对象时使用。
‌获取表单输入值‌	input.value	<input> 和 <textarea> 不使用上述属性，需用 value。
‌注意事项‌：

XML/HTML 中的换行、缩进和空格也会生成文本节点。使用 childNodes 遍历时，务必检查 nodeType === 3 并可能需要使用 .trim() 清理空白。
避免使用正则表达式直接从 HTML 字符串中提取文本，因为无法正确处理嵌套标签、实体编码和 CDATA。