import pickle
try:
    import polars as pl
    schema = [('Test_Nr', pl.UInt32),
              ('Test_Name', pl.Utf8),
              ('ULim', pl.Float32), 
              ('LLim', pl.Float32),
              ('res', pl.Float32),
             ]
except:
    pass

__magic = 808507

def write_pickle(ofile, worker, **kwargs):
    with open(ofile, "wb") as f:
        pickle.dump(__magic, f)
        for item in worker:
            pickle.dump(item, f)


def pickle_worker(ifile):
    with open(ifile, "rb") as f:
        try:
            assert __magic == pickle.load(f), "file was created with mismatching magic" 
            while True:
                yield pickle.load(f)
        except EOFError as e:
            pass
            

def prepare_df(worker):
    (lot_id, test_cod, operator, start_t, add_head, add_sites, ) = next(worker)

    def worker_():
        for item in worker:
            df = pl.DataFrame(item["data"], schema=schema)
            df = df.with_columns(pl.lit(item["part_id"]).cast(pl.Utf8).alias("part_id"),
                                 pl.lit(item["part_txt"]).cast(pl.Utf8).alias("part_txt"))
            if add_head:
                df = df.with_columns(pl.lit(item["head"]).cast(pl.Utf8).alias("head"))
            if add_sites:
                df = df.with_columns(pl.lit(item["site"]).cast(pl.Utf8).alias("site"))
            yield df

    df = pl.concat(worker_())
    df = df.with_columns(pl.lit(test_cod).cast(pl.Categorical).alias("TEST_COD"),
                         pl.lit(lot_id).cast(pl.Categorical).alias("lot_id"),
                         pl.lit(operator).cast(pl.Categorical).alias("operator"),
                         pl.lit(start_t).cast(pl.UInt32).alias("START_T"),
                         pl.col("Test_Name").cast(pl.Categorical).alias("Test_Name"),
                         pl.col("part_id").cast(pl.Categorical).alias("part_id"),
                         pl.col("part_txt").cast(pl.Categorical).alias("part_txt"),)
    return df


def write_parquet(ofile, worker, compression):
    df = prepare_df(worker)
    df.write_parquet(ofile, compression=compression)


def write_ipc(ofile, worker, compression):
    df = prepare_df(worker)
    df.write_ipc(ofile, compression=compression)


def write_xlsx(ofile, worker, compression):
    df = prepare_df(worker)
    df.write_excel(ofile)
