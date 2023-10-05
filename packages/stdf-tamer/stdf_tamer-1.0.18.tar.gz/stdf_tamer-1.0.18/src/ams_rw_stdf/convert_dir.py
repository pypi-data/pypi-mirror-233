"""export stdf data to a more helpful format.

Usage:
  stdfconvert --output=<output> --stdf-in=<stdf-in> [--compression=<zstd>] [--add-site] [--add-head]

  Without the optional 'file_formats' dependancy only pickle files can be generated.

  

Options:
  -h --help     Show this screen.
"""

e = """export stdf data to a more helpful format.

Usage:
  stdfconvert_dir --output=<output-dir> --stdf-in-dir=<stdf-in-dir>

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
from multiprocessing import Queue
from multiprocessing import Pool
import io
import threading


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
import lzma
from rich.progress import Progress
from rich.console import Console


console = Console()
err_console = Console(stderr=True, style="bold red")

tests = 0                 # global to allow to use this value for information printing...

# global to allow for allowing lean data colleciton, setting these global values just once
operator = None           
test_cod = None
lot_id  = None
start_t = None    


def worker(si, ftype, add_sites, add_head, oqueue):
    q = Queue(16)

    def _worker(q):
        with _opener[ftype](si, "rb") as f:
            f.seek(0, io.SEEK_END)
            fsize = f.tell()
            f.seek(0, io.SEEK_SET)
            oqueue.put((si, f.tell(), fsize,))
            
            while True:
                try:
                    a = []
                    for _ in range(1024):
                        a.append(ams_rw_stdf.get_record_bytes(f))
                    q.put(a)
                    a = []
                    oqueue.put((si, f.tell(), fsize,))
                except EOFError as e:
                    q.put(a+[e])
                    oqueue.put((si, f.tell(), fsize,))
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
                global tests
                key = (c.PL.HEAD_NUM, c.PL.SITE_NUM)
                part_tests = len(data[key])
                tests += part_tests
                #console.print(f"Adding part {c.PL.PART_TXT}/{c.PL.PART_ID} of head {c.PL.HEAD_NUM} site {c.PL.SITE_NUM} a total of {part_tests} tests...")
                
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
                global operator
                global test_cod
                global lot_id
                global start_t

                test_cod = c.PL.TEST_COD
                lot_id   = c.PL.LOT_ID
                operator = c.PL.OPER_NAM
                start_t = c.PL.START_T
                data = collections.defaultdict(lambda : [])
                #console.print(f"Converting LOT ID: '{lot_id}'...")
                yield (lot_id, test_cod, operator, start_t, add_head, add_sites, )
            elif type_and_subtyp == (1, 20,):
                return


import multiprocessing

def worker_for_item(param_q, info_q):
    print("goooo")
    while True:
        try:
            item = param_q.get(False)
        except Exception as e:
            break
        
        if item:
            si, ftype, add_sites, add_head, outpath, compression, writer = item
            data_generator = worker(si, ftype, add_sites, add_head, oqueue=info_q)
            writer(outpath, data_generator, compression=compression)
        else:
            break
    


def main():
    start_time = time.time()
    try:
        arguments = docopt(__doc__)
        outpath = pathlib.Path(arguments["--output"])
        si = arguments["--stdf-in"]
        ftype = si.split(".")[-1]

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

        

        
        todo = [(si, ftype, bool(arguments["--add-site"]), bool(arguments["--add-head"]), outpath, arguments["--compression"], writer,)]

        import rich.progress
        with Pool() as pool, Progress(rich.progress.DownloadColumn(), rich.progress.TransferSpeedColumn(), rich.progress.TimeElapsedColumn(), rich.progress.BarColumn(), rich.progress.TimeRemainingColumn(), rich.progress.TextColumn("[progress.description]{task.description}")) as progress: 

            def _work_progress(q, processes):
                bars = {}
                while any((item.is_alive() for item in processes)):
                    print(list((item.is_alive() for item in processes)))
                    try:
                        entry = q.get()
                        if entry:
                            name, pos, size = entry
                            if name not in bars:
                                bars[name] = progress.add_task(name, total=size)
                            progress.update(bars[name], completed=pos)
                        else:
                            break
                    except Exception as e:
                        return
            
            q = Queue()
            todoQ = Queue()
            
            #threading.Thread(target=_work_progress, args=(q,)).start()
            processes = [multiprocessing.Process(target=worker_for_item, args=(todoQ, q,), daemon=False) for _ in range(multiprocessing.cpu_count())]
            for item in todo:
                todoQ.put(item)
            for item in processes:
                item.start()
            _work_progress(q, processes)
            #worker_for_item(todoQ, q)
            #pool.map(worker_for_item, todo)
            #for item in todo:
            #    worker_for_item(todoQ, q)

        #time.sleep(20)

        q.put(None)



        runtime = time.time()-start_time
        console.print(f"conversion complete. Took {runtime:0.3f} s  {tests/runtime:0.1f} tests/s, succesfully written {outpath}")
    except Exception as e:
        err_console.print_exception()


if __name__ == "__main__":
    main()
