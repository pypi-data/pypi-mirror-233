import io

import ruamel.yaml


def set_values(config, keys, value):
    '''
    Given a hierarchy of configuration dicts, a sequence of parsed key strings, and a string value,
    descend into the hierarchy based on the keys to set the value into the right place.
    '''
    if not keys:
        return

    first_key = keys[0]
    if len(keys) == 1:
        config[first_key] = value
        return

    if first_key not in config:
        config[first_key] = {}

    set_values(config[first_key], keys[1:], value)


def convert_value_type(value):
    '''
    Given a string value, determine its logical type (string, boolean, integer, etc.), and return it
    converted to that type.

    Raise ruamel.yaml.error.YAMLError if there's a parse issue with the YAML.
    '''
    return ruamel.yaml.YAML(typ='safe').load(io.StringIO(value))


LEGACY_SECTION_NAMES = {'location', 'storage', 'retention', 'consistency', 'output', 'hooks'}


def strip_section_names(parsed_override_key):
    '''
    Given a parsed override key as a tuple of option and suboption names, strip out any initial
    legacy section names, since configuration file normalization also strips them out.
    '''
    if parsed_override_key[0] in LEGACY_SECTION_NAMES:
        return parsed_override_key[1:]

    return parsed_override_key


def parse_overrides(raw_overrides):
    '''
    Given a sequence of configuration file override strings in the form of "option.suboption=value",
    parse and return a sequence of tuples (keys, values), where keys is a sequence of strings. For
    instance, given the following raw overrides:

        ['my_option.suboption=value1', 'other_option=value2']

    ... return this:

        (
            (('my_option', 'suboption'), 'value1'),
            (('other_option'), 'value2'),
        )

    Raise ValueError if an override can't be parsed.
    '''
    if not raw_overrides:
        return ()

    parsed_overrides = []

    for raw_override in raw_overrides:
        try:
            raw_keys, value = raw_override.split('=', 1)
            parsed_overrides.append(
                (
                    strip_section_names(tuple(raw_keys.split('.'))),
                    convert_value_type(value),
                )
            )
        except ValueError:
            raise ValueError(
                f"Invalid override '{raw_override}'. Make sure you use the form: OPTION=VALUE or OPTION.SUBOPTION=VALUE"
            )
        except ruamel.yaml.error.YAMLError as error:
            raise ValueError(f"Invalid override '{raw_override}': {error.problem}")

    return tuple(parsed_overrides)


def apply_overrides(config, raw_overrides):
    '''
    Given a configuration dict and a sequence of configuration file override strings in the form of
    "option.suboption=value", parse each override and set it the configuration dict.
    '''
    overrides = parse_overrides(raw_overrides)

    for keys, value in overrides:
        set_values(config, keys, value)
