import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from app.backend.main import app
from app.backend.database.models import Base, ThemeIndex
from app.backend.database.connection import get_db


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def override_get_db(session):
    def _override():
        try:
            yield session
        finally:
            pass
    return _override


def test_embedding_insertion_and_search(db_session):
    db_session.add_all([
        ThemeIndex(doc_id="1", ticker="AAPL", embed_vec=[1.0, 0.0]),
        ThemeIndex(doc_id="2", ticker="MSFT", embed_vec=[0.0, 1.0]),
    ])
    db_session.commit()

    app.dependency_overrides[get_db] = override_get_db(db_session)
    client = TestClient(app)

    with patch("app.backend.services.embedding.embed_query", return_value=[1.0, 0.0]):
        res = client.get("/theme", params={"query": "tech"})
    assert res.status_code == 200
    assert res.json()["tickers"][0] == "AAPL"
