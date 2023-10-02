import subprocess
import os
import sys

sys.path.append(
  os.path.dirname(__file__)
)

# This import of environmentinator comes from __file__/..'s folder, 
# so it'll always be up to date!
import environmentinator
# 'pdoc' is not the same as 'pdoc3', yay naming ambiguities.
# fortunately we pass the library name explicitly,
# and the same thing would be necessary for eg the module 'PIL' from the library 'Pillow'
hatch = environmentinator.ensure_module('hatch')

os.environ['PYTHONPATH'] = os.pathsep.join(
  [os.path.dirname(os.path.dirname(hatch.__file__)) ] + os.environ.get('PYTHONPATH', '').split(os.pathsep)
)

def run_hatch(*args):
  subprocess.run([
    sys.executable, '-c', '__import__("hatch.cli").cli.main()', *args
  ])


run_hatch('build')

run_hatch('publish')

