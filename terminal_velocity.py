#!/usr/bin/env python2
"""A fast note-taking app for the unix terminal"""
import argparse
import ConfigParser
import os

import urwid_ui


def main():

    # Parse the command-line option for the config file.
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-c", "--config", dest="config", action="store",
            default="~/.tvrc",
            help="the config file to use (default: %(default)s)")
    args, remaining_argv = parser.parse_known_args()

    # Parse the config file.
    config_file = os.path.abspath(os.path.expanduser(args.config))
    config = ConfigParser.SafeConfigParser()
    config.read(config_file)
    defaults = dict(config.items('DEFAULT'))

    # Parse the rest of the command-line options.
    description = __doc__
    epilog = """
the config file can be used to override the defaults for the optional
arguments, example config file contents:

  [DEFAULT]
  editor = vim
  extension = txt
  notes_dir = ~/Notes

if there is no config file (or an argument is missing from the config file)
the default default will be used"""
    parser = argparse.ArgumentParser(description=description, epilog=epilog,
            parents=[parser],
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-e", "--editor", dest="editor", action="store",
        default=defaults.get("editor", "$EDITOR"),
        help="the text editor to use (default: %(default)s)")
    parser.add_argument("-x", "--extension", dest="extension", action="store",
        default=defaults.get("extension", "txt"),
        help="the filename extension for new notes (default: %(default)s)")
    parser.add_argument("notes_dir", action="store", nargs="?",
        default=defaults.get("notes_dir", "~/Notes"),
        help="the notes directory to use (default: %(default)s)")
    args = parser.parse_args()

    urwid_ui.launch(notes_dir=args.notes_dir, editor=args.editor,
            extension=args.extension)

if __name__ == "__main__":
    main()
