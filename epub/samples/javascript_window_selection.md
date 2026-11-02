window.getSelection() 返回一个 ‌Selection 对象‌，代表用户当前选中的文本区域或光标位置。它主要包含以下只读属性和操作方法：‌‌

📌 核心属性（全部只读）
‌anchorNode / anchorOffset‌：选区的起点节点，以及起点在该节点中的偏移量。
‌focusNode / focusOffset‌：选区的终点节点，以及终点在该节点中的偏移量。
‌baseNode / baseOffset‌：与 anchorNode/anchorOffset 一致（旧版别名）。
‌extentNode / extentOffset‌：与 focusNode/focusOffset 一致（旧版别名）。
‌isCollapsed‌：布尔值，表示起点和终点是否重合。为 true 时说明当前只是光标插入点，没有选中内容。
‌rangeCount‌：选区中包含的 Range 对象数量。多数浏览器下为 1，无选区时为 0。
‌type‌：当前选区的类型，可能是 None（无选区）、Caret（仅光标）或 Range（选中了范围）。‌‌
🛠️ 常用方法
‌getRangeAt(index)‌：按索引获取选区中的 Range 对象，一般用 getRangeAt(0) 取第一个。
‌toString()‌：返回选区的纯文本内容，这是最常用的方法。没选中内容时返回空字符串，不会报错。
‌collapse(node, offset)‌：将选区折叠成一个点（即把起点和终点合并到指定位置），常用于移动光标。
‌extend(node, offset)‌：将选区的终点移动到指定位置，从而扩展或缩小选区。
‌modify(alter, direction, granularity)‌：按字符、单词、段落等粒度移动或扩展选区，如 selection.modify('extend', 'forward', 'word')。
‌collapseToStart() / collapseToEnd()‌：将选区折叠到起点或终点位置，相当于取消选中但保留光标位置。
‌selectAllChildren(node)‌：清除现有选区，并选中指定节点的所有子节点。
‌addRange(range) / removeRange(range) / removeAllRanges()‌：向选区添加、移除或清空 Range 对象。removeAllRanges() 常用于取消选中状态。
‌deleteFromDocument()‌：直接从页面中删除选中的内容。
‌containsNode(node, isPartiallyContained)‌：判断某个节点是否属于当前选区，第二个参数控制是否允许部分包含。
‌selectionLanguageChange()‌：在键盘方向改变时调整 BiDi 优先级，日常开发很少用到。
‌setBaseAndExtent(anchorNode, anchorOffset, focusNode, focusOffset)‌：直接用起止节点和偏移量设置选区范围，适合精确控制。‌‌
⚠️ 需要注意：getSelection() 本身是只读的，它只能“获取”选区。要‌主动设置‌选区，通常得配合 document.createRange() 创建 Range，再用 addRange() 或 selectAllChildren() 等方式应用。‌‌

📝 实用提醒
‌获取选中文本‌：const text = window.getSelection().toString(); 是最常用写法。
‌监听变化‌：用 document.addEventListener('selectionchange',...) 来实时响应选区变化，比在 mouseup 里取更可靠。
‌无选区情况‌：调用 getSelection() 不会返回 null，但 rangeCount === 0，此时调用 getRangeAt(0) 会报错，记得先判断。
‌反向选择‌：从后往前拖选时，anchor 和 focus 的顺序会颠倒，所以别假设 anchorNode 一定在文本前面。
‌跨 iframe‌：在 iframe 内获取选区，必须在对应 iframe 的 contentWindow 上调用，且要求同源