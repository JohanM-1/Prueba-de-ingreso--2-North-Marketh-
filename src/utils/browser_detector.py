"""
Detector automático de navegador instalado en el sistema.
"""

import platform
import subprocess
import os
import re
from typing import Dict, List, Optional


class BrowserDetector:
    """
    Detecta navegadores instalados en el sistema y genera configuración optimizada.
    """
    
    def __init__(self):
        self.system = platform.system().lower()
        self.detected_browsers = {}
        
    def detect_all_browsers(self) -> Dict[str, Dict]:
        """
        Detecta todos los navegadores disponibles en el sistema.
        
        Returns:
            Diccionario con información de navegadores detectados
        """
        browsers = {
            'chrome': self._detect_chrome(),
            'edge': self._detect_edge(),
            'firefox': self._detect_firefox()
        }
        
        # Filtrar navegadores no encontrados
        self.detected_browsers = {
            name: info for name, info in browsers.items() 
            if info['installed']
        }
        
        return self.detected_browsers
    
    def get_recommended_browser(self) -> str:
        """
        Obtiene el navegador recomendado basado en disponibilidad y compatibilidad.
        
        Returns:
            Nombre del navegador recomendado
        """
        if not self.detected_browsers:
            self.detect_all_browsers()
        
        # Orden de preferencia
        preference_order = ['edge', 'chrome', 'firefox']
        
        for browser in preference_order:
            if browser in self.detected_browsers:
                return browser
        
        # Fallback a Chrome si no se detecta nada
        return 'chrome'
    
    def _detect_chrome(self) -> Dict:
        """Detecta Google Chrome."""
        info = {
            'installed': False,
            'version': None,
            'path': None,
            'user_agents': []
        }
        
        try:
            if self.system == 'windows':
                # Buscar en ubicaciones comunes de Windows
                possible_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        info['installed'] = True
                        info['path'] = path
                        info['version'] = self._get_chrome_version_windows(path)
                        break
                        
            elif self.system == 'darwin':  # macOS
                path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
                if os.path.exists(path):
                    info['installed'] = True
                    info['path'] = path
                    info['version'] = self._get_chrome_version_mac()
                    
            else:  # Linux
                try:
                    result = subprocess.run(['google-chrome', '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        info['installed'] = True
                        info['path'] = 'google-chrome'
                        info['version'] = result.stdout.strip()
                except:
                    pass
            
            if info['installed'] and info['version']:
                info['user_agents'] = self._generate_chrome_user_agents(info['version'])
                
        except Exception:
            pass
        
        return info
    
    def _detect_edge(self) -> Dict:
        """Detecta Microsoft Edge."""
        info = {
            'installed': False,
            'version': None,
            'path': None,
            'user_agents': []
        }
        
        try:
            if self.system == 'windows':
                # Edge está integrado en Windows 10/11
                possible_paths = [
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        info['installed'] = True
                        info['path'] = path
                        info['version'] = self._get_edge_version_windows(path)
                        break
                        
            elif self.system == 'darwin':  # macOS
                path = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
                if os.path.exists(path):
                    info['installed'] = True
                    info['path'] = path
                    info['version'] = self._get_edge_version_mac()
                    
            else:  # Linux
                try:
                    result = subprocess.run(['microsoft-edge', '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        info['installed'] = True
                        info['path'] = 'microsoft-edge'
                        info['version'] = result.stdout.strip()
                except:
                    pass
            
            if info['installed'] and info['version']:
                info['user_agents'] = self._generate_edge_user_agents(info['version'])
                
        except Exception:
            pass
        
        return info
    
    def _detect_firefox(self) -> Dict:
        """Detecta Mozilla Firefox."""
        info = {
            'installed': False,
            'version': None,
            'path': None,
            'user_agents': []
        }
        
        try:
            if self.system == 'windows':
                possible_paths = [
                    r"C:\Program Files\Mozilla Firefox\firefox.exe",
                    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        info['installed'] = True
                        info['path'] = path
                        info['version'] = self._get_firefox_version_windows(path)
                        break
                        
            elif self.system == 'darwin':  # macOS
                path = "/Applications/Firefox.app/Contents/MacOS/firefox"
                if os.path.exists(path):
                    info['installed'] = True
                    info['path'] = path
                    info['version'] = self._get_firefox_version_mac()
                    
            else:  # Linux
                try:
                    result = subprocess.run(['firefox', '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        info['installed'] = True
                        info['path'] = 'firefox'
                        info['version'] = result.stdout.strip()
                except:
                    pass
            
            if info['installed'] and info['version']:
                info['user_agents'] = self._generate_firefox_user_agents(info['version'])
                
        except Exception:
            pass
        
        return info
    
    def _get_chrome_version_windows(self, path: str) -> Optional[str]:
        """Obtiene versión de Chrome en Windows."""
        try:
            import win32api
            version_info = win32api.GetFileVersionInfo(path, "\\")
            version = "{}.{}.{}.{}".format(
                version_info['FileVersionMS'] >> 16,
                version_info['FileVersionMS'] & 0xFFFF,
                version_info['FileVersionLS'] >> 16,
                version_info['FileVersionLS'] & 0xFFFF
            )
            return version
        except:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
                pass
        return None
    
    def _get_chrome_version_mac(self) -> Optional[str]:
        """Obtiene versión de Chrome en macOS."""
        try:
            result = subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _get_edge_version_windows(self, path: str) -> Optional[str]:
        """Obtiene versión de Edge en Windows."""
        try:
            result = subprocess.run([path, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _get_edge_version_mac(self) -> Optional[str]:
        """Obtiene versión de Edge en macOS."""
        try:
            result = subprocess.run(['/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _get_firefox_version_windows(self, path: str) -> Optional[str]:
        """Obtiene versión de Firefox en Windows."""
        try:
            result = subprocess.run([path, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _get_firefox_version_mac(self) -> Optional[str]:
        """Obtiene versión de Firefox en macOS."""
        try:
            result = subprocess.run(['/Applications/Firefox.app/Contents/MacOS/firefox', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _generate_chrome_user_agents(self, version: str) -> List[str]:
        """Genera user agents realistas para Chrome."""
        version_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', version)
        if not version_match:
            version_number = "125.0.0.0"
        else:
            version_number = version_match.group(1)
        
        user_agents = [
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version_number} Safari/537.36",
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version_number} Safari/537.36 Edg/125.0.0.0",
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version_number} Safari/537.36"
        ]
        
        return user_agents
    
    def _generate_edge_user_agents(self, version: str) -> List[str]:
        """Genera user agents realistas para Edge."""
        version_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', version)
        if not version_match:
            version_number = "125.0.0.0"
        else:
            version_number = version_match.group(1)
        
        user_agents = [
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/{version_number}",
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/{version_number}"
        ]
        
        return user_agents
    
    def _generate_firefox_user_agents(self, version: str) -> List[str]:
        """Genera user agents realistas para Firefox."""
        version_match = re.search(r'(\d+\.\d+)', version)
        if not version_match:
            version_number = "126.0"
        else:
            version_number = version_match.group(1)
        
        user_agents = [
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{version_number}) Gecko/20100101 Firefox/{version_number}",
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{version_number}) Gecko/20100101 Firefox/{version_number}"
        ]
        
        return user_agents
    
    def get_system_info(self) -> Dict:
        """
        Obtiene información completa del sistema y navegadores.
        
        Returns:
            Diccionario con información del sistema
        """
        self.detect_all_browsers()
        
        recommended = self.get_recommended_browser()
        recommended_info = self.detected_browsers.get(recommended, {})
        
        return {
            'system': platform.system(),
            'version': platform.version(),
            'architecture': platform.machine(),
            'default_browser': recommended,
            'browser_version': recommended_info.get('version', 'Unknown'),
            'detected_browsers': list(self.detected_browsers.keys()),
            'user_agents': recommended_info.get('user_agents', [])
        }


def main():
    """Función principal para testing."""
    detector = BrowserDetector()
    info = detector.get_system_info()
    
    # Comentado para eliminar prints
    # print("🔍 DETECCIÓN DE NAVEGADOR")
    # print("=" * 50)
    # print(f"Sistema: {info['system']} {info['version']}")
    # print(f"Arquitectura: {info['architecture']}")
    # print(f"Navegador predeterminado: {info['default_browser']}")
    # print(f"Versión del navegador: {info['browser_version']}")
    # print(f"\n📋 User Agents de ejemplo:")
    # for i, ua in enumerate(info['user_agents'][:3], 1):
    #     print(f"{i}. {ua}")


if __name__ == "__main__":
    main() 