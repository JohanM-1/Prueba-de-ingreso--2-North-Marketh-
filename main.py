#!/usr/bin/env python3
"""
Script principal para extraer datos de seguidores de Instagram.

Extrae información pública de seguidores de las cuentas:
- @elcorteingles
- @mercadona  
- @carrefoures

Requisitos según PRD:
- Mínimo 100 seguidores por cuenta (300 total)
- Datos públicos únicamente
- Exportación a Excel
- Cumplimiento de términos de servicio
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any
import time

# Agregar src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config.settings import TARGET_ACCOUNTS, OUTPUT_SETTINGS, is_login_enabled, get_instagram_credentials
from src.extractors.instagram_extractor import InstagramExtractor
from src.exporters.excel_exporter import ExcelExporter
from src.utils.helpers import create_directories, format_timestamp


def parse_arguments():
    """
    Parsea argumentos de línea de comandos.
    
    Returns:
        Argumentos parseados
    """
    parser = argparse.ArgumentParser(
        description="Extractor de datos de seguidores de Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                                    # Extraer de todas las cuentas (100 por cuenta)
  python main.py --limit 50                        # Extraer 50 seguidores por cuenta
  python main.py --accounts elcorteingles mercadona # Solo cuentas específicas
  python main.py --output-dir ./resultados         # Directorio de salida personalizado
  python main.py --debug                           # Modo debug con logging detallado

Configuración de autenticación:
  - Copia env_example.txt a .env y configura INSTAGRAM_USERNAME/INSTAGRAM_PASSWORD
  - El login mejora la estabilidad y permite acceso a más datos públicos
        """
    )
    
    parser.add_argument(
        '--accounts',
        nargs='+',
        default=list(TARGET_ACCOUNTS.keys()),
        choices=list(TARGET_ACCOUNTS.keys()),
        help='Cuentas de Instagram a procesar (default: todas)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='data/output',
        help='Directorio de salida para archivos (default: data/output)'
    )
    
    parser.add_argument(
        '--export-format',
        choices=['excel', 'csv', 'both'],
        default='excel',
        help='Formato de exportación (default: excel)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Activar modo debug con logging detallado'
    )
    
    parser.add_argument(
        '--no-selenium',
        action='store_true',
        help='Usar solo Instaloader (sin Selenium)'
    )
    
    parser.add_argument(
        '--delay',
        type=int,
        default=5,
        help='Delay en segundos entre extracción de perfiles (default: 5)'
    )
    
    parser.add_argument(
        '--max-followers',
        type=int,
        default=None,
        help='Máximo número de seguidores a extraer por cuenta (default: todos)'
    )
    
    return parser.parse_args()


def setup_environment(args):
    """
    Configura el entorno de ejecución.
    
    Args:
        args: Argumentos parseados
    """
    # Crear directorios necesarios
    create_directories([
        'data/output',
        args.output_dir
    ])


def validate_requirements(args) -> bool:
    """
    Valida que se cumplan los requisitos del PRD.
    
    Args:
        args: Argumentos parseados
        
    Returns:
        True si todos los requisitos se cumplen
    """
    # Validar cuentas objetivo
    for account in args.accounts:
        if account not in TARGET_ACCOUNTS:
            return False
    
    return True


def extract_followers_data(args) -> Dict[str, List[Dict[str, Any]]]:
    """
    Ejecuta la extracción de datos de seguidores.
    
    Args:
        args: Argumentos parseados
        
    Returns:
        Datos extraídos por cuenta
    """
    # Limitar la cantidad de cuentas si se especifica --max-accounts
    accounts_to_process = args.accounts
    
    # Inicializar extractor
    with InstagramExtractor() as extractor:
        # Configurar delay personalizado si se especifica
        if hasattr(args, 'delay'):
            from src.config.settings import RATE_LIMITS
            RATE_LIMITS['delay_between_profiles'] = args.delay
        
        # Extraer datos de todas las cuentas
        results = extractor.extract_multiple_accounts(accounts_to_process, max_followers=args.max_followers)
        
    
    return results


def export_data(data: Dict[str, List[Dict[str, Any]]], args) -> List[str]:
    """
    Exporta los datos extraídos según el formato especificado.
    
    Args:
        data: Datos a exportar
        args: Argumentos con configuración de exportación
        
    Returns:
        Lista de archivos generados
    """
    # Inicializar exportador
    exporter = ExcelExporter(output_dir=args.output_dir)
    generated_files = []
    
    # Exportar según formato especificado
    if args.export_format in ['excel', 'both']:
        timestamp = format_timestamp()
        excel_filename = f"instagram_followers_{timestamp}.xlsx"
        
        excel_path = exporter.export_to_excel(data, excel_filename)
        generated_files.append(excel_path)
    
    if args.export_format in ['csv', 'both']:
        csv_files = exporter.export_to_csv(data, args.output_dir)
        generated_files.extend(csv_files)
    
    return generated_files


def main():
    """Función principal del script."""
    try:
        # Parsear argumentos
        args = parse_arguments()
        
        # Configurar entorno
        setup_environment(args)
        
        # Validar requisitos
        if not validate_requirements(args):
            sys.exit(1)
        
        # Extraer datos
        data = extract_followers_data(args)
        # Exportar datos
        export_data(data, args)
        
    except KeyboardInterrupt:
        sys.exit(1)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 