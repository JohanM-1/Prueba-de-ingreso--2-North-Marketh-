"""
Extractor base abstracto para diferentes plataformas de redes sociales.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import time
import random


class BaseExtractor(ABC):
    """
    Clase base abstracta para extractores de redes sociales.
    """
    
    def __init__(self):
        """Inicializa el extractor base."""
        self.requests_made = 0
        self.start_time = datetime.now()
        self.last_request_time = None
        
    def __enter__(self):
        """Context manager entry."""
        self.setup()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
        
    @abstractmethod
    def setup(self) -> None:
        """Configuración inicial del extractor."""
        pass
        
    @abstractmethod
    def cleanup(self) -> None:
        """Limpieza de recursos."""
        pass
        
    @abstractmethod
    def extract_followers(self, username: str) -> List[str]:
        """
        Extrae la lista de seguidores de una cuenta.
        
        Args:
            username: Username de la cuenta
            
        Returns:
            Lista de usernames de seguidores
        """
        pass
        
    @abstractmethod
    def extract_profile_data(self, username: str) -> Dict[str, Any]:
        """
        Extrae datos detallados de un perfil.
        
        Args:
            username: Username del perfil
            
        Returns:
            Diccionario con datos del perfil
        """
        pass
    
    def create_profile_template(self, username: str, source_account: str) -> Dict[str, Any]:
        """
        Crea un template básico de datos de perfil.
        
        Args:
            username: Username del perfil
            source_account: Cuenta de origen
            
        Returns:
            Diccionario con template de datos
        """
        return {
            'username': username,
            'full_name': '',
            'phone_numbers': [],
            'account_created_date': None,
            'first_post_date': None,
            'last_post_date': None,
            'follower_count': None,
            'following_count': None,
            'posts_count': None,
            'is_verified': False,
            'is_private': False,
            'bio': '',
            'external_url': '',
            'extraction_timestamp': datetime.now().isoformat(),
            'source_account': source_account
        }
    
    def apply_rate_limiting(self, delay_config: Dict[str, float]) -> None:
        """
        Aplica rate limiting entre requests.
        
        Args:
            delay_config: Configuración de delays
        """
        base_delay = delay_config.get('base', 1.0)
        max_delay = delay_config.get('max', 5.0)
        
        if self.last_request_time:
            elapsed = (datetime.now() - self.last_request_time).total_seconds()
            if elapsed < base_delay:
                sleep_time = base_delay - elapsed
                sleep_time = min(sleep_time, max_delay)
                time.sleep(sleep_time)
        
        self.last_request_time = datetime.now()
        self.requests_made += 1
    
    def get_extraction_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la extracción.
        
        Returns:
            Diccionario con estadísticas
        """
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'requests_made': self.requests_made,
            'elapsed_time': f"{elapsed:.1f}s",
            'avg_requests_per_minute': (self.requests_made / elapsed * 60) if elapsed > 0 else 0
        }
    
    def wait_for_rate_limit_reset(self, minutes: int = 15) -> None:
        """
        Espera cuando se alcanza el rate limit.
        
        Args:
            minutes: Minutos a esperar
        """
        wait_time = minutes * 60
        
        for remaining in range(wait_time, 0, -60):
            minutes_left = remaining / 60
            time.sleep(60)
    
    def retry_with_backoff(
        self, 
        func, 
        max_retries: int = 3, 
        base_delay: float = 1.0,
        backoff_factor: float = 2.0
    ):
        """
        Reintenta una función con backoff exponencial.
        
        Args:
            func: Función a reintentar
            max_retries: Número máximo de reintentos
            base_delay: Delay base en segundos
            backoff_factor: Factor de incremento del delay
            
        Returns:
            Resultado de la función o None si falla
        """
        for attempt in range(max_retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries:
                    return None
                
                delay = base_delay * (backoff_factor ** attempt)
                delay += random.uniform(0, delay * 0.1)  # Jitter
                
                time.sleep(delay)
        
        return None
    
    def handle_authentication_error(self, error: Exception) -> None:
        """
        Maneja errores de autenticación.
        
        Args:
            error: Error de autenticación
        """
        extra_wait = 10 * 60  # 10 minutos extra
        time.sleep(extra_wait) 