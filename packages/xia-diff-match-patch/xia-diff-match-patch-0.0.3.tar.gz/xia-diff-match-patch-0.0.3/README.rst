Introduction
=============================

Current version is a wrap of Google's project: https://github.com/google/diff-match-patch


* Installation:

.. code-block:: bash

   pip install xia-diff-match-patch


* Usage

`apply_patches` function takes a series patched files as arguments, sorted by its priorities.

.. code-block:: python

    from xia_diff_match_patch import apply_patches

    base = "Line 1\n"
    a1 = "Line 1\nLine2\n"
    a2 = "Line 1\n\nCode 1\nCode 2\nCode 3\n"
    a3 = "Line 3\n"

    print(apply_patches(base, a1, a2, a3))


