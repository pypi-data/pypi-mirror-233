#!/usr/bin/env python3

'''
PaDEL feature calculators.

Given the number of PaDEL descriptors and fingerprints, this module generates
the corresponding classes programmatically.
'''

import logging
import sys
import textwrap
from typing import Optional

from PaDEL_pywrapper import PaDEL
from PaDEL_pywrapper.descriptor import descriptors, _fingerprints

from chemfeat.features.calculator import FeatureCalculator, FeatureCalculatorError
from chemfeat.markdown import escape as escape_markdown


LOGGER = logging.getLogger(__name__)
THIS_MODULE = sys.modules[__name__]


class PadelError(FeatureCalculatorError):
    '''
    Errors raised by the PaDEL package.
    '''


def _get_class_name(desc):
    '''
    Get a class name for the given PaDEL descriptor or fingerprint.
    '''
    try:
        return f'padel_{desc.short_name}'
    except AttributeError:
        return f'padel_{desc.name}'


class _PaDELCommonFeatureCalculator(FeatureCalculator):  # pylint: disable=abstract-method
    '''
    Abstract base class for other PaDEL feature calculators.
    '''
    _IS_3D = False

    @property
    def is_3D(self):
        return self._IS_3D


class PaDELDescFeatureCalculator(_PaDELCommonFeatureCalculator):
    '''
    Base class for PaDEL feature calculator subclasses.
    '''
    _PADEL_DESC = NotImplemented

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.padel = PaDEL([self._PADEL_DESC])

    def is_numeric(self, _name):
        return True

    def add_features(self, features, molecule):
        try:
            values = self.padel.calculate([molecule], show_banner=False)
        except Exception as err:
            raise PadelError(f'{self.identifier}: {err}') from err
        for key, value in values.iloc[0].to_dict().items():
            features[self.add_prefix(key)] = value
        return features


class PaDELFPFeatureCalculator(_PaDELCommonFeatureCalculator):
    '''
    Base class for PaDEL fingerprint calculator subclasses.
    '''
    _PADEL_DESC = NotImplemented

    def __init__(
        self,
        *args,
        size: Optional[int] = None,
        search_depth: Optional[int] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._padel_kwargs = {}
        if size is not None:
            self._padel_kwargs['size'] = int(size)
        if search_depth is not None:
            self._padel_kwargs['searchDepth'] = int(search_depth)
        self.padel = PaDEL([self._PADEL_DESC], **self._padel_kwargs)

    @property
    def parameters(self):
        return self._padel_kwargs.copy()

    def is_numeric(self, _name):
        return False

    def add_features(self, features, molecule):
        try:
            fingerprint = self.padel.calculate([molecule], show_banner=False).iloc[0]
        except Exception as err:
            raise PadelError(f'{self.identifier}: {err}') from err
        return self.add_fingerprint_features(features, fingerprint)


def _add_docstring_and_class(cls, name, docstring, features):
    citation_blurb = '''
All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.
'''.strip()

    docstring = '\n\n'.join(
        '\n'.join(textwrap.wrap(block, width=80))
        for block in docstring.split('\n\n')
    )
    docstring += f'\n\n{features}\n\n{citation_blurb}'
    setattr(cls, '__doc__', docstring)

    setattr(THIS_MODULE, name, cls)
    cls.register()


def declare_classes():
    '''
    Declare the descriptor and fingerprint classes.
    '''
    for desc in descriptors:
        name = _get_class_name(desc)
        dcls = type(
            name,
            (PaDELDescFeatureCalculator, ),
            {
                '_PADEL_DESC': desc,
                '_IS_3D': desc.is_3D,
                'FEATURE_SET_NAME': name
            }
        )
        qualifier = '3D ' if desc.is_3D else ''
        features = '\n'.join(
            f'* {escape_markdown(name)}: {escape_markdown(desc)}'
            for name, desc in zip(desc.description.name, desc.description.description)
        )
        docstring = f'''{desc.name} {qualifier}PaDEL descriptor

The following features are calculated:'''
        _add_docstring_and_class(dcls, name, docstring, features)

    for pfp in _fingerprints:
        name = _get_class_name(pfp)
        fpcls = type(
            name,
            (PaDELFPFeatureCalculator, ),
            {
                '_PADEL_DESC': pfp,
                '_IS_3D': pfp.is_3D,
                'FEATURE_SET_NAME': name
            }
        )
        qualifier = '3D ' if pfp.is_3D else ''
        n_bits = pfp.nBits if pfp.nBits else 'variable'
        features = f'''* Number of bits: {n_bits}
* Bit prefix: {pfp.bit_prefix}
'''
        docstring = f'''{qualifier}PaDEL {pfp.short_name}fingerprint

{pfp.name} - {pfp.description.iloc[0]}
'''
        _add_docstring_and_class(fpcls, name, docstring, features)


declare_classes()
