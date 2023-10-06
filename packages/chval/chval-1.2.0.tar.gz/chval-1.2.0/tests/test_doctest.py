import doctest

import chval


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(chval))
    return tests
