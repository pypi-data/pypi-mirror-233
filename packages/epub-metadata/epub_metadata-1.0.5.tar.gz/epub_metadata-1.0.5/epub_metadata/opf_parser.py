import base64
import os
from urllib.parse import unquote
from xml.dom import minicompat, minidom

import arrow


class OpfParser():
    def __init__(self, opf_doc: minidom.Document, opf_path: str):
        self.opf_doc = opf_doc
        self.opf_path = opf_path

    def __tag_filter(self, tag: str, attr: str, value: str) -> minidom.Element:
        for element in self.opf_doc.getElementsByTagName(tag):
            element: minidom.Element
            if attr in element.attributes.keys() and element.attributes[attr].value == value:
                return element

    def __dc_filter(self, dc_type: str) -> minicompat.NodeList[minidom.Element]:
        return self.opf_doc.getElementsByTagName(f'dc:{dc_type}')

    def version(self) -> str:
        """parser version from opf file

        Returns:
            str: version
        """
        return self.opf_doc.getElementsByTagName('package')[0].attributes['version'].value

    def title(self) -> str:
        """parser title from opf file

        Returns:
            str: title
        """
        elements = self.__dc_filter('title')
        if any(elements) == False:
            return ''
        return elements[0].firstChild.data

    def creator(self) -> str:
        """parser creator from opf file

        Returns:
            str: creator
        """
        element = self.__dc_filter('creator')
        if any(element) == False:
            return ''
        return element[0].firstChild.data

    def date(self) -> str:
        """parser public date from opf file

        Returns:
            str: public date
        """
        elements = self.__dc_filter('date')
        if any(elements) == False:
            return ''
        date: str = elements[0].firstChild.data
        try:
            data = arrow.get(date).format('YYYY-MM-DD')
        except arrow.ParserError:
            data = arrow.get(date.split(' ')[0]).format('YYYY-MM-DD')
        return data

    def description(self) -> str:
        """parser description from opf file

        Returns:
            str: description
        """
        elements = self.__dc_filter('description')
        if any(elements) == False:
            return ''
        if elements[0].firstChild == None:
            return ''
        return elements[0].firstChild.data

    def publisher(self) -> str:
        """parser publisher from opf file

        Returns:
            str: publisher
        """
        elements = self.__dc_filter('publisher')
        if any(elements) == False:
            return ''
        return elements[0].firstChild.data

    def identifier(self) -> str:
        """parser identifier from opf file

        Returns:
            str: identifier
        """
        elements = self.__dc_filter('identifier')
        if any(elements) == False:
            return ''
        if elements[0].firstChild == None:
            return ''
        return elements[0].firstChild.data

    def cover(self) -> tuple[str]:
        """parser cover from opf file

        Returns:
            tuple[str]: cover base64 str and cover type
        """
        meta_element = self.__tag_filter('meta', 'name', 'cover')
        if meta_element == None or 'content' not in meta_element.attributes.keys():
            return ('', '')
        item_id = meta_element.attributes['content'].value
        item_element = self.__tag_filter('item', 'id', item_id)
        if item_element == None or 'href' not in item_element.attributes.keys():
            return ('', '')
        cover_path = os.path.join(os.path.dirname(
            self.opf_path), unquote(item_element.attributes['href'].value))
        cover_type = item_element.attributes['media-type'].value
        with open(cover_path, 'rb') as f:
            cover_data = base64.b64encode(f.read())
            return (cover_data.decode('utf-8'), cover_type)
