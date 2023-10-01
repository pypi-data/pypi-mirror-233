import logging
import sys

import pytest
from flexmock import flexmock

from borgmatic.borg import create as module

from ..test_verbosity import insert_logging_mock


def test_expand_directory_with_basic_path_passes_it_through():
    flexmock(module.os.path).should_receive('expanduser').and_return('foo')
    flexmock(module.glob).should_receive('glob').and_return([])

    paths = module.expand_directory('foo')

    assert paths == ['foo']


def test_expand_directory_with_glob_expands():
    flexmock(module.os.path).should_receive('expanduser').and_return('foo*')
    flexmock(module.glob).should_receive('glob').and_return(['foo', 'food'])

    paths = module.expand_directory('foo*')

    assert paths == ['foo', 'food']


def test_expand_directories_flattens_expanded_directories():
    flexmock(module).should_receive('expand_directory').with_args('~/foo').and_return(['/root/foo'])
    flexmock(module).should_receive('expand_directory').with_args('bar*').and_return(
        ['bar', 'barf']
    )

    paths = module.expand_directories(('~/foo', 'bar*'))

    assert paths == ('/root/foo', 'bar', 'barf')


def test_expand_directories_considers_none_as_no_directories():
    paths = module.expand_directories(None)

    assert paths == ()


def test_expand_home_directories_expands_tildes():
    flexmock(module.os.path).should_receive('expanduser').with_args('~/bar').and_return('/foo/bar')
    flexmock(module.os.path).should_receive('expanduser').with_args('baz').and_return('baz')

    paths = module.expand_home_directories(('~/bar', 'baz'))

    assert paths == ('/foo/bar', 'baz')


def test_expand_home_directories_considers_none_as_no_directories():
    paths = module.expand_home_directories(None)

    assert paths == ()


def test_map_directories_to_devices_gives_device_id_per_path():
    flexmock(module.os).should_receive('stat').with_args('/foo').and_return(flexmock(st_dev=55))
    flexmock(module.os).should_receive('stat').with_args('/bar').and_return(flexmock(st_dev=66))

    device_map = module.map_directories_to_devices(('/foo', '/bar'))

    assert device_map == {
        '/foo': 55,
        '/bar': 66,
    }


def test_map_directories_to_devices_with_missing_path_does_not_error():
    flexmock(module.os).should_receive('stat').with_args('/foo').and_return(flexmock(st_dev=55))
    flexmock(module.os).should_receive('stat').with_args('/bar').and_raise(FileNotFoundError)

    device_map = module.map_directories_to_devices(('/foo', '/bar'))

    assert device_map == {
        '/foo': 55,
        '/bar': None,
    }


@pytest.mark.parametrize(
    'directories,additional_directories,expected_directories',
    (
        ({'/': 1, '/root': 1}, {}, ('/',)),
        ({'/': 1, '/root/': 1}, {}, ('/',)),
        ({'/': 1, '/root': 2}, {}, ('/', '/root')),
        ({'/root': 1, '/': 1}, {}, ('/',)),
        ({'/root': 1, '/root/foo': 1}, {}, ('/root',)),
        ({'/root/': 1, '/root/foo': 1}, {}, ('/root/',)),
        ({'/root': 1, '/root/foo/': 1}, {}, ('/root',)),
        ({'/root': 1, '/root/foo': 2}, {}, ('/root', '/root/foo')),
        ({'/root/foo': 1, '/root': 1}, {}, ('/root',)),
        ({'/root': None, '/root/foo': None}, {}, ('/root', '/root/foo')),
        ({'/root': 1, '/etc': 1, '/root/foo/bar': 1}, {}, ('/etc', '/root')),
        ({'/root': 1, '/root/foo': 1, '/root/foo/bar': 1}, {}, ('/root',)),
        ({'/dup': 1, '/dup': 1}, {}, ('/dup',)),
        ({'/foo': 1, '/bar': 1}, {}, ('/bar', '/foo')),
        ({'/foo': 1, '/bar': 2}, {}, ('/bar', '/foo')),
        ({'/root/foo': 1}, {'/root': 1}, ()),
        ({'/root/foo': 1}, {'/root': 2}, ('/root/foo',)),
        ({'/root/foo': 1}, {}, ('/root/foo',)),
    ),
)
def test_deduplicate_directories_removes_child_paths_on_the_same_filesystem(
    directories, additional_directories, expected_directories
):
    assert (
        module.deduplicate_directories(directories, additional_directories) == expected_directories
    )


