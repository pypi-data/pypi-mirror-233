#!/usr/bin/env python3

'''
Morgan fingerprint feature calculator.
'''


from rdkit.Chem import AllChem


from chemfeat.features.calculator import FeatureCalculator


class ECFPFeatureCalculator(FeatureCalculator):
    '''
    ECFP feature calculator.

    Extended-Connectivity fingerprints (ECFP), a.k.a. Morgan fingerprints,
    calculated with [RDKit cheminformatics
    library](http://rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html?highlight=getmorganfingerprintasbitvect#rdkit.Chem.rdMolDescriptors.GetMorganFingerprintAsBitVect)

    > Rogers, David, and Mathew Hahn. “Extended-Connectivity Fingerprints.”
    > Journal of Chemical Information and Modeling 50, no. 5 (May 24, 2010):
    > 742–54. https://doi.org/10.1021/ci100050t.

    Each feature is a single bit of the feature vector.
    '''
    FEATURE_SET_NAME = 'ecfp'

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
        fingerprint = AllChem.GetMorganFingerprintAsBitVect(molecule, 2, nBits=self.size)
        return self.add_fingerprint_features(features, fingerprint)


ECFPFeatureCalculator.register()
