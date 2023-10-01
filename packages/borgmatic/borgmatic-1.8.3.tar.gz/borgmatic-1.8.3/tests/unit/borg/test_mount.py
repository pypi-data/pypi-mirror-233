import logging

from flexmock import flexmock

from borgmatic.borg import mount as module

from ..test_verbosity import insert_logging_mock


def insert_execute_command_mock(command):
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        command,
        borg_local_path='borg',
        extra_environment=None,
    ).once()


def test_mount_archive_calls_borg_with_required_flags():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('repo',))
    insert_execute_command_mock(('borg', 'mount', 'repo', '/mnt'))

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=False)
    module.mount_archive(
        repository_path='repo',
        archive=None,
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_with_borg_features_calls_borg_with_repository_and_match_archives_flags():
    flexmock(module.feature).should_receive('available').and_return(True)
    flexmock(module.flags).should_receive('make_repository_flags').and_return(
        (
            '--repo',
            'repo',
        )
    )
    insert_execute_command_mock(
        ('borg', 'mount', '--repo', 'repo', '--match-archives', 'archive', '/mnt')
    )

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=False)
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_without_archive_calls_borg_with_repository_flags_only():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    insert_execute_command_mock(('borg', 'mount', 'repo::archive', '/mnt'))

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=False)
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_calls_borg_with_path_flags():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    insert_execute_command_mock(('borg', 'mount', 'repo::archive', '/mnt', 'path1', 'path2'))

    mount_arguments = flexmock(
        mount_point='/mnt', options=None, paths=['path1', 'path2'], foreground=False
    )
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_calls_borg_with_remote_path_flags():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    insert_execute_command_mock(
        ('borg', 'mount', '--remote-path', 'borg1', 'repo::archive', '/mnt')
    )

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=False)
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
        remote_path='borg1',
    )


def test_mount_archive_calls_borg_with_umask_flags():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    insert_execute_command_mock(('borg', 'mount', '--umask', '0770', 'repo::archive', '/mnt'))

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=False)
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={'umask': '0770'},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_calls_borg_with_log_json_flags():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    insert_execute_command_mock(('borg', 'mount', '--log-json', 'repo::archive', '/mnt'))

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=False)
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=True),
    )


def test_mount_archive_calls_borg_with_lock_wait_flags():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    insert_execute_command_mock(('borg', 'mount', '--lock-wait', '5', 'repo::archive', '/mnt'))

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=False)
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={'lock_wait': '5'},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_with_log_info_calls_borg_with_info_parameter():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    insert_execute_command_mock(('borg', 'mount', '--info', 'repo::archive', '/mnt'))
    insert_logging_mock(logging.INFO)

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=False)
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_with_log_debug_calls_borg_with_debug_flags():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    insert_execute_command_mock(('borg', 'mount', '--debug', '--show-rc', 'repo::archive', '/mnt'))
    insert_logging_mock(logging.DEBUG)

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=False)
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_calls_borg_with_foreground_parameter():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        ('borg', 'mount', '--foreground', 'repo::archive', '/mnt'),
        output_file=module.DO_NOT_CAPTURE,
        borg_local_path='borg',
        extra_environment=None,
    ).once()

    mount_arguments = flexmock(mount_point='/mnt', options=None, paths=None, foreground=True)
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_calls_borg_with_options_flags():
    flexmock(module.feature).should_receive('available').and_return(False)
    flexmock(module.flags).should_receive('make_repository_archive_flags').and_return(
        ('repo::archive',)
    )
    insert_execute_command_mock(('borg', 'mount', '-o', 'super_mount', 'repo::archive', '/mnt'))

    mount_arguments = flexmock(
        mount_point='/mnt', options='super_mount', paths=None, foreground=False
    )
    module.mount_archive(
        repository_path='repo',
        archive='archive',
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )


def test_mount_archive_with_date_based_matching_calls_borg_with_date_based_flags():
    flexmock(module.flags).should_receive('make_flags').and_return(())
    flexmock(module.flags).should_receive('make_match_archives_flags').and_return(())
    flexmock(module.flags).should_receive('make_flags_from_arguments').and_return(
        (
            '--newer',
            '1d',
            '--newest',
            '1y',
            '--older',
            '1m',
            '--oldest',
            '1w',
            '--match-archives',
            None,
        )
    )
    flexmock(module.flags).should_receive('make_repository_flags').and_return(('--repo', 'repo'))
    flexmock(module.environment).should_receive('make_environment')
    flexmock(module).should_receive('execute_command').with_args(
        (
            'borg',
            'mount',
            '--newer',
            '1d',
            '--newest',
            '1y',
            '--older',
            '1m',
            '--oldest',
            '1w',
            '--match-archives',
            None,
            '--repo',
            'repo',
            '/mnt',
        ),
        borg_local_path='borg',
        extra_environment=None,
    )

    mount_arguments = flexmock(
        mount_point='/mnt',
        options=None,
        paths=None,
        foreground=False,
        newer='1d',
        newest='1y',
        older='1m',
        oldest='1w',
    )
    module.mount_archive(
        repository_path='repo',
        archive=None,
        mount_arguments=mount_arguments,
        config={},
        local_borg_version='1.2.3',
        global_arguments=flexmock(log_json=False),
    )