def test_write_pattern_file_writes_pattern_lines():
    temporary_file = flexmock(name='filename', flush=lambda: None)
    temporary_file.should_receive('write').with_args('R /foo\n+ /foo/bar')
    flexmock(module.tempfile).should_receive('NamedTemporaryFile').and_return(temporary_file)

    module.write_pattern_file(['R /foo', '+ /foo/bar'])


def test_write_pattern_file_with_sources_writes_sources_as_roots():
    temporary_file = flexmock(name='filename', flush=lambda: None)
    temporary_file.should_receive('write').with_args('R /foo\n+ /foo/bar\nR /baz\nR /quux')
    flexmock(module.tempfile).should_receive('NamedTemporaryFile').and_return(temporary_file)

    module.write_pattern_file(['R /foo', '+ /foo/bar'], sources=['/baz', '/quux'])


def test_write_pattern_file_without_patterns_but_with_sources_writes_sources_as_roots():
    temporary_file = flexmock(name='filename', flush=lambda: None)
    temporary_file.should_receive('write').with_args('R /baz\nR /quux')
    flexmock(module.tempfile).should_receive('NamedTemporaryFile').and_return(temporary_file)

    module.write_pattern_file([], sources=['/baz', '/quux'])


def test_write_pattern_file_with_empty_exclude_patterns_does_not_raise():
    module.write_pattern_file([])


def test_write_pattern_file_overwrites_existing_file():
    pattern_file = flexmock(name='filename', flush=lambda: None)
    pattern_file.should_receive('seek').with_args(0).once()
    pattern_file.should_receive('write').with_args('R /foo\n+ /foo/bar')
    flexmock(module.tempfile).should_receive('NamedTemporaryFile').never()

    module.write_pattern_file(['R /foo', '+ /foo/bar'], pattern_file=pattern_file)


@pytest.mark.parametrize(
    'filename_lists,opened_filenames',
    (
        ([('foo', 'bar'), ('baz', 'quux')], ('foo', 'bar', 'baz', 'quux')),
        ([None, ('foo', 'bar')], ('foo', 'bar')),
        ([None, None], ()),
    ),
)
def test_ensure_files_readable_opens_filenames(filename_lists, opened_filenames):
    for expected_filename in opened_filenames:
        flexmock(sys.modules['builtins']).should_receive('open').with_args(
            expected_filename
        ).and_return(flexmock(close=lambda: None))

    module.ensure_files_readable(*filename_lists)


def test_make_pattern_flags_includes_pattern_filename_when_given():
    pattern_flags = module.make_pattern_flags(
        config={'patterns': ['R /', '- /var']}, pattern_filename='/tmp/patterns'
    )

    assert pattern_flags == ('--patterns-from', '/tmp/patterns')


def test_make_pattern_flags_includes_patterns_from_filenames_when_in_config():
    pattern_flags = module.make_pattern_flags(config={'patterns_from': ['patterns', 'other']})

    assert pattern_flags == ('--patterns-from', 'patterns', '--patterns-from', 'other')


def test_make_pattern_flags_includes_both_filenames_when_patterns_given_and_patterns_from_in_config():
    pattern_flags = module.make_pattern_flags(
        config={'patterns_from': ['patterns']}, pattern_filename='/tmp/patterns'
    )

    assert pattern_flags == ('--patterns-from', 'patterns', '--patterns-from', '/tmp/patterns')


def test_make_pattern_flags_considers_none_patterns_from_filenames_as_empty():
    pattern_flags = module.make_pattern_flags(config={'patterns_from': None})

    assert pattern_flags == ()


def test_make_exclude_flags_includes_exclude_patterns_filename_when_given():
    exclude_flags = module.make_exclude_flags(
        config={'exclude_patterns': ['*.pyc', '/var']}, exclude_filename='/tmp/excludes'
    )

    assert exclude_flags == ('--exclude-from', '/tmp/excludes')


def test_make_exclude_flags_includes_exclude_from_filenames_when_in_config():
    exclude_flags = module.make_exclude_flags(config={'exclude_from': ['excludes', 'other']})

    assert exclude_flags == ('--exclude-from', 'excludes', '--exclude-from', 'other')


def test_make_exclude_flags_includes_both_filenames_when_patterns_given_and_exclude_from_in_config():
    exclude_flags = module.make_exclude_flags(
        config={'exclude_from': ['excludes']}, exclude_filename='/tmp/excludes'
    )

    assert exclude_flags == ('--exclude-from', 'excludes', '--exclude-from', '/tmp/excludes')


