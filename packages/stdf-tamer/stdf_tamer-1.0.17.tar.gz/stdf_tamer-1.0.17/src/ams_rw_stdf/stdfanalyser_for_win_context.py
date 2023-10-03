"""Dump stdf records to console.

accepts compressed stdf files (*.stdf, *.stdf.gz, *.stdf.bz2, *.stdf.xz)

Usage:
  stdfanalyser_for_win_context <stdf_file_name_in>

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
from ams_rw_stdf.version import version
from rich.console import Console
from rich.progress import Progress
import pathlib


console = Console()
err_console = Console(stderr=True, style="bold red")
construct.lib.setGlobalPrintFullStrings(True)

def main():
    console = Console()
    arguments = docopt(__doc__)
    si = arguments["<stdf_file_name_in>"]
    ftype = pathlib.Path(si).suffix
    found_end = False
    console.print(f"stdf-tamer ({version})")
    console.print(f"dumping records from: [yellow]{pathlib.Path(si).name}[not yellow]\n\n", highlight=False)
    with Progress() as progress:
        pathlib
        with _opener[ftype](si, "rb") as f:
            parser = ams_rw_stdf.compileable_RECORD.compile()

            outfile = pathlib.Path(si + ".dump.txt")
            if outfile.exists():
                err_console.print("There is already a dump file. Not going to overwrite!")
                input("")
                return 1

            progress_Task = None 
            progress_tranche = 1000000
            working_progress_tranche = progress_tranche
            progressbarname = f"[yellow]converting {progress_tranche} entries:"

            progress_Task = progress.add_task(progressbarname, total=progress_tranche)

            with open(outfile, "w") as of:
                while True:
                    b = ams_rw_stdf.get_record_bytes(f)
                    c = parser.parse(b)
                    of.write(str(c))

                    progress.update(progress_Task, advance=1)
                    if c.REC_TYP == 1 and c.REC_SUB == 20:
                        found_end = True
                        break
                    working_progress_tranche -= 1
                    
                    if working_progress_tranche <= 0:
                        progress_Task = progress.add_task(progressbarname, total=progress_tranche)
                        working_progress_tranche = progress_tranche
    if found_end:
        console.print("found 1/20 record. STDF file ends here...")
        input("")
    else:
        err_console.print("unexpected end of stdf file!")
                        


if __name__ == '__main__':
    main()
