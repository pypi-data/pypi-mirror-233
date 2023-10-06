import importlib.resources
import os
import re
from pathlib import Path
from unittest import mock

import pytest
from wsgi_shim import check_path_is_not_world_readable
from wsgi_shim import check_path_is_world_readable
from wsgi_shim import Config
from wsgi_shim import is_path_world_readable
from wsgi_shim import load_config
from wsgi_shim import main
from wsgi_shim import WSGIConfigException


def test_is_path_world_readable_no_file(tmp_path):
    file = tmp_path / 'not_a_file'
    with pytest.raises(WSGIConfigException, match=r'does not exist'):
        is_path_world_readable(file)


def test_check_path_is_world_readable_fail():
    file = Path('/root')
    with pytest.raises(WSGIConfigException, match=r'not world readable'):
        check_path_is_world_readable(file)


def test_check_path_is_not_world_readable_fail():
    file = Path('/')
    with pytest.raises(WSGIConfigException, match=r'is world readable'):
        check_path_is_not_world_readable(file)


def test_load_config_empty():
    path = Path('/dev/null')
    data = load_config(path)
    assert isinstance(data, dict)
    assert len(data) == 0


def test_load_config_valid_1(tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text("""
    [wsgi]
    """)
    data = load_config(file)
    assert isinstance(data, dict)
    assert data == {'wsgi': {}}


def test_load_config_fail_perms(tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text("""
    [wsgi]
    """)
    file.chmod(0o200)
    with pytest.raises(WSGIConfigException, match=r'Permission denied'):
        load_config(file)


def test_load_config_fail_missing(tmp_path):
    file = tmp_path / 'config.toml'
    with pytest.raises(WSGIConfigException, match=r'file not found'):
        load_config(file)


def test_load_config_fail_toml_syntax(tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text("""
    [
    """)
    with pytest.raises(WSGIConfigException, match=r'syntax error'):
        load_config(file)


def test_load_config_fail_toml_duplicated_section(tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text("""
    [wsgi]
    [wsgi]
    """)
    with pytest.raises(WSGIConfigException, match=r'syntax error'):
        load_config(file)


@pytest.mark.parametrize(
    'section',
    [
        'wsgi',
        'maintenance_mode',
        'secret_files',
        'environment',
    ],
)
def test_load_config_fail_toml_not_section(section, tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text(f"""
    {section} = "foo"
    """)
    with pytest.raises(WSGIConfigException, match=r'not a section'):
        data = load_config(file)
        Config.from_toml_dict(data, tmp_path)


def test_load_config_fail_toml_missing_section():
    with pytest.raises(WSGIConfigException, match=r'missing .* sections'):
        Config.from_toml_dict({}, Path())


@pytest.mark.parametrize(
    'section,key',
    [
        ('wsgi', 'module'),
        ('wsgi', 'app'),
        ('maintenance_mode', 'title'),
        ('maintenance_mode', 'sentinel_file'),
    ],
)
def test_load_config_fail_toml_values_not_str_1(section, key):
    data = {section: {key: 1}}
    with pytest.raises(WSGIConfigException, match=fr'{section}.{key} not a string'):
        Config.from_toml_dict(data, Path())


@pytest.mark.parametrize(
    'section,key',
    [
        ('secret_files', 'filename'),
        ('environment', 'foobar'),
    ],
)
def test_load_config_fail_toml_values_not_str(section, key):
    data = {'wsgi': {}, section: {key: 1}}
    with pytest.raises(WSGIConfigException, match=fr'{section}.{key} not a string'):
        Config.from_toml_dict(data, Path())


@pytest.mark.parametrize(
    'section,key',
    [
        ('secret_files', '0_key_leading_digit'),
        ('environment', 'key_$_special_char'),
    ],
)
def test_load_config_fail_toml_invalid_key(section, key):
    data = {'wsgi': {}, section: {key: 1}}
    with pytest.raises(WSGIConfigException, match=fr'invalid key .* in \[{section}\]'):
        Config.from_toml_dict(data, Path())


def test_load_config_fail_toml_duplicate_keys():
    data = {
        'wsgi': {},
        'secret_files': {'key': 'value1'},
        'environment': {'key': 'value2'},
    }
    with pytest.raises(WSGIConfigException, match=r'duplicated across sections'):
        Config.from_toml_dict(data, Path())


def test_update_os_environment_conflict(monkeypatch):
    data = {
        'wsgi': {},
        'environment': {'FOOBAR': 'value'},
    }
    monkeypatch.setenv('FOOBAR', 'something')
    with pytest.raises(WSGIConfigException, match=r'already has key'):
        config = Config.from_toml_dict(data, Path())
        config.update_os_environment()


@mock.patch.dict(os.environ, {})
def test_update_os_environment_success():
    data = {
        'wsgi': {},
        'environment': {'FOOBAR': 'value'},
    }
    config = Config.from_toml_dict(data, Path())
    assert 'FOOBAR' not in os.environ
    config.update_os_environment()
    assert os.environ['FOOBAR'] == 'value'


def test_load_config_fail_toml_bad_sentinel_file():
    data = {
        'maintenance_mode': {'sentinel_file': '/foobar/maint.txt'},
    }
    with pytest.raises(WSGIConfigException, match=r'not in a readable dir'):
        Config.from_toml_dict(data, Path())


def test_check_secret_files_fail_missing(tmp_path):
    missing_file = tmp_path / 'not_there'
    data = {
        'wsgi': {},
        'secret_files': {'SECRET': str(missing_file)},
    }
    config = Config.from_toml_dict(data, Path())
    with pytest.raises(WSGIConfigException, match=r'is missing or not readable'):
        config.check_secret_files()


def test_check_secret_files_fail_cant_read(tmp_path):
    unreadable_file = tmp_path / 'unreadable'
    unreadable_file.touch(mode=0o000)
    data = {
        'wsgi': {},
        'secret_files': {'SECRET': str(unreadable_file)},
    }
    config = Config.from_toml_dict(data, Path())
    with pytest.raises(WSGIConfigException, match=r'is missing or not readable'):
        config.check_secret_files()


def test_check_secret_files_fail_too_permissive(tmp_path):
    permissive_file = tmp_path / 'permissive'
    permissive_file.touch()
    permissive_file.chmod(mode=0x777)
    data = {
        'wsgi': {},
        'secret_files': {'SECRET': str(permissive_file)},
    }
    config = Config.from_toml_dict(data, Path())
    with pytest.raises(WSGIConfigException, match=r'not adequately protected'):
        config.check_secret_files()


def test_check_secret_files_fail_not_absolute():
    data = {
        'wsgi': {},
        'secret_files': {'FOOBAR': 'not_absolute_path'},
    }
    config = Config.from_toml_dict(data, Path())
    with pytest.raises(WSGIConfigException, match=r'not an absolute path'):
        config.check_secret_files()


def app_wrapper(app) -> tuple[str, str, list[tuple[str, str]]]:
    captured_status = ''
    captured_headers = []

    def start_response(status, headers, _exc_info=None):
        nonlocal captured_status
        nonlocal captured_headers
        captured_status = status
        captured_headers = headers

    html = app({}, start_response)[0].decode('utf-8')  # noqa
    return html, captured_status, captured_headers


def test_hello_world():
    from src.wsgi_shim.hello_world import app_hello_world as app_under_test
    html, status, headers = app_wrapper(app_under_test)
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2


def test_main_maintenance_mode_normal(tmp_path):
    maint_file = tmp_path / 'maint.txt'
    maint_file.touch()
    config_file = tmp_path / 'config.toml'
    config_file.write_text(f"""
    [maintenance_mode]
    title = "Maintenance Page"
    sentinel_file = "{maint_file}"
    """)
    app = main(tmp_path)
    html, status, headers = app_wrapper(app)
    assert re.search(r'This site is down for maintenance', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_main_fail_no_module(tmp_path):
    config_file = tmp_path / 'config.toml'
    config_file.write_text("""
    [wsgi]
    module = "not_there"
    app = "unused"
    """)
    app = main(tmp_path)
    html, status, headers = app_wrapper(app)
    assert re.search(r'Cannot load not_there.unused: No module', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_main_fail_module_perms(tmp_path, monkeypatch):
    unreadable_file = tmp_path / 'unreadable.py'
    unreadable_file.touch(mode=0o000)
    monkeypatch.syspath_prepend(tmp_path)
    config_file = tmp_path / 'config.toml'
    config_file.write_text("""
    [wsgi]
    module = "unreadable"
    app = "unused"
    """)
    app = main(tmp_path)
    html, status, headers = app_wrapper(app)
    assert re.search(r'Cannot load .* Permission denied: ', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_main_fail_no_app(tmp_path, monkeypatch):
    empty_file = tmp_path / 'empty_module.py'
    empty_file.touch()
    monkeypatch.syspath_prepend(tmp_path)
    config_file = tmp_path / 'config.toml'
    config_file.write_text("""
    [wsgi]
    module = "empty_module"
    app = "unused"
    """)
    app = main(tmp_path)
    html, status, headers = app_wrapper(app)
    assert re.search(r'Cannot load .* module .* has no attribute', html)
    assert status == '503 Service Unavailable'
    assert len(headers) == 3


def test_main_normal_module_file(tmp_path, monkeypatch):
    with importlib.resources.files('wsgi_shim').joinpath('hello_world.py').open('r') as f:
        app_source = f.read()
    app_module_file = tmp_path / 'myapp.py'
    app_module_file.write_text(app_source)
    config_file = tmp_path / 'config.toml'
    config_file.write_text(f"""
    [wsgi]
    module = "{app_module_file}"
    app = "app_hello_world"
    """)
    monkeypatch.syspath_prepend(tmp_path)
    app = main(tmp_path)
    html, status, headers = app_wrapper(app)
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2


def test_main_normal_module_default(tmp_path):
    config_file = tmp_path / 'config.toml'
    config_file.write_text("""
    [wsgi]
    module = "wsgi_shim.hello_world"
    app = "app_hello_world"
    """)
    app = main(tmp_path)
    html, status, headers = app_wrapper(app)
    assert re.search(r'Hello, World', html)
    assert status == '200 OK'
    assert len(headers) == 2
