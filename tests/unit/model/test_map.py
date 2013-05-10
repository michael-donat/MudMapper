
import pytest

import model.map as mapModel

@pytest.fixture
def emptyMap():
    return mapModel.Map()

class TestClassLevel:

    def test_addZone(self):

        level = mapModel.Level()

        zone = mapModel.Zone()

        level.assignToZone(zone)

        assert level.zone() is zone

        with pytest.raises(TypeError):
            level.assignToZone(None)



class TestClassMap:

    def test_addZone(self, emptyMap):

        emptyMap.addZone(mapModel.Zone())
        assert len(emptyMap.zones()) == 1

        emptyMap.addZone(mapModel.Zone())
        assert len(emptyMap.zones()) == 2

    def test_addLevel(self, emptyMap):
        pass




class TestClassFactory:

    def test_createNewMap(self):

        map = mapModel.Factory.createNewMap()

        assert isinstance(map, mapModel.Map)

        assert len(map.zones()) == 1, 'There is one zone by default'
        assert len(map.levels()) == 1, 'There is one level by default'
        assert next(map.levels().itervalues()).zone() is next(map.zones().itervalues()), 'Default level belongs to default zone'



