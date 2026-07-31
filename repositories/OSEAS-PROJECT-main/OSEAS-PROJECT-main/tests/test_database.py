from database import csv_repository


def test_append_and_read_rows(tmp_path):
    path = str(tmp_path / "sample.csv")
    header = ["A", "B"]

    assert csv_repository.read_rows(path) == []

    csv_repository.append_row(path, ["1", "2"], header=header)
    csv_repository.append_row(path, ["3", "4"], header=header)

    rows = csv_repository.read_rows(path)
    assert rows == [["1", "2"], ["3", "4"]]


def test_write_rows_overwrites(tmp_path):
    path = str(tmp_path / "summary.csv")
    csv_repository.write_rows(path, [["Metric", "Value"], ["X", "1"]])
    rows = csv_repository.read_rows(path, skip_header=False)
    assert rows == [["Metric", "Value"], ["X", "1"]]
