# 🧭 CONTRIBUTING.md — Guía de Contribución Personal y OSS

> 📅 Generado el 2025-10-18 con la asistencia de **IA (ChatGPT - GPT‑5)** como mentor técnico.  
> Autor: **Nicolás Castañeda** — Proyecto *Backend Roadmap 2025*  
> Propósito: Documentar el flujo Git profesional y las buenas prácticas de contribución personal y open source.

---

## ⚙️ 1. Flujo Git Personal

### 🧱 Ramas principales

| Rama | Propósito |
|------|------------|
| `main` | Versión estable del proyecto. Siempre debe compilar y pasar tests. |
| `dev` | Rama de integración, donde se combinan los features antes de pasar a `main`. |
| `feature/*` | Nuevas funcionalidades o módulos del roadmap. |
| `fix/*` | Correcciones o mejoras pequeñas. |
| `chore/*` | Cambios no funcionales: configuración, CI/CD, dependencias, etc. |

**Ejemplos de nombres:**
```bash
feature/week2-fastapi
fix/typo-in-database-url
chore/add-ci-workflow
```

---

### 🔄 Flujo de trabajo recomendado

```bash
# 1. Partir desde dev
git checkout dev
git pull origin dev

# 2. Crear una nueva rama
git checkout -b feature/week2-fastapi

# 3. Desarrollar y hacer commits claros
git add .
git commit -m "feat: add FastAPI base app and health check endpoint"

# 4. Subir la rama
git push origin feature/week2-fastapi

# 5. Crear un Pull Request hacia dev
# (incluso si eres tú mismo el revisor)
```

#### ✅ Reglas de commit (Convencionales)
Sigue el estándar [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
<tipo>(<opcional>): <descripción>
```

| Tipo | Propósito |
|------|------------|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de errores |
| `docs:` | Documentación |
| `chore:` | Tareas de mantenimiento |
| `test:` | Añadir o mejorar tests |
| `refactor:` | Mejorar estructura sin cambiar comportamiento |
| `ci:` | Cambios en pipelines o workflows |

📘 Ejemplo:
```bash
feat(users): implement async repository pattern for user domain
fix(db): correct alembic migration naming
docs(readme): explain DDD-lite folder structure
```

---

### 🧪 Tests antes de mergear

Antes de hacer merge:
```bash
poetry run ruff check .
poetry run black --check .
poetry run mypy src/
poetry run pytest -q
```
Todos deben pasar ✅  
Esto asegura que `main` siempre esté **estable y limpia**.

---

### 🏷️ Versionado (SemVer)

Usa **Semantic Versioning (SemVer)** para etiquetar tus avances:

| Ejemplo | Descripción |
|----------|--------------|
| `v0.1.0` | Setup inicial y herramientas básicas |
| `v0.2.0` | FastAPI base + health routes |
| `v0.3.0` | SQLAlchemy integration |
| `v0.4.0` | Background tasks con Celery/Redis |

Comando:
```bash
git tag -a v0.3.0 -m "Add SQLAlchemy ORM integration"
git push origin main --tags
```

---

### 🧩 Estructura de Pull Request (PR)

Cada PR debe responder a:
1. **Qué** cambia.  
2. **Por qué** cambia.  
3. **Cómo** se probó.

Ejemplo:
```markdown
### 🧩 Descripción
Añade la configuración base de FastAPI con estructura DDD-lite.

### 🧠 Contexto
Forma parte de la Semana 2 del roadmap.  
Prepara la base para integrar SQLAlchemy en la próxima etapa.

### ✅ Checklist
- [x] Endpoint `/health`
- [x] Configuración de CORS
- [x] Test básico con pytest
```

Incluso si trabajas solo, estos PRs funcionan como **documentación viva** de tu progreso.

---

## 🌍 2. Guía para Contribuir en Open Source

> Cuando empieces a aplicar lo aprendido en proyectos reales (FastAPI, SQLAlchemy, etc.)

### 🧭 Pasos básicos

1. **Buscar un proyecto con buena documentación**
   - Ej: [FastAPI](https://github.com/tiangolo/fastapi), [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
2. **Hacer un fork y crear una rama**
   ```bash
   git clone https://github.com/<tu_usuario>/<repo_fork>.git
   git remote add upstream https://github.com/original/repo.git
   git checkout -b fix/docs-typo
   ```
3. **Sincronizar con el original (upstream)**
   ```bash
   git fetch upstream
   git merge upstream/main
   ```
4. **Hacer commits siguiendo el formato convencional**
5. **Crear un Pull Request explicativo**
   - Título claro: `fix(docs): correct typo in tutorial section`
   - Descripción corta y clara.
   - Adjuntar evidencia si aplica (logs, capturas, etc.)

---

### 📋 Checklist antes de abrir un PR OSS

- [ ] Ejecutaste `ruff`, `black`, y los tests locales.
- [ ] Usaste mensajes de commit limpios y convencionales.
- [ ] El cambio está justificado (no cosmético sin propósito).
- [ ] La rama está actualizada con `main`.
- [ ] Leíste las guías del proyecto (`CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`).
- [ ] Tu PR está redactado en inglés claro y profesional.

---

### 💡 Consejos OSS

| Situación | Buen enfoque |
|------------|---------------|
| PR rechazado | No te frustres; pregunta cómo mejorarlo. |
| PR sin respuesta | Espera 1–2 semanas, luego comenta cortésmente. |
| Error en CI | Lee el log, corrige localmente, sube un fix. |
| Dudas sobre estilo | Revisa PRs previos aceptados como guía. |

**Recuerda:** el respeto al proceso pesa más que el código perfecto.

---

## 🧾 Flujo resumido (recordatorio rápido)

```bash
# Proyecto personal
git checkout dev
git checkout -b feature/fastapi-base
poetry run pytest
git commit -m "feat: add FastAPI app skeleton"
git push origin feature/fastapi-base
git tag -a v0.2.0 -m "FastAPI base done"
git push origin main --tags

# OSS
git clone fork
git checkout -b fix/docs-example
git push origin fix/docs-example
# PR -> upstream main
```

---

## 📚 Recursos recomendados

- 🧱 [First Contributions Guide](https://github.com/firstcontributions/first-contributions)
- 💬 [FastAPI Contributing Guide](https://fastapi.tiangolo.com/contributing/)
- 🧩 [SQLAlchemy Contributing Guide](https://github.com/sqlalchemy/sqlalchemy/blob/main/CONTRIBUTING.rst)
- 🧠 [Python Developer’s Guide](https://devguide.python.org/)
- 🧰 [Good First Issues](https://goodfirstissue.dev/)

---

> ✨ Documento creado en colaboración con **ChatGPT (GPT‑5)**, actuando como mentor técnico para el aprendizaje y profesionalización de **Nicolás Castañeda** dentro del proyecto *Python Backend Roadmap 2025*.
