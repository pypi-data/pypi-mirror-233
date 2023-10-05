import base64
import os


class Metadata():
    def __init__(self, metadata: dict):
        """Metadata object

        Args:
            metadata (dict): epub metadata
        """
        self.__metadata = metadata

    def __repr__(self) -> str:
        return str(self.__metadata)

    @property
    def version(self) -> str:
        """get epub version

        Returns:
            str: epub version
        """
        return self.__metadata['version']

    @property
    def title(self) -> str:
        """get epub title

        Returns:
            str: epub title
        """
        return self.__metadata['title']

    @property
    def creator(self) -> str:
        """get epub creator(author)

        Returns:
            str: epub creator(author)
        """
        return self.__metadata['creator']

    @property
    def date(self) -> str:
        """get epub public date

        Returns:
            str: epub public date
        """
        return self.__metadata['date']

    @property
    def cover(self) -> str:
        """get epub cover base64

        Returns:
            str: epub cover base64
        """
        return self.__metadata['cover']

    @property
    def cover_type(self) -> str:
        """get epub cover type

        Returns:
            str: epub cover type
        """
        return self.__metadata['cover_type']

    @property
    def description(self) -> str:
        """get epub description

        Returns:
            str: epub description
        """
        return self.__metadata['description']

    @property
    def publisher(self) -> str:
        """get epub publisher

        Returns:
            str: epub publisher
        """
        return self.__metadata['publisher']

    @property
    def identifier(self) -> str:
        """get epub identifier

        Returns:
            str: epub identifier
        """
        return self.__metadata['identifier']
