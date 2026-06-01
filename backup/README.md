# Backups Pokeweb

Copias de seguridad antes de cambios grandes (p. ej. migración a Supabase).

| Carpeta | Contenido |
|---------|-----------|
| `pokeweb-pre-supabase-YYYYMMDD_HHMM/` | Snapshot completo: `api/`, `data/`, `sql/`, `js/`, HTML, etc. (~250 MB por `pokemon_db.json`) |

## Crear un backup sin carpetas anidadas

Al copiar el proyecto, **excluye siempre** la carpeta `backup/` (si no, se copia el backup dentro del backup una y otra vez).

Ejemplo en PowerShell (desde la raíz del repo):

```powershell
$dest = "backup\pokeweb-$(Get-Date -Format 'yyyy-MM-dd_HHmm')"
New-Item -ItemType Directory -Path $dest -Force | Out-Null
Get-ChildItem -Exclude backup | Copy-Item -Destination $dest -Recurse -Force
```

Para restaurar: copia la carpeta del snapshot sobre el proyecto (o solo los archivos que necesites). No sustituye la base de datos en la nube; para eso usa export SQL de Supabase o el JSON en `data/`.
