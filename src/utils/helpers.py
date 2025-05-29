"""
Funciones auxiliares para el extractor de Instagram.
"""

import re
import os
from pathlib import Path
from typing import List, Optional, Union, Any
from datetime import datetime

from ..config.settings import VALIDATION_PATTERNS


def clean_text(text: str) -> str:
    """
    Limpia y normaliza texto eliminando espacios extra y caracteres especiales.
    
    Args:
        text: Texto a limpiar
        
    Returns:
        Texto limpio
    """
    if not text:
        return ""
    
    # Eliminar saltos de línea y espacios extra
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Eliminar caracteres de control
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    return text


def extract_emails_from_text(text: str) -> List[str]:
    """
    Extrae direcciones de email de un texto.
    
    Args:
        text: Texto donde buscar emails
        
    Returns:
        Lista de emails encontrados
    """
    if not text:
        return []
    
    # Buscar emails con patrón estricto
    emails = re.findall(VALIDATION_PATTERNS['email'], text.lower())
    
    # Buscar emails con patrón más permisivo si no se encontraron
    if not emails:
        loose_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(loose_pattern, text)
    
    # Eliminar duplicados y validar
    unique_emails = []
    for email in emails:
        email = email.strip().lower()
        if email not in unique_emails and validate_email(email):
            unique_emails.append(email)
    
    return unique_emails


def extract_phones_from_text(text: str) -> List[str]:
    """
    Extrae números de teléfono de un texto.
    
    Args:
        text: Texto donde buscar teléfonos
        
    Returns:
        Lista de teléfonos encontrados
    """
    if not text:
        return []
    
    phones = []
    
    # Buscar patrones de teléfono
    phone_patterns = [
        r'\+\d{1,4}[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3}',  # Internacional
        r'\+\d{1,4}[\s-]?\d{9,12}',  # Internacional simple
        r'\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b',  # Nacional 9 dígitos
        r'\b\d{9}\b',  # 9 dígitos seguidos
    ]
    
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        phones.extend(matches)
    
    # Limpiar y formatear teléfonos
    cleaned_phones = []
    for phone in phones:
        phone = re.sub(r'[^\d+]', '', phone)
        if len(phone) >= 9 and phone not in cleaned_phones:
            # Formatear para España si no tiene código de país
            if not phone.startswith('+'):
                if len(phone) == 9:
                    phone = '+34' + phone
            cleaned_phones.append(phone)
    
    return cleaned_phones


def validate_email(email: str) -> bool:
    """
    Valida formato de email.
    
    Args:
        email: Email a validar
        
    Returns:
        True si es válido
    """
    return bool(re.match(VALIDATION_PATTERNS['email'], email))


def validate_username(username: str) -> bool:
    """
    Valida formato de username de Instagram.
    
    Args:
        username: Username a validar
        
    Returns:
        True si es válido
    """
    if not username:
        return False
    return bool(re.match(VALIDATION_PATTERNS['username'], username))


def safe_get_text(element, default: str = "") -> str:
    """
    Extrae texto de un elemento web de forma segura.
    
    Args:
        element: Elemento web
        default: Valor por defecto
        
    Returns:
        Texto del elemento o valor por defecto
    """
    try:
        if element:
            text = element.text.strip()
            return clean_text(text) if text else default
        return default
    except Exception:
        return default


def safe_get_attribute(element, attribute: str, default: str = "") -> str:
    """
    Extrae atributo de un elemento web de forma segura.
    
    Args:
        element: Elemento web
        attribute: Nombre del atributo
        default: Valor por defecto
        
    Returns:
        Valor del atributo o valor por defecto
    """
    try:
        if element:
            value = element.get_attribute(attribute)
            return value.strip() if value else default
        return default
    except Exception:
        return default


def create_directories(paths: List[Union[str, Path]]) -> None:
    """
    Crea directorios si no existen.
    
    Args:
        paths: Lista de rutas a crear
    """
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)


def format_timestamp(dt: datetime = None) -> str:
    """
    Formatea timestamp para uso en archivos y logs.
    
    Args:
        dt: Datetime a formatear (default: ahora)
        
    Returns:
        Timestamp formateado
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y%m%d_%H%M%S')


def sanitize_filename(filename: str) -> str:
    """
    Sanitiza nombre de archivo eliminando caracteres problemáticos.
    
    Args:
        filename: Nombre de archivo original
        
    Returns:
        Nombre de archivo sanitizado
    """
    # Eliminar caracteres problemáticos
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Eliminar espacios extra
    filename = re.sub(r'\s+', '_', filename.strip())
    
    # Limitar longitud
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext
    
    return filename


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Divide lista en chunks de tamaño específico.
    
    Args:
        lst: Lista a dividir
        chunk_size: Tamaño de cada chunk
        
    Returns:
        Lista de chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def extract_username_from_url(url: str) -> Optional[str]:
    """
    Extrae username de una URL de Instagram.
    
    Args:
        url: URL de Instagram
        
    Returns:
        Username extraído o None
    """
    if not url:
        return None
    
    # Patrón para URLs de Instagram
    pattern = r'instagram\.com/([a-zA-Z0-9._]+)/?'
    match = re.search(pattern, url)
    
    if match:
        username = match.group(1)
        return username if validate_username(username) else None
    
    return None


def is_valid_url(url: str) -> bool:
    """
    Valida si una URL tiene formato válido.
    
    Args:
        url: URL a validar
        
    Returns:
        True si es válida
    """
    return bool(re.match(VALIDATION_PATTERNS['url'], url))


def normalize_phone_number(phone: str, country_code: str = '+34') -> str:
    """
    Normaliza número de teléfono con código de país.
    
    Args:
        phone: Número de teléfono
        country_code: Código de país por defecto
        
    Returns:
        Número normalizado
    """
    if not phone:
        return ""
    
    # Eliminar caracteres no numéricos excepto +
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Agregar código de país si no lo tiene
    if not phone.startswith('+'):
        if len(phone) == 9:  # Número español
            phone = country_code + phone
    
    return phone 