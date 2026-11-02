# Prodato

API para consultar información de productos a partir de su código de barras, desarrollada con **FastAPI**.

Prodato busca facilitar el registro de productos en sistemas de ventas, inventarios y tiendas virtuales: una consulta
devuelve el nombre, la marca, el contenido, el tipo de envase y las imágenes disponibles.

**Estado:** MVP en desarrollo. Los endpoints y el modelo de datos descritos a continuación constituyen el contrato
propuesto.

## Alcance inicial

- Consulta de productos por código de barras EAN/UPC.
- Catálogo inicial enfocado en productos comercializados en Perú.
- Información de la presentación exacta: por ejemplo, una botella de 500 ml.
- Imágenes del producto mediante URL.

Cada presentación se registra por separado. Una botella de 500 ml y otra de 1,5 L son registros distintos.

El catálogo contiene información compartida del producto. El precio de venta y el stock los administra cada tienda en su
propio sistema.

## Contrato de consulta

```http
GET /v1/products/by-barcode/{barcode}
```

Ejemplo de llamada local, una vez implementada la ruta:

```bash
curl http://127.0.0.1:8000/v1/products/by-barcode/1234567890128
```

Respuesta ilustrativa con HTTP `200 OK`:

```json
{
  "id": "a317493a-7b3e-42f4-865c-c703b6b17d32",
  "barcode": "01234567890128",
  "name": "Inca Kola 500 ml",
  "brand": "Inca Kola",
  "category": "Gaseosas",
  "net_content": {
    "value": 500,
    "unit": "ml"
  },
  "packaging": "pet_bottle",
  "images": [
    {
      "url": "https://cdn.example.com/products/inca-kola-500ml.webp",
      "alt_text": "Botella de Inca Kola de 500 ml"
    }
  ],
  "updated_at": "2026-11-02T15:00:00Z"
}
```

El código y la imagen del ejemplo no representan una ficha real del catálogo ni vinculan ese código con Inca Kola.

### Reglas del contrato

- Los códigos se reciben como texto, conservando los ceros iniciales.
- Se admiten GTIN de 8, 12, 13 o 14 dígitos, con validación de longitud y dígito de control.
- Antes de guardar o buscar, se normalizan a 14 dígitos completando con ceros a la izquierda. La respuesta devuelve esa
  representación canónica.
- `id` identifica el registro interno; `barcode` identifica el artículo comercial.
- Los datos desconocidos se devuelven como `null`. Si no se conoce el contenido, `net_content` es `null`.
- Si no hay imágenes, `images` es `[]`. La primera imagen es la principal.
- `net_content.unit` utiliza valores como `ml`, `l`, `g`, `kg` o `unit`.
- `packaging` utiliza valores como `pet_bottle`, `glass_bottle`, `can` o `bag`.
- Las fechas se devuelven en ISO 8601 con zona horaria UTC.

### Respuestas previstas

| Código HTTP | Significado                                   |
|-------------|-----------------------------------------------|
| `200`       | Producto encontrado                           |
| `404`       | No existe una ficha para el código consultado |
| `422`       | El código recibido no supera la validación    |

## Ejecución local

Ejecuta los siguientes comandos desde la raíz del repositorio. La API se ejecuta con uv y PostgreSQL se inicia
con Docker Compose.

### Requisitos

- Python 3.14 o superior.
- uv instalado.
- Docker y Docker Compose disponibles, con el servicio Docker iniciado.

Si ya tienes PostgreSQL accesible y una base de datos creada, puedes omitir el paso de Docker Compose y ajustar
`APP_DATABASE_URL` a tu conexión.

### 1. Instalar dependencias

```bash
uv sync --locked
```

Este comando crea el entorno virtual `.venv` e instala las versiones registradas en `uv.lock`.

### 2. Configurar la conexión

Copia [`.env.example`](.env.example) a `.env.dev` en la raíz del proyecto:

```bash
cp .env.example .env.dev
```

El archivo incluye las credenciales de desarrollo del PostgreSQL definido en [`compose.yaml`](compose.yaml):

```dotenv
APP_DATABASE_URL=postgresql+asyncpg://prodato:prodato@127.0.0.1:5432/prodato_dev
```

La aplicación carga `.env.dev` por defecto. Las variables de configuración utilizan el prefijo `APP_`.
Puedes ajustar `APP_DATABASE_URL`, `APP_DEBUG` y `APP_ALLOWED_ORIGINS` en ese archivo según tu entorno.

### 3. Iniciar PostgreSQL

```bash
docker compose up -d --wait postgres
```

Compose crea la base de datos `prodato_dev` y espera a que PostgreSQL esté listo para aceptar conexiones en
`127.0.0.1:5432`.

Si el puerto 5432 está ocupado, puedes utilizar otro:

```bash
POSTGRES_PORT=5433 docker compose up -d --wait postgres
```

En ese caso, cambia también el puerto de `APP_DATABASE_URL` a `5433` en `.env.dev`.

### 4. Aplicar migraciones

```bash
uv run alembic upgrade head
```

Este comando aplica las migraciones disponibles. No carga productos de ejemplo.

### 5. Iniciar el servidor

```bash
uv run uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`. La opción `--reload` reinicia el servidor cuando cambias el código
y se utiliza durante el desarrollo.

Para comprobar que responde, ejecuta en otra terminal:

```bash
curl http://127.0.0.1:8000/
```

La respuesta esperada es `{"message":"Welcome to the API!!!"}`. La documentación está disponible en:

| Recurso      | Dirección                          |
|--------------|------------------------------------|
| Swagger UI   | http://127.0.0.1:8000/docs         |
| ReDoc        | http://127.0.0.1:8000/redoc        |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |

### 6. Detener el entorno

Detén Uvicorn con `Ctrl+C` en la terminal donde se está ejecutando y detén PostgreSQL con:

```bash
docker compose stop postgres
```

## Desarrollo de migraciones

Después de modificar los modelos:

```bash
uv run alembic revision --autogenerate -m "describe_schema_change"
```

Revisa la migración generada antes de aplicarla:

```bash
uv run alembic upgrade head
```

Para que Alembic detecte las tablas, los módulos de los modelos deben estar importados cuando se configura
`target_metadata` en `alembic/env.py`.

## Documentación de referencia

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [uv](https://docs.astral.sh/uv/guides/projects/)
- [Representación de GTIN — GS1](https://support.gs1.org/support/solutions/articles/43000734355-what-is-the-required-format-of-gtin-in-gs1-edi-standards-)
