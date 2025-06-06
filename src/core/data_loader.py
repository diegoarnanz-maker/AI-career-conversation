"""
Cargador de datos del perfil personal
"""
import os
from pypdf import PdfReader
from src.config import Config

class DataLoader:
    """Maneja la carga de datos del perfil personal"""
    
    def __init__(self):
        self.linkedin_content = ""
        self.summary_content = ""
        self._load_data()
    
    def _load_data(self):
        """Carga todos los datos del perfil"""
        self._load_linkedin_pdf()
        self._load_summary()
    
    def _load_linkedin_pdf(self):
        """Carga el contenido del PDF de LinkedIn"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(Config.LINKEDIN_PDF), exist_ok=True)
            
            if os.path.exists(Config.LINKEDIN_PDF):
                reader = PdfReader(Config.LINKEDIN_PDF)
                self.linkedin_content = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        self.linkedin_content += text
                print(f"[INFO] LinkedIn PDF cargado: {len(self.linkedin_content)} caracteres")
            else:
                print(f"[WARNING] No se encontró el archivo: {Config.LINKEDIN_PDF}")
                self.linkedin_content = "Perfil de LinkedIn no disponible"
        except Exception as e:
            print(f"[ERROR] Error cargando LinkedIn PDF: {e}")
            self.linkedin_content = "Error cargando perfil de LinkedIn"
    
    def _load_summary(self):
        """Carga el resumen personal"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(Config.SUMMARY_FILE), exist_ok=True)
            
            if os.path.exists(Config.SUMMARY_FILE):
                with open(Config.SUMMARY_FILE, "r", encoding="utf-8") as f:
                    self.summary_content = f.read()
                print(f"[INFO] Resumen cargado: {len(self.summary_content)} caracteres")
            else:
                print(f"[WARNING] No se encontró el archivo: {Config.SUMMARY_FILE}")
                self.summary_content = "Resumen personal no disponible"
        except Exception as e:
            print(f"[ERROR] Error cargando resumen: {e}")
            self.summary_content = "Error cargando resumen personal"
    
    def get_linkedin_content(self):
        """Retorna el contenido del LinkedIn"""
        return self.linkedin_content
    
    def get_summary_content(self):
        """Retorna el contenido del resumen"""
        return self.summary_content
    
    def reload_data(self):
        """Recarga todos los datos"""
        print("[INFO] Recargando datos del perfil...")
        self._load_data() 