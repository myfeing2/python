offsetParent 返回的是当前元素‌最近的已定位祖先元素‌（position 不为 static），用于计算 offsetTop 和 offsetLeft 的参照基准。‌‌

具体规则
‌有定位祖先‌：返回离自己最近的 position 为 relative、absolute 或 fixed 的祖先元素。
‌无定位祖先‌：返回 <body> 元素。
‌元素自身是 fixed‌：返回 null（Firefox 除外，它返回 <body>）。
‌<body> 元素本身‌：返回 null。
‌元素或其祖先 display: none‌：返回 null。‌‌
需要注意：offsetParent 只认定位祖先，不认普通父节点，这点和 parentNode 不同。‌‌

实际用途
配合 offsetTop / offsetLeft 获取元素相对定位父级的偏移。
循环累加每一层的 offsetTop 和 offsetLeft，可以算出元素在页面上的绝对位置。‌‌
