import os
import tempfile
import zipfile as zf
from xml.dom import minidom

from .metadata import Metadata
from .opf_parser import OpfParser


class epub(OpfParser):
    def __init__(self, epub_filepath: str):
        self.epub_filepath = epub_filepath

    def __unzip(self, tempdir: str) -> None:
        """unzip epub file to tempdir

        Args:
            tempdir (str): tempdir
        """
        zipfile = zf.ZipFile(self.epub_filepath)
        for names in zipfile.namelist():
            zipfile.extract(names, tempdir)

    def __opf_path(self, container_xml_path: str) -> str:
        """get .opf path from container.xml

        Args:
            container_xml_path (str): container.xml path

        Returns:
            str: .opf path
        """
        container_doc: minidom.Document = minidom.parse(
            container_xml_path)
        opf_path = container_doc.getElementsByTagName(
            'rootfile')[0].attributes['full-path'].value
        return opf_path

    @property
    def filename(self) -> str:
        """return filename not include extension name

        Returns:
            str: filename
        """
        filename = os.path.basename(self.epub_filepath).replace('.epub', '')
        return filename

    @property
    def metadata(self) -> Metadata:
        """get metadata

        Returns:
            Metadata: metadata object
        """
        with tempfile.TemporaryDirectory(prefix='epub_') as tempdir:
            self.__unzip(tempdir)
            container_xml_path = os.path.join(
                tempdir, 'META-INF', 'container.xml')
            opf_filepath = os.path.join(
                tempdir, self.__opf_path(container_xml_path))
            opf_doc: minidom.Document = minidom.parse(opf_filepath)
            super().__init__(opf_doc, opf_filepath)
            cover_base64, cover_type = self.cover()
            _metadata = {
                'version': self.version(),
                'title': self.title(),
                'creator': self.creator(),
                'date': self.date(),
                'cover': cover_base64,
                'cover_type': cover_type,
                'description': self.description(),
                'publisher': self.publisher(),
                'identifier': self.identifier(),
            }
            return Metadata(_metadata)
