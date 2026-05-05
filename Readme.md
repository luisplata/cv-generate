# 📄 Generador de CV Personalizado

Sistema automatizado para generar CVs personalizados en PDF a partir de plantillas LaTeX y archivos YAML, con soporte multi-idioma.

## 🚀 Características

- ✅ Generación automática de CVs en PDF
- 🌍 Soporte multi-idioma (español, inglés, etc.)
- 📝 Personalización por oferta de trabajo
- 🎨 Templates LaTeX personalizables
- 🔗 Links parametrizables por oferta
- 📸 Soporte para foto de perfil (opcional)
- ⚡ Filtrado inteligente de experiencia según roles

## 📋 Requisitos

- Python 3.10+
- pdflatex (LaTeX) - MiKTeX (Windows) o TeX Live (Linux/macOS)
- Git (opcional)

## 🔧 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repo-url>
   cd cv-generate
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   - Windows (PowerShell/CMD): `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
   - Git Bash: `source venv/Scripts/activate`

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Edita .env con tus datos
   ```

## 📁 Estructura del Proyecto

```
cv-generate/
├── data/
│   ├── master/
│   │   └── master.yaml          # Datos maestros (experiencia, educación, etc.)
│   └── offers/
│       ├── ejemplo_simple.yaml  # Ejemplo: Oferta mono-idioma
│       └── ejemplo_multilang.yaml # Ejemplo: Oferta multi-idioma
├── templates/
│   ├── ats.tex                  # Template por defecto
│   ├── ats_es.tex              # Template en español
│   └── ats_en.tex              # Template en inglés
├── build/                       # PDFs generados (auto-creado)
├── .env                         # Variables de entorno
├── generate.py                  # Script principal
└── requirements.txt             # Dependencias Python
```

## ⚙️ Configuración

### 1. Variables de Entorno (.env)

```env
NAME=Tu Nombre Completo
LOCATION=Ciudad, País
EMAIL=tu@email.com
PHONE=+57 3001234567

# Idiomas a generar (separados por coma)
LANGUAGES=es,en

# URL de tu foto (opcional)
PHOTO_URL=https://ejemplo.com/foto.jpg

# Links (dejar vacío si no tienes)
PORTFOLIO=https://tu-portfolio.com
GITHUB=https://github.com/tuusuario
LINKEDIN=https://linkedin.com/in/tuusuario
ITCH=
```

### 2. Master YAML (data/master/master.yaml)

Contiene toda tu información profesional. Soporta multi-idioma.

**Ver archivo de ejemplo:** `data/master/master.example.yaml`

### 3. Ofertas YAML (data/offers/)

Cada archivo representa una personalización para una oferta específica.

#### Oferta Simple (mono-idioma)

**Ver archivo de ejemplo:** `data/offers/ejemplo_simple.yaml`

#### Oferta Multi-idioma

**Ver archivo de ejemplo:** `data/offers/ejemplo_multilang.yaml`

## 🎯 Uso

### Generar todos los CVs

```bash
python generate.py
```

Los PDFs se generan en `build/<nombre_oferta>/`

### Generar solo en español

En `.env`:
```env
LANGUAGES=es
```

### Generar en múltiples idiomas

En `.env`:
```env
LANGUAGES=es,en
```

Para ofertas multi-idioma, genera automáticamente:
- `oferta_es.pdf`
- `oferta_en.pdf`

## 📝 Crear una Nueva Oferta

1. **Copia un ejemplo**
   ```bash
   cp data/offers/ejemplo_simple.yaml data/offers/Mi_Oferta_VASS.yaml
   ```

2. **Edita el archivo**
   - Modifica `profile.title` y `profile.summary`
   - Ajusta `focus.roles` (roles que quieres filtrar)
   - Actualiza `focus.skills` (habilidades relevantes)
   - Personaliza `links` si es necesario

3. **Genera el PDF**
   ```bash
   python generate.py
   ```

4. **Resultado**
   ```
   build/Mi_Oferta_VASS/Mi_Oferta_VASS.pdf
   ```

## 🌍 Multi-idioma

### Estructura de Oferta Multi-idioma

```yaml
profile:
  es:
    title: "Ingeniero de Software"
    summary: "Descripción en español..."
  en:
    title: "Software Engineer"
    summary: "Description in English..."

focus:
  roles:
    - Software Engineer
    - Backend Developer
  skills:
    es:
      - Python
      - Django
    en:
      - Python
      - Django
```

### Estructura de Master Multi-idioma

