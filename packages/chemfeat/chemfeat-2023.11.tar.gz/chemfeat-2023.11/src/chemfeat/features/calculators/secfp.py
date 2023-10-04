#!/usr/bin/env python3

'''
SEC fingerprint feature calculator.
'''


from rdkit.Chem import rdMHFPFingerprint


from chemfeat.features.calculator import FeatureCalculator


class SECFPFeatureCalculator(FeatureCalculator):
    '''
    SECFP feature calculator.


    SMILES Extended Connectivity Fingerprint f

    MinHash Fingerprints (MHFP) / SMILES Extended Connectivity Fingerprints
    (SECFP) calculated with [RDKit cheminformatics
    library](https://rdkit.org/docs/source/rdkit.Chem.rdMHFPFingerprint.html).

    > Probst, Daniel, and Jean-Louis Reymond. “A Probabilistic Molecular
    > Fingerprint for Big Data Settings.” Journal of Cheminformatics 10, no. 1
    > (December 18, 2018): 66. https://doi.org/10.1186/s13321-018-0321-8.

    Each feature is a single bit of the feature vector.
    '''
    FEATURE_SET_NAME = 'secfp'

    def __init__(self, size: int = 2048):
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
        fingerprint = rdMHFPFingerprint.MHFPEncoder().EncodeSECFPMol(molecule, length=self.size)
        return self.add_fingerprint_features(features, fingerprint)


SECFPFeatureCalculator.register()
