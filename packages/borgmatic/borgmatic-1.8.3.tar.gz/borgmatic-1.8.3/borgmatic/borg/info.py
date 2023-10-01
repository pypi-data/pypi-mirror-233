import logging

import borgmatic.logger
from borgmatic.borg import environment, feature, flags
from borgmatic.execute import execute_command, execute_command_and_capture_output

logger = logging.getLogger(__name__)


def display_archives_info(
    repository_path,
    config,
    local_borg_version,
    info_arguments,
    global_arguments,
    local_path='borg',
    remote_path=None,
):
    '''
    Given a local or remote repository path, a configuration dict, the local Borg version, global
    arguments as an argparse.Namespace, and the arguments to the info action, display summary
    information for Borg archives in the repository or return JSON summary information.
    '''
    borgmatic.logger.add_custom_log_levels()
    lock_wait = config.get('lock_wait', None)

    full_command = (
        (local_path, 'info')
        + (
            ('--info',)
            if logger.getEffectiveLevel() == logging.INFO and not info_arguments.json
            else ()
        )
        + (
            ('--debug', '--show-rc')
            if logger.isEnabledFor(logging.DEBUG) and not info_arguments.json
            else ()
        )
        + flags.make_flags('remote-path', remote_path)
        + flags.make_flags('log-json', global_arguments.log_json)
        + flags.make_flags('lock-wait', lock_wait)
        + (
            (
                flags.make_flags('match-archives', f'sh:{info_arguments.prefix}*')
                if feature.available(feature.Feature.MATCH_ARCHIVES, local_borg_version)
                else flags.make_flags('glob-archives', f'{info_arguments.prefix}*')
            )
            if info_arguments.prefix
            else (
                flags.make_match_archives_flags(
                    info_arguments.match_archives
                    or info_arguments.archive
                    or config.get('match_archives'),
                    config.get('archive_name_format'),
                    local_borg_version,
                )
            )
        )
        + flags.make_flags_from_arguments(
            info_arguments, excludes=('repository', 'archive', 'prefix', 'match_archives')
        )
        + flags.make_repository_flags(repository_path, local_borg_version)
    )

    if info_arguments.json:
        return execute_command_and_capture_output(
            full_command,
            extra_environment=environment.make_environment(config),
            borg_local_path=local_path,
        )
    else:
        execute_command(
            full_command,
            output_log_level=logging.ANSWER,
            borg_local_path=local_path,
            extra_environment=environment.make_environment(config),
        )
