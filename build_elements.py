# Copyright 2017 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from pathlib import Path

import pandas as pd


def _elements(*drop_list):
    from mendeleev import get_table
    table = get_table('elements')
    numeric = table.select_dtypes(exclude=[object])
    list_ = drop_list if drop_list else [
        'group_id',
        'series_id',
        'fusion_heat',
        'abundance_crust',
        'abundance_sea',
        # 'is_monoisotopic',
        'is_radioactive',
    ]
    numeric = numeric.drop(list_, 1)
    numeric = numeric.reindex_axis(sorted(numeric.columns), axis=1)
    numeric = numeric.rename(lambda i: table.loc[i, 'symbol'])

    return numeric


if __name__ == '__main__':
    from sha256 import refresh
    name = 'elements.pkl.pd_'
    db_path = Path(__file__).parent
    data = pd.read_csv(str(db_path / 'elements.csv'))
    data = data.rename(lambda i: data.loc[i, 'symbol']).drop('symbol', axis=1)
    data.to_pickle(str(db_path / name))
    refresh(name)
