"""
Configuración central del extractor de Instagram.
"""
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import os

# Intentar cargar variables de entorno desde archivo .env
try:
    # Buscar archivo .env en el directorio raíz del proyecto
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Variables de entorno cargadas desde: {env_path}")
    else:
        print("ℹ️  Archivo .env no encontrado - usando valores por defecto")
except Exception as e:
    print(f"⚠️  Error cargando variables de entorno: {e}")

def get_env_variable(var_name: str, default=None, var_type=str):
    """
    Obtiene variable de entorno con conversión de tipo.
    
    Args:
        var_name: Nombre de la variable
        default: Valor por defecto
        var_type: Tipo de dato esperado
        
    Returns:
        Valor de la variable convertido al tipo especificado
    """
    value = os.getenv(var_name)
    
    if value is None:
        return default
    
    if var_type == bool:
        return value.lower() in ('true', '1', 'yes', 'on')
    elif var_type == int:
        try:
            return int(value)
        except ValueError:
            return default
    elif var_type == float:
        try:
            return float(value)
        except ValueError:
            return default
    else:
        return value

# Cuentas objetivo según PRD
TARGET_ACCOUNTS = {
    'elcorteingles': {
        'username': 'elcorteingles',
        'name': 'El Corte Inglés',
        'sector': 'Retail/Moda',
        'min_followers': 100
    },
    'mercadona': {
        'username': 'mercadona', 
        'name': 'Mercadona',
        'sector': 'Supermercados',
        'min_followers': 100
    },
    'carrefoures': {
        'username': 'carrefoures',
        'name': 'Carrefour España', 
        'sector': 'Supermercados',
        'min_followers': 100
    }
}

# Campos requeridos según PRD sección 4.1
REQUIRED_FIELDS = {
    'mandatory': [
        'username',
        'full_name', 
        'is_private',
        'extraction_timestamp',
        'source_account'
    ],
    'optional': [
        'phone_numbers',
        'account_created_date',
        'first_post_date',
        'last_post_date',
        'follower_count',
        'following_count', 
        'posts_count',
        'is_verified',
        'bio',
        'external_url'
    ]
}

# Configuración de rate limiting y compliance (con variables de entorno)
RATE_LIMITS = {
    'requests_per_minute': get_env_variable('MAX_REQUESTS_PER_MINUTE', 20, int),
    'delay_between_requests': get_env_variable('CUSTOM_DELAY_BETWEEN_REQUESTS', 3, int),
    'delay_between_profiles': get_env_variable('CUSTOM_DELAY_BETWEEN_PROFILES', 5, int),
    'max_retries': get_env_variable('MAX_RETRIES', 3, int),
    'backoff_factor': get_env_variable('BACKOFF_MULTIPLIER', 2, int),
    'timeout': get_env_variable('REQUEST_TIMEOUT', 30, int),
    # Nuevas configuraciones para modo abuelo
    'delay_variation': get_env_variable('DELAY_VARIATION', 2, int),
    'account_break_minutes': get_env_variable('ACCOUNT_BREAK_MINUTES', 5, int),
    'conservative_mode': get_env_variable('CONSERVATIVE_MODE', False, bool),
    'skip_on_error': get_env_variable('SKIP_ON_ERROR', False, bool),
    'enable_random_waits': get_env_variable('ENABLE_RANDOM_WAITS', False, bool)
}

# Configuración de salida (con variables de entorno)
OUTPUT_SETTINGS = {
    'excel_filename': 'instagram_followers_data.xlsx',
    'sheet_prefix': 'Seguidores_',
    'include_metadata': get_env_variable('INCLUDE_METADATA', True, bool),
    'date_format': get_env_variable('DATE_FORMAT', '%Y-%m-%d'),
    'datetime_format': get_env_variable('DATETIME_FORMAT', '%Y-%m-%d %H:%M:%S')
}