def test_make_exclude_flags_considers_none_exclude_from_filenames_as_empty():
    exclude_flags = module.make_exclude_flags(config={'exclude_from': None})

    assert exclude_flags == ()


def test_make_exclude_flags_includes_exclude_caches_when_true_in_config():
    exclude_flags = module.make_exclude_flags(config={'exclude_caches': True})

    assert exclude_flags == ('--exclude-caches',)


def test_make_exclude_flags_does_not_include_exclude_caches_when_false_in_config():
    exclude_flags = module.make_exclude_flags(config={'exclude_caches': False})

    assert exclude_flags == ()


def test_make_exclude_flags_includes_exclude_if_present_when_in_config():
    exclude_flags = module.make_exclude_flags(
        config={'exclude_if_present': ['exclude_me', 'also_me']}
    )

    assert exclude_flags == (
        '--exclude-if-present',
        'exclude_me',
        '--exclude-if-present',
        'also_me',
    )


def test_make_exclude_flags_includes_keep_exclude_tags_when_true_in_config():
    exclude_flags = module.make_exclude_flags(config={'keep_exclude_tags': True})

    assert exclude_flags == ('--keep-exclude-tags',)


def test_make_exclude_flags_does_not_include_keep_exclude_tags_when_false_in_config():
    exclude_flags = module.make_exclude_flags(config={'keep_exclude_tags': False})

    assert exclude_flags == ()


def test_make_exclude_flags_includes_exclude_nodump_when_true_in_config():
    exclude_flags = module.make_exclude_flags(config={'exclude_nodump': True})

    assert exclude_flags == ('--exclude-nodump',)


def test_make_exclude_flags_does_not_include_exclude_nodump_when_false_in_config():
    exclude_flags = module.make_exclude_flags(config={'exclude_nodump': False})

    assert exclude_flags == ()


def test_make_exclude_flags_is_empty_when_config_has_no_excludes():
    exclude_flags = module.make_exclude_flags(config={})

    assert exclude_flags == ()


def test_make_list_filter_flags_with_debug_and_feature_available_includes_plus_and_minus():
    flexmock(module.logger).should_receive('isEnabledFor').and_return(True)
    flexmock(module.feature).should_receive('available').and_return(True)

    assert module.make_list_filter_flags(local_borg_version=flexmock(), dry_run=False) == 'AME+-'


def test_make_list_filter_flags_with_info_and_feature_available_omits_plus_and_minus():
    flexmock(module.logger).should_receive('isEnabledFor').and_return(False)
    flexmock(module.feature).should_receive('available').and_return(True)

    assert module.make_list_filter_flags(local_borg_version=flexmock(), dry_run=False) == 'AME'


def test_make_list_filter_flags_with_debug_and_feature_available_and_dry_run_includes_plus_and_minus():
    flexmock(module.logger).should_receive('isEnabledFor').and_return(True)
    flexmock(module.feature).should_receive('available').and_return(True)

    assert module.make_list_filter_flags(local_borg_version=flexmock(), dry_run=True) == 'AME+-'


def test_make_list_filter_flags_with_info_and_feature_available_and_dry_run_includes_plus_and_minus():
    flexmock(module.logger).should_receive('isEnabledFor').and_return(False)
    flexmock(module.feature).should_receive('available').and_return(True)

    assert module.make_list_filter_flags(local_borg_version=flexmock(), dry_run=True) == 'AME+-'


def test_make_list_filter_flags_with_debug_and_feature_not_available_includes_x():
    flexmock(module.logger).should_receive('isEnabledFor').and_return(True)
    flexmock(module.feature).should_receive('available').and_return(False)

    assert module.make_list_filter_flags(local_borg_version=flexmock(), dry_run=False) == 'AMEx-'


def test_make_list_filter_flags_with_info_and_feature_not_available_omits_x():
    flexmock(module.logger).should_receive('isEnabledFor').and_return(False)
    flexmock(module.feature).should_receive('available').and_return(False)

    assert module.make_list_filter_flags(local_borg_version=flexmock(), dry_run=False) == 'AME-'


def test_collect_borgmatic_source_directories_set_when_directory_exists():
    flexmock(module.os.path).should_receive('exists').and_return(True)
    flexmock(module.os.path).should_receive('expanduser')

    assert module.collect_borgmatic_source_directories('/tmp') == ['/tmp']


def test_collect_borgmatic_source_directories_empty_when_directory_does_not_exist():
    flexmock(module.os.path).should_receive('exists').and_return(False)
    flexmock(module.os.path).should_receive('expanduser')

    assert module.collect_borgmatic_source_directories('/tmp') == []


