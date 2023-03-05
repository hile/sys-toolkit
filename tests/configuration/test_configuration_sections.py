"""
Unit tests for configuration sections
"""
from pathlib import Path
from typing import Any, Dict, Optional

import pytest

from sys_toolkit.configuration.base import ConfigurationList, ConfigurationSection
from sys_toolkit.exceptions import ConfigurationError

CALLABLE_SECTION_NAME = 'callme'
CALLABLE_SECTION_VALUE = 'test callable value'

TEST_DEFAULT_DATA = {
    'test_key': 'test value',
    'nested_level_1': {
        'test_nested_key': 'test nested value'
    }
}

TEST_NESTED_LIST_DATA = {
    'nested_item_1': {
        'list_field': [
            {
                'list_nested_item': {
                    'field': 1234,
                }
            },
            'text list item'
        ]
    }
}

TEST_LIST_DATA_REPLACE = [
    1234,
    2234,
    3334,
    4444,
]

TEST_EMPTY_DATA = {
    'test_key_empty': '',
    'nested_level_1': {}
}

TEST_INVALID_VALUES = (
    (1, 'test numeric value'),
    ('spaced out', 'test invalid attr string'),
    ('dashed-string', 'test invalid dashed string'),
)


class FormattedConfigurationList(ConfigurationList):
    """
    Section loader with values formatted to integers
    """
    def __format_item__(self, value: str) -> int:
        """
        Format string items added to the object as integers
        """
        return int(value)


class EnvDefaultsConfigurationSection(ConfigurationSection):
    """
    Configuration with default settings and environment
    variables
    """
    __default_settings__ = {
        'test_key': 'test value'
    }
    __environment_variables__ = {
        'TEST_RESULT_KEY': 'test_key'
    }


class DefaultsConfigurationSection(ConfigurationSection):
    """
    Configuration with default variables
    """
    __default_settings__ = {
        'test_key': 'test value',
        'nested_default': {
            'test_nested_key': 'nested value'
        }
    }


class EnvConfigurationSection(ConfigurationSection):
    """
    Configuration with environment variables
    """
    __environment_variables__ = {
        'MY_TEST_KEY': 'test_key'
    }
    __environment_variable_prefix__ = 'PREFIXED'


class InvalidDefaultConfigurationSection(ConfigurationSection):
    """
    Configuration with invalid default settings
    """
    __default_settings__ = {
        'test key': 'test value'
    }


class InvalidEnvConfigurationSection(ConfigurationSection):
    """
    Configuration with invalid environment settings
    """
    __environment_variables__ = {
        'TEST_RESULT_KEY': 'test key'
    }


class NestedConfigurationSection(ConfigurationSection):
    """
    Nested configuration section
    """
    __name__ = 'nested'


class NestedDefaultConfigurationSection(ConfigurationSection):
    """
    Nested configuration section default for unnamed sections
    """


class NestedListConfigurationSection(ConfigurationSection):
    """
    Nested configuration section default for list sections
    """
    __name__ = 'lists'


class CallableSetConfigurationSection(ConfigurationSection):
    """
    Configuration section class with a callable set() method
    """
    __name__ = CALLABLE_SECTION_NAME

    def __init__(self,
                 data: Dict = dict,
                 parent: ConfigurationSection = None,
                 debug_enabled: bool = False,
                 silent: bool = False):
        super().__init__(data, parent, debug_enabled, silent)
        self.set_call_count = 0
        self.set_call_args = []

    def set(self, attr: str, value: Any) -> None:
        """
        Store set() call arguments to the section
        """
        print(f'set {attr} value {value}')
        self.set_call_count += 1
        self.set_call_args.append((attr, value))


class CallableBaseConfiguration(ConfigurationSection):
    """
    Configuratio section with a child section that has a callable set() method
    """
    __section_loaders__ = (
        CallableSetConfigurationSection,
    )


class NestedRootConfigurationSection(ConfigurationSection):
    """
    NestedRoot configuration section for nested configurations
    """
    __dict_loader_class__ = NestedDefaultConfigurationSection
    __list_loader_class__ = NestedListConfigurationSection
    __section_loaders__ = (
        NestedConfigurationSection,
        NestedListConfigurationSection,
    )


class InvalidRootConfigurationSection(ConfigurationSection):
    """
    NestedRoot configuration section with base ConfigurationSection

    Causes error due to no section name
    """
    __section_loaders__ = (
        ConfigurationSection,
    )


