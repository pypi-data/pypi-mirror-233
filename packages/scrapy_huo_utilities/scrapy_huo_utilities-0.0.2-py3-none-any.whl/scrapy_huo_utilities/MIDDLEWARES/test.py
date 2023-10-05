from lxml import etree


def remove_text_tags(html_data):
    # 将html_data转换为lxml的Element对象
    root = etree.HTML(html_data)
    # 找到所有的text标签
    text_tags = root.xpath('//strong')
    for tag in text_tags:
        # 获取标签的父节点
        parent = tag.getparent()
        # 将text标签的内容插入到父节点中
        if tag.text:
            print(parent.xpath('string()'))
            print(tag.text)
            # parent.text = (parent.text or '') + tag.text
        # 移除text标签
        # parent.remove(tag)
    # 将移除text标签后的Element对象转换回字符串形式
    cleaned_html = etree.tostring(root, encoding='unicode')
    return cleaned_html


# 示例用法
html_data = '''
<html>
    <body>
        <p>这是包含标签的段落：<strong>加粗文本</strong>，<em>斜体文本</em>，<a href="https://example.com">链接</a>测试</p>
    </body>
</html>
'''

cleaned_html = remove_text_tags(html_data)
print(cleaned_html)
