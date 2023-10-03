import os
import json
from tests.utils import fixtures_path
from hestia_earth.earth_engine.boundary import run, get_size_km2

fixtures_folder = os.path.join(fixtures_path, 'boundary')


def test_run_raster_by_period():
    with open(os.path.join(fixtures_folder, 'raster-by-period.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert round(results[0], 10) == 0.7707182633


def test_run_raster_by_period_reduce_years():
    with open(os.path.join(fixtures_folder, 'raster-by-period-reduce-years.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert round(results[0], 10) == 0.9758098238


def test_run_raster():
    with open(os.path.join(fixtures_folder, 'raster.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert round(results[0], 10) == 85


def test_run_raster_multiple():
    with open(os.path.join(fixtures_folder, 'raster-multiple.json'), encoding='utf-8') as f:
        data = json.load(f)

    results = run(data)
    assert [round(r) for r in results] == [85, 1, 1, 36, 1, 1]


def test_run_vector():
    expected = '5180'

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
    expected = ['5180', 'PA0445', '5180', 'PA0402']

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
    with open(os.path.join(fixtures_folder, 'boundary.json'), encoding='utf-8') as f:
        data = json.load(f)

    assert round(get_size_km2(data)) == 5284
