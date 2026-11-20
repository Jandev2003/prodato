# AGENTS.md

## Trabajo con APIs

Before responding to any non-trivial API engineering task — designing, implementing, mocking, testing, monitoring,
documenting, or deploying an API or Postman Flow — read `postman/skills/api-engineer/SKILL.md` and follow it. It is the
default entry point for API work in this repository. Pure questions and trivial one-line edits do not need it.

## Calidad del código

### Estilo de código

- Prioriza código fácil de leer. Prefiere soluciones simples y explícitas
  frente a expresiones compactas o "ingeniosas".
- Usa nombres descriptivos que comuniquen intención. Sin abreviaturas ambiguas.
- Funciones con una sola responsabilidad. No extraigas una función que se usa
  una vez si no mejora la lectura.
- Abstrae solo cuando exista repetición real (3+ usos) o un concepto claro del
  dominio. No añadas capas para necesidades hipotéticas, pero respeta las capas
  ya definidas en el proyecto.
- Reduce la anidación con early returns. Usa constantes con nombre en lugar de
  números o strings mágicos.
- Tipado obligatorio en funciones públicas.

### Comentarios y docstrings

- Redacta los comentarios y docstrings en español. Conserva los nombres técnicos,
  identificadores y referencias a librerías tal como aparecen en el código.
- Añade comentarios solo cuando aporten contexto que no sea evidente al leer el
  código: decisiones de diseño, reglas de negocio, restricciones, casos límite
  o el orden necesario de un flujo complejo.
- Al cambiar un comportamiento, actualiza o elimina los comentarios y docstrings
  que hayan quedado desactualizados.

### Verificación con Ruff

Antes de dar por terminada una tarea con cambios en Python, ejecuta
`uv run ruff check` desde la raíz del repositorio. Si Ruff reporta errores
relacionados con tus cambios, corrígelos y vuelve a ejecutar el comando para
verificar las correcciones.

## Verificación de endpoints

- Si añades, modificas o eliminas un endpoint HTTP, o cambias código que
  afecte su comportamiento, delega la verificación a `postman_verifier`
  antes de dar la tarea por terminada.

## Verificación de migraciones

- Si añades, modificas o eliminas migraciones, o cambias modelos ORM o
  configuración de Alembic que afecten el esquema, el agente principal debe
  delegar la verificación a `migration_verifier` antes de dar la tarea por terminada.
- Al crear o revisar una migración que cambie una columna existente de nullable
  a `NOT NULL`, incluye un paso que resuelva los `NULL` existentes mediante
  `UPDATE` con valores válidos según las reglas de negocio **antes** de aplicar
  la restricción.
- No inventes valores de relleno. Si no se puede deducir un valor válido,
  solicita la decisión necesaria antes de completar la migración.
- Usa `DELETE` únicamente cuando eliminar esos registros sea una decisión
  de negocio explícitamente autorizada.
- Un `server_default` en una columna existente no reemplaza la limpieza
  de los `NULL` previamente almacenados.