def test_collect_borgmatic_source_directories_defaults_when_directory_not_given():
    flexmock(module.os.path).should_receive('exists').and_return(True)
    flexmock(module.os.path).should_receive('expanduser')

    assert module.collect_borgmatic_source_directories(None) == [
        module.state.DEFAULT_BORGMATIC_SOURCE_DIRECTORY
    ]


def test_pattern_root_directories_deals_with_none_patterns():
    assert module.pattern_root_directories(patterns=None) == []


def test_pattern_root_directories_parses_roots_and_ignores_others():
    assert module.pattern_root_directories(
        ['R /root', '+ /root/foo', '- /root/foo/bar', 'R /baz']
    ) == ['/root', '/baz']


@pytest.mark.parametrize(
    'character_device,block_device,fifo,expected_result',
    (
        (False, False, False, False),
        (True, False, False, True),
        (False, True, False, True),
        (True, True, False, True),
        (False, False, True, True),
        (False, True, True, True),
        (True, False, True, True),
    ),
)
def test_special_file_looks_at_file_type(character_device, block_device, fifo, expected_result):
    flexmock(module.os).should_receive('stat').and_return(flexmock(st_mode=flexmock()))
    flexmock(module.stat).should_receive('S_ISCHR').and_return(character_device)
    flexmock(module.stat).should_receive('S_ISBLK').and_return(block_device)
    flexmock(module.stat).should_receive('S_ISFIFO').and_return(fifo)

    assert module.special_file('/dev/special') == expected_result


def test_special_file_treats_broken_symlink_as_non_special():
    flexmock(module.os).should_receive('stat').and_raise(FileNotFoundError)

    assert module.special_file('/broken/symlink') is False


def test_any_parent_directories_treats_parents_as_match():
    module.any_parent_directories('/foo/bar.txt', ('/foo', '/etc'))


def test_any_parent_directories_treats_grandparents_as_match():
    module.any_parent_directories('/foo/bar/baz.txt', ('/foo', '/etc'))


def test_any_parent_directories_treats_unrelated_paths_as_non_match():
    module.any_parent_directories('/foo/bar.txt', ('/usr', '/etc'))


def test_collect_special_file_paths_parses_special_files_from_borg_dry_run_file_list():
    flexmock(module).should_receive('execute_command_and_capture_output').and_return(
        'Processing files ...\n- /foo\n+ /bar\n- /baz'
    )
    flexmock(module).should_receive('special_file').and_return(True)
    flexmock(module).should_receive('any_parent_directories').and_return(False)

    assert module.collect_special_file_paths(
        ('borg', 'create'),
        local_path=None,
        working_directory=None,
        borg_environment=None,
        skip_directories=flexmock(),
    ) == ('/foo', '/bar', '/baz')


def test_collect_special_file_paths_excludes_requested_directories():
    flexmock(module).should_receive('execute_command_and_capture_output').and_return(
        '+ /foo\n- /bar\n- /baz'
    )
    flexmock(module).should_receive('special_file').and_return(True)
    flexmock(module).should_receive('any_parent_directories').and_return(False).and_return(
        True
    ).and_return(False)

    assert module.collect_special_file_paths(
        ('borg', 'create'),
        local_path=None,
        working_directory=None,
        borg_environment=None,
        skip_directories=flexmock(),
    ) == ('/foo', '/baz')


def test_collect_special_file_paths_excludes_non_special_files():
    flexmock(module).should_receive('execute_command_and_capture_output').and_return(
        '+ /foo\n+ /bar\n+ /baz'
    )
    flexmock(module).should_receive('special_file').and_return(True).and_return(False).and_return(
        True
    )
    flexmock(module).should_receive('any_parent_directories').and_return(False)

    assert module.collect_special_file_paths(
        ('borg', 'create'),
        local_path=None,
        working_directory=None,
        borg_environment=None,
        skip_directories=flexmock(),
    ) == ('/foo', '/baz')


def test_collect_special_file_paths_omits_exclude_no_dump_flag_from_command():
    flexmock(module).should_receive('execute_command_and_capture_output').with_args(
        ('borg', 'create', '--dry-run', '--list'),
        capture_stderr=True,
        working_directory=None,
        extra_environment=None,
        borg_local_path='borg',
    ).and_return('Processing files ...\n- /foo\n+ /bar\n- /baz').once()
    flexmock(module).should_receive('special_file').and_return(True)
    flexmock(module).should_receive('any_parent_directories').and_return(False)

    module.collect_special_file_paths(
        ('borg', 'create', '--exclude-nodump'),
        local_path='borg',
        working_directory=None,
        borg_environment=None,
        skip_directories=flexmock(),
    )


