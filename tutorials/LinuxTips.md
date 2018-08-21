# Linux tips session

* ``shopt -s histappend``  - make all your bash instances will share one history
* ``sudo !!`` - re-run your last command with ``sudo``
* ``command < infile -`` - pipe infile to ``command``, followed by standard input.  Suggestion: use infile to automatically answer the first questions, then you answer the rest manually
  * See alse: ``pee`` from moreutils package
* ``tldr`` - give condensed version of manpages (from https://github.com/tldr-pages/tldr)
* ``tmux`` - terminal multiplexer, like ``screen`` but better.  Create side-by-side terminals within one session.  Attach to your session from somewhere else and keep all the output etc. Scroll without using your terminal
* ``sync`` - ensure that everything is written to disk.  Recommendation: use to ensure files are synchronised with network filesystem.  Also: do it after using ``dd``
* ``pv`` - show a nice progress bar when piping data around



kdjfls

```sh
ls -l
indexamajig
```
