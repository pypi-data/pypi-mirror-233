import ee

from .utils import EEType, use_geopandas, get_param, get_required_param, get_fields_from_params
from .utils.gee import (
    load_geometry, area_km2,
    get_result, get_result_key, rename_field, clean_collection, data_from_raster, data_from_raster_by_period,
    defaut_scale, aggregate_by_area, clip_collection
)


def get_size_km2(boundary: dict):
    return area_km2(load_geometry(boundary)).getInfo()


def _data_from_vector(geometry: ee.Geometry, collection: str, params: dict):
    fields = get_fields_from_params(params)
    reducer = get_param(params, 'reducer', 'first')
    collection = ee.FeatureCollection(collection).filterBounds(geometry)
    return aggregate_by_area(clip_collection(collection, geometry), fields, reducer)


def _data_from_raster(geometry: ee.Geometry, collection: str, params: dict):
    image = ee.Image(collection)
    scale = int(get_param(params, 'scale', defaut_scale(image)))
    reducer = get_param(params, 'reducer', 'first')
    fields = get_fields_from_params(params)
    field = fields[0] if len(fields) == 1 else None
    data = data_from_raster(image, geometry, reducer, scale, False)
    return clean_collection(data.map(rename_field(reducer, field)) if field else data)


def _data_from_raster_by_period(geometry: ee.Geometry, collection: str, params: dict):
    image = ee.ImageCollection(collection)
    band_name = get_required_param(params, 'band_name')
    scale = int(get_param(params, 'scale', 10))
    reducer = get_param(params, 'reducer', 'first')
    reducer_regions = get_param(params, 'reducer_regions', 'mean')
    year = str(get_param(params, 'year', 2000))
    start_date = get_param(params, 'start_date', f"{year}-01-01")
    end_date = get_param(params, 'end_date', f"{year}-12-31")
    reducer_years = get_param(params, 'reducer_years')
    fields = get_fields_from_params(params)
    field = fields[0] if len(fields) == 1 else None
    data = data_from_raster_by_period(
        image, geometry, reducer, reducer_regions, scale, band_name, start_date, end_date, False,
        reducer_years=reducer_years
    )
    return clean_collection(data.map(rename_field(reducer_regions, field)) if field else data)


_DATA_BY_TYPE = {
    EEType.VECTOR.value: _data_from_vector,
    EEType.RASTER.value: _data_from_raster,
    EEType.RASTER_BY_PERIOD.value: _data_from_raster_by_period
}


def _run_single_collection(ee_type: str, geometry: ee.Geometry, collection: dict):
    return _DATA_BY_TYPE[ee_type](geometry, collection.get('collection'), collection)


def _run_single(ee_type: str, collections: list, boundaries: list):
    # run each coordinate in sequence, all collections per boundaries
    results = []
    for boundary in boundaries:
        geometry = load_geometry(boundary)
        for collection in collections:
            result = _run_single_collection(ee_type, geometry, collection)
            results.append(get_result(result, get_result_key(collection)))
    return results


def _run_vector(ee_type: str, collections: list, boundaries: list):
    if use_geopandas():
        from .utils.vector import run_by_boundaries
        return run_by_boundaries(collections, boundaries)
    else:
        return _run_single(ee_type, collections, boundaries)


_RUN_BY_TYPE = {
    EEType.VECTOR.value: _run_vector,
    EEType.RASTER.value: _run_single,
    EEType.RASTER_BY_PERIOD.value: _run_single
}


def run(data: dict):
    ee_type = get_required_param(data, 'ee_type')
    collections = get_required_param(data, 'collections')
    boundaries = get_required_param(data, 'boundaries')
    return _RUN_BY_TYPE[ee_type](ee_type, collections, boundaries)