DEFAULT_ARCHIVE_NAME = '{hostname}-{now:%Y-%m-%dT%H:%M:%S.%f}'  # noqa: FS003
REPO_ARCHIVE_WITH_PATHS = (f'repo::{DEFAULT_ARCHIVE_NAME}', 'foo', 'bar')


def test_create_archive_calls_borg_with_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_calls_borg_with_environment():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    environment = {'BORG_THINGY': 'YUP'}
    flexmock(module.environment).should_receive('make_environment').and_return(environment)
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=environment,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_patterns_calls_borg_with_patterns_including_converted_source_directories():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    pattern_flags = ('--patterns-from', 'patterns')
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(
        flexmock(name='/tmp/patterns')
    ).and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(pattern_flags)
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + pattern_flags + (f'repo::{DEFAULT_ARCHIVE_NAME}',),
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'patterns': ['pattern'],
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_sources_and_used_config_paths_calls_borg_with_sources_and_config_paths():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(
        ('foo', 'bar', '/etc/borgmatic/config.yaml')
    )
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').with_args([]).and_return(())
    flexmock(module).should_receive('expand_directories').with_args(
        ('foo', 'bar', '/etc/borgmatic/config.yaml')
    ).and_return(('foo', 'bar', '/etc/borgmatic/config.yaml'))
    flexmock(module).should_receive('expand_directories').with_args([]).and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    environment = {'BORG_THINGY': 'YUP'}
    flexmock(module.environment).should_receive('make_environment').and_return(environment)
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + REPO_ARCHIVE_WITH_PATHS + ('/etc/borgmatic/config.yaml',),
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=environment,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=['/etc/borgmatic/config.yaml']),
    )


def test_create_archive_with_sources_and_used_config_paths_with_store_config_files_false_calls_borg_with_sources_and_no_config_paths():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').with_args([]).and_return(())
    flexmock(module).should_receive('expand_directories').with_args(('foo', 'bar')).and_return(
        ('foo', 'bar')
    )
    flexmock(module).should_receive('expand_directories').with_args([]).and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    environment = {'BORG_THINGY': 'YUP'}
    flexmock(module.environment).should_receive('make_environment').and_return(environment)
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=environment,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'store_config_files': False,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=['/etc/borgmatic/config.yaml']),
    )


def test_create_archive_with_exclude_patterns_calls_borg_with_excludes():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    exclude_flags = ('--exclude-from', 'excludes')
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(('exclude',))
    flexmock(module).should_receive('write_pattern_file').and_return(None).and_return(
        flexmock(name='/tmp/excludes')
    )
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(exclude_flags)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + exclude_flags + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': ['exclude'],
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_log_info_calls_borg_with_info_parameter():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--info') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    insert_logging_mock(logging.INFO)

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_log_info_and_json_suppresses_most_borg_output():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command_and_capture_output').with_args(
        ('borg', 'create', '--json') + REPO_ARCHIVE_WITH_PATHS,
        working_directory=None,
        extra_environment=None,
        borg_local_path='borg',
    )
    insert_logging_mock(logging.INFO)

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        json=True,
    )


def test_create_archive_with_log_debug_calls_borg_with_debug_parameter():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--debug', '--show-rc') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    insert_logging_mock(logging.DEBUG)

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_log_debug_and_json_suppresses_most_borg_output():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command_and_capture_output').with_args(
        ('borg', 'create', '--json') + REPO_ARCHIVE_WITH_PATHS,
        working_directory=None,
        extra_environment=None,
        borg_local_path='borg',
    )
    insert_logging_mock(logging.DEBUG)

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        json=True,
    )


def test_create_archive_with_dry_run_calls_borg_with_dry_run_parameter():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--dry-run') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=True,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_stats_and_dry_run_calls_borg_without_stats_parameter():
    # --dry-run and --stats are mutually exclusive, see:
    # https://borgbackup.readthedocs.io/en/stable/usage/create.html#description
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--dry-run', '--info') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    insert_logging_mock(logging.INFO)

    module.create_archive(
        dry_run=True,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        stats=True,
    )


