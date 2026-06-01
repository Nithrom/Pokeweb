"""
Regenera trainers_db.json con todos los scripts de actualización del repo.
Uso (desde api/):  python run_all_trainer_updates.py

Después: sube/deploy la carpeta data/ (y el repo si usas Railway/Git).
Opcional BD local: python import_db.py --only trainers
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

API_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    'update_gen2_gyms.py',
    'update_hgss_trainers.py',
    'update_rs_gyms.py',
    'update_emerald_gyms.py',
    'update_frlg_gyms.py',
    'update_dp_gyms.py',
    'update_bdsp_gyms.py',
    'update_bw_gyms.py',
    'update_bw2_gyms.py',
    'update_xy_trainers.py',
    'update_oras_trainers.py',
    'update_lgpe_trainers.py',
    'update_swsh_gyms.py',
    'update_sv_trainers.py',
]


def run_script(name: str) -> None:
    path = API_DIR / name
    if not path.is_file():
        print(f'  SKIP (no existe): {name}')
        return
    spec = importlib.util.spec_from_file_location(name.removesuffix('.py'), path)
    if not spec or not spec.loader:
        print(f'  ERROR cargando: {name}')
        return
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    if hasattr(mod, 'main'):
        print(f'--- {name} ---')
        mod.main()
    else:
        print(f'  SKIP (sin main): {name}')


def main() -> None:
    print('Regenerando data/trainers_db.json...\n')
    for name in SCRIPTS:
        run_script(name)
    print('\nListo. Siguiente paso: deploy web con data/trainers_db.json actualizado.')


if __name__ == '__main__':
    main()
