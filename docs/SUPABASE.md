# Pokeweb en Supabase

La fuente de datos en JSON sigue siendo `data/pokemon_db.json` y `data/trainers_db.json`.  
Supabase guarda la misma información en PostgreSQL para que la API Flask sirva la web sin cargar JSON enormes.

## 1. Crear tablas en Supabase

1. Abre tu proyecto en [Supabase](https://supabase.com).
2. **SQL Editor** → New query.
3. Pega y ejecuta todo el archivo [`sql/init.postgres.sql`](../sql/init.postgres.sql).

## 2. Configurar la API

```powershell
cd api
copy .env.example .env
```

En `.env`, pon la **Connection string (URI)** de Supabase:

`Project Settings → Database → Connection string → URI`

```env
DATABASE_URL=postgresql://postgres:...@db....supabase.co:5432/postgres
```

Instala dependencias:

```powershell
pip install -r requirements.txt
```

## 3. Importar datos (una vez o tras actualizar JSON)

Desde la carpeta `api/`:

```powershell
# Import completo (pokémon + entrenadores). Tarda varios minutos por pokemon_db.json
python import_db.py --reset

# Solo entrenadores (tras run_all_trainer_updates.py)
python import_db.py --only trainers --reset
```

Comprueba:

```powershell
python -c "import db; print(db.query_one('SELECT COUNT(*) AS n FROM trainers'))"
```

## 4. Arrancar la API

```powershell
python app.py
```

- Salud: http://127.0.0.1:5000/health → `"db": "connected"`, `"backend": "postgres"`
- Estadísticas: http://127.0.0.1:5000/stats
- Entrenadores: http://127.0.0.1:5000/trainers?game_slug=scarlet-violet

La web (`trainers.html`, `teams.html`) usa la API si `/health` responde bien; si no, cae al JSON local.

## 5. Deploy (Railway, Render, etc.)

En el servicio **API** (p. ej. `api-pokeweb`), no solo la web estática:

| Variable | Valor |
|----------|--------|
| `DATABASE_URL` | **Obligatoria.** Supabase → Project Settings → Database → Connection string → **URI** (`postgresql://postgres:...@db....supabase.co:5432/postgres`) |
| `FLASK_ENV` | `production` (opcional) |

Sin `DATABASE_URL`, `/health` intenta MariaDB en `127.0.0.1` y verás `Connection refused`.

Tras guardar variables: **Redeploy** del servicio API.

Comprueba: `https://TU-API.up.railway.app/health` → `"db":"connected"`, `"backend":"postgres"`.

Tras cada cambio en `data/*.json` en el repo:

1. Ejecuta `python import_db.py --only trainers` (o `--reset` completo) **con** `DATABASE_URL` apuntando a producción, **o**
2. Automatiza el import en CI (cuidado con borrar `--reset` en prod).

## Flujo habitual

```text
Serebii / scripts update_*.py  →  data/trainers_db.json
import_db.py                    →  Supabase (PostgreSQL)
Flask app.py                    →  frontend vía /trainers, /pokemon, …
```

## MariaDB local (opcional)

Si **no** defines `DATABASE_URL`, la API e `import_db.py` usan MariaDB (`DB_HOST`, etc.) y `sql/init.sql` como antes.
