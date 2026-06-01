# Deploy Pokeweb

## Servicios

| Servicio | Contenido | Variables |
|----------|-----------|-----------|
| **API** (`api/`) | Flask + Gunicorn | `DATABASE_URL` (Supabase) |
| **Web** (raíz) | HTML, `js/`, `css/`, `img/` | `POKEWEB_API_BASE` en HTML → URL de la API |

La carpeta `api/` **no está en GitHub** (`.gitignore`). Sigue en tu PC; en Railway el servicio API puede seguir desplegado desde el repo hasta el próximo push, o redeploy manual / otro repo solo-API.

## Qué no subir a la web estática

- `data/pokemon_db.json`, `data/trainers_db.json` (~MB) — la web usa la API si `/health` OK
- `api/`, `backup/`, `sql/`
- `.env`

## Flujo al cambiar entrenadores

```text
api/update_*.py  →  data/trainers_db.json  →  import_db.py  →  Supabase
```

No hace falta redeploy de la web estática solo por datos de entrenadores.
