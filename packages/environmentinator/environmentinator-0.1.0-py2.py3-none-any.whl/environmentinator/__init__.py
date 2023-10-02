
# This file is the entire environmentor library.
# It does not depend on anything beyond the python
# standard library version 3.7+ or so and an internet connection
# or other source of packages available to `python -m pip`.

import os
import sys
import subprocess
import importlib
import inspect
import shutil
import time

def ensure_module(module_name, package_name=None):
  '''
    Returns the imported module `module_name` if it exists,
    if not uses `pip` to install `package_name` and returns the imported module `module_name`.

    `package_name` may be multiple packages seperated by whitespace,
    for eg AI libraries where soft-dependencies
    would be good to install at the same time even though you will never
    explicitly import them (eg you want to use the module `torch` but installing the packages
    `torch torchvision torchaudio` will ensure the module `torch`'s vision APIs are available.)

    Packages are installed to the folder `.py-env/{MAJOR}_{MINOR}/{PACKAGE_NAME}` relative
    to the code that calls `environmentinator.ensure_module`. This folder is added to `sys.path` during imports,
    but we do not modify environment variables. If you need sub-processes to see the same imported
    packages, do something clever like `os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)` before spawning
    your sub-processes.

    If you use a lot of code under version control ensure that `.py-env` is in your `.gitignore` file.

    ## Example Uses

    ```python
      import environmentinator
      json5 = environmentinator.ensure_module('json5')
      # equivelant to manual environment setup + "import json5"
      my_var = json5.loads('{"not": "valid", /* json */ }')
    ```

  '''
  if not isinstance(module_name, str):
    raise Exception('module_name must be a string, got {}'.format(module_name))

  if package_name is None:
    package_name = module_name

  if not isinstance(package_name, str):
    raise Exception('package_name must be a string, got {}'.format(package_name))
  
  vers_major = sys.version_info[0]
  vers_minor = sys.version_info[1]

  callee_file = __file__
  try:
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    callee_file = module.__file__
  except:
    pass

  env_target = os.path.join(os.path.dirname(callee_file), '.py-env', '{}_{}'.format(vers_major, vers_minor))
  os.makedirs(env_target, mode=0o777, exist_ok=True)
  if not env_target in sys.path:
    sys.path.append(env_target)

  try:
    return importlib.import_module(module_name)
  except:
    try:
      import pip # prove we _have_ pip
      subprocess.run([
        sys.executable, '-m', 'pip', 'install', '--target={}'.format(env_target), *(package_name.split())
      ])
    except:
      subprocess.run([
        sys.executable, '-m', 'ensurepip',
      ])
      subprocess.run([
        sys.executable, '-m', 'pip', 'install', '--target={}'.format(env_target), *(package_name.split())
      ])


  return importlib.import_module(module_name)

def delete_all_environmentinator_modules():
  '''
    Deletes the folder `.py-env/{MAJOR}_{MINOR}` relative to the code that calls `environmentinator.delete_all_environmentinator_modules`
  '''
  vers_major = sys.version_info[0]
  vers_minor = sys.version_info[1]

  callee_file = __file__
  try:
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    callee_file = module.__file__
  except:
    pass

  env_target = os.path.join(os.path.dirname(callee_file), '.py-env', '{}_{}'.format(vers_major, vers_minor))
  if os.path.exists(env_target):
    shutil.rmtree(env_target)

def ensure_py_version(comparison_eval_str, addtl_runtime_locations=[], executable_name='python'):
    '''
      This function checks the current runtime's major + minor version
    '''

    vers_major = sys.version_info[0]
    vers_minor = sys.version_info[1]
    vers_str = '{}.{}'.format(vers_major, vers_minor)

    is_good_py_version = eval_expr('{}{}'.format(vers_str, comparison_eval_str))
    if not is_good_py_version:
  
      if 't' in os.environ.get('ENVIRONMENTINATOR_IS_SUBPROCESS', '').lower():
        raise Exception('Environmentinator is refusing to run ensure_py_version() from a sub-processes because you likely have an infinite loop in your dependency resolution!')

      os.environ['PATH'] = os.pathsep.join( addtl_runtime_locations + os.environ.get('PATH', '').split(os.pathsep) )
      os.environ['LD_LIBRARY_PATH'] = os.pathsep.join( addtl_runtime_locations + os.environ.get('LD_LIBRARY_PATH', '').split(os.pathsep) )

      os.environ['ENVIRONMENTINATOR_IS_SUBPROCESS'] = 't'
      proc = subprocess.Popen( [ executable_name ] + sys.argv )
      while proc.poll() is None:
        time.sleep(0.1)
      child_ret_code = proc.poll()
      sys.exit(child_ret_code)



# Stolen from https://stackoverflow.com/a/9558001
# to avoid eval()-ing strings

import ast
import operator as op

# supported operators
operators = {
  ast.Add: op.add,
  ast.Sub: op.sub,
  ast.Mult: op.mul,
  ast.Div: op.truediv,
  ast.Pow: op.pow,
  ast.BitXor: op.xor,
  ast.USub: op.neg,
  
  ast.Not: op.not_,
  ast.Eq: op.eq,
  ast.NotEq: op.ne,
  ast.Lt: op.lt,
  ast.LtE: op.le,
  ast.Gt: op.gt,
  ast.GtE: op.ge,
}

def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    elif isinstance(node, ast.BoolOp): # <left> <operator> <right> e.g., True or False
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.Compare): # <left> <operator> <right> e.g., 1 > 2
      if len(node.ops) == 1 and len(node.comparators) == 1:
        return operators[type(node.ops[0])](eval_(node.left), eval_(node.comparators[0]))
      else:
        raise Exception('Multi-comparison shorthand not supported! Please replace eg (1 < x < 2) with (1 < x and x < 2)')
    else:
        raise TypeError(node)



