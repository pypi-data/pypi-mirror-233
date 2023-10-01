# pylint: disable=missing-module-docstring,missing-function-docstring


def test_debug_logs(cli_runner):
    ret = cli_runner("-d", "--demo", 1)
    assert "demo=1" in ret.stderr
    assert "input_filename='output/sample.csv'" in ret.stderr
