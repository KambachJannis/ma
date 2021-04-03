from models import lcfcn

def getModel(model_dict, exp_dict = None, train_set = None):
    name = model_dict['name']
    if name in ["lcfcn"]:
        model =  lcfcn.LCFCN(exp_dict, train_set = train_set)
    else:
        raise ValueError(f'Model {name} not defined.')
    return model