def test_create_archive_with_checkpoint_interval_calls_borg_with_checkpoint_interval_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--checkpoint-interval', '600') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'checkpoint_interval': 600,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_checkpoint_volume_calls_borg_with_checkpoint_volume_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--checkpoint-volume', '1024') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'checkpoint_volume': 1024,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_chunker_params_calls_borg_with_chunker_params_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--chunker-params', '1,2,3,4') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'chunker_params': '1,2,3,4',
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_compression_calls_borg_with_compression_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--compression', 'rle') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'compression': 'rle',
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


@pytest.mark.parametrize(
    'feature_available,option_flag',
    ((True, '--upload-ratelimit'), (False, '--remote-ratelimit')),
)
def test_create_archive_with_upload_rate_limit_calls_borg_with_upload_ratelimit_parameters(
    feature_available, option_flag
):
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(feature_available)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', option_flag, '100') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'upload_rate_limit': 100,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_working_directory_calls_borg_with_working_directory():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').with_args('/working/dir').and_return(
        '/working/dir'
    )
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory='/working/dir',
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'working_directory': '/working/dir',
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_one_file_system_calls_borg_with_one_file_system_parameter():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--one-file-system') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'one_file_system': True,
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


@pytest.mark.parametrize(
    'feature_available,option_flag',
    ((True, '--numeric-ids'), (False, '--numeric-owner')),
)
def test_create_archive_with_numeric_ids_calls_borg_with_numeric_ids_parameter(
    feature_available, option_flag
):
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(feature_available)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', option_flag) + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'numeric_ids': True,
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_read_special_calls_borg_with_read_special_parameter():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('collect_special_file_paths').and_return(())
    create_command = ('borg', 'create', '--read-special') + REPO_ARCHIVE_WITH_PATHS
    flexmock(module).should_receive('execute_command').with_args(
        create_command + ('--dry-run', '--list'),
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    flexmock(module).should_receive('execute_command').with_args(
        create_command,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'read_special': True,
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


@pytest.mark.parametrize(
    'option_name,option_value',
    (
        ('ctime', True),
        ('ctime', False),
        ('birthtime', True),
        ('birthtime', False),
    ),
)
def test_create_archive_with_basic_option_calls_borg_with_corresponding_parameter(
    option_name, option_value
):
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    option_flag = '--no' + option_name.replace('', '') if option_value is False else None
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + ((option_flag,) if option_flag else ()) + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            option_name: option_value,
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


@pytest.mark.parametrize(
    'option_value,feature_available,option_flag',
    (
        (True, True, '--atime'),
        (True, False, None),
        (False, True, None),
        (False, False, '--noatime'),
    ),
)
def test_create_archive_with_atime_option_calls_borg_with_corresponding_parameter(
    option_value, feature_available, option_flag
):
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(feature_available)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + ((option_flag,) if option_flag else ()) + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'atime': option_value,
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


@pytest.mark.parametrize(
    'option_value,feature_available,option_flag',
    (
        (True, True, None),
        (True, False, None),
        (False, True, '--noflags'),
        (False, False, '--nobsdflags'),
    ),
)
def test_create_archive_with_flags_option_calls_borg_with_corresponding_parameter(
    option_value, feature_available, option_flag
):
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(feature_available)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create') + ((option_flag,) if option_flag else ()) + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'flags': option_value,
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_files_cache_calls_borg_with_files_cache_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--files-cache', 'ctime,size') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'files_cache': 'ctime,size',
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_local_path_calls_borg_via_local_path():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg1', 'create') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg1',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        local_path='borg1',
    )


def test_create_archive_with_remote_path_calls_borg_with_remote_path_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--remote-path', 'borg1') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        remote_path='borg1',
    )


def test_create_archive_with_umask_calls_borg_with_umask_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--umask', '740') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'umask': 740,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_log_json_calls_borg_with_log_json_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--log-json') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=True, used_config_paths=[]),
    )


def test_create_archive_with_lock_wait_calls_borg_with_lock_wait_parameters():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--lock-wait', '5') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'lock_wait': 5,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_stats_calls_borg_with_stats_parameter_and_answer_output_log_level():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--stats') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=module.borgmatic.logger.ANSWER,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        stats=True,
    )


def test_create_archive_with_files_calls_borg_with_list_parameter_and_answer_output_log_level():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--list', '--filter', 'FOO') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=module.borgmatic.logger.ANSWER,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        list_files=True,
    )


def test_create_archive_with_progress_and_log_info_calls_borg_with_progress_parameter_and_no_list():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--info', '--progress') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=module.DO_NOT_CAPTURE,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    insert_logging_mock(logging.INFO)

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        progress=True,
    )


def test_create_archive_with_progress_calls_borg_with_progress_parameter():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--progress') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=module.DO_NOT_CAPTURE,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        progress=True,
    )