class RequiredSettingsConfigurationSection(ConfigurationSection):
    """
    Configuration section with required settings
    """
    __required_settings__ = (
        'test_key',
    )


class FormattedConfigurationSection(ConfigurationSection):
    """
    Configuration with formatter callback
    """
    @staticmethod
    def format_test_key(value: str) -> str:
        """
        Format expected test key value
        """
        return value.upper()


class ValidatedConfigurationSection(ConfigurationSection):
    """
    Configuration with validator callback
    """
    @staticmethod
    def validate_test_key(value: str) -> str:
        """
        Validate expected test key value
        """
        return value


class InvalidatedConfigurationSection(ConfigurationSection):
    """
    Configuration with validator callback raising error
    """
    @staticmethod
    def validate_test_key(value: str) -> None:
        """
        Validate expected test key value
        """
        raise ValueError('Invalid value')


def validate_configuration_section(
        section: ConfigurationSection,
        data: Dict,
        parent: Optional[ConfigurationSection] = None) -> None:
    """
    Validate configuration section details
    """
    assert section.__parent__ == parent

    for key, value in data.items():
        assert hasattr(section, key)
        if isinstance(value, dict):
            validate_configuration_section(
                getattr(section, key),
                value,
                section
            )
        else:
            assert getattr(section, key) == value


def test_configuration_list_formatting() -> None:
    """
    Test loading a configuration list that formats values to integers
    """
    obj = FormattedConfigurationList(data=['1', '2'])
    obj.insert(1, '2')
    assert len(obj) == 3
    for value in obj:
        assert isinstance(value, int)


def test_configuration_section_default_empty() -> None:
    """
    Test loading empty configuration section without data
    """
    section = ConfigurationSection()
    assert isinstance(section.__section_loaders__, tuple)
    assert isinstance(section.__default_settings__, dict)
    assert isinstance(section.__required_settings__, (tuple, list))


def test_configuration_section_invalid_parent() -> None:
    """
    Test initializing configuration section with invalid parent
    """
    with pytest.raises(TypeError):
        ConfigurationSection(parent={})


def test_configuration_section_attribute_name() -> None:
    """
    Test validation of attribute names for configuration secrion
    """
    configuration = ConfigurationSection()

    for attr in ('test', 'test123'):
        configuration.__validate_attribute__(attr)

    with pytest.raises(ConfigurationError):
        configuration.__validate_attribute__('hähää')


def test_configuration_section_empty_data() -> None:
    """
    Test loading configuration section with empty values in data
    """
    configuration = ConfigurationSection(data=TEST_EMPTY_DATA)

    assert configuration.__config_root__ == configuration

    # pylint: disable=no-member
    assert configuration.test_key_empty is None

    with pytest.raises(ConfigurationError):
        configuration.__get_section_loader__('')

    assert configuration.__key_from_attribute__('test') == 'test'
    configuration.__key_attribute_map__ = {
        'other': 'match'
    }
    assert configuration.__key_from_attribute__('match') == 'other'
    assert configuration.__key_from_attribute__('other') == 'other'


def test_configuration_section_list_data() -> None:
    """
    Test loading configuration section with list of mixed content
    """
    configuration = ConfigurationSection(data=TEST_NESTED_LIST_DATA)
    # pylint: disable=no-member
    nested_item = configuration.nested_item_1
    assert isinstance(nested_item, ConfigurationSection)
    assert nested_item.__config_root__ == configuration

    list_value = nested_item.list_field
    assert isinstance(list_value.__repr__(), str)
    assert isinstance(list_value, ConfigurationList)
    assert len(list_value) == 2
    assert list_value.__config_root__ == configuration

    assert isinstance(list_value[0], ConfigurationSection)
    assert isinstance(list_value[1], str)

    for item in list_value:
        assert item is not None

    list_value.insert(1, CALLABLE_SECTION_VALUE)
    assert len(list_value) == 3

    list_value.set(None, TEST_LIST_DATA_REPLACE)
    assert len(list_value) == 4

    list_value[1] = None
    assert len(list_value) == 4

    list_value.set(None, None)
    assert len(list_value) == 0


def test_configuration_section_default_with_data() -> None:
    """
    Test loading default configuration section with test data
    """
    section = ConfigurationSection(data=TEST_DEFAULT_DATA)
    validate_configuration_section(section, TEST_DEFAULT_DATA)


