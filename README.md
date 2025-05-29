# Instagram Followers Extractor

Script para extraer información pública de seguidores de cuentas de Instagram y exportarla a Excel o CSV.

## Características
- Extrae seguidores de cuentas objetivo (ej: @elcorteingles, @mercadona, @carrefoures)
- Exporta datos a Excel y/o CSV
- Solo usa datos públicos

## Uso rápido
1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el script:
   ```bash
   python main.py
   ```
   Opciones:
   - `--max-followers N` para limitar seguidores
   - `--accounts cuenta1 cuenta2` para cuentas específicas
   - `--output-dir ./resultados` para cambiar carpeta de salida

## Notas
- Para mejor estabilidad, configura usuario/contraseña en `.env` (ver `env_example.txt`).
- Cumple términos de servicio de Instagram.
