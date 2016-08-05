"""
Usage:
  mail to <recipients>... subj <subject> [attach <files>...]
"""

from .mymail import MyMail
from docopt import docopt

def main():

	args = docopt(__doc__)
	print(args)

	print("... nothing happens here ... yet")

if __name__ == '__main__':
    main()