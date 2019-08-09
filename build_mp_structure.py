# Copyright 2019 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import json
from itertools import zip_longest
from pathlib import Path

import pandas as pd
from pymatgen import MPRester
from tqdm import tqdm


def _mp_structure(mp_ids, *, api_key=''):
    # split requests into fixed number groups
    # eg: grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    def grouper(iterable, n, fillvalue=None):
        """Collect data into fixed-length chunks or blocks"""
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    # the following props will be fetched
    mp_props = ['structure', 'material_id']

    entries = []
    mpid_groups = [g for g in grouper(mp_ids, 1000)]

    with MPRester(api_key) as mpr:
        for group in tqdm(mpid_groups):
            mpid_list = [id for id in filter(None, group)]
            chunk = mpr.query({"material_id": {"$in": mpid_list}}, mp_props)
            entries.extend(chunk)

    # entries = [e.as_dict() for e in entries]

    df = pd.DataFrame(entries, index=[e['material_id'] for e in entries])
    df = df.drop('material_id', axis=1)
    df = df.reindex(columns=sorted(df.columns))

    return df


if __name__ == '__main__':
    from sha256 import refresh
    name = 'mp_structure.pd.xz'
    db_path = Path(__file__).parent
    with open('ids.json', 'r') as f:
        mp_ids = json.load(f)
    _mp = _mp_structure(mp_ids, api_key='1vRmHNP6w40CzaiO')
    _mp.to_pickle(str(db_path / name))
    # _mp.iloc[:10, :].to_excel(str(db_path / 'output.xlsx'))
    refresh(name)
