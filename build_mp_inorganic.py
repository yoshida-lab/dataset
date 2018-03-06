# Copyright 2017 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from itertools import zip_longest
from pathlib import Path

import pandas as pd
from pymatgen import MPRester
from tqdm import tqdm


def _mp_inorganic(*args, **kwargs):
    # material projects API-key
    api_key = 'Zrp32nS1LVBHsGCK'
    if 'api_key' in kwargs:
        api_key = kwargs['api_key']

    # split requests into fixed number groups
    # eg: grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    def grouper(iterable, n, fillvalue=None):
        """Collect data into fixed-length chunks or blocks"""
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    # the following props will be fetched
    mp_props = [
        'anonymous_formula',
        'band_gap',
        'density',
        'volume',
        # 'discovery_year',
        # 'elastic_tensor',
        'elements',
        'efermi',
        'e_above_hull',
        'formation_energy_per_atom',
        'final_energy_per_atom',
        'has_bandstructure',
        'oxide_type',
        'total_magnetization',
        'unit_cell_formula',
    ]

    props = args if args else mp_props
    props.append('pretty_formula')

    # fetch data
    with MPRester(api_key) as mpr:
        elements = [
            'H',
            'He',
            'Li',
            'Be',
            'B',
            'C',
            'N',
            'O',
            'F',
            'Ne',
            'Na',
            'Mg',
            'Al',
            'Si',
            'P',
            'S',
            'Cl',
            'Ar',
            'K',
            'Ca',
            'Sc',
            'Ti',
            'V',
            'Cr',
            'Mn',
            'Fe',
            'Co',
            'Ni',
            'Cu',
            'Zn',
            'Ga',
            'Ge',
            'As',
            'Se',
            'Br',
            'Kr',
            'Rb',
            'Sr',
            'Y',
            'Zr',
            'Nb',
            'Mo',
            'Tc',
            'Ru',
            'Rh',
            'Pd',
            'Ag',
            'Cd',
            'In',
            'Sn',
            'Sb',
            'Te',
            'I',
            'Xe',
            'Cs',
            'Ba',
            'La',
            'Ce',
            'Pr',
            'Nd',
            'Pm',
            'Sm',
            'Eu',
            'Gd',
            'Tb',
            'Dy',
            'Ho',
            'Er',
            'Tm',
            'Yb',
            'Lu',
            'Hf',
            'Ta',
            'W',
            'Re',
            'Os',
            'Ir',
            'Pt',
            'Au',
            'Hg',
            'Tl',
            'Pb',
            'Bi',
            'Po',
            'At',
            'Rn',
            'Fr',
            'Ra',
            'Ac',
            'Th',
            'Pa',
            'U',
            'Np',
            'Pu',
            'Am',
            'Cm',
            'Bk',
            'Cf',
            'Es',
            'Fm',
            'Md',
            'No',
            'Lr',
            'Rf',
            'Db',
            'Sg',
            'Bh',
            'Hs',
            'Mt',
            'Ds',
            'Rg',
            'Cn',
            'Nh',
            'Fl',
            'Mc',
            'Lv',
            'Ts',
            'Og',
        ]
        # entries = mpr.query({"elements": "O", "nelements": {"$gte": 1}}, props)
        entries = mpr.query({"elements": {'$in': elements}}, ['material_id'])
        mp_ids = [e['material_id'] for e in entries]
        print('All norganic in MaterialProjects: {}'.format(len(mp_ids)))

    entries = []
    mpid_groups = [g for g in grouper(mp_ids, 1000)]

    with MPRester(api_key) as mpr:
        for group in tqdm(mpid_groups):
            mpid_list = [id for id in filter(None, group)]
            chunk = mpr.query({"material_id": {"$in": mpid_list}}, props)
            entries.extend(chunk)

    df = pd.DataFrame(entries, index=[f['pretty_formula'] for f in entries])
    df = df.drop('pretty_formula', axis=1)
    df = df.rename(columns={'unit_cell_formula': 'composition'})
    df = df.reindex(columns=sorted(df.columns))

    return df


# %%
if __name__ == '__main__':
    db_path = Path(__file__).parent
    _mp = _mp_inorganic()
    _mp.to_pickle(str(db_path / 'mp_inorganic.pkl'))
    # _mp.to_csv(str(db_path / 'inorganic_proporty.csv'))