def test_create_archive_with_progress_and_stream_processes_calls_borg_with_progress_parameter():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    processes = flexmock()
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('collect_special_file_paths').and_return(())
    create_command = (
        'borg',
        'create',
        '--one-file-system',
        '--read-special',
        '--progress',
    ) + REPO_ARCHIVE_WITH_PATHS
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_command + ('--dry-run', '--list'),
        processes=processes,
        output_log_level=logging.INFO,
        output_file=module.DO_NOT_CAPTURE,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_command,
        processes=processes,
        output_log_level=logging.INFO,
        output_file=module.DO_NOT_CAPTURE,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        progress=True,
        stream_processes=processes,
    )


def test_create_archive_with_stream_processes_ignores_read_special_false_and_logs_warnings():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    processes = flexmock()
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(flexmock(name='/tmp/excludes'))
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module.logger).should_receive('warning').twice()
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('collect_special_file_paths').and_return(('/dev/null',))
    create_command = (
        'borg',
        'create',
        '--one-file-system',
        '--read-special',
    ) + REPO_ARCHIVE_WITH_PATHS
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_command + ('--dry-run', '--list'),
        processes=processes,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_command,
        processes=processes,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'read_special': False,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        stream_processes=processes,
    )


def test_create_archive_with_stream_processes_adds_special_files_to_excludes():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    processes = flexmock()
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(()).and_return(
        ('special',)
    )
    flexmock(module).should_receive('write_pattern_file').and_return(None).and_return(
        flexmock(name='/excludes')
    )
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(()).and_return(
        '--exclude-from', '/excludes'
    )
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('collect_special_file_paths').and_return(('special',))
    create_flags = (
        'borg',
        'create',
        '--one-file-system',
        '--read-special',
    )
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_flags + ('--dry-run', '--list') + REPO_ARCHIVE_WITH_PATHS,
        processes=processes,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_flags + ('--exclude-from', '/excludes') + REPO_ARCHIVE_WITH_PATHS,
        processes=processes,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        stream_processes=processes,
    )


def test_create_archive_with_stream_processes_and_read_special_does_not_add_special_files_to_excludes():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    processes = flexmock()
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(()).and_return(
        ('special',)
    )
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('collect_special_file_paths').and_return(('special',))
    create_command = (
        'borg',
        'create',
        '--one-file-system',
        '--read-special',
    ) + REPO_ARCHIVE_WITH_PATHS
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_command + ('--dry-run', '--list'),
        processes=processes,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_command,
        processes=processes,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'read_special': True,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        stream_processes=processes,
    )


def test_create_archive_with_json_calls_borg_with_json_parameter():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command_and_capture_output').with_args(
        ('borg', 'create', '--json') + REPO_ARCHIVE_WITH_PATHS,
        working_directory=None,
        extra_environment=None,
        borg_local_path='borg',
    ).and_return('[]')

    json_output = module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        json=True,
    )

    assert json_output == '[]'


def test_create_archive_with_stats_and_json_calls_borg_without_stats_parameter():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command_and_capture_output').with_args(
        ('borg', 'create', '--json') + REPO_ARCHIVE_WITH_PATHS,
        working_directory=None,
        extra_environment=None,
        borg_local_path='borg',
    ).and_return('[]')

    json_output = module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        json=True,
        stats=True,
    )

    assert json_output == '[]'


def test_create_archive_with_source_directories_glob_expands():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'food'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', f'repo::{DEFAULT_ARCHIVE_NAME}', 'foo', 'food'),
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    flexmock(module.glob).should_receive('glob').with_args('foo*').and_return(['foo', 'food'])

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo*'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_non_matching_source_directories_glob_passes_through():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo*',))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', f'repo::{DEFAULT_ARCHIVE_NAME}', 'foo*'),
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    flexmock(module.glob).should_receive('glob').with_args('foo*').and_return([])

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo*'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_glob_calls_borg_with_expanded_directories():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'food'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', f'repo::{DEFAULT_ARCHIVE_NAME}', 'foo', 'food'),
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo*'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_archive_name_format_calls_borg_with_archive_name():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::ARCHIVE_NAME',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', 'repo::ARCHIVE_NAME', 'foo', 'bar'),
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'archive_name_format': 'ARCHIVE_NAME',
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_archive_name_format_accepts_borg_placeholders():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    repository_archive_pattern = 'repo::Documents_{hostname}-{now}'  # noqa: FS003
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (repository_archive_pattern,)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', repository_archive_pattern, 'foo', 'bar'),
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'archive_name_format': 'Documents_{hostname}-{now}',  # noqa: FS003
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_repository_accepts_borg_placeholders():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    repository_archive_pattern = '{fqdn}::Documents_{hostname}-{now}'  # noqa: FS003
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (repository_archive_pattern,)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', repository_archive_pattern, 'foo', 'bar'),
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='{fqdn}',  # noqa: FS003
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['{fqdn}'],  # noqa: FS003
            'exclude_patterns': None,
            'archive_name_format': 'Documents_{hostname}-{now}',  # noqa: FS003
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_extra_borg_options_calls_borg_with_extra_options():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'create', '--extra', '--options') + REPO_ARCHIVE_WITH_PATHS,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
            'extra_borg_options': {'create': '--extra --options'},
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
    )


