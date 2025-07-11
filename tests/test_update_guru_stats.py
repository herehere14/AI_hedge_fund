from datetime import datetime
from types import SimpleNamespace

import pytest

import app.backend.tasks.update_guru_stats as task


def test_calculate_cagr():
    assert task.calculate_cagr(100, 121, 2) == pytest.approx(0.1)
    assert task.calculate_cagr(0, 120, 1) is None
    assert task.calculate_cagr(100, 120, 0) is None


def test_update_guru_stats(monkeypatch):
    stat = SimpleNamespace(
        start_date=datetime(2020, 1, 1),
        end_date=datetime(2021, 1, 1),
        start_value=100,
        end_value=110,
        cagr=None,
    )

    class FakeQuery:
        def all(self):
            return [stat]

    class FakeSession:
        def __init__(self):
            self.committed = False

        def query(self, model):
            assert model is task.GuruStats
            return FakeQuery()

        def commit(self):
            self.committed = True

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(task, "SessionLocal", lambda: FakeSession())
    task.update_guru_stats()
    assert stat.cagr == pytest.approx(0.10)
