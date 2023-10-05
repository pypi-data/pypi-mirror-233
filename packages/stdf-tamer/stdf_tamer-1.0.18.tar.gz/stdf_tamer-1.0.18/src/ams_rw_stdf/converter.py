"""
Usage:
  stdfconvert --output=<output> --stdf-in=<stdf-in> [--compression=<zstd>] [--add-site] [--add-head]

  Without the optional 'file_formats' dependancy only pickle files can be generated.

Options:
  -h --help     Show this screen.
"""
import ams_rw_stdf
import bz2
import construct
from docopt import docopt
import gzip
import pathlib
import ams_rw_stdf._output_workers as _output_workers
from ams_rw_stdf._opener_collection import _opener
from ams_rw_stdf.version import version
from ams_rw_stdf.convdir import work_todo


output_writers = {".pickle": _output_workers.write_pickle}

try:
    import polars as pl
    
    output_writers[".ipc"] =     _output_workers.write_ipc
    output_writers[".feather"] = _output_workers.write_ipc
    output_writers[".parquet"] = _output_workers.write_parquet
    output_writers[".xlsx"] =    _output_workers.write_xlsx

except:
    pass

import collections
import time
import sys
import threading
import queue
import lzma
from rich.progress import Progress
from rich.console import Console


console = Console()
err_console = Console(stderr=True, style="bold red")
    

def main():
    start_time = time.time()
    try:
        arguments = docopt(__doc__)
        outpath = pathlib.Path(arguments["--output"])
        si = arguments["--stdf-in"]
        ftype = pathlib.Path(si).suffix

        console.print(f"stdf-tamer ({version})")
        console.print(f"converting from: [yellow]{pathlib.Path(si).name}[not yellow] to: [yellow]{pathlib.Path(outpath).name}[not yellow]\n\n", highlight=False)

        if ftype not in _opener:
            err_console.print(f"{ftype} is an unsupported file extension, only *.{', *.'.join(_opener.keys())} are supported")
            sys.exit(1)
        try:
            writer = output_writers[outpath.suffix]
        except KeyError:
            err_console.print(f"please use one of these file formats as output: *{', *'.join(output_writers.keys())}")
            err_console.print("""
The optional dependency group 'file_formats' adds additional file formats, like xlsx, feather and ipd.

These optional dependencies are less portable than stdf-tamer itself and may not be available on pypy or legacy python versions.""")
            sys.exit(1)
    
        try:
            pathlib.Path(outpath).unlink(missing_ok=False)
            console.print(f"{outpath} has been cleared")
        except FileNotFoundError as e:
            pass
        except TypeError:
            pass #pre 3.8

        work_todo([(si, bool(arguments["--add-site"]), bool(arguments["--add-head"]), outpath, arguments["--compression"], outpath.suffix[1:],)],
                  parse_stdf_message="\n[bold]Parsing stdf file[no bold]", 
                  flush_results=f"\n[bold]writing result[no bold]")
        
        runtime = time.time()-start_time
        console.print(f"conversion complete. Took {runtime:0.3f} s, succesfully written {outpath}")
    except Exception as e:
        err_console.print_exception()


if __name__ == "__main__":
    main()
