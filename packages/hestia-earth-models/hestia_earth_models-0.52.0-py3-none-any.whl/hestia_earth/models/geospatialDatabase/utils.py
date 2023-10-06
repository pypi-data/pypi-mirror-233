import os
from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.api import search

from hestia_earth.models.log import logger, debugValues, logErrorRun, logRequirements
from hestia_earth.models.utils import is_from_model, _load_calculated_node
from hestia_earth.models.utils.site import region_factor, region_level_1_id
from . import MODEL

EXISTING_SEARCH_ENABLED = os.getenv('ENABLE_EXISTING_SEARCH', 'false').lower() == 'true'
MAX_AREA_SIZE = int(os.getenv('MAX_AREA_SIZE', '5000'))


def _collection_name(id: str): return id if '/' in id else f"users/hestiaplatform/{id}"


def has_coordinates(site: dict): return all([site.get('latitude') is not None, site.get('longitude') is not None])


def has_boundary(site: dict): return site.get('boundary') is not None


def _site_gadm_id(site: dict): return site.get('region', site.get('country', {})).get('@id')


def has_geospatial_data(site: dict):
    """
    Determines whether the Site has enough geospatial data to run calculations. We are checking for:
    1. If the coordinates (latitude and longitude) are present
    2. Otherwise if the `region` or `country` is present
    3. Otherwise if the `boundary` is present
    Note: this is a general pre-check only, each model can have 1 or more other checks.

    Parameters
    ----------
    site : dict
        The `Site` node.

    Returns
    -------
    bool
        If we should run geospatial calculations on this model or not.
    """
    return has_coordinates(site) or _site_gadm_id(site) is not None or has_boundary(site)


def _get_boundary_area_size(boundary: dict):
    try:
        from hestia_earth.earth_engine.boundary import get_size_km2
    except ImportError:
        raise ImportError("Run `pip install hestia_earth.earth_engine` to use this functionality")

    try:
        return get_size_km2(boundary)
    except Exception:
        return None


def _get_area_size(site: dict):
    return (
        # fallback if `boundary` provided but no `boundaryArea` was computed
        site.get('boundaryArea') or _get_boundary_area_size(site.get('boundary'))
    ) if has_boundary(site) else download_hestia(_site_gadm_id(site)).get('area')


def _is_below_max_size(term: str, site: dict) -> bool:
    current_size = _get_area_size(site)
    if current_size is not None:
        logRequirements(site, model=MODEL, term=term,
                        current_size=int(current_size),
                        max_area_size=MAX_AREA_SIZE)
        return current_size <= MAX_AREA_SIZE
    return True


def should_download(term: str, site: dict) -> bool:
    return has_coordinates(site) or _is_below_max_size(term, site)


def download(term: str, site: dict, data: dict, only_coordinates=False) -> dict:
    """
    Downloads data from Hestia Earth Engine API.

    Returns
    -------
    dict
        Data returned from the API.
    """
    try:
        from hestia_earth.earth_engine import run
    except ImportError:
        raise ImportError("Run `pip install hestia_earth.earth_engine` to use this functionality")

    try:
        location_data = {
            'coordinates': [{'latitude': site.get('latitude'), 'longitude': site.get('longitude')}]
        } if has_coordinates(site) else ({} if only_coordinates else {
            'boundaries': [site.get('boundary')]
        } if has_boundary(site) else {
            'gadm-ids': [_site_gadm_id(site)]
        })
        data = {
            'ee_type': data.get('ee_type'),
            **location_data,
            'collections': [
                {
                    **data,
                    'collection': _collection_name(data.get('collection'))
                }
            ]
        }
        res = run(data)
        value = res[0] if len(res) > 0 else None
        if value is None:
            debugValues(site, model=MODEL, term=term, value_from_earth_engine=None)
        return value
    except Exception as e:
        logErrorRun(MODEL, term, str(e))
        return None


def get_region_factor(term_id: str, site: dict, termType: TermTermType = TermTermType.MEASUREMENT):
    region_id = region_level_1_id(site.get('region', {}).get('@id'))
    country_id = site.get('country', {}).get('@id')
    return region_factor(MODEL, region_id, term_id, termType) or region_factor(MODEL, country_id, term_id, termType)


def _coordinates_query(site: dict):
    return {
        'filter': {
            'geo_distance': {
                'distance': '1m',
                'location': {
                    'lat': site.get('latitude'),
                    'lon': site.get('longitude')
                }
            }
        }
    } if has_coordinates(site) else None


def _region_query(site: dict):
    query = [
        {'match': {'region.name.keyword': site.get('region').get('name')}}
    ] if site.get('region') else [
        {'match': {'country.name.keyword': site.get('country').get('name')}}
    ] if site.get('country') else None
    return {
        'should': query,
        'minimum_should_match': 1
    } if query else None


def _find_measurement(site: dict, term_id, year: int = None):
    def match(measurement: dict):
        # only use measurements that have been added by the spatial models
        is_added = is_from_model(measurement)
        # match year if required
        same_year = year is None or measurement.get('endDate', '').startswith(str(year))
        return is_added and same_year and measurement.get('term', {}).get('@id') == term_id

    return next((m for m in site.get('measurements', []) if match(m)), None)


def _measurement_query(field: str, value: str):
    return {
        'nested': {
            'path': 'measurements',
            'query': {
                'match': {
                    f"measurements.{field}": value
                }
            }
        }
    }


def _find_existing_sites(site: dict, term_id: str, year: int = None):
    location_query = _coordinates_query(site) or _region_query(site)
    query = {
        'bool': {
            'must': [
                {'match': {'@type': SchemaType.SITE.value}},
                _measurement_query('term.name.keyword', download_hestia(term_id).get('name')),
                _measurement_query('methodModel.name.keyword', 'Spatial')
            ] + ([
                _measurement_query('endDate', year)
            ] if year else []),
            **location_query
        }
    } if location_query else None
    return search(query, sort={'createdAt': 'asc'}) if query else []


def find_existing_measurement(term_id: str, site: dict, year: int = None):
    """
    Find the same Measurement in existing Site to avoid calling the Hestia Earth Engine API.

    Returns
    -------
    dict
        Measurement if found.
    """
    sites = _find_existing_sites(site, term_id, year) if EXISTING_SEARCH_ENABLED else []
    for site in sites:
        data = _load_calculated_node(site, SchemaType.SITE)
        measurement = _find_measurement(data, term_id, year)
        if measurement:
            value = measurement.get('value', [None])[0]
            logger.debug('model=%s, term=%s, matching measurement value=%s', MODEL, term_id, value)
            return value
    return None
