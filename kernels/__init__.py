"""Governed simulation kernels, extracted from landed artifacts.

Admission rule (mirror of VOCABULARY.md's): a kernel enters only if at
least two landed artifacts already use the pattern; each module header
cites its sources. Every module runs closed-form anchors from the
derive layers under --selftest. stdlib only. kernels/*.py is covered by
the law gate (LAW-34): these functions are imported by falsifiers, so
they cannot change silently.
"""
