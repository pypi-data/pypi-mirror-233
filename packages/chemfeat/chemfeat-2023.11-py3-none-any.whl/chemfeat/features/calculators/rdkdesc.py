#!/usr/bin/env python3

'''
RDK descriptor feature calculator.
'''


from rdkit.Chem import Descriptors


from chemfeat.features.calculator import FeatureCalculator


class RDKDescFeatureCalculator(FeatureCalculator):
    '''
    RDK descriptor feature calculator.

    Various chemical descriptors calculated with the RDKit cheminformatics
    library: https://www.rdkit.org/docs/source/rdkit.Chem.Descriptors.html

    The following features are calculated:

    * FpDensityMorgan1
    * FpDensityMorgan2
    * FpDensityMorgan3
    * MaxAbsPartialCharge
    * MaxPartialCharge
    * MinAbsPartialCharge
    * MinPartialCharge
    * NumRadicalElectrons
    * NumValenceElectron
    '''
    FEATURE_SET_NAME = 'rdkdesc'

    def is_numeric(self, _name):
        return True

    def add_features(self, features, molecule):
        features.update(
            (self.add_prefix(name), getattr(Descriptors, name)(molecule))
            for name in (
                'FpDensityMorgan1',
                'FpDensityMorgan2',
                'FpDensityMorgan3',
                'MaxAbsPartialCharge',
                'MaxPartialCharge',
                'MinAbsPartialCharge',
                'MinPartialCharge',
                'NumRadicalElectrons',
                'NumValenceElectrons'
            )
        )
        return features


RDKDescFeatureCalculator.register()
