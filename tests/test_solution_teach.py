from tools.solution_teach import check


def test_teach_check_finds_all_commands():
    result = check(__import__("pathlib").Path.cwd())
    assert result["status"] == "PASS"
    assert result["command_count"] == 6
