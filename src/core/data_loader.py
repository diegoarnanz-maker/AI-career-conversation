"""
Cargador de datos del perfil personal
"""
import os
import json
from pypdf import PdfReader
from src.config import Config

class DataLoader:
    """Maneja la carga de datos del perfil personal"""
    
    def __init__(self):
        self.linkedin_content = ""
        self.cv_content = ""
        self.contexto_content = ""
        self.faq_content = ""
        self._load_data()
    
    def _load_data(self):
        """Carga todos los datos del perfil"""
        self._load_linkedin_pdf()
        self._load_cv_json()
        self._load_contexto_json()
        self._load_faq_json()
    
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
    
    def _load_cv_json(self):
        """Carga el CV en formato JSON"""
        try:
            cv_path = "data/me/cv.json"
            if os.path.exists(cv_path):
                with open(cv_path, "r", encoding="utf-8") as f:
                    cv_data = json.load(f)
                    self.cv_content = json.dumps(cv_data, indent=2, ensure_ascii=False)
                print(f"[INFO] CV JSON cargado: {len(self.cv_content)} caracteres")
            else:
                print(f"[WARNING] No se encontró el archivo: {cv_path}")
                self.cv_content = "CV no disponible"
        except Exception as e:
            print(f"[ERROR] Error cargando CV JSON: {e}")
            self.cv_content = "Error cargando CV"
    
    def _load_contexto_json(self):
        """Carga el contexto del asistente"""
        try:
            contexto_path = "data/me/contexto-asistente.json"
            if os.path.exists(contexto_path):
                with open(contexto_path, "r", encoding="utf-8") as f:
                    contexto_data = json.load(f)
                    self.contexto_content = json.dumps(contexto_data, indent=2, ensure_ascii=False)
                print(f"[INFO] Contexto cargado: {len(self.contexto_content)} caracteres")
            else:
                print(f"[WARNING] No se encontró el archivo: {contexto_path}")
                self.contexto_content = "Contexto no disponible"
        except Exception as e:
            print(f"[ERROR] Error cargando contexto: {e}")
            self.contexto_content = "Error cargando contexto"
    
    def _load_faq_json(self):
        """Carga las preguntas frecuentes"""
        try:
            faq_path = "data/me/faq.json"
            if os.path.exists(faq_path):
                with open(faq_path, "r", encoding="utf-8") as f:
                    faq_data = json.load(f)
                    self.faq_content = json.dumps(faq_data, indent=2, ensure_ascii=False)
                print(f"[INFO] FAQ cargado: {len(self.faq_content)} caracteres")
            else:
                print(f"[WARNING] No se encontró el archivo: {faq_path}")
                self.faq_content = "FAQ no disponible"
        except Exception as e:
            print(f"[ERROR] Error cargando FAQ: {e}")
            self.faq_content = "Error cargando FAQ"
    
    def get_linkedin_content(self):
        """Retorna el contenido del LinkedIn"""
        return self.linkedin_content
    
    def get_cv_content(self):
        """Retorna el contenido del CV"""
        return self.cv_content
    
    def get_contexto_content(self):
        """Retorna el contexto del asistente"""
        return self.contexto_content
    
    def get_faq_content(self):
        """Retorna las preguntas frecuentes"""
        return self.faq_content
    
    def reload_data(self):
        """Recarga todos los datos"""
        print("[INFO] Recargando datos del perfil...")
        self._load_data() 