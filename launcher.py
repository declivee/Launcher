# necessário

#  py -m pip install Nuitka PyQt6

# compilar

# py -m nuitka launcher.py ^
 # --onefile ^
 # --windows-console-mode=disable ^
 # --enable-plugin=pyqt6 ^
 # --windows-icon-from-ico="data\icon.ico" ^
 # --include-data-dir="data=data"

import os
import shutil
import tempfile
import requests
import stat
import subprocess
import zipfile
import webbrowser

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt6.QtGui import QPixmap, QIcon
from io import BytesIO

TOKEN = "token_github_here"

CLIENT_FOLDER = "client"
LOCAL_VERSION_FILE = os.path.join(CLIENT_FOLDER, "version.txt")

# --- site url ---
SITE_URL = "http://127.0.0.0/index.php"

# --- site url ---
DISCORD_URL = "https://discord.gg/..."

# --- metadata url ---
VERSION_URL = "https://raw.githubusercontent.com/usuario/seu_repo/main/version.txt"


# --- client folder url ---
CLIENT_ZIP_URL = "https://github.com/usuario/seu_repo/releases/latest/download/client.zip"

# --- client folder exe ---
CLIENT_EXECUTABLE = os.path.join(CLIENT_FOLDER, "otclient_dx_x64.exe")

# --- icon file ---
ICON_FILE = "data/icon.ico"