def test_configuration_section_empty_set_invalid_values() -> None:
    """
    Test loading default configuration section with test data
    """
    section = ConfigurationSection()
    for item in TEST_INVALID_VALUES:
        with pytest.raises(ConfigurationError):
            section.set(item[0], item[1])

    for invalid_value in (None, [1, 2, 3]):
        with pytest.raises(ConfigurationError):
            section.__load_dictionary__(invalid_value)

        with pytest.raises(ConfigurationError):
            section.__load_section__('test', invalid_value)


def test_configuration_section_load_section_explicit() -> None:
    """
    Load new section explicitly
    """
    configuration = ConfigurationSection()
    configuration.__load_section__(
        'test',
        {'test_key': 'test value'}
    )
    # pylint: disable=no-member
    assert configuration.test.test_key == 'test value'


def test_configuration_section_load_section_nomatch_path() -> None:
    """
    Load new section with complex path
    """
    configuration = ConfigurationSection()

    configuration.__load_section__(
        'test',
        '123',
        path='other.bar.test_key'
    )
    # pylint: disable=no-member
    assert configuration.test.other.bar.test_key == '123'

    # pylint: disable=no-member
    configuration.__load_section__(
        'test',
        {'test_key': 'test value'},
        path='other.sub.test_key'
    )
    # pylint: disable=no-member
    assert configuration.test.other.sub.test_key == 'test value'


def test_configuration_section_defaults() -> None:
    """
    Test configuration section with default settings
    """
    configuration = DefaultsConfigurationSection()
    assert len(configuration.__valid_settings__) == 1


def test_configuration_section_env(monkeypatch) -> None:
    """
    Test configuration section with environment settings
    """
    configuration = EnvConfigurationSection()
    assert len(configuration.__valid_settings__) == 1
    # pylint: disable=no-member
    assert configuration.test_key is None

    value = 'mock me env'
    with monkeypatch.context() as context:
        context.setenv('PREFIXED_TEST_KEY', value)
        configuration = EnvConfigurationSection()
        # pylint: disable=no-member
        assert configuration.test_key == value

    with monkeypatch.context() as context:
        context.setenv('MY_TEST_KEY', value)
        configuration = EnvConfigurationSection()
        # pylint: disable=no-member
        assert configuration.test_key == value


def test_configuration_section_env_defaults() -> None:
    """
    Test configuration section with default and environment settings
    """
    configuration = EnvDefaultsConfigurationSection()
    assert len(configuration.__valid_settings__) == 1
    # pylint: disable=no-member
    assert configuration.test_key == 'test value'


def test_configuration_section_invalid_defaults() -> None:
    """
    Test configuration section with invalid default settings
    """
    with pytest.raises(ConfigurationError):
        InvalidDefaultConfigurationSection()


def test_configuration_section_invalid_env() -> None:
    """
    Test configuration section with invalid environment settings
    """
    with pytest.raises(ConfigurationError):
        InvalidEnvConfigurationSection()


def test_configuration_section_nested_loader_unknown() -> None:
    """
    Test configuration sections with nested classes
    """
    configuration = ConfigurationSection()
    loader = configuration.__get_section_loader__('test')
    assert loader == ConfigurationSection

    configuration = NestedRootConfigurationSection()
    loader = configuration.__get_section_loader__(NestedConfigurationSection.__name__)
    assert loader == NestedConfigurationSection

    dict_output = configuration.as_dict()
    assert isinstance(dict_output, dict)


def test_configuration_section_nested_classes() -> None:
    """
    Test configuration sections with nested classes
    """
    configuration = NestedRootConfigurationSection()
    subsection = getattr(configuration, 'nested', None)
    assert subsection is not None
    assert isinstance(subsection, NestedConfigurationSection)
    assert subsection.__name__ == 'nested'

    assert configuration.__list_loader__ == NestedListConfigurationSection
    list_section = getattr(configuration, 'lists', None)
    assert list_section is not None
    assert isinstance(list_section, NestedListConfigurationSection)
    assert list_section.__name__ == 'lists'

    loader = configuration.__get_or_create_subsection__('unknown')
    assert loader.__name__ == 'unknown'

    configuration.__load_section__('test', {'test_key': 'test value'})
    # pylint: disable=no-member
    section = configuration.test
    assert isinstance(section, NestedDefaultConfigurationSection)
    assert section.test_key == 'test value'


def test_configuration_register_subsection_fail() -> None:
    """
    Test failure registering subsection without name
    """
    with pytest.raises(ConfigurationError):
        InvalidRootConfigurationSection()


