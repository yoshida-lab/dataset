# Copyright 2019 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# first install qmpy
from __future__ import unicode_literals

from qmpy import *

from collections import OrderedDict

import joblib
import pandas as pd
from pymatgen import Structure
from tqdm import tqdm


def extract(entry):
    struct = entry.structure
    spacegroup = entry.spacegroup
    pmg_s = Structure(struct.cell, struct.site_compositions, struct.site_coords)

    return OrderedDict([
        ('id', entry.id),
        ('label', entry.label),
        ('proto_label', entry.proto_label),
        ('formula', entry.name),
        ('composition', entry.spec_comp),
        ('reduced_comp', entry.red_comp),
        ('unit_comp', entry.unit_comp),
        ('total_energy_pa', entry.total_energy),
        ('formation_energy_pa', entry.energy),
        ('experiment', entry.composition.experiment),
        ('mass', entry.mass),
        ('stable', entry.stable),
        ('e_above_hull', entry.formationenergy_set.first().stability),
        ('is_ordered', pmg_s.is_ordered),
        ('band_gap', entry.band_gap),
        ('spacegroup', spacegroup.hm),
        ('spacegroup_hall', spacegroup.hall),
        ('spacegroup_id', spacegroup.number),
        ('spacegroup_schoenflies', spacegroup.schoenflies),
        ('is_centro_symmetric', spacegroup.centrosymmetric),
        ('natoms', struct.natoms),
        ('ntypes', struct.ntypes),
        ('nsites', struct.nsites),
        # ('stresses', struct.stresses),
        # ('forces', struct.forces),
        ('volume', struct.volume),
        ('volume_pa', struct.volume_pa),
        # ('magmon', struct.magmom),
        # ('magmon_pa', struct.magmom_pa),
    ]), OrderedDict([('id', entry.id), ('structure', pmg_s.as_dict())])


def _main():
    info = []
    stru = []

    with tqdm(total=Entry.objects.count()) as pbar:
        for entry in Entry.objects.iterator():
            try:
                if entry.stable is None:
                    print(entry)
                    pbar.update(1)
                    continue
                i, s = extract(entry)
                info.append(i)
                stru.append(s)
            except Exception as e:
                print('%s | %s | error:%s' % (entry.name, entry.id, e))
            pbar.update(1)

    props = pd.DataFrame(data=info).set_index('id')
    structures = pd.DataFrame(data=info).set_index('id')

    return props, structures


if __name__ == '__main__':
    from sha256 import refresh
    from pathlib import Path
    name_p = 'oqmd_inorganic.pd.xz'
    name_s = 'oqmd_structure.pd.xz'
    db_path = Path(__file__).parent
    props, structures = _main()
    props.to_pickle(str(db_path / name_p))
    structures.to_pickle(str(db_path / name_s))
    # _mp.iloc[:10, :].to_excel(str(db_path / 'output.xlsx'))
    refresh(name_p, name_s)
