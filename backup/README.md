# Backups Pokeweb

Copias de seguridad antes de cambios grandes (p. ej. migración a Supabase).

| Carpeta | Contenido |
|---------|-----------|
| `pokeweb-pre-supabase-YYYYMMDD_HHMM/` | Snapshot completo: `api/`, `data/`, `sql/`, `js/`, HTML, etc. (~250 MB por `pokemon_db.json`) |

Para restaurar: copia la carpeta sobre el proyecto (o solo los archivos que necesites). No sustituye la base de datos en la nube; para eso usa export SQL de Supabase o el JSON en `data/`.
