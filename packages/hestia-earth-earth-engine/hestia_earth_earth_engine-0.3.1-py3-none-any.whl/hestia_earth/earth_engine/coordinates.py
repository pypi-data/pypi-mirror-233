import ee

from .utils import EEType, use_geopandas, get_param, get_required_param, get_fields_from_params
from .utils.gee import (
    get_result, get_result_key, data_from_raster, data_from_raster_by_period, defaut_scale, clean_collection
)


def _data_from_vector(point: ee.Geometry, collection: str, params: dict):
    fields = get_fields_from_params(params)
    collection = ee.FeatureCollection(collection).filterBounds(point)
    return clean_collection(collection, fields)


def _data_from_raster(point: ee.Geometry, collection: str, params: dict):
    image = ee.Image(collection)
    scale = int(get_param(params, 'scale', defaut_scale(image)))
    reducer = get_param(params, 'reducer', 'first')
    return data_from_raster(image.clip(point), point, reducer, scale)


def _data_from_point_by_period(point: ee.Geometry, collection: str, params: dict):
    image = ee.ImageCollection(collection)
    band_name = get_required_param(params, 'band_name')
    scale = int(get_param(params, 'scale', 10))
    reducer = get_param(params, 'reducer', 'first')
    reducer_regions = get_param(params, 'reducer_regions', 'mean')
    year = str(get_param(params, 'year', 2000))
    start_date = get_param(params, 'start_date', f"{year}-01-01")
    end_date = get_param(params, 'end_date', f"{year}-12-31")
    reducer_years = get_param(params, 'reducer_years')
    return data_from_raster_by_period(
        image, point, reducer, reducer_regions, scale, band_name, start_date, end_date, reducer_years=reducer_years
    )


_DATA_BY_TYPE = {
    EEType.VECTOR.value: _data_from_vector,
    EEType.RASTER.value: _data_from_raster,
    EEType.RASTER_BY_PERIOD.value: _data_from_point_by_period
}


def _run_single_collection(ee_type: str, coords: dict, collection: dict):
    point = ee.Geometry.Point(coords.get('longitude'), coords.get('latitude'))
    return _DATA_BY_TYPE[ee_type](point, collection.get('collection'), collection)


def _run_single(ee_type: str, collections: list, coordinates: list):
    # run each coordinate in sequence, all collections per coordinates
    results = []
    for coords in coordinates:
        for collection in collections:
            result = _run_single_collection(ee_type, coords, collection)
            results.append(get_result(result, get_result_key(collection)))
    return results


def _run_vector(ee_type: str, collections: list, coordinates: list):
    if use_geopandas():
        from .utils.vector import run_by_coordinates
        return run_by_coordinates(collections, coordinates)
    else:
        return _run_single(ee_type, collections, coordinates)


_RUN_BY_TYPE = {
    EEType.VECTOR.value: _run_vector,
    EEType.RASTER.value: _run_single,
    EEType.RASTER_BY_PERIOD.value: _run_single
}


def run(data: dict):
    ee_type = get_required_param(data, 'ee_type')
    collections = get_required_param(data, 'collections')
    coordinates = get_required_param(data, 'coordinates')
    return _RUN_BY_TYPE[ee_type](ee_type, collections, coordinates)
