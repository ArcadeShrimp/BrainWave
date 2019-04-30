from unittest import TestCase
from itertools import product
import utils
from data_record import DataRecord
import pandas as pd

class DataRecordTest(TestCase):

    def test_df(self):
        data_record = DataRecord()
        data_record.cache.append({
            ("TP9", "DELTA"): 0, ("TP9", "ALPHA"): 2,
        })
        data_record.cache.append({
            ("TP9", "DELTA"): 1, ("TP9", "ALPHA"): 3,
        })
        data_record.cache.append({
            ("TP9", "DELTA"): 9, ("TP9", "ALPHA"): 9,
        })
        multi_index = pd.MultiIndex.from_product(iterables=[
            [c.name for c in utils.Channel],
            [b.name for b in utils.Band]
        ], names=["channel", "band"])
        # cols = list(product(
        #     [c.name for c in utils.Channel],
        #     [b.name for b in utils.Band] ))
        cols = [("TP9", "DELTA"), ("TP9", "ALPHA")]
        df = pd.DataFrame.from_items(items=data_record.cache, orient="index", columns=cols)
        print(df)

