from tools.validate_benchmark_fixtures import validate


def test_solution_fixture_specification_is_complete():
    result = validate(__import__("pathlib").Path("benchmarks/solution-selection/fixtures.json"))
    assert result["status"] == "PASS"
    assert result["fixture_count"] == 16
