#!/usr/bin/env python3

'''
RDK fingerprint feature calculator.
'''


from rdkit import Chem


from chemfeat.features.calculator import FeatureCalculator


class RDKFPFeatureCalculator(FeatureCalculator):
    '''
    RDK fingerprint feature calculator.

    RDK topological fingerprint calculated with the [RDKit cheminformatics
    library](https://www.rdkit.org/docs/source/rdkit.Chem.rdmolops.html#rdkit.Chem.rdmolops.RDKFingerprint

    Each feature is a single bit of the feature vector.
    '''
    FEATURE_SET_NAME = 'rdkfp'

    def __init__(self, size: int = 2048):
        '''
        Args:
            size:
                The fingerprint size. It should be 1024, 2048 or 4096.
        '''
        size = int(size)
        valid_sizes = (1024, 2048, 4096)
        if size not in valid_sizes:
            raise ValueError(
                f'Invalid size for fingerprint: {size}. '
                f'Valid sizes: {valid_sizes}'
            )
        self.size = 2048

    @property
    def parameters(self):
        return {'size': self.size}

    def is_numeric(self, _name):
        return False

    def add_features(self, features, molecule):
        fingerprint = Chem.RDKFingerprint(molecule, fpSize=self.size)
        return self.add_fingerprint_features(features, fingerprint)


RDKFPFeatureCalculator.register()
