# mochitest-logs
Scripts for analyzing Firefox test logs


* clean_lsan.py - Extract LSan results from the log of a Mochitest
  run.  This can be run directly or used as a parsing library.

* parse_suppression.py - Read in an LSan suppression file.  This can
  be run directly or used as a parsing library.

* local_suppressor.py - This reads in the LSan results from a
  Mochitest run and an LSan suppression file, and only prints out the
  parts of the LSan run that do not match the suppression file. This
  is useful for figuring out the effect of changes to a suppression
  file without having to re-run the entire test suite.
