"""convert the pickle which was created by stdf tamers stdfconvert to a more helpful format.

Usage:
  pickleconvert --output=<output> --pickle-in=<pickle-in> [--compression=<zstd>]

This is useful when the conversion from stdf files was donne with pypy for speed.

Options:
  -h --help     Show this screen.
"""
import ams_rw_stdf._output_workers as _output_workers
import time
from rich.console import Console
from docopt import docopt
import pathlib
import sys
from ams_rw_stdf.version import version


console = Console()
err_console = Console(stderr=True, style="bold red")


output_writers = {}
output_writers[".ipc"] =     _output_workers.write_ipc
output_writers[".feather"] = _output_workers.write_ipc
output_writers[".parquet"] = _output_workers.write_parquet
output_writers[".xlsx"] =    _output_workers.write_xlsx


def main():
    start_time = time.time()
    try:
        arguments = docopt(__doc__)
        outpath = pathlib.Path(arguments["--output"])
        si = arguments["--pickle-in"]
        ftype = pathlib.Path(si).suffix

        console.print(f"stdf-tamer ({version})")
        console.print(f"converting pickles from: [yellow]{pathlib.Path(si).name}[not yellow] to: [yellow]{pathlib.Path(outpath).name}[not yellow]\n\n", highlight=False)

        if ftype not in {"pickle"}:
            err_console.print(f"{ftype} is an unsupported file extension, only *.pickle is supported")
            sys.exit(1)
        try:
            writer = output_writers[outpath.suffix]
        except KeyError:
            err_console.print(f"please use one of these file formats as output: *{', *'.join(output_writers.keys())}")
            err_console.print("""
The optional dependency group 'file_formats' adds additional file formats, like xlsx, feather and ipd.

These optional dependencies are less portable than stdf-tamer itself and are notably not available on python < 3.8.""")
            sys.exit(1)
    
        try:
            pathlib.Path(outpath).unlink(missing_ok=False)
            console.print(f"{outpath} has been cleared")
        except FileNotFoundError as e:
            pass

        
        with console.status("conversion is taking place...", spinner="runner"):
            data_generator = _output_workers.pickle_worker(si)
            writer(outpath, data_generator, compression=arguments["--compression"])

        runtime = time.time()-start_time
        console.print(f"conversion complete. Took {runtime:0.3f} s, succesfully written {outpath}")
    except Exception as e:
        err_console.print_exception()


if __name__ == "__main__":
    main()