# --- background  file --
BACKGROUND_FILE = "data/background.png"


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Launcher Otclient")
        self.setFixedSize(580, 240)
        
        self.setObjectName("LauncherBackground")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet(f"""
           #LauncherBackground {{
               border-image: url("{BACKGROUND_FILE}") 0 0 0 0 stretch stretch;
           }}
        """)

        if os.path.exists(ICON_FILE):
            self.setWindowIcon(QIcon(ICON_FILE))
            print(f"✓ Ícone carregado: {ICON_FILE}")
        else:
            print(f"⚠ Ícone não encontrado: {ICON_FILE}")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 20, 0, 0) 
        top_layout.setSpacing(10)


        self.site_btn = QPushButton("Site")
        self.site_btn.setFixedSize(60, 30)
        self.site_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.site_btn.clicked.connect(self.open_site)
        
        self.site_btn.setStyleSheet("""
            QPushButton {
                background-color: #4d4cff;
                color: black;
                border: 1px solid #3e3e42;
                padding: 4px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #7373ff;
                border: 1px solid #0078d4;
            }
            QPushButton:pressed {
                background-color: #0000ff;   
            }
        """)
        


        self.discord_btn = QPushButton("Discord")
        self.discord_btn.setFixedSize(60, 30)
        self.discord_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.discord_btn.clicked.connect(self.open_discord)
        
        self.discord_btn.setStyleSheet("""
            QPushButton {
                background-color: #4d4cff;
                color: black;
                border: 1px solid #3e3e42;
                padding: 4px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #7373ff;
                border: 1px solid #0078d4;
            }
            QPushButton:pressed {
                background-color: #0000ff;   
            }
        """)
        
        
        top_layout.addStretch(1)
        top_layout.addWidget(self.site_btn)
        top_layout.addWidget(self.discord_btn)
        top_layout.addStretch(1)

           
        main_layout.addLayout(top_layout)

        content_layout = QVBoxLayout()
        content_layout.addStretch(1)

        
        self.label = QLabel("Ready to check.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(True)


        self.remove_data_btn = QPushButton("Remove Client")
        self.remove_data_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_data_btn.setFixedHeight(40)
        self.remove_data_btn.clicked.connect(self.remove_client_data)
        self.remove_data_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6666;
                color: white;
                border: 1px solid #3e3e42;
                padding: 4px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #ff3333;
                border: 1px solid #0078d4;
            }
            QPushButton:pressed {
                background-color: #cc0000;
            }
        """)

        
        self.btn = QPushButton("Play")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setFixedHeight(40)
        self.btn.clicked.connect(self.start_update_process)

        content_layout.addWidget(self.label)
        content_layout.addWidget(self.progress)


        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)  

        self.btn.setFixedWidth(150)  
        buttons_layout.addWidget(self.btn)

        buttons_layout.addSpacing(20) 

        self.remove_data_btn.setFixedWidth(150) 
        buttons_layout.addWidget(self.remove_data_btn)

        buttons_layout.addStretch(1)  
        content_layout.addLayout(buttons_layout)

        
        content_layout.setContentsMargins(50, 0, 50, 30)
        content_layout.setSpacing(10)

        main_layout.addLayout(content_layout)
        
        self.setLayout(main_layout)

            
         
          
    def remove_client_data(self):
        """Remove a pasta do client e permite um novo download"""
        if os.path.exists(CLIENT_FOLDER):
            try:
                shutil.rmtree(CLIENT_FOLDER, onerror=remove_readonly)
                self.set_progress(0, "Data removed. You can download it again.")
                print("✓ 'client' folder removed successfully.")

            except Exception as e:
                self.set_progress(0, f"Error removing data: {e}")
                print(f"✗ Error removing client: {e}")

        else:
            self.set_progress(0, "No client folder found.")
            print("⚠ No 'client' folder to remove.")

    def open_site(self):
        try:
            webbrowser.open(SITE_URL)
            print(f"🌐 Abrindo: {SITE_URL}")
        except Exception as e:
            print(f"✗ Erro ao abrir site: {e}")
            
    def open_discord(self):
        try:
            webbrowser.open(DISCORD_URL)
            print(f"🌐 Abrindo: {DISCORD_URL}")
        except Exception as e:
            print(f"✗ Erro ao abrir site: {e}")             
            


    def set_progress(self, value, text):
        self.progress.setValue(value)
        self.label.setText(text)
        QApplication.processEvents()

    def get_remote_version(self):
        
        GITHUB_TOKEN = TOKEN
        OWNER = "" # user github
        REPO = ""  # name repo
        FILE_PATH = "version.txt"  # caminho dentro do repositório main
        BRANCH = "main"

        api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}?ref={BRANCH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        try:
            r = requests.get(api_url, headers=headers, timeout=10)
            r.raise_for_status()
            content = r.json()

            if "content" in content and content["encoding"] == "base64":
                import base64
                decoded = base64.b64decode(content["content"]).decode("utf-8")
                return decoded.strip()
            else:
                raise Exception("Arquivo inválido ou não encontrado.")
        except Exception as e:
            print(f"✗ Erro ao buscar versão remota: {e}")
            return None


    def get_local_version(self):
        if not os.path.exists(LOCAL_VERSION_FILE):
            return None
        try:
            with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except:
            return None

    def start_update_process(self):
        self.btn.setEnabled(False)
        self.set_progress(0, "Checking versions...")
        

        remote_version = self.get_remote_version()
        if remote_version is None:
            self.set_progress(0, "Error: Could not check the online version.")
            self.btn.setEnabled(True)
            return

        local_version = self.get_local_version()
        
        print(f"Local: {local_version} | Remoto: {remote_version}")

        if local_version == remote_version:
            self.launch_game()
            return

        self.update_client(remote_version)

    def extract_and_move(self, temp_zip_path, temp_extract_dir):
        try:
            def extract_recursive(zip_path, extract_to):
                print(f"Extraindo: {os.path.basename(zip_path)}")
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    bad_file = zip_ref.testzip()
                    if bad_file:
                        raise Exception(f"ZIP corrompido: {bad_file}")
                    
                    zip_ref.extractall(extract_to)
                
                for root, dirs, files in os.walk(extract_to):
                    for file in files:
                        if file.lower().endswith('.zip'):
                            nested_zip = os.path.join(root, file)
                            print(f"  ⚠️  ZIP aninhado encontrado: {file}")
                            
                            nested_extract_dir = os.path.join(root, file.replace('.zip', ''))
                            os.makedirs(nested_extract_dir, exist_ok=True)
                            
                            extract_recursive(nested_zip, nested_extract_dir)
                            os.remove(nested_zip)
                            print(f"  ✓ ZIP aninhado extraído e removido: {file}")
            
            extract_recursive(temp_zip_path, temp_extract_dir)
            
            print(f"✓ ZIP extraído com sucesso (incluindo aninhados)")
            
            extracted_items = os.listdir(temp_extract_dir)
            print(f"Itens extraídos: {extracted_items}")
            
            os.makedirs(CLIENT_FOLDER, exist_ok=True)
            
            if len(extracted_items) == 1 and os.path.isdir(os.path.join(temp_extract_dir, extracted_items[0])):
                source_dir = os.path.join(temp_extract_dir, extracted_items[0])
                print(f"Pasta raiz detectada: {extracted_items[0]}")
                
                for item in os.listdir(source_dir):
                    src = os.path.join(source_dir, item)
                    dst = os.path.join(CLIENT_FOLDER, item)
                    
                    if os.path.isdir(src):
                        if os.path.exists(dst):
                            shutil.rmtree(dst, onerror=remove_readonly)
                        shutil.move(src, dst)
                    else:
                        if os.path.exists(dst):
                            os.remove(dst)
                        shutil.move(src, dst)
                    
                    print(f"  ✓ Movido: {item}")
            else:
                print("Sem pasta raiz, movendo tudo")
                for item in extracted_items:
                    src = os.path.join(temp_extract_dir, item)
                    dst = os.path.join(CLIENT_FOLDER, item)
                    
                    if os.path.isdir(src):
                        if os.path.exists(dst):
                            shutil.rmtree(dst, onerror=remove_readonly)
                        shutil.move(src, dst)
                    else:
                        if os.path.exists(dst):
                            os.remove(dst)
                        shutil.move(src, dst)
                    
                    print(f"  ✓ Movido: {item}")
            
            print("✓ Extração e movimento concluído")
            return True
            
        except Exception as e:
            print(f"✗ Erro ao extrair: {e}")
            raise

    def update_client(self, remote_version):
        self.set_progress(5, f"New version ({remote_version}). Downloading ZIP...")

        temp_zip_path = None
        temp_extract_dir = None

        GITHUB_TOKEN = TOKEN
        OWNER = "" # user github
        REPO = ""  # name repo
        ASSET_NAME = "client.zip"

        try:

            temp_zip_fd, temp_zip_path = tempfile.mkstemp(suffix=".zip")
            os.close(temp_zip_fd)
            print(f"Arquivo temporário: {temp_zip_path}")

            api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json"
            }

            r = requests.get(api_url, headers=headers, timeout=30)
            r.raise_for_status()
            release = r.json()

            asset = None
            for a in release["assets"]:
                if a["name"] == ASSET_NAME:
                    asset = a
                    break

            if not asset:
                raise Exception(f"Asset {ASSET_NAME} não encontrado na release mais recente.")

            download_url = asset["url"]
            headers["Accept"] = "application/octet-stream"

            r = requests.get(download_url, headers=headers, stream=True, timeout=30)
            r.raise_for_status()

            total_length = r.headers.get('content-length')
            dl = 0

            with open(temp_zip_path, 'wb') as f:
                if total_length is None:
                    f.write(r.content)
                    self.set_progress(50, "Download completed.")
                else:
                    total_length = int(total_length)
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            dl += len(chunk)
                            f.write(chunk)
                            percent = int((dl / total_length) * 100)
                            self.set_progress(percent, f"Baixando... {percent}%")

            file_size = os.path.getsize(temp_zip_path)
            print(f"✓ Download completed: {file_size / (1024*1024):.2f} MB")
            if file_size < 1000:
                raise Exception(f"Arquivo muito pequeno: {file_size} bytes")

            self.set_progress(85, "Removing old version...")
            if os.path.exists(CLIENT_FOLDER):
                shutil.rmtree(CLIENT_FOLDER, onerror=remove_readonly)

            self.set_progress(90, "Extracting files...")
            temp_extract_dir = tempfile.mkdtemp()
            self.extract_and_move(temp_zip_path, temp_extract_dir)


            self.set_progress(98, "Finalizing...")
            os.makedirs(CLIENT_FOLDER, exist_ok=True)
            with open(LOCAL_VERSION_FILE, "w", encoding="utf-8") as f:
                f.write(remote_version)

            print(f"✓ Versão atualizada: {remote_version}")
            self.launch_game()

        except Exception as e:
            self.set_progress(0, f"Erro crítico: {str(e)}")
            print(f"✗ Detalhe do erro: {e}")
            self.btn.setEnabled(True)

        finally:
            if temp_extract_dir and os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir, onerror=remove_readonly)
            if temp_zip_path and os.path.exists(temp_zip_path):
                os.remove(temp_zip_path)



    def launch_game(self):
        self.set_progress(100, "Starting game...")
        try:
            if os.path.exists(CLIENT_EXECUTABLE):
                subprocess.Popen(CLIENT_EXECUTABLE)
                self.close()
            else:
                self.set_progress(0, f"Error: Executable not found at {CLIENT_EXECUTABLE}")
                self.btn.setEnabled(True)
        except Exception as e:
            self.set_progress(0, f"Error: {str(e)}")
            self.btn.setEnabled(True)



def set_dark_theme(app):
    dark_stylesheet = """
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            font-size: 14px;
            font-family: 'Segoe UI', sans-serif;
        }
        QPushButton {
            background-color: #4d4cff;
            color: black;
            border: 1px solid #3e3e42;
            padding: 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #7373ff;
            border: 1px solid #0078d4;
        }
        QPushButton:pressed {
            background-color: #0000ff;
        }
        QPushButton:disabled {
            background-color: #000040;
            color: #888888;
        }
        QProgressBar {
            background-color: #99b3ff;
            border: 1px solid #3e3e42;
            border-radius: 4px;
            text-align: center;
            color: white;
            height: 25px;
        }
        QProgressBar::chunk {
            background-color: #5c26ff;
            width: 20px;
        }
        QLabel {
            color: #ffffff;
            font-weight: bold;
            margin-bottom: 5px;
        }
    """
    app.setStyleSheet(dark_stylesheet)

if __name__ == "__main__":
    app = QApplication([])
    set_dark_theme(app)
    window = Launcher()
    window.show()
    app.exec()