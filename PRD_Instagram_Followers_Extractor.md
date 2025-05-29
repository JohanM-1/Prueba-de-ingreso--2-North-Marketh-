# PRD: Instagram Followers Data Extractor
## Product Requirements Document

**Proyecto:** Extractor de Datos de Seguidores de Instagram  
**Versión:** 1.0  
**Fecha:** Diciembre 2024  
**Propósito:** Prueba Técnica - Desarrollador Junior North Marketh  

---

## 1. Resumen Ejecutivo / Executive Summary

### Español
Este proyecto consiste en desarrollar un script en Python que extraiga información pública de los seguidores de tres cuentas específicas de Instagram (@elcorteingles, @mercadona y @carrefoures). El objetivo es recopilar datos de contacto y perfil de al menos 100 seguidores por cuenta, consolidando la información en un archivo Excel.

### English
This project involves developing a Python script that extracts public information from followers of three specific Instagram accounts (@elcorteingles, @mercadona and @carrefoures). The goal is to collect contact and profile data from at least 100 followers per account, consolidating the information into an Excel file.

---

## 2. Objetivos del Proyecto / Project Objectives

### Objetivos Principales / Main Objectives
- ✅ Extraer información pública de seguidores de Instagram
- ✅ Procesar datos de 3 cuentas específicas
- ✅ Obtener mínimo 100 registros por cuenta (300 total)
- ✅ Consolidar datos en formato Excel
- ✅ Crear video demostrativo del funcionamiento

### Objetivos Secundarios / Secondary Objectives
- 🔄 Implementar manejo de errores robusto
- 🔄 Optimizar velocidad de extracción
- 🔄 Garantizar cumplimiento de términos de servicio
- 🔄 Documentar código apropiadamente

---

## 3. Cuentas Objetivo / Target Accounts

| Cuenta | Nombre Comercial | Sector |
|--------|------------------|--------|
| @elcorteingles | El Corte Inglés | Retail/Moda |
| @mercadona | Mercadona | Supermercados |
| @carrefoures | Carrefour España | Supermercados |

---

## 4. Especificaciones de Datos / Data Specifications

### 4.1 Campos Requeridos / Required Fields

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `username` | String | ✅ | Nombre de usuario de Instagram |
| `full_name` | String | ✅ | Nombre completo del perfil |
| `phone_numbers` | List[String] | ❌ | Números de teléfono (si públicos) |
| `email_addresses` | List[String] | ❌ | Direcciones de email (si públicas) |
| `account_created_date` | Date | ❌ | Fecha de creación del perfil |
| `first_post_date` | Date | ❌ | Fecha de primera publicación |
| `last_post_date` | Date | ❌ | Fecha de última publicación |
| `follower_count` | Integer | ❌ | Número de seguidores |
| `following_count` | Integer | ❌ | Número de seguidos |
| `posts_count` | Integer | ❌ | Número de publicaciones |
| `is_verified` | Boolean | ❌ | Estado de verificación |
| `is_private` | Boolean | ✅ | Si la cuenta es privada |
| `bio` | String | ❌ | Biografía del perfil |
| `external_url` | String | ❌ | URL externa del perfil |
| `extraction_timestamp` | DateTime | ✅ | Momento de extracción |
| `source_account` | String | ✅ | Cuenta de la que es seguidor |

### 4.2 Reglas de Validación / Validation Rules

- **Teléfonos:** Formato internacional (+XX XXX XXX XXX)
- **Emails:** Validación RFC 5322
- **Fechas:** Formato ISO 8601 (YYYY-MM-DD)
- **Usernames:** Sin caracteres especiales excepto _, . y -

---

## 5. Requerimientos Técnicos / Technical Requirements

### 5.1 Tecnologías Obligatorias / Mandatory Technologies
- **Lenguaje:** Python 3.8+
- **Formato salida:** Excel (.xlsx)
- **Control versiones:** Git

### 5.2 Librerías Recomendadas / Recommended Libraries
```python
# Core libraries
requests>=2.28.0
beautifulsoup4>=4.11.0
selenium>=4.15.0
pandas>=1.5.0
openpyxl>=3.0.10

# Instagram API alternatives
instaloader>=4.9.0
instagram-private-api>=1.6.0

# Data processing
regex>=2022.10.31
python-dateutil>=2.8.2

# Utilities
tqdm>=4.64.0
python-dotenv>=0.19.0
```

### 5.3 Arquitectura del Sistema / System Architecture

```
instagram_followers_extractor/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── base_extractor.py
│   │   └── instagram_extractor.py
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── data_cleaner.py
│   │   └── data_validator.py
│   ├── exporters/
│   │   ├── __init__.py
│   │   └── excel_exporter.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── helpers.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── output/
├── tests/
├── docs/
├── requirements.txt
├── main.py
└── README.md
```

---

## 6. Funcionalidades / Features

### 6.1 Funcionalidades Core / Core Features

#### F1: Extracción de Seguidores
- **Descripción:** Obtener lista de seguidores de cada cuenta objetivo
- **Entrada:** Username de Instagram
- **Salida:** Lista de usernames de seguidores
- **Criterios de aceptación:**
  - Mínimo 100 seguidores por cuenta
  - Manejo de paginación
  - Rate limiting compliance