# Configuración de Selenium (sin detección de navegador por ahora para evitar import circular)
SELENIUM_CONFIG_BASE = {
    'headless': get_env_variable('SELENIUM_HEADLESS', True, bool),
    'window_size': (
        get_env_variable('SELENIUM_WINDOW_WIDTH', 1920, int),
        get_env_variable('SELENIUM_WINDOW_HEIGHT', 1080, int)
    ),
    'implicit_wait': 10,
    'page_load_timeout': 30,
    'enable_cookies': get_env_variable('ENABLE_COOKIES', True, bool),
    'enable_user_agent_rotation': get_env_variable('ENABLE_USER_AGENT_ROTATION', True, bool),
    'stealth_mode': get_env_variable('STEALTH_MODE', True, bool),
    'disable_images': get_env_variable('DISABLE_IMAGES', True, bool),
    'use_real_browser_profile': get_env_variable('USE_REAL_BROWSER_PROFILE', False, bool),
}

def initialize_browser_detection():
    """Inicializa la detección de navegador cuando sea necesario."""
    try:
        from src.utils.browser_detector import BrowserDetector, get_realistic_user_agents
        
        browser_detector = BrowserDetector()
        browser_info = browser_detector.get_detection_info()
        
        # Actualizar configuración con detección de navegador
        SELENIUM_CONFIG_BASE.update({
            'user_agents': get_realistic_user_agents(15),
            'detected_browser': browser_info['default_browser'],
            'detected_version': browser_info['browser_version'],
            'browser_options': browser_info['browser_options'],
        })
        
        return True
    except Exception as e:
        print(f"⚠️  Error en detección de navegador: {e}")
        # Fallback a user agents básicos
        SELENIUM_CONFIG_BASE.update({
            'user_agents': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
            ],
            'detected_browser': 'chrome',
            'detected_version': '125.0.0.0',
            'browser_options': {}
        })
        return False

# Usar la configuración base como SELENIUM_CONFIG
SELENIUM_CONFIG = SELENIUM_CONFIG_BASE

# Configuración de logging (con variables de entorno)
LOGGING_CONFIG = {
    'level': get_env_variable('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'filename': 'instagram_extractor.log',
    'max_bytes': get_env_variable('LOG_FILE_SIZE_MB', 10, int) * 1024 * 1024,  # Convertir MB a bytes
    'backup_count': get_env_variable('LOG_BACKUP_COUNT', 5, int)
}

# Patrones regex para validación
VALIDATION_PATTERNS = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone_international': r'^\+\d{1,4}\s\d{3}\s\d{3}\s\d{3}$',
    'phone_loose': r'[\+]?[\d\s\-\(\)]{10,}',
    'username': r'^[a-zA-Z0-9._-]+$',
    'url': r'^https?://[^\s/$.?#].[^\s]*$'
}

# Paths de datos (con variables de entorno)
DATA_PATHS = {
    'raw': 'data/raw',
    'processed': 'data/processed', 
    'output': 'data/output',
    'logs': 'logs',
    'temp': get_env_variable('TEMP_DATA_DIR', 'data/temp'),
    'backup': get_env_variable('BACKUP_DIR', 'backups')
}

# Configuración de Instagram específica (con variables de entorno)
INSTAGRAM_CONFIG = {
    'base_url': 'https://www.instagram.com',
    'login_required': False,  # Se actualiza automáticamente si hay credenciales
    'max_followers_per_account': get_env_variable('MAX_FOLLOWERS_PER_ACCOUNT', 150, int),
    'scroll_pause_time': 2,
    'selectors': {
        'followers_button': 'a[href*="/followers/"]',
        'followers_list': '[role="dialog"] div[style*="padding-bottom"]',
        'profile_link': 'a[role="link"]',
        'profile_name': 'div._ap3a._aaco._aacw._aacx._aad7._aade',
        'follower_count': 'meta[property="og:description"]',
        'bio': 'div._aa_c h1',
        'external_link': 'div._aa_c a[target="_blank"]',
        'verified_badge': 'div[title="Verified"]'
    }
}

