import os


class bkPaths:

    base_dir = os.path.dirname(__file__)

    styles = os.path.join(base_dir, "style")
    icons = os.path.join(styles, "icons")
    ui_files = os.path.join(base_dir, "ui")

    # File loaders.

    @classmethod
    def style(cls, filename):
        return os.path.join(cls.styles, filename)

    @classmethod
    def icon(cls, filename):
        return os.path.join(cls.icons, filename)
    
    @classmethod
    def ui_file(cls, filename):
        return os.path.join(cls.ui_files, filename)
