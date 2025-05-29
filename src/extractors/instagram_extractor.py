"""
Instagram extractor usando Selenium en modo interactivo.
"""

import time
import random
import concurrent.futures
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from .base_extractor import BaseExtractor
from ..config import settings


class InstagramExtractor(BaseExtractor):
    """
    Extractor de datos de Instagram usando Selenium en modo interactivo.
    """
    
    def __init__(self):
        super().__init__()
        self.selenium_driver = None
        self.is_logged_in = False
        self.login_username = None
    
    def setup(self) -> None:
        """Configura el extractor de Instagram con autenticación interactiva opcional."""
        try:
            self._setup_driver()
            
            # Intentar login interactivo con Selenium
            if settings.is_login_enabled():
                login_success = self._attempt_login_interactive()
                if login_success:
                    pass
                else:
                    pass
            else:
                pass
            
        except Exception as e:
            raise
    
    def cleanup(self) -> None:
        """Limpia recursos de Selenium."""
        try:
            if self.selenium_driver:
                self.selenium_driver.quit()
                self.selenium_driver = None
                
        except Exception as e:
            pass
    
    def _setup_driver(self):
        """Configura el driver de Selenium con opciones optimizadas para modo interactivo."""
        try:
            # Detectar navegador y configurar según lo detectado
            detected_browser = settings.SELENIUM_CONFIG.get('detected_browser', 'chrome')
            browser_options_config = settings.SELENIUM_CONFIG.get('browser_options', {})
            
            if detected_browser == 'edge':
                self.selenium_driver = self._setup_edge_driver_interactive(browser_options_config)
            elif detected_browser == 'firefox':
                self.selenium_driver = self._setup_firefox_driver_interactive(browser_options_config)
            else:
                self.selenium_driver = self._setup_chrome_driver_interactive(browser_options_config)
            
            # Configuración común para todos los navegadores
            self.selenium_driver.implicitly_wait(settings.SELENIUM_CONFIG['implicit_wait'])
            self.selenium_driver.set_page_load_timeout(settings.SELENIUM_CONFIG['page_load_timeout'])
                
        except Exception as e:
            # Fallback a Chrome básico en modo interactivo
            self.selenium_driver = self._setup_chrome_driver_interactive({})
            self.selenium_driver.implicitly_wait(settings.SELENIUM_CONFIG['implicit_wait'])
            self.selenium_driver.set_page_load_timeout(settings.SELENIUM_CONFIG['page_load_timeout'])
    
    def _setup_edge_driver_interactive(self, browser_config):
        """Configura Microsoft Edge en modo interactivo (visible)."""
        options = EdgeOptions()
        
        # Opciones mínimas para modo interactivo
        interactive_options = [
            '--no-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-notifications',
            '--disable-popup-blocking',
            '--disable-web-security',
            '--allow-running-insecure-content',
            '--lang=es-ES'
        ]
        
        for option in interactive_options:
            options.add_argument(option)
        
        # Configurar ventana grande para que puedas ver bien
        options.add_argument('--window-size=1400,1000')
        options.add_argument('--start-maximized')
        
        # User agent real de tu sistema
        user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/{settings.SELENIUM_CONFIG.get('detected_version', '136.0.3240.92')}"
        options.add_argument(f'--user-agent={user_agent}')
        
        # Preferencias para mejor experiencia
        prefs = {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0,
            'intl.accept_languages': 'es-ES,es,en-US,en'
        }
        
        options.add_experimental_option('prefs', prefs)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Configurar servicio
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        # Script anti-detección
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _setup_chrome_driver_interactive(self, browser_config):
        """Configura Chrome en modo interactivo (visible)."""
        options = webdriver.ChromeOptions()
        
        # Opciones mínimas para modo interactivo
        interactive_options = [
            '--no-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-notifications',
            '--disable-popup-blocking',
            '--lang=es-ES',
            '--start-maximized'
        ]
        
        for option in interactive_options:
            options.add_argument(option)
        
        # User agent real
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        options.add_argument(f'--user-agent={user_agent}')
        
        # Preferencias para mejor experiencia
        prefs = {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0,
            'intl.accept_languages': 'es-ES,es,en-US,en'
        }
        
        options.add_experimental_option('prefs', prefs)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Configurar servicio
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Script anti-detección
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _setup_firefox_driver_interactive(self, browser_config):
        """Configura Firefox en modo interactivo (visible)."""
        options = FirefoxOptions()
        
        # Preferencias de Firefox
        firefox_prefs = {
            'dom.webnotifications.enabled': False,
            'dom.push.enabled': False,
            'intl.locale.requested': 'es-ES'
        }
        
        for pref, value in firefox_prefs.items():
            options.set_preference(pref, value)
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        return driver
    
    def _handle_instagram_popups(self):
        """Maneja popups comunes de Instagram después del login."""
        try:
            # Lista de selectores XPath para cerrar popups
            popup_xpaths = [
                "//button[contains(text(), 'Ahora no')]",
                "//button[contains(text(), 'Not Now')]",
                "//button[contains(text(), 'Dismiss')]",
                "//button[@aria-label='Close']",
                "//*[contains(text(), 'Ahora no')]",
                "//*[contains(text(), 'Not Now')]"
            ]
            
            for xpath in popup_xpaths:
                try:
                    elements = self.selenium_driver.find_elements(By.XPATH, xpath)
                    if elements:
                        elements[0].click()
                        time.sleep(2)
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            return False
    
    def extract_followers_interactive(self, username: str, max_followers: int = None) -> List[str]:
        """
        Extrae seguidores en modo interactivo usando el navegador visible.
        
        Args:
            username: Username de la cuenta
            
        Returns:
            Lista de usernames de seguidores
        """
        try:
            # URL del perfil
            profile_url = f"https://www.instagram.com/{username}/"
            
            # Navegar al perfil
            self.selenium_driver.get(profile_url)
            
            # Dar tiempo al usuario para ver la página
            time.sleep(2)
            
            # Buscar información básica del perfil
            try:
                # Intentar obtener el número de seguidores desde los meta tags
                followers_meta = self.selenium_driver.find_elements(
                    By.CSS_SELECTOR, 
                    'meta[property="og:description"]'
                )
                
                # Buscar el enlace de seguidores
                followers_links = self.selenium_driver.find_elements(
                    By.CSS_SELECTOR,
                    'a[href*="/followers/"]'
                )
                
                if followers_links:
                    followers_url = followers_links[0].get_attribute('href')
                    
                    # Hacer clic en el enlace de seguidores
                    followers_links[0].click()
                    
                    # Esperar a que se abra el modal
                    time.sleep(3)
                    
                    # Intentar extraer seguidores del modal
                    followers = self._extract_followers_from_modal(max_followers=max_followers)
                    
                    if followers:
                        pass
                    else:
                        # Mantener navegador abierto para inspección manual
                        time.sleep(30)
                    
                    return followers
                
                else:
                    # Mantener navegador abierto para inspección manual
                    time.sleep(20)
                    
                    return []
                    
            except Exception as e:
                time.sleep(2)
                return []
                
        except Exception as e:
            return []
    
    def _extract_followers_from_modal(self, max_followers: int = None) -> List[str]:
        """Extrae seguidores del modal abierto."""
        followers = []
        
        try:
            # Buscar contenedores de seguidores en el modal
            selectors = [
                '[role="dialog"] a[href*="/"]',  # Enlaces en el modal
                '[role="dialog"] [role="button"]',  # Botones en el modal
                'div[style*="transform"] a',  # Área scrolleable
                '._aano a'  # Selector específico de Instagram
            ]
            
            for selector in selectors:
                try:
                    elements = self.selenium_driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if max_followers is not None and len(followers) >= max_followers:
                            break
                        try:
                            href = element.get_attribute('href')
                            if href and '/' in href:
                                # Extraer username de la URL
                                username = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
                                if username and username not in followers and len(username) > 0:
                                    # Validar que parece un username válido
                                    if username.replace('_', '').replace('.', '').isalnum():
                                        followers.append(username)
                        except:
                            continue
                            
                    if followers:
                        break  # Si encontramos seguidores, no probar más selectores
                        
                except Exception as e:
                    continue
            
            return followers[:max_followers] if max_followers is not None else followers
            
        except Exception as e:
            return [] 

    def create_profile_template(self, username: str, source_account: str) -> Dict[str, Any]:
        """
        Crea un template básico de datos de perfil con campos extraíbles.
        
        Args:
            username: Username del perfil
            source_account: Cuenta de origen
            
        Returns:
            Diccionario con template de datos
        """
        from datetime import datetime
        
        return {
            'username': username,
            'full_name': '',
            'bio': '',
            'posts_count': 0,
            'follower_count': 0,
            'following_count': 0,
            'extraction_timestamp': datetime.now().isoformat(),
            'source_account': source_account
        }

    def extract_profile_detailed_info(self, username: str) -> Dict[str, Any]:
        """
        Extrae información detallada del perfil usando solo el meta tag og:description para seguidores, siguiendo y publicaciones.
        """
        try:
            profile_url = f"https://www.instagram.com/{username}/"
            self.selenium_driver.get(profile_url)
            time.sleep(2)
            profile_data = self.create_profile_template(username, "")
            # Extraer datos del meta tag og:description
            followers_meta = self.selenium_driver.find_elements(
                By.CSS_SELECTOR,
                'meta[property="og:description"]'
            )
            if followers_meta:
                description = followers_meta[0].get_attribute('content')
                # Parsear: '1M seguidores, 747 siguiendo, 11K publicaciones - ...'
                try:
                    parts = description.split(' - ')[0].split(',')
                    for part in parts:
                        if 'seguidor' in part:
                            profile_data['follower_count'] = self._convert_number_text(part.split()[0])
                        elif 'siguiendo' in part:
                            profile_data['following_count'] = self._convert_number_text(part.split()[0])
                        elif 'publicacion' in part:
                            profile_data['posts_count'] = self._convert_number_text(part.split()[0])
                except Exception as e:
                    pass
            
            return profile_data
        except Exception as e:
            return self.create_profile_template(username, "")
    
    def _convert_number_text(self, number_text: str) -> int:
        """
        Convierte texto de número (ej: '1M', '2K', '500') a entero.
        """
        try:
            number_text = number_text.strip().replace(',', '').replace('.', '')
            
            if number_text.endswith('M'):
                return int(float(number_text[:-1]) * 1000000)
            elif number_text.endswith('K'):
                return int(float(number_text[:-1]) * 1000)
            else:
                return int(number_text)
        except Exception as e:
            return 0
    
    def _attempt_login_interactive(self) -> bool:
        """Intenta hacer login de forma interactiva usando Selenium."""
        try:
            username, password = settings.get_instagram_credentials()
            
            if not username or not password:
                return False
            
            # Navegar a página de login
            self.selenium_driver.get("https://www.instagram.com/accounts/login/")
            
            time.sleep(3)
            
            # Buscar y llenar campos de login
            try:
                # Buscar campos de usuario y contraseña
                username_inputs = self.selenium_driver.find_elements(
                    By.CSS_SELECTOR,
                    'input[name="username"], input[aria-label="Phone number, username, or email"]'
                )
                
                password_inputs = self.selenium_driver.find_elements(
                    By.CSS_SELECTOR,
                    'input[name="password"], input[aria-label="Password"]'
                )
                
                if username_inputs and password_inputs:
                    # Rellenar credenciales
                    username_inputs[0].clear()
                    username_inputs[0].send_keys(username)
                    time.sleep(1)
                    
                    password_inputs[0].clear()
                    password_inputs[0].send_keys(password)
                    time.sleep(1)
                    
                    # Buscar botón de login
                    login_buttons = self.selenium_driver.find_elements(
                        By.CSS_SELECTOR,
                        'button[type="submit"]'
                    )
                    
                    # Si no encuentra por type, buscar por otros métodos
                    if not login_buttons:
                        login_buttons = self.selenium_driver.find_elements(
                            By.XPATH,
                            "//button[contains(text(), 'Entrar') or contains(text(), 'Log in') or contains(text(), 'Iniciar')]"
                        )
                    
                    if login_buttons:
                        login_buttons[0].click()
                    else:
                        raise Exception("Botón de login no encontrado")
                    
                    # Esperar a que se procese el login
                    time.sleep(10)
                    
                    # Verificar si el login fue exitoso
                    current_url = self.selenium_driver.current_url
                    if "instagram.com" in current_url and "login" not in current_url:
                        self.is_logged_in = True
                        self.login_username = username
                        return True
                    else:
                        # Dar tiempo al usuario para resolver manualmente
                        time.sleep(30)
                        
                        # Verificar nuevamente
                        current_url = self.selenium_driver.current_url
                        if "login" not in current_url:
                            self.is_logged_in = True
                            self.login_username = username
                            return True
                        else:
                            return False
                            
            except Exception as e:
                time.sleep(60)
                
                # Verificar si el usuario se logueó manualmente
                current_url = self.selenium_driver.current_url
                if "login" not in current_url and "instagram.com" in current_url:
                    self.is_logged_in = True
                    self.login_username = username
                    return True
                else:
                    return False
                    
        except Exception as e:
            return False

    def extract_multiple_accounts(self, accounts: List[str], max_followers: int = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extrae datos de múltiples cuentas en modo interactivo con información detallada y procesamiento en lotes de 5 pestañas.
        """
        results = {}
        
        for i, account in enumerate(accounts):
            try:
                followers = self.extract_followers_interactive(account, max_followers=max_followers)
                if not followers:
                    results[account] = []
                    continue
                
                random.shuffle(followers)
                account_data = []
                batch_size = 5
                for batch_start in range(0, len(followers), batch_size):
                    batch = followers[batch_start:batch_start+batch_size]
                    for idx, username in enumerate(batch):
                        if idx == 0:
                            self.selenium_driver.switch_to.window(self.selenium_driver.window_handles[0])
                            self.selenium_driver.get(f"https://www.instagram.com/{username}/")
                        else:
                            self.selenium_driver.execute_script(f"window.open('https://www.instagram.com/{username}/', '_blank');")
                    time.sleep(2)
                    tabs = self.selenium_driver.window_handles
                    batch_results = []
                    for idx, username in enumerate(batch):
                        self.selenium_driver.switch_to.window(tabs[idx])
                        try:
                            profile_data = self.extract_profile_detailed_info(username)
                            profile_data['source_account'] = f"@{account}"
                            batch_results.append(profile_data)
                        except Exception as e:
                            basic_data = self.create_profile_template(username, account)
                            batch_results.append(basic_data)
                        time.sleep(random.uniform(1.0, 2.5))
                    account_data.extend(batch_results)
                    for idx in range(len(batch)-1, 0, -1):
                        self.selenium_driver.switch_to.window(tabs[idx])
                        self.selenium_driver.close()
                    self.selenium_driver.switch_to.window(tabs[0])
                results[account] = account_data
                if i < len(accounts) - 1:
                    time.sleep(5)
            except Exception as e:
                results[account] = []
                if i < len(accounts) - 1:
                    response = input(f"\n🤔 Error en @{account}. ¿Continuar con la siguiente cuenta? (y/N): ")
                    if response.lower() != 'y':
                        break
        return results
    
    def get_login_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado del login.
        
        Returns:
            Dict con información del estado de login
        """
        return {
            'login_enabled': settings.is_login_enabled(),
            'authenticated': self.is_logged_in,
            'username': settings.get_instagram_credentials()[0] if settings.is_login_enabled() else None
        } 
    
    def extract_followers(self, username: str) -> List[str]:
        """
        Método requerido por la clase base - delega a extract_followers_interactive.
        
        Args:
            username: Username de la cuenta
            
        Returns:
            Lista de usernames de seguidores
        """
        return self.extract_followers_interactive(username)
    
    def extract_profile_data(self, username: str) -> Dict[str, Any]:
        """
        Método requerido por la clase base - delega a extract_profile_detailed_info.
        
        Args:
            username: Username del perfil
            
        Returns:
            Diccionario con datos del perfil
        """
        return self.extract_profile_detailed_info(username) 
