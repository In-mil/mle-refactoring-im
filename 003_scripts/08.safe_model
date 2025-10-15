def save_model(model, path: str) -> None:
    """
    Saves a trained model with skops.

    Args:
        model: Trained model.
        path (str): Output file path.
    """
    import os
    import skops.io as sio
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fout:
        sio.dump(model, fout)
