# tests/test_search_factories_basic.py

from fastapi.testclient import TestClient
from apps.search_app.main import app
from libs.catalogue import models  # Assuming models.Factory and models.RawMaterial exist.
from libs.catalogue.db import get_db

# A very basic FakeQuery that ignores filters and always returns preset factories.
class FakeQuery:
    def __init__(self, factories):
        self.factories = factories

    def filter(self, *args, **kwargs):
        # For simplicity, ignore filter conditions and return self.
        return self

    def all(self):
        return self.factories

# A fake DB session that returns preset factory data.
class FakeDB:
    def __init__(self):
        # Create a dummy factory.
        factory = models.Factory()
        factory.id = 1
        factory.name = "Test Factory"
        factory.location = "Test Location"
        factory.product = "Test Product"
        
        # Create dummy raw materials.
        rm1 = models.RawMaterial()
        rm1.id = 1
        rm1.name = "Material A"
        rm2 = models.RawMaterial()
        rm2.id = 2
        rm2.name = "Material B"
        
        factory.raw_materials = [rm1, rm2]
        self.factories = [factory]

    def query(self, model):
        # If the model is Factory, return a FakeQuery with our preset factories.
        if model == models.Factory:
            return FakeQuery(self.factories)
        # For any other model, return an empty FakeQuery.
        return FakeQuery([])

    def close(self):
        pass

# Override the get_db dependency to yield our fake DB.
def fake_get_db():
    db = FakeDB()
    yield db

app.dependency_overrides[get_db] = fake_get_db

# Create a TestClient for the search app.
client = TestClient(app)

def test_search_factories_no_filter():
    """
    Test the /factories/ endpoint with no filters.
    Expect the endpoint to return our preset factory data.
    """
    response = client.get("/factories/")
    assert response.status_code == 200, response.text

    data = response.json()
    # The endpoint should return a list.
    assert isinstance(data, list)
    # We expect our fake DB to return one factory.
    assert len(data) == 1

    factory = data[0]
    assert factory["name"] == "Test Factory"
    assert factory["location"] == "Test Location"
    assert factory["product"] == "Test Product"

    # Verify that raw_materials are returned as a list with two items.
    assert "raw_materials" in factory
    assert isinstance(factory["raw_materials"], list)
    assert len(factory["raw_materials"]) == 2

    # Check that each raw material has an id and a name.
    for rm in factory["raw_materials"]:
        assert "id" in rm
        assert "name" in rm
