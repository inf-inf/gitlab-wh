from pathlib import Path

CURRENT_PATH = Path(__file__).absolute().parent.parent
STATIC_FOLDER_PATH = Path(CURRENT_PATH, "static")
HTML_TEMPLATES_FOLDER_PATH = Path(CURRENT_PATH, "templates")
