给元素添加自定义属性，常用的有两种方式：setAttribute() 和 dataset。setAttribute() 更通用，dataset 专门处理 data-* 属性，写法更简洁。‌

🛠️ setAttribute 方法
‌添加/修改属性‌：element.setAttribute('属性名', '属性值')，属性已存在就更新，不存在就新建。
‌获取属性值‌：用 element.getAttribute('属性名')。
‌删除属性‌：用 element.removeAttribute('属性名')。‌
javascript
// 给 div 添加自定义属性 data-id
let div = document.getElementById('myDiv');
div.setAttribute('data-id', '123');
🧩 dataset 方法（推荐）
dataset 是专门操作 data-* 属性的现代方式，代码更简洁。‌

‌设置属性‌：element.dataset.属性名 = '值'，会自动生成对应的 data-* 属性。
‌获取属性值‌：直接 element.dataset.属性名。
‌删除属性‌：用 delete element.dataset.属性名。‌
javascript
// 设置 data-user-id 属性
div.dataset.userId = '123';  // HTML 中显示为 data-user-id="123"

// 读取
console.log(div.dataset.userId);  // 输出 "123"
⚠️ 注意事项
dataset 的命名规则是‌全小写加连字符‌，比如 data-user-id，访问时自动转成驼峰 userId；如果用 data-userId 或 data_user_id，浏览器会直接忽略，dataset 读不到。
dataset 取出来的值‌永远是字符串‌，数字或布尔值需要手动转换，比如 Number(el.dataset.count)。
如果属性名带下划线、数字开头，或者需要动态 key，直接用 getAttribute 更稳妥。‌
实际开发中存对象数据时，可以先 JSON.stringify 再存，取出来再 JSON.parse。‌