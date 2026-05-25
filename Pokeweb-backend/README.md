# Pokeweb Backend

MariaDB + phpMyAdmin + Flask API, todo en Docker.

## Arrancar por primera vez

```bash
# 1. Entra en esta carpeta
cd Pokeweb-backend

# 2. Levanta los contenedores (la primera vez descarga las imágenes, tarda un poco)
docker compose up -d

# 3. Comprueba que todo está corriendo
docker compose ps
```

Deberías ver 3 contenedores en estado "running":
- `pokeweb_db`          → MariaDB en puerto 3306
- `pokeweb_phpmyadmin`  → phpMyAdmin en http://localhost:8080
- `pokeweb_api`         → Flask API en http://localhost:5000

## Acceder a phpMyAdmin

Abre http://localhost:8080 en el navegador.
- Usuario: `pokeweb_user`
- Contraseña: `pokeweb_pass`

La base de datos `pokeweb` ya estará creada con todas las tablas (se crea sola
al arrancar por el archivo `sql/init.sql`).

## Probar la API

```bash
# Health check
curl http://localhost:5000/health

# Lista de pokémon (vacía hasta que importes datos)
curl http://localhost:5000/pokemon

# Pokémon por tipo
curl http://localhost:5000/type/fire

# Efectividades de tipos
curl http://localhost:5000/effectiveness
```

## Importar datos desde el JSON existente

Si ya tienes `pokemon_db.json` del proyecto anterior, puedes importarlo con:

```bash
# Copia el json a la carpeta api/
cp ../Pokeweb/data/pokemon_db.json ./api/

# Ejecuta el script de importación dentro del contenedor
docker exec pokeweb_api python import_db.py
```

(El script `import_db.py` se generará en el siguiente paso)

## Parar los contenedores

```bash
docker compose down        # para pero conserva los datos
docker compose down -v     # para Y borra todos los datos (reset completo)
```

## Estructura de carpetas

```
Pokeweb-backend/
├── docker-compose.yml     ← configuración de contenedores
├── sql/
│   └── init.sql           ← esquema de tablas (se ejecuta al crear la DB)
└── api/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py             ← API Flask con todos los endpoints
```

## Endpoints disponibles

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | /health | Estado de la API y DB |
| GET | /pokemon | Lista todos los pokémon |
| GET | /pokemon/{name} | Datos de un pokémon |
| GET | /pokemon/{name}/moves | Movimientos de un pokémon |
| GET | /type/{name} | Pokémon de ese tipo |
| GET | /type/{t1}/{t2} | Pokémon de doble tipo |
| GET | /effectiveness | Tabla de efectividades |
| GET | /games | Lista de juegos/versiones |
| GET | /trainers?game_id=X | Entrenadores de un juego |
| GET | /trainer/{id} | Equipo completo de un entrenador |
| POST | /teams | Crear equipo de usuario |
| GET | /teams/{id} | Obtener equipo |
| DELETE | /teams/{id} | Borrar equipo |
