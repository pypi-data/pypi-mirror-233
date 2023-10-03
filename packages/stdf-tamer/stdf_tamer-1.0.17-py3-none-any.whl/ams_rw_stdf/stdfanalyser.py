"""Dump stdf records to console.

accepts compressed stdf files (stdf.gz, stdf.bz2)

Usage:
  stdfanalyse <stdf_file_name_in>

Options:
  -h --help     Show this screen.
"""


import ams_rw_stdf
import construct
import construct.lib
from docopt import docopt
from rich.console import Console
from ams_rw_stdf._opener_collection import _opener
import pathlib


construct.lib.setGlobalPrintFullStrings(True)

def main():
    console = Console()
    arguments = docopt(__doc__)
    si = arguments["<stdf_file_name_in>"]
    ftype = pathlib.Path(si).suffix
    with _opener[ftype](si, "rb") as f:
        parser = ams_rw_stdf.compileable_RECORD.compile()
        while True:
             b = ams_rw_stdf.get_record_bytes(f)
             c = parser.parse(b)
             console.print(str(c))
             if c.REC_TYP == 1 and c.REC_SUB == 20:
                 break


if __name__ == '__main__':
    main()
