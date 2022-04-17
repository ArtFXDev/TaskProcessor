from taskprocessor import config_manager
CONTEXT_SELECT_UI_PATH = config_manager.get_qt_ui_file_path("contextselect")
EDITOR_WINDOW_UI_PATH = config_manager.get_qt_ui_file_path("window")

from .editor_window import EditorWindow
from .context_select_window import ContextSelectWindow
