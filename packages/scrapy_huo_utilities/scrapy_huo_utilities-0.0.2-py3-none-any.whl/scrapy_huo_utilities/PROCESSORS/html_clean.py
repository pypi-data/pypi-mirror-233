def clean_html_attributes(html_data, whitelist):
    '''
    用于清除HTML标签中的属性，除了白名单中包含的属性。
    :param html_data:传入html
    :param whitelist:白名单
    :return: html_data处理后的html
    '''
    # 将html_data转换为lxml的Element对象
    root = etree.HTML(html_data)
    # 遍历所有标签
    for element in root.iter("*"):
        # 将_attrib对象转换为字典
        attributes = dict(element.attrib)
        # 清除标签的所有属性，除了白名单中包含的属性
        for attribute in attributes:
            if attribute not in whitelist:
                del element.attrib[attribute]
    # 将清除属性后的Element对象转换回字符串形式
    cleaned_html = etree.tostring(root, method="html", encoding='unicode')
    return cleaned_html.replace('<body>', '').replace('</body>', '').replace('<html>', '').replace('</html>', '')


def clean_html_tags(html_data, remove_tags, reserve_content=True):
    '''
    用于清除指定列表中的HTML标签。
    :param html_data:
    :param remove_tags:删除标签列表
    :param reserve_content:是否保留删除标签的文本内容，默认保留。
    :return: 处理后的html
    '''
    # 将html_data转换为lxml的Element对象
    root = etree.HTML(html_data)

    # 找到所有要清除的标签
    for tag in remove_tags:
        tags_to_remove = root.xpath(f'//{tag}')
        for tag in tags_to_remove:
            # 获取标签的文本
            text = etree.tostring(tag, method='text', encoding='unicode')
            # 获取标签的内容
            content = tag.xpath('string()')
            # 创建一个新的文本节点，并将内容赋值给它
            text_node = etree.Element("text")
            text_node.text = content
            # 将新的文本节点插入到标签之前
            tag.addprevious(text_node)
            # 移除标签
            tag.getparent().remove(tag)
        # 将清除标签后的Element对象转换回字符串形式
    cleaned_html = etree.tostring(root, method="html", encoding='unicode')
    if reserve_content:
        return cleaned_html.replace('<text>', '').replace('</text>', '').replace('<body>', '').replace('</body>', '').replace('<html>', '').replace('</html>', '')
    else:
        return cleaned_html.replace('<body>', '').replace('</body>', '').replace('<html>', '').replace('</html>', '')


def clean_empty_img_tags(html_data):
    '''
    清除没有src属性或src属性为空字符串的img标签
    :param html_data:
    :return:
    '''
    # 将html_data转换为lxml的Element对象
    root = etree.HTML(html_data)
    # 找到所有空的img标签
    empty_img_tags = root.xpath('//img[not(@src) or @src=""]')
    for img_tag in empty_img_tags:
        # 移除空的img标签
        img_tag.getparent().remove(img_tag)
    # 将清除标签后的Element对象转换回字符串形式
    cleaned_html = etree.tostring(root, method="html", encoding='unicode')
    return cleaned_html.replace('<body>', '').replace('</body>', '').replace('<html>', '').replace('</html>', '')


from lxml import etree


def clean_empty_a_tags(html_data):
    '''
    清除没有href属性或href属性为空字符串的a标签
    :param html_data:
    :return:
    '''
    # 将html_data转换为lxml的Element对象
    root = etree.HTML(html_data)
    # 找到所有空的a标签
    empty_a_tags = root.xpath('//a[not(@href) or @href=""]')
    for a_tag in empty_a_tags:
        # 移除空的a标签
        a_tag.getparent().remove(a_tag)
    # 将清除标签后的Element对象转换回字符串形式
    cleaned_html = etree.tostring(root, method="html", encoding='unicode')
    return cleaned_html.replace('<body>', '').replace('</body>', '').replace('<html>', '').replace('</html>', '')
if __name__ == '__main__':
    html_data ='<div>Hello, World!</div>'
    print(clean_empty_a_tags(html_data))