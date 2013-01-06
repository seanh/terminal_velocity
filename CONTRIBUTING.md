If you want to contribute bug reports or feature requests, documentation, or
code to Terminal Velocity, you can send them to me by email or by whatever means
you prefer. But if you're looking for instructions, here are my suggestions:

If you want to contribute a bug report or feature request to Terminal Velocity,
use
[GitHub Issues](https://github.com/seanh/terminal_velocity/issues?state=open).

If you want to contribute documentation, for example to explain how to combine
Terminal Velocity with an external tool that handles something like note
synchronisation or encryption, use
[the wiki](https://github.com/seanh/terminal_velocity/wiki).

If you want to contribute code to Terminal Velocity: create your own GitHub
account, fork Terminal Velocity, create a new bugfix or feature branch and
commit your code to it, push your branch to your Terminal Velocity fork on
GitHub, then send me a pull request asking me to pull your feature branch into
my master branch. In detail:

1. [Create a GitHub account](https://github.com/signup) (it's free!)

2. Fork my Terminal Velocity repo: click the _Fork_ button on the Terminal
   Velocity GitHub page.

3. `git clone` your Terminal Velocity fork to your development machine.

4. Checkout a new branch forked from the master branch
   (e.g. `git checkout -b my-new-feature`).

   Note about branches: It's best if you keep the master branch of your fork,
   and any other branches corresponding to branches from the main Terminal
   Velocity repo, as pristine copies of their corresponding branches. In other
   words, _never commit to the master branch_, only pull changes from the main
   repo into the master branch.

   Instead, create a new feature or bugfix branch for each feature or bugfix
   you develop. Develop each feature or bugfix on its own branch.

5. Commit your code on the new branch, and push it to your fork on GitHub:
   `git push origin my-new-feature`.

6. Use the _Pull Request_ button on the main Terminal Velocity project page to
   send me a pull request, asking me to pull your bugfix or feature branch into
   my master branch.

7. Once I've pulled your pull request, then you can pull my master branch into
   the master branch of your fork and get your new feature or bugfix in your
   master branch.

   First add the main Terminal Velocity repo as a remote (you only need to do
   this once):

        git remote add seanh https://github.com/seanh/terminal_velocity.git

   Now pull the main master branch into your master branch, and push it to your
   fork:

        git checkout master
        git pull seanh master
        git push origin master

For code style, I try to follow [PEP 8](http://www.python.org/dev/peps/pep-0008/) and
[PEP 257](http://www.python.org/dev/peps/pep-0257/). I try to make code compatible
with Python 2, version 2.6 or newer (i.e. don't use
[Python 2.7-only features](http://docs.python.org/2/whatsnew/2.7.html)).
That being said, I also try to write Python 2 code that's
[forward-compatible with Python 3](http://lucumr.pocoo.org/2011/1/22/forwards-compatible-python/).
For git commit messages, I try to follow these [Commit Guidelines](http://git-scm.com/book/en/Distributed-Git-Contributing-to-a-Project#Commit-Guidelines).

