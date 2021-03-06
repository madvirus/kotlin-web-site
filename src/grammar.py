import os
import os.path as path
from xml.etree.ElementTree import ElementTree

from src.markdown.makrdown import customized_markdown


def _get_description(node):
    description = {
        'type': 'description',
        'content': []
    }
    for children in node:
        token = {}

        if children.tag == 'whiteSpace':
            token['type'] = 'whitespace'
            token['content'] = children.text
        elif children.tag == 'identifier':
            token['type'] = 'identifier'
            token['name'] = children.attrib['name']
        elif children.tag == 'string' or children.tag == 'symbol' or children.tag == 'other':
            token['type'] = children.tag
            token['content'] = children.text

            if children.tag == 'string':
                token['content'] = token['content'].replace('<', '&lt;').replace('>', '&gt;')
        elif 'crlf':
            token['type'] = 'crlf'

        description['content'].append(token)
    return description


def _get_declaration(node):
    declaration = {
        'type': 'declaration',
        'name': node.attrib['name'],
        'usages': []
    }

    for usage in node.findall('usages'):
        for children in usage:
            declaration['usages'].append({
                'name': children.text
            })
    return declaration


def _get_item_content(node):
    item = {
        'type': 'item',
        'content': []
    }
    for children in node:
        if children.tag == 'annotation':
            item['content'].append({
                'type': 'annotation',
                'content': children.text
            })
        elif children.tag == 'declaration':
            item['content'].append(_get_declaration(children))
        elif children.tag == 'description':
            item['content'].append(_get_description(children))
    return item


def get_grammar():
    data = []
    grammar_file = path.join(path.dirname(path.dirname(__file__)), 'grammar.xml')
    print(grammar_file)
    if not os.path.isfile(grammar_file):
        return None
    grammar_xml = ElementTree(file=grammar_file).getroot()
    for grammar_set in grammar_xml:
        set = {
            'file-name': grammar_set.attrib['file-name'],
            'content': []
        }
        for node in grammar_set:
            if node.tag == 'doc':
                set['content'].append({
                    'type': 'comment',
                    'content': customized_markdown(node.text)
                })
            elif node.tag == 'item':
                set['content'].append(_get_item_content(node))
        data.append(set)
    return data


def get_grammar_ko():
    data = []
    grammar_file = path.join(path.dirname(path.dirname(__file__)), 'grammar_ko.xml')
    if not os.path.isfile(grammar_file):
        return None
    grammar_xml = ElementTree(file=grammar_file).getroot()
    for grammar_set in grammar_xml:
        set = {
            'file-name': grammar_set.attrib['file-name'],
            'content': []
        }
        for node in grammar_set:
            if node.tag == 'doc':
                set['content'].append({
                    'type': 'comment',
                    'content': customized_markdown(node.text)
                })
            elif node.tag == 'item':
                set['content'].append(_get_item_content(node))
        data.append(set)
    return data
