def transform_constructor_params(model, args):
    try:
        for dict_item in args:
            for key, value in dict_item.items():
                try:
                    if hasattr(model, key):
                        setattr(model, key, value)
                except Exception as e:
                    pass
    except Exception as e:
        pass


# transform json data with update method
def transform_update_params(model, dict_item):
    try:
        for key, value in dict_item.items():
            try:
                if hasattr(model, key):
                    setattr(model, key, value)
            except Exception as e:
                pass
    except Exception as e:
        pass
