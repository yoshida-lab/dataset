# Copyright 2019 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import json

# import joblib
from pymatgen.ext.matproj import MPRester


def update(api_key):
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
        print('All inorganic in MaterialProjects: {}'.format(len(mp_ids)))

        return mp_ids


if __name__ == "__main__":
    ids = update('')
    # with open('ids.pkl.z', 'wb') as f:
    #     joblib.dump(ids, f)

    with open('ids.json', 'w') as f:
        json.dump(ids, f)
