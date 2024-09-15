def sanitize_model_name(model_name):
    model_name = model_name.replace("/", "_")
    return model_name