#### F2: Extracción de Datos de Perfil
- **Descripción:** Recopilar información pública de cada seguidor
- **Entrada:** Username de seguidor
- **Salida:** Diccionario con datos del perfil
- **Criterios de aceptación:**
  - Extracción de todos los campos especificados
  - Manejo de perfiles privados
  - Detección de datos de contacto en bio

#### F3: Procesamiento de Datos
- **Descripción:** Limpiar y validar datos extraídos
- **Entrada:** Datos raw
- **Salida:** Datos procesados y validados
- **Criterios de aceptación:**
  - Validación de formatos
  - Eliminación de duplicados
  - Normalización de datos

#### F4: Exportación a Excel
- **Descripción:** Generar archivo Excel con resultados
- **Entrada:** Datos procesados
- **Salida:** Archivo .xlsx
- **Criterios de aceptación:**
  - Una hoja por cuenta objetivo
  - Formato tabular claro
  - Metadatos de extracción

### 6.2 Funcionalidades Adicionales / Additional Features

#### F5: Logging y Monitoreo
- Registro detallado de actividades
- Métricas de rendimiento
- Manejo de errores

#### F6: Configuración
- Parámetros configurables
- Credenciales en archivo separado
- Opciones de salida

---

## 7. Consideraciones de Cumplimiento / Compliance Considerations

### 7.1 Términos de Servicio de Instagram
- ✅ Solo datos públicos
- ✅ Respeto al rate limiting
- ✅ No almacenamiento permanente sin consentimiento
- ✅ Uso para fines educativos/demostrativos

### 7.2 GDPR y Privacidad
- ⚠️ Datos personales mínimos
- ⚠️ Propósito específico y limitado
- ⚠️ No transferencia a terceros
- ⚠️ Eliminación tras demostración

### 7.3 Buenas Prácticas
- Delays entre requests
- User-Agent rotation
- Proxy rotation (opcional)
- Respeto a robots.txt

---

## 8. Entregables / Deliverables

### 8.1 Código
- ✅ Script Python funcional
- ✅ Documentación inline
- ✅ README con instrucciones
- ✅ requirements.txt

### 8.2 Datos
- ✅ Archivo Excel con resultados
- ✅ Mínimo 300 registros totales
- ✅ Estructura de datos definida

### 8.3 Documentación
- ✅ Video demostrativo
- ✅ Guía de instalación
- ✅ Documentación de API

### 8.4 Control de Versiones
- ✅ Repositorio Git
- ✅ Commits descriptivos
- ✅ Estructura organizada

---

## 9. Cronograma Estimado / Estimated Timeline

| Fase | Duración | Actividades |
|------|----------|-------------|
| **Fase 1: Setup** | 1 día | Configuración del entorno, investigación de APIs |
| **Fase 2: Desarrollo Core** | 3-4 días | Implementación de extracción y procesamiento |
| **Fase 3: Testing** | 1 día | Pruebas y depuración |
| **Fase 4: Documentación** | 1 día | README, comentarios, video demo |
| **Total** | **6-7 días** | |

---

## 10. Riesgos y Mitigaciones / Risks and Mitigations

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| **Rate Limiting** | Alta | Alto | Implementar delays, rotar proxies |
| **Cambios en Instagram API** | Media | Alto | Usar múltiples métodos de extracción |
| **Perfiles Privados** | Alta | Medio | Filtrar solo perfiles públicos |
| **Datos Incompletos** | Media | Medio | Validación y manejo de datos faltantes |
| **Bloqueo de IP** | Media | Alto | Rotar User-Agents y usar proxies |

---

## 11. Métricas de Éxito / Success Metrics

### Métricas Cuantitativas
- ✅ **300+ registros** extraídos (100 por cuenta)
- ✅ **>85% completitud** de datos obligatorios
- ✅ **<5% duplicados** en el dataset final
- ✅ **0 errores** críticos en el script

### Métricas Cualitativas
- ✅ Código limpio y documentado
- ✅ Video demo claro y profesional
- ✅ Cumplimiento de términos de servicio
- ✅ Estructura de datos coherente

---

## 12. Appendices / Anexos

### A. Ejemplo de Estructura de Datos
```json
{
  "username": "usuario_ejemplo",
  "full_name": "Juan Pérez García",
  "phone_numbers": ["+34 666 777 888"],
  "email_addresses": ["juan.perez@email.com"],
  "account_created_date": "2020-03-15",
  "first_post_date": "2020-03-20",
  "last_post_date": "2024-12-01",
  "follower_count": 1250,
  "following_count": 800,
  "posts_count": 45,
  "is_verified": false,
  "is_private": false,
  "bio": "Amante del deporte y la tecnología 📱⚽",
  "external_url": "https://ejemplo.com",
  "extraction_timestamp": "2024-12-02T10:30:00Z",
  "source_account": "@elcorteingles"
}
```

### B. Comandos de Instalación
```bash
# Clonar repositorio
git clone <repository_url>
cd instagram_followers_extractor

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar script
python main.py
```

---

**Fecha de creación:** Diciembre 2024  
**Última actualización:** Diciembre 2024  
**Estado:** Draft v1.0 