# Copyright 2017 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# first install qmpy
from qmpy import *
import pandas as pd
from pymatgen.core import Structure
from django.core.exceptions import MultipleObjectsReturned
import sys
import os
from __future__ import unicode_literals

# ELEMENT_SET=['F', 'Cl', 'Br', 'I', 'O', 'S', 'Se', 'Te', 'N', 'P', 'As', 'C', 'H']
# query = Structure.objects.filter(calculated__converged=True, calculated__label__in=['static', 'standard'], element_set__in=ELEMENT_SET).exclude(calculated__formationenergy=None)
query = Structure.objects.filter(
    calculated__converged=True, calculated__label__in=[
        'static', 'standard'
    ]).exclude(calculated__formationenergy=None)
count = query.count()
structures = [s for s in query.all()]


def extract(s):
    pmg_s = Structure(s.cell, s.site_compositions, s.site_coords)
    cal = s.calculated.first()
    fe = cal.formationenergy_set.first()

    return dict(
        oqmd_s_id=s.id,
        label=s.label,
        formula=s.name,
        natoms=s.natoms,
        ntypes=s.ntypes,
        nsites=s.nsites,
        stresses=s.stresses,
        forces=s.forces,
        volume=s.volume,
        volume_pa=s.volume_pa,
        composition=s.comp,
        magmon=cal.magmom,
        magmon_pa=cal.magmom_pa,
        band_gap=cal.band_gap,
        energy=cal.energy,
        energy_pa=cal.energy_pa,
        formation_energy=fe.delta_e,
        stability=fe.stability,
        spacegroup_hm=s.spacegroup.hm,
        spacegroup_hall=s.spacegroup.hall,
        spacegroup_id=s.spacegroup_id,
        spacegroup_schoenflies=s.spacegroup.schoenflies,
        is_centro_symmetric=s.spacegroup.centrosymmetric,
        structure=pmg_s,
    )


def _main():
    tmp = []
    for i, s in enumerate(structures):
        try:
            tmp.append(extract(s))
        except Exception as e:
            print('%s | %s | error:%s' % (s.name, s.id, e))

        if i % 10000 == 0:
            print('%s done!' % i)

    return pd.DataFrame(data=tmp)


if __name__ == '__main__':
    from sha256 import refresh
    from pathlib import Path
    name = 'oqmd_v1.2_%s.pkl.z' % count
    db_path = Path(__file__).parent
    # _oqmd = _main()
    # _oqmd.to_pickle(str(db_path / name))
    # _mp.iloc[:10, :].to_excel(str(db_path / 'output.xlsx'))
    refresh(name)
