**This is my unmaintained archived copy of Terminal Velocity**.

Development has moved to Vincent Perricone's fork, you should use this instead: https://github.com/vhp/terminal_velocity

Terminal Velocity (seanh's archived copy)
=========================================


`Terminal Velocity` is a fast note-taking app for the UNIX terminal, that
focuses on letting you create or find a note as quickly and easily as possible,
then uses your ``$EDITOR`` to open and edit the note. It is heavily inspired
by the OS X app `Notational Velocity <http://notational.net/>`_.
For screenshots and features, see the
`Terminal Velocity website <http://seanh.github.com/terminal_velocity>`_.

To install Terminal Velocity, run::

    pip install terminal_velocity

Then to launch it just run::

    terminal_velocity

To use a different notes directory, run::

    terminal_velocity path/to/your/notes/dir

To see all the command-line options, run::

    terminal_velocity -h

To quit the app, press ``ctrl-c`` or ``ctrl-x``.

To upgrade Terminal Velocity to the latest version, run::

    pip install --upgrade terminal_velocity

To uninstall it, run::

    pip uninstall terminal_velocity

To make a bug report or feature request, use `GitHub Issues <https://github.com/seanh/terminal_velocity/issues>`_.

To contribute documentation, use `the wiki <https://github.com/seanh/terminal_velocity/wiki>`_.

To contribute code to Terminal Velocity, see
`CONTRIBUTING <https://github.com/seanh/terminal_velocity/blob/master/CONTRIBUTING.md#contributing-to-terminal-velocity>`_.


Hacking
-------

To release a new version of Terminal Velocity:

1. Increment the version number in the
   `setup.py file <setup.py>`_,
   add an entry te the `changelog <CHANGELOG.txt>`_,
   commit both changes to git and push them to github.
   For example, see `aae87b <https://github.com/seanh/terminal_velocity/commit/aae87bcc50f88037b8fc76c78c0da2086c5e89ae>`_.

2. Upload the new release to `the terminal_velocity package on pypi <https://pypi.python.org/pypi/terminal_velocity>`_: run ``python setup.py sdist upload -r pypi``.

For more information see https://packaging.python.org/.
