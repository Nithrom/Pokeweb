# Migración Pokeweb → Supabase

## 1. Crear proyecto en [Supabase](https://supabase.com/)

1. Nuevo proyecto → anota la **contraseña** de `postgres`.
2. **SQL Editor** → pega y ejecuta el contenido de [`sql/init.postgres.sql`](../sql/init.postgres.sql).

## 2. Variables de entorno (API)

Copia `api/.env.example` a `api/.env`:

```env
DATABASE_URL=postgresql://postgres:PASSWORD@db.PROJECT_REF.supabase.co:5432/postgres
```

La URI está en: **Project Settings → Database → Connection string → URI**.

## 3. Importar datos

```powershell
cd api
pip install -r requirements.txt
python import_db.py --reset
```

`--reset` vacía tablas y reimporta desde `data/pokemon_db.json` y `data/trainers_db.json` (tarda varios minutos por el tamaño del dex).

Comprueba:

- `python -c "import os; from dotenv import load_dotenv; load_dotenv(); import app"` (opcional)
- Arranca API: `flask --app app run` o Docker
- `http://127.0.0.1:5000/health` → `"db": "connected"`, `"backend": "postgres"`

## 4. Frontend (solo API)

En cada HTML puedes fijar la API antes de cargar scripts:

```html
<script>window.POKEWEB_API_BASE = 'http://127.0.0.1:5000';</script>
```

En producción: URL de tu API (Render, Railway, etc.) con CORS habilitado.

## 5. Desplegar

| Pieza | Sugerencia |
|-------|------------|
| Base de datos | Supabase (ya hecho) |
| API Flask | [Render](https://render.com/), Railway, Fly.io — variable `DATABASE_URL` |
| Web estática | Cloudflare Pages, Netlify — carpeta raíz del repo |

## Backup local

Antes de migrar se guardó una copia en `backup/pokeweb-pre-supabase-*`. Los JSON en `data/` siguen siendo la fuente para reimportar.

## MariaDB local (opcional)

Si **no** defines `DATABASE_URL`, la API y `import_db.py` siguen usando MariaDB (`docker compose up`).
