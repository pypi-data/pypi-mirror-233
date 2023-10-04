#!/usr/bin/env python3

'''
Base clase for feature calculators.
'''

import inspect
import logging
from collections import OrderedDict

from docstring_parser import parse as parse_docstring


LOGGER = logging.getLogger(__name__)

# Dictionary mapping feature set names to their corresponding feature
# calculators. Each subclass will add itself.
FEATURE_CALCULATORS = {}


PREFIX_SEPARATOR = '__'


class FeatureCalculatorError(Exception):
    '''
    Exception base class for featrue calculator errors.
    '''


def split_prefix(name):
    '''
    Split a fully qualified feature name into a feature set name and an an unqualified feature name.
    '''
    return name.split(PREFIX_SEPARATOR, 1)


def _describe_func_args(func, header=None):
    '''
    Describe the arguments of a function.

    Args:
        func:
            The input function.

        header:
            An optional section header with preceding number signs to emit
            before the parameter list.

    Returns:
        A generator over markdown strings.
    '''
    docstring = parse_docstring(func.__doc__)
    param_descs = {param.arg_name: param.description for param in docstring.params}
    argspec = inspect.getfullargspec(func)
    n_args = len(argspec.args)

    required_args = n_args - len(argspec.defaults) \
        if argspec.defaults is not None \
        else n_args

    defaults = argspec.kwonlydefaults
    if defaults is None:
        defaults = {}
    defaults.update({
        arg: argspec.defaults[i - required_args]
        for i, arg in enumerate(argspec.args)
        if i >= required_args
    })

    all_args = [*argspec.args, *argspec.kwonlyargs]

    is_first = True
    for arg in all_args:
        if arg == 'self':
            continue
        annotations = argspec.annotations[arg]
        desc = f'* {arg}'
        specs = OrderedDict()
        if annotations:
            specs['type'] = annotations.__name__
        try:
            specs['default'] = defaults[arg]
        except KeyError:
            pass
        if specs:
            specs = '; '.join(f'{key}: {value}' for key, value in specs.items())
            desc += f' ({specs})'
        desc += f': {param_descs.get(arg, "Description unavailable.")}'

        if is_first and header:
            yield header
            yield ''
        yield desc
        is_first = False

    if not is_first:
        yield '\n\n'


class FeatureCalculator():
    '''
    Base class for feature calculators.
    '''
    FEATURE_SET_NAME = NotImplemented

    @classmethod
    def register(cls):
        '''
        Register this FeatureCalculator subclass among the available feature
        calculators.
        '''
        prev_cls = FEATURE_CALCULATORS.get(cls.FEATURE_SET_NAME)
        if prev_cls is None:
            LOGGER.debug(
                'Registering feature calculator %s: %s',
                cls.FEATURE_SET_NAME,
                cls
            )
        else:
            LOGGER.warning(
                'Reregistering feature calculator %s: %s -> %s',
                cls.FEATURE_SET_NAME,
                prev_cls,
                cls
            )
        FEATURE_CALCULATORS[cls.FEATURE_SET_NAME] = cls

    @classmethod
    def get_description(cls, level=1):
        '''
        A description of the feature set with relevant references and a
        description of the recognized parameters.

        Args:
            level:
                Markdown header level for the returned description.

        Returns:
            The description as a markdown string.
        '''
        level = max(level, 1)
        header_signs = '#' * level

        cls_docstring = parse_docstring(cls.__doc__)
        cls_desc = [
            cls_docstring.short_description,
            cls_docstring.long_description
        ]
        cls_desc = [desc for desc in cls_desc if desc]
        if cls_desc:
            cls_desc = '\n\n'.join(cls_desc)
        if not cls_desc:
            LOGGER.warning('No class description for %s', cls.__name__)
            cls_desc = 'No description available.'

        yield f'''{header_signs} {cls.FEATURE_SET_NAME}

{cls_desc}

'''
        yield from _describe_func_args(cls.__init__, header=f'{header_signs}# Parameters')

    @classmethod
    def get_short_description(cls):
        '''
        The short description from the class' docstring.

        Returns:
            The short description as a string.
        '''
        return parse_docstring(cls.__doc__).short_description

    @property
    def identifier(self):
        '''
        Get a unique ID for this feature set with the given parameters.
        '''
        params = self.parameters
        if not params:
            return self.FEATURE_SET_NAME
        param_str = '-'.join(
            f'{name}:{value}'
            for name, value in sorted(params.items())
            if value is not None
        )
        return f'{self.FEATURE_SET_NAME}-{param_str}'

    @property
    def parameters(self):
        '''
        Return a dictionary representing the parametes required to re-initialize
        the feature calculator.
        '''
        return {}

    def add_prefix(self, name):
        '''
        Add the feature set prefix to the feature name.

        Args:
            name:
                The name of a feature in the feature set handled by a subclass
                of this class.

        Returns:
            The feature name with the feature set previx.
        '''
        return f'{self.identifier}{PREFIX_SEPARATOR}{name}'

    def remove_prefix(self, name):
        '''
        Remove the feature set prefix from the feature name.

        Args:
            name:
                The name, with or without the feature set prefix.

        Returns:
            The feature name without the feature set prefix.
        '''
        return split_prefix(name)[1]

    def is_numeric(self, name):
        '''
        Return True if the given feature name is numeric and not categoric.
        '''

    @property
    def is_3D(self):
        '''
        True if the features depend on 3D molecular information.
        '''
        return False

    def add_features(self, features, molecule):
        '''
        Args:
            features:
                A dict to which to add the calculated features. The keys should
                be prefixed feature names as returned by add_prefix() and the
                values should be there value.

            molecule:
                The RDKit molecule object for which to calculate features.

        Returns:
            The updated features dict.
        '''
        raise NotImplementedError(f'{self.__class__.__name__} does not implemented add_features()')

    def add_fingerprint_features(self, features, fingerprint, name=''):
        '''
        Convenience method for adding fingerprint vectors as separate features.

        Args:
            features:
                Same as add_features().

            fingerprint:
                An iterable of values to add as separate features. These will be
                named sequentially.

            name:
                An optional name to insert between the prefix and the index.

        Returns:
            The updated features dict.
        '''
        size = len(fingerprint)
        n_digits = len(str(size - 1))
        names = list(self.add_prefix(f'{name}{i:0{n_digits:d}d}') for i in range(size))
        features.update(zip(names, fingerprint))
        return features
