# Copyright 2019 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# first install qmpy
from __future__ import unicode_literals

import joblib
import pandas as pd

from tqdm import tqdm
from qmpy import *
from pymatgen.core import Structure


def extract(entry):
    struct = entry.structure
    spacegroup = entry.spacegroup
    pmg_s = Structure(struct.cell, struct.site_compositions, struct.site_coords)
    
    return dict(
        id=entry.id,
        label=entry.label,
        proto_label=entry.proto_label,
        formula=entry.name,
        composition=entry.spec_comp,
        reduced_comp=entry.name,
        total_energy_pa=entry.total_energy,
        formation_energy_pa=entry.energy,
        experiment=entry.composition.experiment,
        mass_pa=entry.mass,
        stable=entry.stable,
        band_gap=entry.band_gap,
        spacegroup_hm=spacegroup.hm,
        spacegroup_hall=spacegroup.hall,
        spacegroup_id=spacegroup.number,
        spacegroup_schoenflies=spacegroup.schoenflies,
        is_centro_symmetric=spacegroup.centrosymmetric,
        natoms=struct.natoms,
        ntypes=struct.ntypes,
        nsites=struct.nsites,
#         stresses=struct.stresses,
#         forces=struct.forces,
        volume=struct.volume,
        volume_pa=struct.volume_pa,
        magmon=struct.magmom,
        magmon_pa=struct.magmom_pa,
        structure=pmg_s.as_dict(),
    )


def _main():
    # ELEMENT_SET=['F', 'Cl', 'Br', 'I', 'O', 'S', 'Se', 'Te', 'N', 'P', 'As', 'C', 'H']
    tmp = []
    with tqdm(total=Entry.objects.count()) as pbar:
        for entry in Entry.objects.iterator():
            try:
                tmp.append(extract(entry))
            except Exception as e:
                print('%s | %s | error:%s' % (entry.name, entry.id, entry))
            pbar.update(1)

    data = pd.DataFrame(data=tmp).set_index('oqmd_s_id')
    props = data.drop(['structure'], axis=1)
    structures = pd.DataFrame(data['structure'])

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
