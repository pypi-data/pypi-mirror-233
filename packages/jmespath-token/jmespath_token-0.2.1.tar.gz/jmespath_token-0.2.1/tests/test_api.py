# -*- coding: utf-8 -*-

from jmespath_token import api


def test():
    _ = api


if __name__ == "__main__":
    from jmespath_token.tests import run_cov_test

    run_cov_test(__file__, "jmespath_token.api", preview=False)
