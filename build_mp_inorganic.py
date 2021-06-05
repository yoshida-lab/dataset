# Copyright 2019 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from itertools import zip_longest
from pathlib import Path
import json

import pandas as pd
from pymatgen.ext.matproj import MPRester
from tqdm import tqdm
import numpy as np


def _mp_inorganic(mp_ids, *, api_key=''):
    # split requests into fixed number groups
    # eg: grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    def grouper(iterable, n, fillvalue=None):
        """Collect data into fixed-length chunks or blocks"""
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    # the following props will be fetched
    mp_props = [
        # 'anonymous_formula',
        'band_gap',
        'density',
        'volume',
        'material_id',
        # 'discovery_year',
        # 'elastic_tensor',
        # 'elasticity',
        'is_ordered',
        'spacegroup',
        'pretty_formula',
        'elements',
        'efermi',
        # 'diel',
        # 'has',
        'e_above_hull',
        'formation_energy_per_atom',
        'final_energy_per_atom',
        'has_bandstructure',
        'oxide_type',
        'total_magnetization',
        'unit_cell_formula',
    ]

    entries = []
    mpid_groups = [g for g in grouper(mp_ids, 1000)]

    with MPRester(api_key) as mpr:
        for group in tqdm(mpid_groups):
            mpid_list = [id for id in filter(None, group)]
            chunk = mpr.query({"material_id": {"$in": mpid_list}}, mp_props)
            entries.extend(chunk)

    def split_dict(e):
        sg = e['spacegroup']
        del e['spacegroup']
        e['space_group_number'] = sg['number']
        e['space_group'] = sg['symbol']
        e['point_group'] = sg['point_group']
        e['n_elemets'] = len(e['elements'])

        # if 'elasticity' in e['has']:
        #     sg = e['elasticity']
        #     del e['elasticity']
        #     e['G_VRH'] = sg['G_VRH'] if 'G_VRH' in sg else np.nan
        #     e['K_VRH'] = sg['K_VRH'] if 'K_VRH' in sg else np.nan
        #     e['poisson_ratio'] = sg['G_VRH'] if 'G_VRH' in sg else np.nan

        # if 'diel' in e['has']:
        #     sg = e['diel']
        #     del e['diel']
        #     e['refractive_index'] = sg['n'] if 'n' in sg else np.nan
        #     e['electric_dielectric_cons'] = sg[
        #         'poly_electronic'] if 'poly_electronic' in sg else np.nan
        #     e['total_dielectric_cons'] = sg['poly_total'] if 'poly_electronic' in sg else np.nan

        return e

    entries = [split_dict(e) for e in entries]

    df = pd.DataFrame(entries, index=[e['material_id'] for e in entries])
    df = df.drop('material_id', axis=1)
    df = df.rename(columns={'unit_cell_formula': 'composition'})
    df = df.reindex(columns=sorted(df.columns))

    return df


if __name__ == '__main__':
    from sha256 import refresh
    name = 'mp_inorganic.pd.xz'
    db_path = Path(__file__).parent

    with open('ids.json', 'r') as f:
        mp_ids = json.load(f)
    _mp = _mp_inorganic(mp_ids, api_key='')
    _mp.to_pickle(str(db_path / name))
    # _mp.to_csv(str(db_path / 'inorganic_proporty.csv'))
    refresh(name)
