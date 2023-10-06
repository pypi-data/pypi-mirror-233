"""
Region

The model calculates the finest scale GADM region possible,
moving from gadm level 5 (for example, a village) to GADM level 0 (Country).
"""
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import linked_node

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from .utils import download, has_coordinates
from . import MODEL

REQUIREMENTS = {
    "Site": {
        "latitude": "",
        "longitude": ""
    }
}
RETURNS = {
    "Term": {"@type": "Term", "termType": "region"}
}
MODEL_KEY = 'region'
EE_PARAMS = {
    'ee_type': 'vector'
}


def _download_by_level(site: dict, level: int):
    gadm_id = download(
        MODEL_KEY,
        site,
        {
            **EE_PARAMS,
            'collection': f"gadm36_{level}",
            'fields': f"GID_{level}"
        },
        only_coordinates=True
    )
    try:
        return None if gadm_id is None else linked_node(download_hestia(f"GADM-{gadm_id}"))
    except Exception:
        # the Term might not exist in our glossary if it was marked as duplicate
        return None


def _run(site: dict):
    for level in [5, 4, 3, 2, 1]:
        value = _download_by_level(site, level)
        if value is not None:
            debugValues(site, model=MODEL, key=MODEL_KEY,
                        value=value.get('@id'))
            break

    return value


def _should_run(site: dict):
    contains_coordinates = has_coordinates(site)

    logRequirements(site, model=MODEL, key=MODEL_KEY,
                    contains_coordinates=contains_coordinates)

    should_run = all([contains_coordinates])
    logShouldRun(site, MODEL, None, should_run, key=MODEL_KEY)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else None
