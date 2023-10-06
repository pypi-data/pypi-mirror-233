* chval 1.2.0 (2023-10-05)

  * Add Python3.12 support
  * Drop Python3.9 support

  -- Louis Paternault <spalax@gresille.org>

* chval 1.1.1 (2023-03-08)

  * Python3.11 support

  -- Louis Paternault <spalax@gresille.org>

* chval 1.1.0 (2022-10-13)

  * Change progress bar (add a "[completed/total]" field).
  * Refactor getmail calls.
  * Remove delay between getmail calls.

  -- Louis Paternault <spalax@gresille.org>

* chval 1.0.0 (2022-09-22)

  * Restart from scratch: chval is now a wrapper to getmail, with:
    * parallel calls;
    * progress bars.

  -- Louis Paternault <spalax@gresille.org>

* chval 0.6.7 (2015-03-20)

  * Updated installation process, to publish it on pypi.

  -- Louis Paternault <spalax@gresille.org>

* chval 0.6.6 (2013-05-06)

  * Added "-n" as default getmail option.

  -- Louis Paternault <spalax@gresille.org>

* chval 0.6.5 (2013-05-06)

  * Taking into account pycrypto version 2.6.0
  * Fixing a few bugs.

  -- Louis Paternault <spalax@gresille.org>

* chval 0.6.4 (2013-03-03)

  * Fixed: Forgot to change name from gams to chval in man pages.

  -- Louis Paternault <spalax@gresille.org>

* chval 0.6.3 (2013-01-27)

  * Changed name from 'gams' to 'chval'.
  * Increased timeout lock, which was too low and made the daemon (and client) crash
  * Changed project URL

  -- Louis Paternault <spalax@gresille.org>

* gams 0.6.1 (2011-02-13)

  * Closes bug: Lock FIFO before writing to them (no more concurrent write problems)
  * Closes bug: "gams getmail" no longer asks password if not needed.
  * Code improvements

  -- Louis Paternault <spalax@gresille.org>

* gams 0.6.0 (2011-02-06)

  This new version changes the way passwords are stored. It is necessary to run tool gams5to6.py (in directory "meta") to convert password file from old format to old format. Syntax is:

      gams5to6.py [gamsrc]

  Now, the actual changelog:

  * Using different methods to encrypt and decrypt strings: solves the following bugs.
    * Closes bug: long passwords are now allowed;
    * Closes bug: brackets are no longer ignored at the end of passwords.
  * Improved behaviour when Ctrl-C is hit.
  * The same password is now encrypted in a different string for different getmailrc files (there is no way to tell that two getmailrc files have the same password because their hash are the same).
  * Closes bug: Using strong random function.
  * Closes bug: Options --gamsdir and --version can now be used after command.
  * Closes bug: A daemon that was not answering to ping made client crash.
  * Closes bug in "gams fill": Password was asked for getmailrc files that already contained passwords.
  * Closes bug: Ignore getmailrc files without passwords with "gams getmail"
  * Closes bug: Daemon now asks password only if it needs it
  * Minor code refactoring and improvement.

  -- Louis Paternault <spalax@gresille.org>

* gams 0.5.1 (2010-12-20)

  * Closes bug: The client no longer crashes when no daemon is running.
  * Closes bug: The daemon no longer crashes when no getmailrc file exists.
  * Closes bug: It is now possible to run several daemons at the same time.
  * Improved program response when user hits Ctrl-C (but far from being perfect)

  -- Louis Paternault <spalax@gresille.org>

* gams 0.5.0 (2010-12-01)

  * Added option --gamsdir.
  * Added options --daemon and --only for "gams scan".
  * If no getmailrc files is given with "gams daemon", only consider getmailrc files that are not already handled by other daemons.
  * Closes bug, when to daemons where run with the same name.

  -- Louis Paternault <spalax@gresille.org>

* gams 0.4.0 (2011-11-21)

  * Added interface "dialog".
  * Improved interface "standard".
  * Interface "linear" behaves well with pipes.
  * Multiple daemons handled by interfaces.
  * Bug corrections.
  * Code improvement.

  -- Louis Paternault <spalax@gresille.org>

* gams 0.3.3 (2010-11-04)

  * Removed irrelevant option --gap with "gams client".
  * Added possible value "--delay 0" for daemon.
  * Solved bug that made daemon sometime call getmail twice in a row.
  * Corrected a small bug in interface "standard".
  * Code improvement.

  -- Louis Paternault <spalax@gresille.org>

* gams 0.3.2 (2010-10-31)

  * Corrected bugs

  -- Louis Paternault <spalax@gresille.org>

* gams 0.3.1 (2010-10-31)

  * Added options
    - --gap: can wait a few seconds between two successive calls of getmail, to avoid overload when dozens of getmail process where launched at the same time.
    - --getmaildir: can tell in which directory are stored getmail configuration files
    - Can now ask to get mail from a single getmailrc file of a daemon
  * Bug corrections
    - No longer fails if password is given in the getmailrc file.
  * Improved layout
    - Added interfaces
    - Improved help formatting
  * Check if client and daemon have the same version
  * Plus some code improvements that are not visible from outside.

  -- Louis Paternault <spalax@gresille.org>

* gams 0.2.0 (2010-08-17)

  * Improved installation script
  * Man pages
    - completed man page for gams
    - created man page for gamsrc
  * Added parallel mode
  * Added options and commands
    - commnands: kill clean
    - options: --auth
  * Configuration file
    - Added options
    - Renamed from config to gamsrc
  * Passwords
    - Fail after three wrong passwords
    - Sorted out when main password is asked
  * Changed I/O
    - print daemon name before traces
    - behaves well with EOF when asking passwords
    - changed password prompt
  * Internal changes
    - dropped optparse for argparse
    - dropped signals (do not behave well with Threads)
    - split program into a main program and a core module
  * Still bugs
    - still do not accept long password: raise a clean error if user try to do so

  -- Louis Paternault <spalax@gresille.org>

* gams 0.1.0 (2010-07-26)

  * Initial release.

  -- Louis Paternault <spalax@gresille.org>
