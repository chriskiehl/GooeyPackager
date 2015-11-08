import os
import subprocess
import sys
import tempfile
from textwrap import dedent
from gooey import Gooey, GooeyParser
import pexpect


def local_path():
  return getattr(sys, 'frozen', None) or os.path.dirname(__file__)

@Gooey(program_name='Gooey Packager', monospace_display=True)
def main():
  parser = GooeyParser(description='Package your Gooey applications into standalone executables')
  parser.add_argument(
    "program_name",
    metavar='Program Name',
    help='Destination name for the packaged executable'
  )
  parser.add_argument(
    "source_path",
    metavar="Program Source",
    help='The main source file of your program',
    widget="FileChooser"
  )

  parser.add_argument(
    "output_dir",
    metavar="Output Directory",
    help='Location to store the generated files',
    widget="DirChooser"
  )

  args = parser.parse_args()

  if not os.path.exists(args.source_path):
    raise IOError('{} does not appear to be a valid file path'.format(args.source_path))

  if not os.path.exists(args.output_dir):
    raise IOError('{} does not appear to be a valid directory'.format(args.output_dir))

  with open(os.path.join(local_path(), 'build_template'), 'r') as f:
    spec_details = f.read().format(program_name=args.program_name, source_path=args.source_path)

  fileno, path = tempfile.mkstemp(prefix='gooeybuild', suffix='.spec')
  with open(path, 'w') as f:
    f.write(spec_details)

  cmd = 'pyinstaller "{0}" --distpath="{1}"'.format(path, args.output_dir)
  print cmd
  from pexpect.popen_spawn import PopenSpawn
  child = PopenSpawn(cmd)
  child.logfile = sys.stdout
  child.wait()
  print dedent('''
  ___  _ _  ______                 _
 / _ \| | | |  _  \               | |
/ /_\ \ | | | | | |___  _ __   ___| |
|  _  | | | | | | / _ \| '_ \ / _ \ |
| | | | | | | |/ / (_) | | | |  __/_|
\_| |_/_|_| |___/ \___/|_| |_|\___(_)
  ''')
  print 'Wrote Executable file to {}'.format(args.output_dir)



if __name__ == '__main__':
  sys.argv += ["My Cool App", "C:\\Users\\Chris\\Documents\\learning_django\\widget_demo.py", "C:\\Users\\Chris\\Documents\\learning_django\\dist"]
  main()
