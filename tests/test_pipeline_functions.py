import logging
import pytest
from pipeline.duckdb_import import find_table_name

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "file_name, expected_result",
    [
        ("Asher_diaper2.csv", "diaper"),
        ("Asher_expressed.csv", "expressed"),
        ("Asher_formula.csv", "formula"),
        ("Asher_growth.csv", "growth"),
        ("Asher_medication2.csv", "medication"),
        ("Asher_milestone.csv", "milestone"),
        ("Asher_nursing2.csv", "nursing"),
        ("Asher_sleep.csv", "sleep"),
        ("pump_test_file.csv", "pump"),
    ],
)
def test_find_table_name(file_name, expected_result):
    assert find_table_name(file_name) == expected_result


def test_find_table_name_logging_warning(caplog):
    caplog.set_level(logging.WARNING)
    find_table_name("Asher_nonexistant_table.csv")
    assert (
        "No matching table could be found for Asher_nonexistant_table.csv"
        in caplog.text
    )
