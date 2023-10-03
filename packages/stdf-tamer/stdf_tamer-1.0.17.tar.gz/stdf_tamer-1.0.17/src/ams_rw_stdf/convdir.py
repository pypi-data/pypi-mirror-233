"""
Usage:
  stdfconvert_dir --output=<output-dir> --stdf-in-dir=<stdf-in-dir> --output-format=<output-format> [--compression=lz4]  [--add-site] [--add-head]

  Without the optional 'file_formats' dependancy only pickle files can be generated.

  --compression=<algorithm>   [default: lz4]


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
from multiprocessing import Queue
from multiprocessing import Pool
import multiprocessing
import glob
import io
import enum
import threading
import rich.progress
from rich.table import Table
import os
import logging
import random

output_writers = {"pickle": _output_workers.write_pickle}

try:
    import polars as pl
    
    output_writers["ipc"] =     _output_workers.write_ipc
    output_writers["feather"] = _output_workers.write_ipc
    output_writers["parquet"] = _output_workers.write_parquet
    output_writers["xlsx"] =    _output_workers.write_xlsx

except:
    pass

import collections
import time
import sys
import threading
import lzma
from rich.progress import Progress
from rich.console import Console

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


console = Console()
err_console = Console(stderr=True, style="bold red")

_type = enum.Enum("progress", ["progress", "result"])

def worker(si, ftype, add_sites, add_head, oqueue):
    q = Queue(16)

    def _worker(q):
        with _opener[ftype](si, "rb") as f:
            f.seek(0, io.SEEK_END)
            fsize = f.tell()
            f.seek(0, io.SEEK_SET)
            oqueue.put(("progress", si, f.tell(), fsize,))
            
            while True:
                try:
                    a = []
                    for _ in range(4096):
                        a.append(ams_rw_stdf.get_record_bytes(f))
                    q.put(a)
                    a = []
                    oqueue.put(("progress", si, f.tell(), fsize,))
                except EOFError as e:
                    q.put(a+[e])
                    oqueue.put(("progress", si, f.tell(), fsize,))
                    return

    t = threading.Thread(target=_worker, daemon=True, args=(q,))
    t.start()

    data = None
    parser = ams_rw_stdf.compileable_RECORD.compile()

        
    while True:
        d = q.get()
        for c in d:
            if c is EOFError:
                console.print("Unexpected end of file...")
                return
            c = parser.parse(c)
            type_and_subtyp = (c.REC_TYP, c.REC_SUB,)
            if type_and_subtyp == (15, 10,):
                key = (c.PL.HEAD_NUM,  c.PL.SITE_NUM,)
                data[key].append((c.PL.TEST_NUM, c.PL.TEST_TXT,
                                c.PL.HI_LIMIT, c.PL.LO_LIMIT,
                                c.PL.RESULT,))
            elif type_and_subtyp == (5, 20,):
                key = (c.PL.HEAD_NUM, c.PL.SITE_NUM)
                res = {"data": data[key]}
                res["part_id"]  = c.PL.PART_ID
                res["part_txt"] = c.PL.PART_TXT
                if add_sites:
                    res["site"] = c.PL.SITE_NUM
                if add_head:
                    res["head"] = c.PL.HEAD_NUM
                yield res
                data[key] = []
            elif type_and_subtyp == (1, 10,):
                test_cod = c.PL.TEST_COD
                lot_id   = c.PL.LOT_ID
                operator = c.PL.OPER_NAM
                start_t = c.PL.START_T
                data = collections.defaultdict(lambda : [])
                yield (lot_id, test_cod, operator, start_t, add_head, add_sites, )
            elif type_and_subtyp == (1, 20,):
                return


def worker_for_item(param_q, info_q):
    while True:
        try:
            item = param_q.get()
            if item is None:
                break
        except Exception as e:
            break
        try:
            si, add_sites, add_head, outpath, compression, output_format = item
            writer = output_writers[output_format]
            data_generator = worker(si, pathlib.Path(si).suffix, add_sites, add_head, oqueue=info_q)
            writer(outpath, data_generator, compression=compression)
            info_q.put(("result", si, "success"))
        except Exception as e:
            info_q.put(("result", si, "fail", e))


def work_todo(todo, parse_stdf_message="\n[bold]Parsing stdf files[no bold]", flush_results=f"\n[bold]writing results[no bold]"):
    todo_len = len(todo)
    q = Queue()
    num_of_workers = multiprocessing.cpu_count()
    todoQ = Queue(maxsize=len(todo)+num_of_workers)
    processes = [multiprocessing.Process(target=worker_for_item, args=(todoQ, q,), daemon=True) for _ in range(num_of_workers)]
    for item in todo:
        todoQ.put(item)
    for _ in range(num_of_workers):
        todoQ.put(None)
    for item in processes:
        item.start()
    
    todo_parse_len = todo_len
    total_len = todo_len

    console.print(parse_stdf_message)
    
    with Progress(rich.progress.DownloadColumn(),
                  rich.progress.TransferSpeedColumn(),
                  rich.progress.TimeElapsedColumn(),
                  rich.progress.BarColumn(),
                  rich.progress.TimeRemainingColumn(),
                  rich.progress.TextColumn("[progress.description]{task.description}"), auto_refresh=False) as progress: 
        bars = {}
            
        while todo_parse_len > 0:
            try:
                entry = q.get()
                if entry[0] == "progress":
                    _, name, pos, size = entry
                    if name not in bars:
                        bars[name] = progress.add_task(pathlib.Path(name).name, total=size)
                    progress.update(bars[name], completed=pos, refresh=True)
                    if entry[2] == entry[3]:
                        todo_parse_len -= 1
                elif entry[0] == "result":
                    if entry[2] == "fail":
                        exception = entry[-1]
                        logging.error(f"failed due to {str(exception)}!")
                    todo_len -= 1
            except Exception as e:
                return
    
    console.print(flush_results)
    with Progress() as progress:
        bar = progress.add_task("files written", total=total_len)
        progress.update(bar, completed=0)
        progress.update(bar, completed=(total_len-todo_len))
        
        while todo_len:
            entry = q.get()
            if entry[0] == "result":
                progress.update(bar, advance=1, refresh=True)
                if entry[2] == "fail":
                    exception = entry[-1]
                    logging.error(f"failed due to {str(exception)}!")
                todo_len -= 1

def convert_direcotry(outpath, inpath, add_site, add_head, compression, output_format):
        start_time = time.time()
        console.print(f"stdf-tamer ({version})")
        console.print(f"converting from directory: [yellow]{inpath}[not yellow] to: [yellow]{pathlib.Path(outpath)}[not yellow]\n\n", highlight=False)
        outpath = pathlib.Path(outpath)
        inpath = pathlib.Path(inpath)
        if output_format not in output_writers:
            err_console.print(f"please use one of these file formats as output: {', '.join(output_writers.keys())}")
            err_console.print("""
