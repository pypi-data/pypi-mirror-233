#!/usr/bin/env python3

'''
QED feature calculator.
'''


from rdkit.Chem import QED


from chemfeat.features.calculator import FeatureCalculator


class QEDFeatureCalculator(FeatureCalculator):
    '''
    QED feature calculator.

    Quantitative estimation of drug-likeness features calculated with the [RDKit
    cheminformatics
    library](https://www.rdkit.org/docs/source/rdkit.Chem.QED.html)

    > Bickerton, G. Richard, Gaia V. Paolini, Jérémy Besnard, Sorel Muresan, and
    > Andrew L. Hopkins. “Quantifying the Chemical Beauty of Drugs.” Nature
    > Chemistry 4, no. 2 (February 2012): 90–98.
    > https://doi.org/10.1038/nchem.1243.

    The following features are calculated:

    * ALERTS: The number of structural alerts.
    * ALOGP: The octanol-water partition coefficient.
    * AROM: The number of aromatic rings.
    * HBA: The number of hydrogen bond acceptors.
    * HBD: The number of hydrogen bond donors.
    * MW: The molecular weight.
    * PSA: Polar surface area.
    * ROTB: The number of rotatable bonds.
    '''

    FEATURE_SET_NAME = 'qed'

    def is_numeric(self, _name):
        return True

    def add_features(self, features, molecule):
        properties = QED.properties(molecule)
        features.update(
            (self.add_prefix(name), value)
            for name, value in properties._asdict().items()
        )
        return features


QEDFeatureCalculator.register()
