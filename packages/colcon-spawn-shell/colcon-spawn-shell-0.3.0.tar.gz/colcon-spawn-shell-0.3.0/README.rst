==================
Colcon Spawn Shell
==================

Introduction
------------

This is a `colcon <https://colcon.readthedocs.io>`_ plugin to chain workspaces in new shells.
It allows quickly un-chaining workspaces by exiting the spawned shell.

The shell's prompt is edited to show the workspace order.
The only supported shell is **bash**.

.. image:: https://raw.githubusercontent.com/colcon/colcon-spawn-shell/8de6d0a687619bfd8342647b6d216695bb76dfaf/doc/colcon_spawn_shell_example.gif

Quick Start
-----------

**Optional:** Create and source a virtual environment.

    .. code-block:: bash

        python3 -m venv env
        . env/bin/activate

From Pip
~~~~~~~~

1. Download ``colcon-spawn-shell`` from pip.

    .. code-block:: bash

        pip install colcon-spawn-shell

2. Build the colcon workspace you would like to spawn in a new shell.

    .. code-block:: bash

        cd my_cool_workspace
        colcon build

3. Source ``spawn_shell.bash`` to activate the workspace.

    .. code-block:: bash

        . install/spawn_shell.bash

_`From Source`
~~~~~~~~~~~~~~

.. note::

    It's recommended to install to a virutal environment for development.
    See `this tutorial <https://docs.python.org/3/tutorial/venv.html>`_ for more information.

1. Download the source code for ``colcon-spawn-shell``

    .. code-block:: bash

        mkdir -b spawn_shell_ws/src
        cd spawn_shell_ws/src
        git clone https://github.com/colcon/colcon-spawn-shell.git

2. Build the workspace using colcon

    .. code-block:: bash

        colcon build

3. Source the workspace

    .. code-block:: bash

        . install/local_setup.bash

From now on future workspaces can be activated by sourcing ``spawn_shell.bash``

    .. code-block:: bash

        cd my_cool_workspace
        colcon build
        . install/spawn_shell.bash

Contributing
------------

1. `Fork <https://help.github.com/articles/fork-a-repo/>`_ the `colcon/colcon-spawn-shell <https://github.com/colcon/colcon-spawn-shell>`_ repository.
2. Follow the `"From Source" instructions <From Source_>`_, except clone your forked repository.
3. Make changes and commit them to a branch.

    .. code-block:: bash

        # Creat a branch for your changes
        git checkout -b my-cool-changes
        # Make your changes ...
        git commit -m "committing my changes"
        # Push them to your fork
        git push --set-upstream origin my-cool-changes

4. Create a `Pull Request <https://help.github.com/articles/creating-a-pull-request-from-a-fork/>`_ from your branch to the branch **develop** on `colcon/colcon-spawn-shell <colcon/colcon-spawn-shell_>`_


.. note::

    Please create pull requests from the branch **develop** because `this repository <colcon/colcon-spawn-shell_>`_ uses the `nvie git branching model <http://nvie.com/posts/a-successful-git-branching-model/>`_.
