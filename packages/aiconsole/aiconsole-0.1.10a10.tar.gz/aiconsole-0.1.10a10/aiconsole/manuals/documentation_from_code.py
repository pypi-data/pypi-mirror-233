
import importlib.util
import logging

log = logging.getLogger(__name__)


def documentation_from_code(module_name: str, path: str):

    def create_content(context):
        import inspect
        spec = importlib.util.spec_from_file_location(
            module_name, path)

        if not spec or spec.loader is None:
            raise Exception(f'Could not load module {module_name} from {path}')

        python_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(python_module)

        #TODO: get all functions and modules, this does not work right now
        docstrings = []
        for name, obj in inspect.getmembers(python_module):
            
            # take only locally defined exports, no imports
            if not name.startswith('_'):
                continue

            log.info(f'{name}, {obj}')

            if inspect.isfunction(obj) or inspect.ismodule(obj):
                docstrings.append(inspect.getdoc(obj) or '')
        
        # get main docstring
        docstring = inspect.getdoc(python_module)

        newline = '\n'
        return f'''
{docstring}

Function list:
{newline.join(docstrings)}
'''.strip()

    return create_content
