from fastapi.testclient import TestClient
from apps.admin_app.main import app
from libs.catalogue.db import get_db

# A minimal fake DB session that supports the operations used by the endpoint.
class FakeDB:
    def __init__(self):
        self.added_objects = []

    def query(self, model):
        # For simplicity, always return self (i.e. no existing objects).
        self._model = model
        return self

    def filter(self, condition):
        # Always return self; our fake always simulates "not found".
        return self

    def first(self):
        # Simulate that no matching record exists.
        return None

    def add(self, obj):
        # Record the added object.
        self.added_objects.append(obj)

    def flush(self):
        # No-op in this fake.
        pass

    def commit(self):
        # No-op in this fake.
        pass

    def refresh(self, obj):
        # Simulate that the object receives an ID.
        obj.id = 1
        # Also assign IDs to raw materials.
        if hasattr(obj, "raw_materials"):
            for i, rm in enumerate(obj.raw_materials):
                rm.id = i + 1
        return

    def close(self):
        # No-op.
        pass

# Override the get_db dependency with our fake.
def fake_get_db():
    db = FakeDB()
    yield db

app.dependency_overrides[get_db] = fake_get_db

client = TestClient(app)

def test_create_factory_basic():
    payload = {
        "name": "Test Factory",
        "location": "Test Location",
        "product": "Test Product",
        "raw_materials": ["Material A", "Material B"]
    }
    response = client.post("/factories/", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["location"] == payload["location"]
    assert data["product"] == payload["product"]

    # Verify that raw_materials are returned as a list with two items.
    assert isinstance(data["raw_materials"], list)
    assert len(data["raw_materials"]) == 2

    for rm in data["raw_materials"]:
        assert "id" in rm
        assert "name" in rm
        assert rm["name"] in payload["raw_materials"]
