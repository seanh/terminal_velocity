Terminal Velocity
=================

For install instructions, usage and features, see the
`Terminal Velocity website <http://seanh.github.com/terminal_velocity>`_.

Hacking
-------

To install Terminal Velocity for development, you need
`Python <http://www.python.org/>`_,
`virtualenv <http://www.virtualenv.org/>`_,
`virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_
and `git <http://git-scm.com/>`_
(technically you can make do without virtualenv and virtualenvwrapper, but they
make development a lot more convenient).

Use virtualenvwrapper to create a Python virtualenv and install Terminal
Velocity and its dependences into the virtualenv, for example::

    $ mkvirtualenv terminal_velocity
    (terminal_velocity) $ mkdir -p ~/Projects/terminal_velocity
    (terminal_velocity) $ cd ~/Projects/terminal_velocity
    (terminal_velocity) $ setvirtualenvproject
    (terminal_velocity) $ git clone https://github.com/seanh/terminal_velocity.git
    (terminal_velocity) $ cd terminal_velocity
    (terminal_velocity) $ python setup.py develop
    (terminal_velocity) $ deactivate
    $ workon terminal_velocity

At this point, the ``terminal_velocity`` command should run your development
copy of Terminal Velocity from your virtualenv::

    (terminal_velocity) $ which terminal_velocity
    /home/seanh/.virtualenvs/terminal_velocity/bin/terminal_velocity

Each time you open a new shell to start working on Terminal Velocity
development, you need to activate your terminal_velocity virtualenv::

    $ workon terminal_velocity
    (terminal_velocity) $

When you're finished working, deactivate the virtualenv::

    (terminal_velocity) $ deactivate
    $

While the virtualenv is deactivated, the ``terminal_velocity`` command will run
your installed release version of Terminal Velocity (if you have one) rather
than the development version installed in your virtualenv::

    $ which terminal_velocity
    /usr/local/bin/terminal_velocity

So you can easily switch between your stable and development copies of Terminal
Velocity by activating and deactivating your virtualenv with the ``workon`` and
``deactivate`` commands. You can also have multiple shells open, some with the
virtualenv activated and others not, so you can use your stable copy of
Terminal Velocity to takes note while you hack on your development version.

You can also setup different aliases (e.g. in your ``~/.bashrc`` or
``~/.zshrc``) for running the release and development versions::

    alias tv="/usr/local/bin/terminal_velocity"
    alias tvdev="/home/seanh/.virtualenvs/terminal_velocity/bin/python /home/seanh/Projects/terminal_velocity/bin/terminal_velocity"

