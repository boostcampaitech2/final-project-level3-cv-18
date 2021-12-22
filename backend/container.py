from argparse import Namespace
import yaml
import string
from inference.inference import load_model_and_converter

def get_model_converter_opt():
    with open("./opt.yaml", "r") as f:
        opt = yaml.load(f, yaml.FullLoader)
        opt = Namespace(**opt)
        opt.character = string.printable[:-6] if opt.sensitive else opt.character
        
    model, converter = load_model_and_converter(opt)
    return model, converter, opt

class ModelContainer:
    def __init__(self):
        self.model, self.converter, self.opt = get_model_converter_opt()
        
    def __call__(self):
        return self.model, self.converter, self.opt