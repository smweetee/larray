﻿New features
------------

* added a feature (see the :ref:`miscellaneous section <misc>` for details).

* added another feature.

.. _misc:

Miscellaneous improvements
--------------------------

* changed display of arrays (closes :issue:`243`):

    >>> ndtest((3, 3))
    a\\b  b0  b1  b2
     a0   0   1   2
     a1   3   4   5
     a2   6   7   8

  instead of

    >>> ndtest((3, 3))
    a\\b | b0 | b1 | b2
     a0 |  0 |  1 |  2
     a1 |  3 |  4 |  5
     a2 |  6 |  7 |  8

Fixes
-----

* fixed something (closes :issue:`1`).