def test_create_archive_with_stream_processes_calls_borg_with_processes_and_read_special():
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    processes = flexmock()
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('deduplicate_directories').and_return(('foo', 'bar'))
    flexmock(module).should_receive('map_directories_to_devices').and_return({})
    flexmock(module).should_receive('expand_directories').and_return(())
    flexmock(module).should_receive('pattern_root_directories').and_return([])
    flexmock(module.os.path).should_receive('expanduser').and_raise(TypeError)
    flexmock(module).should_receive('expand_home_directories').and_return(())
    flexmock(module).should_receive('write_pattern_file').and_return(None)
    flexmock(module).should_receive('make_list_filter_flags').and_return('FOO')
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module).should_receive('ensure_files_readable')
    flexmock(module).should_receive('make_pattern_flags').and_return(())
    flexmock(module).should_receive('make_exclude_flags').and_return(())
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        (f'repo::{DEFAULT_ARCHIVE_NAME}',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('collect_special_file_paths').and_return(())
    create_command = (
        'borg',
        'create',
        '--one-file-system',
        '--read-special',
    ) + REPO_ARCHIVE_WITH_PATHS
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_command + ('--dry-run', 'list'),
        processes=processes,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )
    flexmock(module).should_receive('execute_command_with_processes').with_args(
        create_command,
        processes=processes,
        output_log_level=logging.INFO,
        output_file=None,
        borg_local_path='borg',
        working_directory=None,
        extra_environment=None,
    )

    module.create_archive(
        dry_run=False,
        repository_path='repo',
        config={
            'source_directories': ['foo', 'bar'],
            'repositories': ['repo'],
            'exclude_patterns': None,
        },
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False, used_config_paths=[]),
        stream_processes=processes,
    )


def test_create_archive_with_non_existent_directory_and_source_directories_must_exist_raises_error():
    '''
    If a source directory doesn't exist and source_directories_must_exist is True, raise an error.
    '''
    flexmock(module.borgmatic.logger).should_receive('add_custom_log_levels')
    flexmock(module.logging).ANSWER = module.borgmatic.logger.ANSWER
    flexmock(module).should_receive('collect_borgmatic_source_directories').and_return([])
    flexmock(module).should_receive('check_all_source_directories_exist').and_raise(ValueError)

    with pytest.raises(ValueError):
        module.create_archive(
            dry_run=False,
            repository_path='repo',
            config={
                'source_directories': ['foo', 'bar'],
                'repositories': ['repo'],
                'exclude_patterns': None,
                'source_directories_must_exist': True,
            },
            local_borg_version='1.2.3',
            global_arguments=flexmock(log_json=False, used_config_paths=[]),
        )


def test_check_all_source_directories_exist_with_glob_and_tilde_directories():
    flexmock(module).should_receive('expand_directory').with_args('foo*').and_return(
        ('foo', 'food')
    )
    flexmock(module).should_receive('expand_directory').with_args('~/bar').and_return(
        ('/root/bar',)
    )
    flexmock(module.os.path).should_receive('exists').and_return(False)
    flexmock(module.os.path).should_receive('exists').with_args('foo').and_return(True)
    flexmock(module.os.path).should_receive('exists').with_args('food').and_return(True)
    flexmock(module.os.path).should_receive('exists').with_args('/root/bar').and_return(True)

    module.check_all_source_directories_exist(['foo*', '~/bar'])


def test_check_all_source_directories_exist_with_non_existent_directory_raises():
    flexmock(module).should_receive('expand_directory').with_args('foo').and_return(('foo',))
    flexmock(module.os.path).should_receive('exists').and_return(False)

    with pytest.raises(ValueError):
        module.check_all_source_directories_exist(['foo'])
