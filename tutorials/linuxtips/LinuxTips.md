# Linux tips session

* ``shopt -s histappend``  - make all your bash instances will share one history
* ``sudo !!`` - re-run your last command with ``sudo``
* ``command < infile -`` - pipe infile to ``command``, followed by standard input.  Suggestion: use infile to automatically answer the first questions, then you answer the rest manually
  * See also: ``pee`` from moreutils package
* ``tldr`` - give condensed version of manpages (from https://github.com/tldr-pages/tldr)
* ``tmux`` - terminal multiplexer, like ``screen`` but better.  Create side-by-side terminals within one session.  Attach to your session from somewhere else and keep all the output etc. Scroll without using your terminal
* ``sync`` - ensure that everything is written to disk.  Recommendation: use to ensure files are synchronised with network filesystem.  Also: do it after using ``dd``
* ``pv`` - show a nice progress bar when piping data around
* ``python``
* ``mosh`` - mobile shell.  Kind of a substitute for SSH, which smooths out problems due to bad internet connections (e.g. when on the train)
* "moreutils" package - lots of somewhat specialist but kind of cool utilities
* ``pbcopy`` - copy stdin to clipboard.  Also ``pbpaste`` - copy clipboard to stdout.  Available as standard on Mac OS, maybe available as an extension for Linux somewhere.
* Make ``/var`` a separate partition, to avoid log files filling up your entire hard drive
* ``chroot`` - use a different folder as the effective ``/``
* ``lynx`` and ``elinks`` - text mode web browsers
* ``htop`` - like ``top`` but much more informative and colourful
* ``mmv`` - multiple move or copy.  Rename a common pattern in all filenames with a different pattern.
  * See also: ``vidir`` in the moreutils package
* ``fortune`` and ``cowsay`` - show inspirational quotes and draw pictures with cow
  * See also: ``apt-get moo`` for Debian-based systems
* ``nohup`` - stop your program from terminating when the session ends
* ``apt-get``
* ``brew`` (Homebrew) for Mac users - package management system, install loads of "Linux software"
* ``scp`` and ``rsync`` for synchronising files
  * If you have a lot of small files, do this: ``tar -czf - myfolder | ssh me@somewhere tar -xzf -`` (if I remember correctly!).  Rationale: both ``scp`` and ``rsync`` are very slow when there are lots of small files.
* ``paste`` - put two files side by side, line by line
* ``tac`` - like ``cat``, but writes out the file backwards
* ``${VARIABLE%.jpg}`` - cut off trailing .jpg for contents of $VARIABLE
  * See also ``basename -s`` (and ``dirname``)
* ``netcat`` - like ``cat`` over a TCP connection.  Can also make a server using ``netcat -l``
* ``pax`` - unpack tar or cpio archives