```yaml
experience:
  - company: "Empresa S.A."
    period:
      es: "Enero 2020 – Presente"
      en: "January 2020 – Present"
    roles:
      - Software Engineer
    achievements:
      es:
        - Desarrollé APIs REST
      en:
        - Developed REST APIs
```

## 🔗 Links Personalizados

### Desde .env (global)

```env
PORTFOLIO=https://portfolio.com
GITHUB=https://github.com/user
```

### Por oferta (YAML)

```yaml
links:
  - name: "Portfolio"
    url: "https://mi-portfolio.com"
  - name: "GitHub"
    url: "https://github.com/usuario"
  - name: "GameJolt"
    url: "https://gamejolt.com/@usuario"
```

## 🎨 Personalizar Templates

Los templates LaTeX están en `templates/`:

- `ats_es.tex` - Encabezados en español
- `ats_en.tex` - Encabezados en inglés

Edita estos archivos para cambiar el diseño visual.

## 🎯 Personalización por Rol

El sistema permite personalizar los achievements de cada experiencia según el rol de la oferta:

### Estructura en master.yaml

```yaml
experience:
  - company: "Empresa S.A."
    period:
      es: "Enero 2020 – Presente"
      en: "January 2020 – Present"
    roles: [backend, fullstack]
    achievements:
      # Achievements por defecto (se usan si no hay específicos del rol)
      es:
        - Desarrollé aplicaciones web
      en:
        - Developed web applications
      
      # Achievements específicos para rol backend
      backend:
        es:
          - Diseñé arquitectura de microservicios
          - Implementé APIs RESTful de alto rendimiento
        en:
          - Designed microservices architecture
          - Implemented high-performance RESTful APIs
      
      # Achievements específicos para rol fullstack
      fullstack:
        es:
          - Desarrollé aplicaciones full-stack con React y Node.js
        en:
          - Developed full-stack applications with React and Node.js
```

### Cómo funciona

1. **Se muestra toda la experiencia** (no hay filtrado por roles)
2. Si en la oferta defines `focus.roles: [backend]`, y existe `achievements.backend` en master.yaml, se usan esos achievements
3. Si no existen achievements específicos del rol, se usan los generales (`es`/`en`)
4. Esto te permite tener **un solo master.yaml** con múltiples versiones de tus logros según el puesto

### En la oferta

```yaml
focus:
  roles:
    - backend  # Usará achievements.backend si existen
```

## 🐛 Troubleshooting

### Error: "pdflatex not found"

Instala LaTeX:
- **Windows**: [MiKTeX](https://miktex.org/download)
- **macOS**: `brew install mactex`
- **Linux**: `sudo apt install texlive-full`

### Error: "ModuleNotFoundError: No module named 'yaml'"

```bash
pip install -r requirements.txt
```

### El PDF no muestra experiencia

Verifica que tengas experiencias definidas en `master.yaml`. Ahora **toda la experiencia se muestra**, independientemente de los roles.

### Los achievements no son los esperados

Verifica la estructura de `achievements` en `master.yaml`:
- Si tienes `achievements.backend`, se usará cuando `focus.roles` incluya `backend`
- Si no hay achievements específicos del rol, se usan los generales (`es`/`en`)

### Links no aparecen

- Verifica que estén en `.env` O en el YAML de la oferta
- Asegúrate de que `show.links: true` en la oferta

## 📚 Ejemplos de Uso

Ver archivos de ejemplo:
- **Master**: `data/master/master.example.yaml` - Plantilla con todos tus datos profesionales
- **Oferta simple**: `data/offers/ejemplo_simple.example.yaml` - CV mono-idioma
- **Oferta multi-idioma**: `data/offers/ejemplo_multilang.example.yaml` - CV en español e inglés
- **Variables de entorno**: `.env.example` - Configuración de datos personales
- **Guía rápida**: `QUICKSTART.md` - Pasos para empezar en 5 minutos

### Comenzar desde Cero

1. Copia los ejemplos:
   ```bash
   cp .env.example .env
   cp data/master/master.example.yaml data/master/master.yaml
   cp data/offers/ejemplo_simple.example.yaml data/offers/MiPrimeraOferta.yaml
   ```

2. Edita con tus datos:
   - `.env` - Tus datos personales
   - `data/master/master.yaml` - Tu experiencia completa
   - `data/offers/MiPrimeraOferta.yaml` - Personalización para la oferta

3. Genera:
   ```bash
   python generate.py
   ```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

MIT License - Libre para uso personal y comercial.