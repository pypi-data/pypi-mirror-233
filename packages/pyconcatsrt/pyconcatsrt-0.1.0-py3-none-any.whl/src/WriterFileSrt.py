# -*- coding: utf-8 -*-
"""
Class in charge of giving SRT format to Dialog objects and writing them to a
final SRT file.
"""


class WriterSrt(object):

    def write(self, filename: str = None, data: str = None):
        with open(filename, 'w') as file:
            file.write(data)

    def convertData(self, data: list) -> str:
        if data != []:
            indx = 1
            string_script = ""
            for objLine in data:
                string_script += "{0}\n{1}\n{2}\n\n".format(
                    indx,
                    self.__format_timestamp(objLine),
                    self.__get_lines(objLine)
                )
                indx += 1
            return string_script
        else:
            return ''

    def __format_timestamp(self, item) -> str:
        return "{0} --> {1}".format(item.time_start, item.time_end)

    def __get_lines(self, item) -> str:
        return '\n'.join(item.dialog)
