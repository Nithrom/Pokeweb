# Pokeweb — Supabase + Railway

## Arquitectura simple (un repo en GitHub)

| Servicio Railway | Root directory | Qué hace |
|------------------|----------------|----------|
| **Web** (HTML) | `/` (raíz del repo) | `index.html`, `js/`, `css/` — sin carpeta `data/` |
| **api-pokeweb** | `api/` | Flask + Gunicorn → Supabase |

La carpeta `api/` **sí debe estar en GitHub** (código + `Dockerfile`).  
**No** subas `api/.env` (está en `.gitignore`).

Variables solo en el servicio **api-pokeweb**:

| Variable | Valor |
|----------|--------|
| `DATABASE_URL` | URI de Supabase (Project Settings → Database → Connection string → URI) |

En los HTML (`index.html`, `trainers.html`, `teams.html`):

```html
<script>window.POKEWEB_API_BASE = 'https://api-pokeweb.up.railway.app';</script>
```

Comprueba: `https://api-pokeweb.up.railway.app/health` → `"db":"connected"`, `"backend":"postgres"`.

---

## Datos

- Edición: `data/*.json` + scripts `api/update_*.py` (local, opcional en Git).
- Producción: **Supabase**, vía `import_db.py` desde tu PC.

## 1. Tablas en Supabase (una vez)

SQL Editor → ejecutar [`sql/init.postgres.sql`](../sql/init.postgres.sql).

O en local: `cd api` → `python setup_supabase_schema.py` (con `DATABASE_URL` en `.env`).

## 2. API local (`api/.env`)

```env
DATABASE_URL=postgresql://postgres:...@db....supabase.co:5432/postgres
```

```powershell
cd api
pip install -r requirements.txt
```

## 3. Importar JSON → Supabase

```powershell
cd api
python import_db.py --reset
# o solo entrenadores:
python import_db.py --only trainers --reset
```

## 4. Tras cambiar entrenadores

```text
api/update_*.py  →  data/trainers_db.json  →  import_db.py  →  Supabase
```

No hace falta redeploy de la web por datos; sí mantener la API en Railway con `DATABASE_URL`.

## 5. Volver a subir `api/` a GitHub

Si quitaste `api/` del repo y Railway ya no despliega la API:

```powershell
git add api/
git add .gitignore docs/
git commit -m "Restaurar api/ para Railway; quitar stack Docker/MariaDB"
git push
```

En Railway → servicio **api-pokeweb** → Settings → **Root Directory** = `api` → Redeploy.
