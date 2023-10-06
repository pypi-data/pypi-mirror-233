from hestia_earth.schema import TermTermType

from hestia_earth.models.geospatialDatabase.utils import get_region_factor, _get_area_size


def test_get_region_factor():
    site = {'country': {'@id': 'GADM-ALB'}}
    assert get_region_factor('croppingIntensity', site, TermTermType.LANDUSEMANAGEMENT) == 0.9999775685587958


def test_get_area_size():
    site = {'country': {'@id': 'GADM-ALB'}}
    assert _get_area_size(site) == 28735.42144

    site['boundary'] = {'type': 'Polygon'}
    site['boundaryArea'] = 1000
    assert _get_area_size(site) == 1000
