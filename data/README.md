# Datos fuente (desarrollo)

Estos JSON **no se sirven en producción** si la API usa Supabase. Sirven para:

1. Editar / regenerar con `api/update_*.py` y `api/run_all_trainer_updates.py`
2. Volcar a Supabase con `api/import_db.py`

| Archivo | Uso |
|---------|-----|
| `pokemon_db.json` | Import pokédex y movimientos |
| `trainers_db.json` | Import entrenadores y equipos |

En el deploy **estático** (HTML/JS) de Railway no hace falta subir esta carpeta.