def test_configuration_section_required_settings() -> None:
    """
    Test loading configuration section with required settings
    """
    section = RequiredSettingsConfigurationSection(data=TEST_DEFAULT_DATA)
    validate_configuration_section(section, TEST_DEFAULT_DATA)

    invalid_data = TEST_DEFAULT_DATA.copy()
    invalid_data['test_key'] = None
    with pytest.raises(ConfigurationError):
        RequiredSettingsConfigurationSection(data=invalid_data)

    with pytest.raises(ConfigurationError):
        RequiredSettingsConfigurationSection()


def test_configuration_section_paths() -> None:
    """
    Test loading configuration section with subsection paths
    """
    configuration = ConfigurationSection()
    section, field = configuration.__init_subsection_path__('test', 'test_field')
    assert section.__config_root__ == configuration
    assert section.__name__ == 'test'
    assert field == 'test_field'

    section, field = configuration.__init_subsection_path__('test', 'inner.value')
    assert section.__config_root__ == configuration
    assert isinstance(section, ConfigurationSection)
    assert section.__name__ == 'inner'
    assert section.__parent__.__name__ == 'test'
    assert field == 'value'

    configuration.__load_section__('sub', {'test': 'value'}, path='outer')
    # pylint: disable=no-member
    assert configuration.sub.outer.test == 'value'

    configuration.__load_section__('sub', 'value', path='inner.test')
    # pylint: disable=no-member
    assert configuration.sub.inner.test == 'value'


def test_configuration_section_load_dictionary() -> None:
    """
    Test loading dictionaries with __load_dictionary__ method using some more funky formats
    """
    configuration = ConfigurationSection()
    data = {
        'foo.bar': 'test',
        'bar.baz': {
            'zyxxy': 'item'
        }
    }
    configuration.__load_dictionary__(data)
    # pylint: disable=no-member
    assert configuration.foo.bar == 'test'
    # pylint: disable=no-member
    assert configuration.bar.baz.zyxxy == 'item'

    dict_output = configuration.as_dict()
    assert isinstance(dict_output, dict)


def test_configuration_section_set() -> None:
    """
    Test set() method of configuration section
    """
    configuration = ConfigurationSection()
    configuration.set('test', {'key': 'value'})
    # pylint: disable=no-member
    assert configuration.test.key == 'value'
    configuration.set('foo.bar', 'baz')
    # pylint: disable=no-member
    assert configuration.foo.bar == 'baz'


def test_configuration_section_set_formatters() -> None:
    """
    Test configuration section with number attribute formatters
    """
    configuration = ConfigurationSection()
    configuration.__integer_settings__ = ('integrity',)
    configuration.__float_settings__ = ('floating',)
    configuration.__path_settings__ = ('root',)

    configuration.set('test', {'a': 'a value'})
    # pylint: disable=no-member
    assert isinstance(configuration.test, ConfigurationSection)
    # pylint: disable=no-member
    assert configuration.test.a == 'a value'

    configuration.set('integrity', '123')
    # pylint: disable=no-member
    assert configuration.integrity == 123
    configuration.set('floating', '123.25')
    # pylint: disable=no-member
    assert configuration.floating == 123.25

    configuration.set('root', '/tmp')
    # pylint: disable=no-member
    assert isinstance(configuration.root, Path)


def test_configuration_section_field_formatter_pass() -> None:
    """
    Test configuration section with custom formatter passing
    """
    configuration = FormattedConfigurationSection(data=TEST_DEFAULT_DATA)
    # pylint: disable=no-member
    assert configuration.test_key == 'TEST VALUE'

    with pytest.raises(ConfigurationError):
        FormattedConfigurationSection(data={'test_key': 123})


def test_configuration_section_field_validation_pass() -> None:
    """
    Test configuration section with custom validation passing
    """
    section = ValidatedConfigurationSection(data=TEST_DEFAULT_DATA)
    validate_configuration_section(section, TEST_DEFAULT_DATA)


def test_configuration_section_field_validation_fail() -> None:
    """
    Test configuration section with custom validation fails
    """
    with pytest.raises(ConfigurationError):
        InvalidatedConfigurationSection(data=TEST_DEFAULT_DATA)


def test_configuration_section_callable_set_method() -> None:
    """
    Test calling a callable set method in child section loader class
    """
    section = CallableBaseConfiguration()
    assert hasattr(section, CALLABLE_SECTION_NAME)
    called = getattr(section, CALLABLE_SECTION_NAME)
    assert called.set_call_count == 0

    section.set(CALLABLE_SECTION_NAME, CALLABLE_SECTION_VALUE)
    assert called.set_call_count == 1
