from abc import ABC

"""
This file declares the collections of file processors with different implementations of objects being processed
"""


class FileProcessor(ABC):

    """
    FileProcessor defines the basic methods of processing between object and csv file
    """

    def read_file_to_object(self, filename: str) -> list[any]:
        """
        Read the csv file and create a list of objects
        :param filename: csv file name to read
        :return: list of objects by implementation
        """
        pass

    def write_object_to_file(self, objects: list[any], filename: str):
        """
        Write a list of objects into rows of csv files
        :param objects: list of objects to write
        :param filename: csv file name to write
        """
        pass

    def _object_to_csv_row(self, obj: any) -> str:
        """
        Convert object to csv row
        :param obj: object to convert
        :return: csv row data
        """
        pass

    def _csv_row_to_object(self, csv_row: str) -> any:
        """
        Load csv row data to object
        :param csv_row: csv row data to be loaded
        :return: object by implementation
        """
        pass
