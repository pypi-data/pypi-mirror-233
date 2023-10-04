
import os, sys

import environmentinator

print(f'Python process number {os.getpid()} is version {sys.version_info[0]}.{sys.version_info[1]}!')

# I use python 3.11, but have 3.10 in a container that gets booted up to
# do AI work. By adding the paths to python3.10 and libpython3.10.so
# that version can be looked up on the PATH and loaded here.
environmentinator.ensure_py_version('==3.10', addtl_runtime_locations=[
  '/mnt/scratch/containers/tableitizer-container/bin',
  '/mnt/scratch/containers/tableitizer-container/usr/lib',
],
  executable_name='python3.10' # This can usually be omitted, but b/c of how my container is layed out 'python' is the 3.11 one.
)

print('This statement is run within python 3.10, or not run at all if 3.10 cannot be found!')

json5 = environmentinator.ensure_module('json5')

print(f'I have loaded json5 from {json5}')