The optional dependency group 'file_formats' adds additional file formats, like xlsx, feather and ipd.

These optional dependencies are less portable than stdf-tamer itself and may not be available on pypy or legacy python versions.""")
            sys.exit(1)
    
        if not outpath.is_dir():
            err_console.print(f"--output path is not a direcotry: {str(outpath)}")
            sys.exit(1)
        if not inpath.is_dir():
            err_console.print(f"--stdf-in-dir path is not a direcotry: {str(inpath)}")
            sys.exit(1)
    
        iFiles = list(inpath.glob("**/*.stdf")) + list(inpath.glob("**/*.stdf.gz")) + list(inpath.glob("**/*.stdf.bz2")) + list(inpath.glob("**/*.stdf.xz")) 

        iFiles = sorted( iFiles, key =  lambda x: -1 * os.stat(x).st_size)
        i_and_o_files = list((ifile, pathlib.Path(outpath) / pathlib.Path(ifile).relative_to(inpath).with_suffix(f".{output_format}"),) for ifile in iFiles )

        table = Table(title="Files to convert")
        table.add_column("input file [1]")
        table.add_column("file size [1]")
        for item in iFiles:
            table.add_row(str(item), str(os.path.getsize(item)))
        console.print(table)

        todo = [(ifile, add_site, add_head, ofile, compression, output_format,) for ifile, ofile in i_and_o_files]
        work_todo(todo)
        runtime = time.time()-start_time
        console.print("\n")
        if output_format != "pickle":
            table = Table(title="Statistics")
            table.add_column("Result file")
            table.add_column("in size [1]")
            table.add_column("out size [1]")
            table.add_column("size reduction [1]", style="green")
            table.add_column("size [%]", style="green")
            
            for ifile, ofile in i_and_o_files:
                isize = os.path.getsize(ifile)
                osize = os.path.getsize(ofile)
                percentage = (100*((isize - osize)/isize))
                table.add_row(str(ofile), str(isize), str(osize), str(isize - osize), f"{percentage:.2f}")
            console.print(table)
        
        console.print(f"conversion complete. Took {runtime:0.3f} s")

def main():
    try:
        arguments = docopt(__doc__)
        outpath = pathlib.Path(arguments["--output"])
        inpath = pathlib.Path(arguments["--stdf-in-dir"])

        add_site = bool(arguments["--add-site"])
        add_head = bool(arguments["--add-head"])
        compression = arguments["--compression"]
        convert_direcotry(outpath, inpath, add_site, add_head, compression, arguments["--output-format"])
        
        
    except Exception as e:
        err_console.print_exception()


if __name__ == "__main__":
    main()
