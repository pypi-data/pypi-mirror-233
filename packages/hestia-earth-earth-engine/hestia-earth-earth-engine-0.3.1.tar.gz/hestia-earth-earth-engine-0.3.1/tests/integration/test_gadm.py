import os
import json
from tests.utils import fixtures_path
from hestia_earth.earth_engine.gadm import run, get_size_km2

fixtures_folder = os.path.join(fixtures_path, 'gadm')


def test_run_raster_by_period():
    with open(os.path.join(fixtures_folder, 'raster-by-period.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert round(results[0], 10) == 0.1705916511


def test_run_raster_by_period_reduce_years():
    with open(os.path.join(fixtures_folder, 'raster-by-period-reduce-years.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert round(results[0], 10) == 0.2302398705


def test_run_raster_by_period_histosol():
    with open(os.path.join(fixtures_folder, 'raster-by-period-histosol.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert round(results[0], 10) == 241.8813767742


def test_run_raster():
    with open(os.path.join(fixtures_folder, 'raster.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert round(results[0], 10) == 78


def test_run_raster_ecoClimateZone():
    with open(os.path.join(fixtures_folder, 'raster-ecoClimateZone.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert round(results[0], 10) == 11


def test_run_vector():
    expected = '10435'

    os.environ['HEE_USE_GEOPANDAS'] = 'true'
    with open(os.path.join(fixtures_folder, 'vector.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert results[0] == expected

    os.environ['HEE_USE_GEOPANDAS'] = 'false'
    with open(os.path.join(fixtures_folder, 'vector-ee.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert results[0] == expected


def test_run_vector_multiple():
    expected = ['4647', 'PA0409', '5592', 'PA0445']

    os.environ['HEE_USE_GEOPANDAS'] = 'true'
    with open(os.path.join(fixtures_folder, 'vector-multiple.json'), encoding='utf-8') as f:
        data = json.load(f)

    values = run(data)
    assert values == expected

    os.environ['HEE_USE_GEOPANDAS'] = 'false'
    with open(os.path.join(fixtures_folder, 'vector-ee-multiple.json'), encoding='utf-8') as f:
        data = json.load(f)

    values = run(data)
    assert values == expected


def test_get_size_km2():
    assert round(get_size_km2('GADM-AUS.8.14_1')) == 78