# Configuración desde variables de entorno
INSTAGRAM_USERNAME = get_env_variable('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = get_env_variable('INSTAGRAM_PASSWORD')
PROXY_LIST = get_env_variable('PROXY_LIST', '').split(',') if get_env_variable('PROXY_LIST') else []
DEBUG_MODE = get_env_variable('DEBUG_MODE', False, bool)

# Configuración de backup automático
AUTO_BACKUP = get_env_variable('AUTO_BACKUP', True, bool)

# Configuración de notificaciones (para futuras mejoras)
NOTIFICATION_EMAIL = get_env_variable('NOTIFICATION_EMAIL')
WEBHOOK_URL = get_env_variable('WEBHOOK_URL')

# Actualizar configuración basada en credenciales disponibles
if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
    INSTAGRAM_CONFIG['login_required'] = True
    print(f"✅ Credenciales de Instagram configuradas para usuario: {INSTAGRAM_USERNAME}")
else:
    print("ℹ️  No se configuraron credenciales de Instagram - modo solo datos públicos")

# Validar configuración de proxies
if PROXY_LIST and PROXY_LIST != ['']:
    print(f"✅ Configurados {len(PROXY_LIST)} proxies")

# Mostrar configuración cargada (solo en modo debug)
if DEBUG_MODE:
    print("🔧 Configuración DEBUG activada:")
    print(f"  - Rate limits: {RATE_LIMITS['delay_between_requests']}s entre requests")
    print(f"  - Selenium headless: {SELENIUM_CONFIG['headless']}")
    print(f"  - Log level: {LOGGING_CONFIG['level']}")
    print(f"  - Auto backup: {AUTO_BACKUP}")
    
    # Información específica del modo abuelo
    if RATE_LIMITS['conservative_mode']:
        print("👴 MODO ABUELO ACTIVADO:")
        print(f"  - Delay variation: ±{RATE_LIMITS['delay_variation']}s")
        print(f"  - Account breaks: {RATE_LIMITS['account_break_minutes']} minutos")
        print(f"  - Skip on error: {RATE_LIMITS['skip_on_error']}")
        print(f"  - Random waits: {RATE_LIMITS['enable_random_waits']}")

def get_instagram_credentials():
    """
    Obtiene las credenciales de Instagram si están disponibles.
    
    Returns:
        Tuple (username, password) o (None, None)
    """
    return (INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD) if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD else (None, None)

def is_login_enabled():
    """
    Verifica si el login está habilitado.
    
    Returns:
        bool: True si hay credenciales configuradas
    """
    return bool(INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD)

def get_proxy_list():
    """
    Obtiene lista de proxies configurados.
    
    Returns:
        List[str]: Lista de proxies en formato host:port
    """
    return [proxy.strip() for proxy in PROXY_LIST if proxy.strip()]

def is_conservative_mode():
    """
    Verifica si está activado el modo conservativo (abuelo).
    
    Returns:
        bool: True si está en modo abuelo
    """
    return RATE_LIMITS['conservative_mode']

def get_mode_description():
    """
    Obtiene descripción del modo actual basado en la configuración.
    
    Returns:
        str: Descripción del modo actual
    """
    delay_requests = RATE_LIMITS['delay_between_requests']
    delay_profiles = RATE_LIMITS['delay_between_profiles']
    
    if RATE_LIMITS['conservative_mode']:
        return "👴 Modo Abuelo (máxima paciencia)"
    elif delay_requests >= 8 and delay_profiles >= 15:
        return "🐌 Modo Lento (seguro)"
    elif delay_requests <= 3 and delay_profiles <= 5:
        return "⚡ Modo Rápido (riesgo de bloqueo)"
    else:
        return "🚀 Modo Normal (equilibrado)" 