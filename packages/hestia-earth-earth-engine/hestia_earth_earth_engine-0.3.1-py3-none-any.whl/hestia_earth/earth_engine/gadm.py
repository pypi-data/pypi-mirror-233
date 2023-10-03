import ee

from .utils import EEType, use_geopandas, get_param, get_required_param, get_fields_from_params
from .utils.gee import (
    load_region, area_km2, get_point,
    get_result, get_result_key, rename_field, clean_collection, data_from_raster, data_from_raster_by_period,
    defaut_scale, aggregate_by_area, clip_collection
)

DEFAULT_SCALE = 30
DEFAULT_YEAR = 2000


def get_size_km2(gadm_id: str):
    region = load_region(gadm_id)
    return area_km2(region.geometry()).getInfo()


def get_distance_to_coordinates(gadm_id: str, latitude: float, longitude: float):
    """
    Returns the distance between the coordinates and the GADM region, in meters.
    """
    region = load_region(gadm_id)
    coordinates = get_point(longitude=longitude, latitude=latitude)
    return region.geometry().distance(coordinates).getInfo()


def get_id_by_coordinates(level: int, latitude: float, longitude: float):
    """
    Returns the GADM ID of the closest region to the coordinates by level (0 to 5).
    """
    collection = load_region(level=level)
    coordinates = get_point(longitude=longitude, latitude=latitude)
    region = collection.filterBounds(coordinates).first()
    return region.get(f"GID_{level}").getInfo()


def _data_from_vector(region: ee.FeatureCollection, collection: str, params: dict):
    fields = get_fields_from_params(params)
    reducer = get_param(params, 'reducer', 'first')
    collection = ee.FeatureCollection(collection).filterBounds(region)
    return aggregate_by_area(clip_collection(collection, region.geometry()), fields, reducer)


def _data_from_raster(region: ee.FeatureCollection, collection: str, params: dict):
    image = ee.Image(collection)
    scale = int(get_param(params, 'scale', defaut_scale(image, default=DEFAULT_SCALE)))
    reducer = get_param(params, 'reducer', 'mean')
    fields = get_fields_from_params(params)
    field = fields[0] if len(fields) == 1 else None
    data = data_from_raster(image.clip(region), region, reducer, scale, False)
    return clean_collection(data.map(rename_field(reducer, field)) if field else data)


def _data_from_raster_by_period(region: ee.FeatureCollection, collection: str, params: dict):
    image = ee.ImageCollection(collection)
    band_name = get_required_param(params, 'band_name')
    scale = int(get_param(params, 'scale', DEFAULT_SCALE))
    reducer = get_param(params, 'reducer', 'mean')
    reducer_regions = get_param(params, 'reducer_regions', 'mean')
    year = str(get_param(params, 'year', DEFAULT_YEAR))
    start_date = get_param(params, 'start_date', f"{year}-01-01")
    end_date = get_param(params, 'end_date', f"{year}-12-31")
    reducer_years = get_param(params, 'reducer_years')
    fields = get_fields_from_params(params)
    field = fields[0] if len(fields) == 1 else None
    data = data_from_raster_by_period(
        image, region, reducer, reducer_regions, scale, band_name, start_date, end_date, False,
        reducer_years=reducer_years
    )
    return clean_collection(data.map(rename_field(reducer_regions, field)) if field else data)


_DATA_BY_TYPE = {
    EEType.VECTOR.value: _data_from_vector,
    EEType.RASTER.value: _data_from_raster,
    EEType.RASTER_BY_PERIOD.value: _data_from_raster_by_period
}


def _run_single_collection(ee_type: str, geometry: ee.FeatureCollection, collection: dict):
    return _DATA_BY_TYPE[ee_type](geometry, collection.get('collection'), collection)


def _run_single(ee_type: str, collections: list, gadm_ids: list):
    # run each coordinate in sequence, all collections per gadm ID
    results = []
    for gadm_id in gadm_ids:
        region = load_region(gadm_id)
        for collection in collections:
            result = _run_single_collection(ee_type, region, collection)
            results.append(get_result(result, get_result_key(collection)))
    return results


def _run_vector(ee_type: str, collections: list, gadm_ids: list):
    if use_geopandas():
        from .utils.vector import run_by_gadm_ids
        return run_by_gadm_ids(collections, gadm_ids)
    else:
        return _run_single(ee_type, collections, gadm_ids)


_RUN_BY_TYPE = {
    EEType.VECTOR.value: _run_vector,
    EEType.RASTER.value: _run_single,
    EEType.RASTER_BY_PERIOD.value: _run_single
}


def run(data: dict):
    ee_type = get_required_param(data, 'ee_type')
    collections = get_required_param(data, 'collections')
    gadm_ids = get_required_param(data, 'gadm-ids')
    return _RUN_BY_TYPE[ee_type](ee_type, collections, gadm_ids)
