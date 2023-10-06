# components/theme_utils.py

CURRENT_THEME = "light"  # default theme

def set_global_theme(theme_name):
    global CURRENT_THEME
    CURRENT_THEME = theme_name

def get_global_theme():
    return CURRENT_THEME
