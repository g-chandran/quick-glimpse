import importlib
from .algorithm.inference import Inference
# inf = importlib.import_module(".inference", "algorithm")

info_ratio = 80
max_length = 150


def getData(input_data):
    # inferenceObject = inf.Inference(info_ratio, input_data, max_length)
    inferenceObject = Inference(info_ratio, input_data, max_length)
    result = inferenceObject.main()
    return " ".join(result)
