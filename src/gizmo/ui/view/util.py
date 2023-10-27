def setSettings(obj, config):

    s=config.get('Settings', {})
    for k, v in s.items():
        setattr(obj, k, v)
