# -*- coding: utf-8 -*-
"""
Class in charge of controlling the information workflow between ReaderSrt,
WriterSrt, ErrorData.
"""

from src.ReaderFileSrt import ReaderSrt
from src.WriterFileSrt import WriterSrt
from src.ErrorClass import ErrorData

from typing import Union


class Control(object):

    def __init__(self):
        """
        Constructor
        """
        self.path = None
        self.errors_data = []
        self.writer = WriterSrt()
        self.errorData = ErrorData()

    def read(
                self,
                path: str = None,
                paths: list = None,
                discs: int = 1
            ) -> list:
        """
        Sends `path` to ReaderSrt and returns the processed data sorted by
        start time.
        """
        result_data = []
        if path is not None:
            try:
                reader = ReaderSrt(path, discs, self.errorData)
                result_data = reader.process()
                return self.sort_by_timestamp(result_data)
            except FileNotFoundError as e:
                return e

        elif paths is not None:
            try:
                result_data = []
                for i in paths:
                    r = ReaderSrt(i.name, discs, self.errorData)
                    result_data += r.process()
                return self.sort_by_timestamp(result_data)
            except FileNotFoundError as e:
                return e

    def sort_by_timestamp(self, listLineObj: list) -> list:
        """
        Returns the list of `Dialog` objects sorted by start timestamp.
        """
        return sorted(
                listLineObj,
                key=lambda x: x.getTimestamps()['start']
            )

    def to_write(
                    self,
                    filename: str,
                    data: str = None,
                    writeLog: bool = False
                ) -> Union[bool, None]:
        """
        Writes "data" if not empty, optionally writes the generated error log.
        """
        if writeLog:
            self.write_log()
        if data != "" and data is not None:
            if not filename.endswith('.srt'):
                filename = filename + '.srt'
            self.writer.write(filename, data)
            return True
        else:
            print('>> The data is empty. File has not been written.\n')
            return None

    def write_log(self):
        """
        Writes errors to the log file.
        """
        self.errorData.writeLog()

    def convertData(self, data: list = None) -> Union[str, None]:
        """
        Converts the list of `Dialog` objects to SRT format and returns it
        in `str`.
        """
        if data != "":
            return self.writer.convertData(data)
        else:
            print('>> The data is empty.\n')
            return None
