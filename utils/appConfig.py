def set_config(app, test_config):
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)
