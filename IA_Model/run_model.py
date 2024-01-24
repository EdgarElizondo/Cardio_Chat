from .main_model import ann_model

# Execute Test
def run_ann(values):
    model = ann_model()
    model.load(values)
    prediction = model.evaluate()

    return prediction