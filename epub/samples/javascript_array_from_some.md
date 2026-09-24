Array.from(element).some(...) 这段代码的作用是：‌先把类数组或可迭代对象转成真正的数组，再用 .some() 判断其中是否至少有一个元素满足条件。‌ ‌‌

element 通常是 DOM 集合（如 querySelectorAll 返回的 NodeList）、arguments 或字符串等。Array.from() 负责转换，.some() 负责“存在性检查”——只要有一个元素让回调返回 true，就立刻停止遍历并返回 true，否则返回 false。‌‌

常见用法示例
‌检查表单里是否有空值‌：Array.from(inputs).some(input => input.value === '')，返回 true 就说明有未填项。
‌检查权限列表‌：Array.from(userPermissions).some(perm => perm === 'delete')，判断是否拥有某个权限。
‌检查对象数组里是否有缺货商品‌：Array.from(products).some(p => p.stock === 0)，有库存为 0 的商品就返回 true。‌‌
⚠️ 注意：.some() 对空数组永远返回 false；如果 element 本身就是数组，也可以直接写 element.some(...)，不需要先 Array.from()。另外不要在遍历过程中修改原数组，否则可能导致元素被跳过或重复检查。‌‌