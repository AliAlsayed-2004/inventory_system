def load_stylesheet(app, path):
    with open(path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())