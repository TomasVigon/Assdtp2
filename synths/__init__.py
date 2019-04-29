from importlib import import_module

from .base_synth import base_synth

def create(synth_name, *args, **kwargs):

    try:
        if '.' in synth_name:
            module_name, class_name = synth_name.rsplit('.', 1)
        else:
            module_name = synth_name
            class_name = synth_name
        synth_module = import_module('.' + module_name, package='synths') 
        synth_class = getattr(synth_module, class_name)
        instance = synth_class(*args, **kwargs)

    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of our synth selection!'.format(synth_name))
    else:
        if not issubclass(synth_class, base_synth):
            raise ImportError("We currently don't have {}, but you are welcome to send in the request for it!".format(synth_class))

    return instance


