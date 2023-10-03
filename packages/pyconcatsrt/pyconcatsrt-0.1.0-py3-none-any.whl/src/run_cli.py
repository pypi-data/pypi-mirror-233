# -*- coding: utf-8 -*-
"""
Run command line interface of PyConcatSRT.
"""

import os
import sys
import argparse


def main():
    sys.path.append('.')

    parser = argparse.ArgumentParser(
                    prog='concatsrt',
                    description='Concatenate SRT files.',
                    epilog='Easy way of concatenate multiples files Srt.'
                )
    parser.add_argument(
        '-p',
        '--path',
        type=str,
        help='set path of file or directory.',
        required=True
    )
    parser.add_argument(
        '-d',
        '--discs',
        type=int,
        help='set number of discs, default = 1.'
    )
    parser.add_argument(
        '-l',
        '--log',
        type=str,
        help='writes a log file with problem files, default = no.'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='final SRT file.'
    )

    args = parser.parse_args()

    path = args.path
    output = args.output
    discs = args.discs
    log = args.log

    if path is not None:
        if os.path.exists(path):
            write = False
            if discs is None:
                discs = 1
            if log is None:
                write = False
            else:
                if log.lower() == 'yes':
                    write = True
            if output is None:
                output = 'final_srt.srt'
            else:
                if not output.endswith('.srt'):
                    output += '.srt'

            from src.Controller import Control
            control = Control()
            read_data = control.read(path, discs)
            if read_data != []:
                data = control.convertData(read_data)
                control.to_write(output, data, writeLog=write)

        else:
            print(f'--> {path} <-- not exists.\n')


if __name__ == '__main__':
    main()
