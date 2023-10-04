# ecfp

ECFP feature calculator.

Extended-Connectivity fingerprints (ECFP), a.k.a. Morgan fingerprints,
calculated with [RDKit cheminformatics
library](http://rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html?highlight=getmorganfingerprintasbitvect#rdkit.Chem.rdMolDescriptors.GetMorganFingerprintAsBitVect)

> Rogers, David, and Mathew Hahn. “Extended-Connectivity Fingerprints.”
> Journal of Chemical Information and Modeling 50, no. 5 (May 24, 2010):
> 742–54. https://doi.org/10.1021/ci100050t.

Each feature is a single bit of the feature vector.


## Parameters

* size (type: int; default: 2048): The fingerprint size. It should be 1024, 2048 or 4096.



# padel_ALOGP

ALOGP PaDEL descriptor

The following features are calculated:

* ALogP: Ghose-Crippen LogKow
* ALogp2: Square of ALogP
* AMR: Molar refractivity

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_AP2DFP

PaDEL AP2DFPfingerprint

2D atom pairs fingerprint - Presence of atom pairs at various topological
distances

* Number of bits: 780
* Bit prefix: AP2DFP


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_AP2DFPC

PaDEL AP2DFPCfingerprint

2D atom pairs fingerprint count - Count of atom pairs at various topological
distances

* Number of bits: 780
* Bit prefix: AP2DFPC


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_APol

APol PaDEL descriptor

The following features are calculated:

* apol: Sum of the atomic polarizabilities (including implicit hydrogens)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_AcidicGroupCount

AcidicGroupCount PaDEL descriptor

The following features are calculated:

* nAcid: Number of acidic groups. The list of acidic groups is defined by these SMARTS "$([O    H1]-[C,S,P]=O)", "$([*  -       !$(*~[* +])])", "$([NH](S(=O)=O)C(F)(F)F)", and "$(n1nnnc1)" originally presented in JOELib

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_AromaticAtomsCount

AromaticAtomsCount PaDEL descriptor

The following features are calculated:

* naAromAtom: Number of aromatic atoms

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_AromaticBondsCount

AromaticBondsCount PaDEL descriptor

The following features are calculated:

* nAromBond: Number of aromatic bonds

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_AtomCount

AtomCount PaDEL descriptor

The following features are calculated:

* nAtom: Number of atoms
* nHeavyAtom: Number of heavy atoms (i.e. not hydrogen)
* nH: Number of hydrogen atoms
* nB: Number of boron atoms
* nC: Number of carbon atoms
* nN: Number of nitrogen atoms
* nO: Number of oxygen atoms
* nS: Number of sulphur atoms
* nP: Number of phosphorus atoms
* nF: Number of fluorine atoms
* nCl: Number of chlorine atoms
* nBr: Number of bromine atoms
* nI: Number of iodine atoms
* nX: Number of halogen atoms (F, Cl, Br, I, At, Uus)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_Autocorrelation

Autocorrelation PaDEL descriptor

The following features are calculated:

* ATS0m: Broto-Moreau autocorrelation - lag 0 / weighted by mass
* ATS1m: Broto-Moreau autocorrelation - lag 1 / weighted by mass
* ATS2m: Broto-Moreau autocorrelation - lag 2 / weighted by mass
* ATS3m: Broto-Moreau autocorrelation - lag 3 / weighted by mass
* ATS4m: Broto-Moreau autocorrelation - lag 4 / weighted by mass
* ATS5m: Broto-Moreau autocorrelation - lag 5 / weighted by mass
* ATS6m: Broto-Moreau autocorrelation - lag 6 / weighted by mass
* ATS7m: Broto-Moreau autocorrelation - lag 7 / weighted by mass
* ATS8m: Broto-Moreau autocorrelation - lag 8 / weighted by mass
* ATS0v: Broto-Moreau autocorrelation - lag 0 / weighted by van der Waals volumes
* ATS1v: Broto-Moreau autocorrelation - lag 1 / weighted by van der Waals volumes
* ATS2v: Broto-Moreau autocorrelation - lag 2 / weighted by van der Waals volumes
* ATS3v: Broto-Moreau autocorrelation - lag 3 / weighted by van der Waals volumes
* ATS4v: Broto-Moreau autocorrelation - lag 4 / weighted by van der Waals volumes
* ATS5v: Broto-Moreau autocorrelation - lag 5 / weighted by van der Waals volumes
* ATS6v: Broto-Moreau autocorrelation - lag 6 / weighted by van der Waals volumes
* ATS7v: Broto-Moreau autocorrelation - lag 7 / weighted by van der Waals volumes
* ATS8v: Broto-Moreau autocorrelation - lag 8 / weighted by van der Waals volumes
* ATS0e: Broto-Moreau autocorrelation - lag 0 / weighted by Sanderson electronegativities
* ATS1e: Broto-Moreau autocorrelation - lag 1 / weighted by Sanderson electronegativities
* ATS2e: Broto-Moreau autocorrelation - lag 2 / weighted by Sanderson electronegativities
* ATS3e: Broto-Moreau autocorrelation - lag 3 / weighted by Sanderson electronegativities
* ATS4e: Broto-Moreau autocorrelation - lag 4 / weighted by Sanderson electronegativities
* ATS5e: Broto-Moreau autocorrelation - lag 5 / weighted by Sanderson electronegativities
* ATS6e: Broto-Moreau autocorrelation - lag 6 / weighted by Sanderson electronegativities
* ATS7e: Broto-Moreau autocorrelation - lag 7 / weighted by Sanderson electronegativities
* ATS8e: Broto-Moreau autocorrelation - lag 8 / weighted by Sanderson electronegativities
* ATS0p: Broto-Moreau autocorrelation - lag 0 / weighted by polarizabilities
* ATS1p: Broto-Moreau autocorrelation - lag 1 / weighted by polarizabilities
* ATS2p: Broto-Moreau autocorrelation - lag 2 / weighted by polarizabilities
* ATS3p: Broto-Moreau autocorrelation - lag 3 / weighted by polarizabilities
* ATS4p: Broto-Moreau autocorrelation - lag 4 / weighted by polarizabilities
* ATS5p: Broto-Moreau autocorrelation - lag 5 / weighted by polarizabilities
* ATS6p: Broto-Moreau autocorrelation - lag 6 / weighted by polarizabilities
* ATS7p: Broto-Moreau autocorrelation - lag 7 / weighted by polarizabilities
* ATS8p: Broto-Moreau autocorrelation - lag 8 / weighted by polarizabilities
* ATS0i: Broto-Moreau autocorrelation - lag 0 / weighted by first ionization potential
* ATS1i: Broto-Moreau autocorrelation - lag 1 / weighted by first ionization potential
* ATS2i: Broto-Moreau autocorrelation - lag 2 / weighted by first ionization potential
* ATS3i: Broto-Moreau autocorrelation - lag 3 / weighted by first ionization potential
* ATS4i: Broto-Moreau autocorrelation - lag 4 / weighted by first ionization potential
* ATS5i: Broto-Moreau autocorrelation - lag 5 / weighted by first ionization potential
* ATS6i: Broto-Moreau autocorrelation - lag 6 / weighted by first ionization potential
* ATS7i: Broto-Moreau autocorrelation - lag 7 / weighted by first ionization potential
* ATS8i: Broto-Moreau autocorrelation - lag 8 / weighted by first ionization potential
* ATS0s: Broto-Moreau autocorrelation - lag 0 / weighted by I-state
* ATS1s: Broto-Moreau autocorrelation - lag 1 / weighted by I-state
* ATS2s: Broto-Moreau autocorrelation - lag 2 / weighted by I-state
* ATS3s: Broto-Moreau autocorrelation - lag 3 / weighted by I-state
* ATS4s: Broto-Moreau autocorrelation - lag 4 / weighted by I-state
* ATS5s: Broto-Moreau autocorrelation - lag 5 / weighted by I-state
* ATS6s: Broto-Moreau autocorrelation - lag 6 / weighted by I-state
* ATS7s: Broto-Moreau autocorrelation - lag 7 / weighted by I-state
* ATS8s: Broto-Moreau autocorrelation - lag 8 / weighted by I-state
* AATS0m: Average Broto-Moreau autocorrelation - lag 0 / weighted by mass
* AATS1m: Average Broto-Moreau autocorrelation - lag 1 / weighted by mass
* AATS2m: Average Broto-Moreau autocorrelation - lag 2 / weighted by mass
* AATS3m: Average Broto-Moreau autocorrelation - lag 3 / weighted by mass
* AATS4m: Average Broto-Moreau autocorrelation - lag 4 / weighted by mass
* AATS5m: Average Broto-Moreau autocorrelation - lag 5 / weighted by mass
* AATS6m: Average Broto-Moreau autocorrelation - lag 6 / weighted by mass
* AATS7m: Average Broto-Moreau autocorrelation - lag 7 / weighted by mass
* AATS8m: Average Broto-Moreau autocorrelation - lag 8 / weighted by mass
* AATS0v: Average Broto-Moreau autocorrelation - lag 0 / weighted by van der Waals volumes
* AATS1v: Average Broto-Moreau autocorrelation - lag 1 / weighted by van der Waals volumes
* AATS2v: Average Broto-Moreau autocorrelation - lag 2 / weighted by van der Waals volumes
* AATS3v: Average Broto-Moreau autocorrelation - lag 3 / weighted by van der Waals volumes
* AATS4v: Average Broto-Moreau autocorrelation - lag 4 / weighted by van der Waals volumes
* AATS5v: Average Broto-Moreau autocorrelation - lag 5 / weighted by van der Waals volumes
* AATS6v: Average Broto-Moreau autocorrelation - lag 6 / weighted by van der Waals volumes
* AATS7v: Average Broto-Moreau autocorrelation - lag 7 / weighted by van der Waals volumes
* AATS8v: Average Broto-Moreau autocorrelation - lag 8 / weighted by van der Waals volumes
* AATS0e: Average Broto-Moreau autocorrelation - lag 0 / weighted by Sanderson electronegativities
* AATS1e: Average Broto-Moreau autocorrelation - lag 1 / weighted by Sanderson electronegativities
* AATS2e: Average Broto-Moreau autocorrelation - lag 2 / weighted by Sanderson electronegativities
* AATS3e: Average Broto-Moreau autocorrelation - lag 3 / weighted by Sanderson electronegativities
* AATS4e: Average Broto-Moreau autocorrelation - lag 4 / weighted by Sanderson electronegativities
* AATS5e: Average Broto-Moreau autocorrelation - lag 5 / weighted by Sanderson electronegativities
* AATS6e: Average Broto-Moreau autocorrelation - lag 6 / weighted by Sanderson electronegativities
* AATS7e: Average Broto-Moreau autocorrelation - lag 7 / weighted by Sanderson electronegativities
* AATS8e: Average Broto-Moreau autocorrelation - lag 8 / weighted by Sanderson electronegativities
* AATS0p: Average Broto-Moreau autocorrelation - lag 0 / weighted by polarizabilities
* AATS1p: Average Broto-Moreau autocorrelation - lag 1 / weighted by polarizabilities
* AATS2p: Average Broto-Moreau autocorrelation - lag 2 / weighted by polarizabilities
* AATS3p: Average Broto-Moreau autocorrelation - lag 3 / weighted by polarizabilities
* AATS4p: Average Broto-Moreau autocorrelation - lag 4 / weighted by polarizabilities
* AATS5p: Average Broto-Moreau autocorrelation - lag 5 / weighted by polarizabilities
* AATS6p: Average Broto-Moreau autocorrelation - lag 6 / weighted by polarizabilities
* AATS7p: Average Broto-Moreau autocorrelation - lag 7 / weighted by polarizabilities
* AATS8p: Average Broto-Moreau autocorrelation - lag 8 / weighted by polarizabilities
* AATS0i: Average Broto-Moreau autocorrelation - lag 0 / weighted by first ionization potential
* AATS1i: Average Broto-Moreau autocorrelation - lag 1 / weighted by first ionization potential
* AATS2i: Average Broto-Moreau autocorrelation - lag 2 / weighted by first ionization potential
* AATS3i: Average Broto-Moreau autocorrelation - lag 3 / weighted by first ionization potential
* AATS4i: Average Broto-Moreau autocorrelation - lag 4 / weighted by first ionization potential
* AATS5i: Average Broto-Moreau autocorrelation - lag 5 / weighted by first ionization potential
* AATS6i: Average Broto-Moreau autocorrelation - lag 6 / weighted by first ionization potential
* AATS7i: Average Broto-Moreau autocorrelation - lag 7 / weighted by first ionization potential
* AATS8i: Average Broto-Moreau autocorrelation - lag 8 / weighted by first ionization potential
* AATS0s: Average Broto-Moreau autocorrelation - lag 0 / weighted by I-state
* AATS1s: Average Broto-Moreau autocorrelation - lag 1 / weighted by I-state
* AATS2s: Average Broto-Moreau autocorrelation - lag 2 / weighted by I-state
* AATS3s: Average Broto-Moreau autocorrelation - lag 3 / weighted by I-state
* AATS4s: Average Broto-Moreau autocorrelation - lag 4 / weighted by I-state
* AATS5s: Average Broto-Moreau autocorrelation - lag 5 / weighted by I-state
* AATS6s: Average Broto-Moreau autocorrelation - lag 6 / weighted by I-state
* AATS7s: Average Broto-Moreau autocorrelation - lag 7 / weighted by I-state
* AATS8s: Average Broto-Moreau autocorrelation - lag 8 / weighted by I-state
* ATSC0c: Centered Broto-Moreau autocorrelation - lag 0 / weighted by charges
* ATSC1c: Centered Broto-Moreau autocorrelation - lag 1 / weighted by charges
* ATSC2c: Centered Broto-Moreau autocorrelation - lag 2 / weighted by charges
* ATSC3c: Centered Broto-Moreau autocorrelation - lag 3 / weighted by charges
* ATSC4c: Centered Broto-Moreau autocorrelation - lag 4 / weighted by charges
* ATSC5c: Centered Broto-Moreau autocorrelation - lag 5 / weighted by charges
* ATSC6c: Centered Broto-Moreau autocorrelation - lag 6 / weighted by charges
* ATSC7c: Centered Broto-Moreau autocorrelation - lag 7 / weighted by charges
* ATSC8c: Centered Broto-Moreau autocorrelation - lag 8 / weighted by charges
* ATSC0m: Centered Broto-Moreau autocorrelation - lag 0 / weighted by mass
* ATSC1m: Centered Broto-Moreau autocorrelation - lag 1 / weighted by mass
* ATSC2m: Centered Broto-Moreau autocorrelation - lag 2 / weighted by mass
* ATSC3m: Centered Broto-Moreau autocorrelation - lag 3 / weighted by mass
* ATSC4m: Centered Broto-Moreau autocorrelation - lag 4 / weighted by mass
* ATSC5m: Centered Broto-Moreau autocorrelation - lag 5 / weighted by mass
* ATSC6m: Centered Broto-Moreau autocorrelation - lag 6 / weighted by mass
* ATSC7m: Centered Broto-Moreau autocorrelation - lag 7 / weighted by mass
* ATSC8m: Centered Broto-Moreau autocorrelation - lag 8 / weighted by mass
* ATSC0v: Centered Broto-Moreau autocorrelation - lag 0 / weighted by van der Waals volumes
* ATSC1v: Centered Broto-Moreau autocorrelation - lag 1 / weighted by van der Waals volumes
* ATSC2v: Centered Broto-Moreau autocorrelation - lag 2 / weighted by van der Waals volumes
* ATSC3v: Centered Broto-Moreau autocorrelation - lag 3 / weighted by van der Waals volumes
* ATSC4v: Centered Broto-Moreau autocorrelation - lag 4 / weighted by van der Waals volumes
* ATSC5v: Centered Broto-Moreau autocorrelation - lag 5 / weighted by van der Waals volumes
* ATSC6v: Centered Broto-Moreau autocorrelation - lag 6 / weighted by van der Waals volumes
* ATSC7v: Centered Broto-Moreau autocorrelation - lag 7 / weighted by van der Waals volumes
* ATSC8v: Centered Broto-Moreau autocorrelation - lag 8 / weighted by van der Waals volumes
* ATSC0e: Centered Broto-Moreau autocorrelation - lag 0 / weighted by Sanderson electronegativities
* ATSC1e: Centered Broto-Moreau autocorrelation - lag 1 / weighted by Sanderson electronegativities
* ATSC2e: Centered Broto-Moreau autocorrelation - lag 2 / weighted by Sanderson electronegativities
* ATSC3e: Centered Broto-Moreau autocorrelation - lag 3 / weighted by Sanderson electronegativities
* ATSC4e: Centered Broto-Moreau autocorrelation - lag 4 / weighted by Sanderson electronegativities
* ATSC5e: Centered Broto-Moreau autocorrelation - lag 5 / weighted by Sanderson electronegativities
* ATSC6e: Centered Broto-Moreau autocorrelation - lag 6 / weighted by Sanderson electronegativities
* ATSC7e: Centered Broto-Moreau autocorrelation - lag 7 / weighted by Sanderson electronegativities
* ATSC8e: Centered Broto-Moreau autocorrelation - lag 8 / weighted by Sanderson electronegativities
* ATSC0p: Centered Broto-Moreau autocorrelation - lag 0 / weighted by polarizabilities
* ATSC1p: Centered Broto-Moreau autocorrelation - lag 1 / weighted by polarizabilities
* ATSC2p: Centered Broto-Moreau autocorrelation - lag 2 / weighted by polarizabilities
* ATSC3p: Centered Broto-Moreau autocorrelation - lag 3 / weighted by polarizabilities
* ATSC4p: Centered Broto-Moreau autocorrelation - lag 4 / weighted by polarizabilities
* ATSC5p: Centered Broto-Moreau autocorrelation - lag 5 / weighted by polarizabilities
* ATSC6p: Centered Broto-Moreau autocorrelation - lag 6 / weighted by polarizabilities
* ATSC7p: Centered Broto-Moreau autocorrelation - lag 7 / weighted by polarizabilities
* ATSC8p: Centered Broto-Moreau autocorrelation - lag 8 / weighted by polarizabilities
* ATSC0i: Centered Broto-Moreau autocorrelation - lag 0 / weighted by first ionization potential
* ATSC1i: Centered Broto-Moreau autocorrelation - lag 1 / weighted by first ionization potential
* ATSC2i: Centered Broto-Moreau autocorrelation - lag 2 / weighted by first ionization potential
* ATSC3i: Centered Broto-Moreau autocorrelation - lag 3 / weighted by first ionization potential
* ATSC4i: Centered Broto-Moreau autocorrelation - lag 4 / weighted by first ionization potential
* ATSC5i: Centered Broto-Moreau autocorrelation - lag 5 / weighted by first ionization potential
* ATSC6i: Centered Broto-Moreau autocorrelation - lag 6 / weighted by first ionization potential
* ATSC7i: Centered Broto-Moreau autocorrelation - lag 7 / weighted by first ionization potential
* ATSC8i: Centered Broto-Moreau autocorrelation - lag 8 / weighted by first ionization potential
* ATSC0s: Centered Broto-Moreau autocorrelation - lag 0 / weighted by I-state
* ATSC1s: Centered Broto-Moreau autocorrelation - lag 1 / weighted by I-state
* ATSC2s: Centered Broto-Moreau autocorrelation - lag 2 / weighted by I-state
* ATSC3s: Centered Broto-Moreau autocorrelation - lag 3 / weighted by I-state
* ATSC4s: Centered Broto-Moreau autocorrelation - lag 4 / weighted by I-state
* ATSC5s: Centered Broto-Moreau autocorrelation - lag 5 / weighted by I-state
* ATSC6s: Centered Broto-Moreau autocorrelation - lag 6 / weighted by I-state
* ATSC7s: Centered Broto-Moreau autocorrelation - lag 7 / weighted by I-state
* ATSC8s: Centered Broto-Moreau autocorrelation - lag 8 / weighted by I-state
* AATSC0c: Average centered Broto-Moreau autocorrelation - lag 0 / weighted by charges
* AATSC1c: Average centered Broto-Moreau autocorrelation - lag 1 / weighted by charges
* AATSC2c: Average centered Broto-Moreau autocorrelation - lag 2 / weighted by charges
* AATSC3c: Average centered Broto-Moreau autocorrelation - lag 3 / weighted by charges
* AATSC4c: Average centered Broto-Moreau autocorrelation - lag 4 / weighted by charges
* AATSC5c: Average centered Broto-Moreau autocorrelation - lag 5 / weighted by charges
* AATSC6c: Average centered Broto-Moreau autocorrelation - lag 6 / weighted by charges
* AATSC7c: Average centered Broto-Moreau autocorrelation - lag 7 / weighted by charges
* AATSC8c: Average centered Broto-Moreau autocorrelation - lag 8 / weighted by charges
* AATSC0m: Average centered Broto-Moreau autocorrelation - lag 0 / weighted by mass
* AATSC1m: Average centered Broto-Moreau autocorrelation - lag 1 / weighted by mass
* AATSC2m: Average centered Broto-Moreau autocorrelation - lag 2 / weighted by mass
* AATSC3m: Average centered Broto-Moreau autocorrelation - lag 3 / weighted by mass
* AATSC4m: Average centered Broto-Moreau autocorrelation - lag 4 / weighted by mass
* AATSC5m: Average centered Broto-Moreau autocorrelation - lag 5 / weighted by mass
* AATSC6m: Average centered Broto-Moreau autocorrelation - lag 6 / weighted by mass
* AATSC7m: Average centered Broto-Moreau autocorrelation - lag 7 / weighted by mass
* AATSC8m: Average centered Broto-Moreau autocorrelation - lag 8 / weighted by mass
* AATSC0v: Average centered Broto-Moreau autocorrelation - lag 0 / weighted by van der Waals volumes
* AATSC1v: Average centered Broto-Moreau autocorrelation - lag 1 / weighted by van der Waals volumes
* AATSC2v: Average centered Broto-Moreau autocorrelation - lag 2 / weighted by van der Waals volumes
* AATSC3v: Average centered Broto-Moreau autocorrelation - lag 3 / weighted by van der Waals volumes
* AATSC4v: Average centered Broto-Moreau autocorrelation - lag 4 / weighted by van der Waals volumes
* AATSC5v: Average centered Broto-Moreau autocorrelation - lag 5 / weighted by van der Waals volumes
* AATSC6v: Average centered Broto-Moreau autocorrelation - lag 6 / weighted by van der Waals volumes
* AATSC7v: Average centered Broto-Moreau autocorrelation - lag 7 / weighted by van der Waals volumes
* AATSC8v: Average centered Broto-Moreau autocorrelation - lag 8 / weighted by van der Waals volumes
* AATSC0e: Average centered Broto-Moreau autocorrelation - lag 0 / weighted by Sanderson electronegativities
* AATSC1e: Average centered Broto-Moreau autocorrelation - lag 1 / weighted by Sanderson electronegativities
* AATSC2e: Average centered Broto-Moreau autocorrelation - lag 2 / weighted by Sanderson electronegativities
* AATSC3e: Average centered Broto-Moreau autocorrelation - lag 3 / weighted by Sanderson electronegativities
* AATSC4e: Average centered Broto-Moreau autocorrelation - lag 4 / weighted by Sanderson electronegativities
* AATSC5e: Average centered Broto-Moreau autocorrelation - lag 5 / weighted by Sanderson electronegativities
* AATSC6e: Average centered Broto-Moreau autocorrelation - lag 6 / weighted by Sanderson electronegativities
* AATSC7e: Average centered Broto-Moreau autocorrelation - lag 7 / weighted by Sanderson electronegativities
* AATSC8e: Average centered Broto-Moreau autocorrelation - lag 8 / weighted by Sanderson electronegativities
* AATSC0p: Average centered Broto-Moreau autocorrelation - lag 0 / weighted by polarizabilities
* AATSC1p: Average centered Broto-Moreau autocorrelation - lag 1 / weighted by polarizabilities
* AATSC2p: Average centered Broto-Moreau autocorrelation - lag 2 / weighted by polarizabilities
* AATSC3p: Average centered Broto-Moreau autocorrelation - lag 3 / weighted by polarizabilities
* AATSC4p: Average centered Broto-Moreau autocorrelation - lag 4 / weighted by polarizabilities
* AATSC5p: Average centered Broto-Moreau autocorrelation - lag 5 / weighted by polarizabilities
* AATSC6p: Average centered Broto-Moreau autocorrelation - lag 6 / weighted by polarizabilities
* AATSC7p: Average centered Broto-Moreau autocorrelation - lag 7 / weighted by polarizabilities
* AATSC8p: Average centered Broto-Moreau autocorrelation - lag 8 / weighted by polarizabilities
* AATSC0i: Average centered Broto-Moreau autocorrelation - lag 0 / weighted by first ionization potential
* AATSC1i: Average centered Broto-Moreau autocorrelation - lag 1 / weighted by first ionization potential
* AATSC2i: Average centered Broto-Moreau autocorrelation - lag 2 / weighted by first ionization potential
* AATSC3i: Average centered Broto-Moreau autocorrelation - lag 3 / weighted by first ionization potential
* AATSC4i: Average centered Broto-Moreau autocorrelation - lag 4 / weighted by first ionization potential
* AATSC5i: Average centered Broto-Moreau autocorrelation - lag 5 / weighted by first ionization potential
* AATSC6i: Average centered Broto-Moreau autocorrelation - lag 6 / weighted by first ionization potential
* AATSC7i: Average centered Broto-Moreau autocorrelation - lag 7 / weighted by first ionization potential
* AATSC8i: Average centered Broto-Moreau autocorrelation - lag 8 / weighted by first ionization potential
* AATSC0s: Average centered Broto-Moreau autocorrelation - lag 0 / weighted by I-state
* AATSC1s: Average centered Broto-Moreau autocorrelation - lag 1 / weighted by I-state
* AATSC2s: Average centered Broto-Moreau autocorrelation - lag 2 / weighted by I-state
* AATSC3s: Average centered Broto-Moreau autocorrelation - lag 3 / weighted by I-state
* AATSC4s: Average centered Broto-Moreau autocorrelation - lag 4 / weighted by I-state
* AATSC5s: Average centered Broto-Moreau autocorrelation - lag 5 / weighted by I-state
* AATSC6s: Average centered Broto-Moreau autocorrelation - lag 6 / weighted by I-state
* AATSC7s: Average centered Broto-Moreau autocorrelation - lag 7 / weighted by I-state
* AATSC8s: Average centered Broto-Moreau autocorrelation - lag 8 / weighted by I-state
* MATS1c: Moran autocorrelation - lag 1 / weighted by charges
* MATS2c: Moran autocorrelation - lag 2 / weighted by charges
* MATS3c: Moran autocorrelation - lag 3 / weighted by charges
* MATS4c: Moran autocorrelation - lag 4 / weighted by charges
* MATS5c: Moran autocorrelation - lag 5 / weighted by charges
* MATS6c: Moran autocorrelation - lag 6 / weighted by charges
* MATS7c: Moran autocorrelation - lag 7 / weighted by charges
* MATS8c: Moran autocorrelation - lag 8 / weighted by charges
* MATS1m: Moran autocorrelation - lag 1 / weighted by mass
* MATS2m: Moran autocorrelation - lag 2 / weighted by mass
* MATS3m: Moran autocorrelation - lag 3 / weighted by mass
* MATS4m: Moran autocorrelation - lag 4 / weighted by mass
* MATS5m: Moran autocorrelation - lag 5 / weighted by mass
* MATS6m: Moran autocorrelation - lag 6 / weighted by mass
* MATS7m: Moran autocorrelation - lag 7 / weighted by mass
* MATS8m: Moran autocorrelation - lag 8 / weighted by mass
* MATS1v: Moran autocorrelation - lag 1 / weighted by van der Waals volumes
* MATS2v: Moran autocorrelation - lag 2 / weighted by van der Waals volumes
* MATS3v: Moran autocorrelation - lag 3 / weighted by van der Waals volumes
* MATS4v: Moran autocorrelation - lag 4 / weighted by van der Waals volumes
* MATS5v: Moran autocorrelation - lag 5 / weighted by van der Waals volumes
* MATS6v: Moran autocorrelation - lag 6 / weighted by van der Waals volumes
* MATS7v: Moran autocorrelation - lag 7 / weighted by van der Waals volumes
* MATS8v: Moran autocorrelation - lag 8 / weighted by van der Waals volumes
* MATS1e: Moran autocorrelation - lag 1 / weighted by Sanderson electronegativities
* MATS2e: Moran autocorrelation - lag 2 / weighted by Sanderson electronegativities
* MATS3e: Moran autocorrelation - lag 3 / weighted by Sanderson electronegativities
* MATS4e: Moran autocorrelation - lag 4 / weighted by Sanderson electronegativities
* MATS5e: Moran autocorrelation - lag 5 / weighted by Sanderson electronegativities
* MATS6e: Moran autocorrelation - lag 6 / weighted by Sanderson electronegativities
* MATS7e: Moran autocorrelation - lag 7 / weighted by Sanderson electronegativities
* MATS8e: Moran autocorrelation - lag 8 / weighted by Sanderson electronegativities
* MATS1p: Moran autocorrelation - lag 1 / weighted by polarizabilities
* MATS2p: Moran autocorrelation - lag 2 / weighted by polarizabilities
* MATS3p: Moran autocorrelation - lag 3 / weighted by polarizabilities
* MATS4p: Moran autocorrelation - lag 4 / weighted by polarizabilities
* MATS5p: Moran autocorrelation - lag 5 / weighted by polarizabilities
* MATS6p: Moran autocorrelation - lag 6 / weighted by polarizabilities
* MATS7p: Moran autocorrelation - lag 7 / weighted by polarizabilities
* MATS8p: Moran autocorrelation - lag 8 / weighted by polarizabilities
* MATS1i: Moran autocorrelation - lag 1 / weighted by first ionization potential
* MATS2i: Moran autocorrelation - lag 2 / weighted by first ionization potential
* MATS3i: Moran autocorrelation - lag 3 / weighted by first ionization potential
* MATS4i: Moran autocorrelation - lag 4 / weighted by first ionization potential
* MATS5i: Moran autocorrelation - lag 5 / weighted by first ionization potential
* MATS6i: Moran autocorrelation - lag 6 / weighted by first ionization potential
* MATS7i: Moran autocorrelation - lag 7 / weighted by first ionization potential
* MATS8i: Moran autocorrelation - lag 8 / weighted by first ionization potential
* MATS1s: Moran autocorrelation - lag 1 / weighted by I-state
* MATS2s: Moran autocorrelation - lag 2 / weighted by I-state
* MATS3s: Moran autocorrelation - lag 3 / weighted by I-state
* MATS4s: Moran autocorrelation - lag 4 / weighted by I-state
* MATS5s: Moran autocorrelation - lag 5 / weighted by I-state
* MATS6s: Moran autocorrelation - lag 6 / weighted by I-state
* MATS7s: Moran autocorrelation - lag 7 / weighted by I-state
* MATS8s: Moran autocorrelation - lag 8 / weighted by I-state
* GATS1c: Geary autocorrelation - lag 1 / weighted by charges
* GATS2c: Geary autocorrelation - lag 2 / weighted by charges
* GATS3c: Geary autocorrelation - lag 3 / weighted by charges
* GATS4c: Geary autocorrelation - lag 4 / weighted by charges
* GATS5c: Geary autocorrelation - lag 5 / weighted by charges
* GATS6c: Geary autocorrelation - lag 6 / weighted by charges
* GATS7c: Geary autocorrelation - lag 7 / weighted by charges
* GATS8c: Geary autocorrelation - lag 8 / weighted by charges
* GATS1m: Geary autocorrelation - lag 1 / weighted by mass
* GATS2m: Geary autocorrelation - lag 2 / weighted by mass
* GATS3m: Geary autocorrelation - lag 3 / weighted by mass
* GATS4m: Geary autocorrelation - lag 4 / weighted by mass
* GATS5m: Geary autocorrelation - lag 5 / weighted by mass
* GATS6m: Geary autocorrelation - lag 6 / weighted by mass
* GATS7m: Geary autocorrelation - lag 7 / weighted by mass
* GATS8m: Geary autocorrelation - lag 8 / weighted by mass
* GATS1v: Geary autocorrelation - lag 1 / weighted by van der Waals volumes
* GATS2v: Geary autocorrelation - lag 2 / weighted by van der Waals volumes
* GATS3v: Geary autocorrelation - lag 3 / weighted by van der Waals volumes
* GATS4v: Geary autocorrelation - lag 4 / weighted by van der Waals volumes
* GATS5v: Geary autocorrelation - lag 5 / weighted by van der Waals volumes
* GATS6v: Geary autocorrelation - lag 6 / weighted by van der Waals volumes
* GATS7v: Geary autocorrelation - lag 7 / weighted by van der Waals volumes
* GATS8v: Geary autocorrelation - lag 8 / weighted by van der Waals volumes
* GATS1e: Geary autocorrelation - lag 1 / weighted by Sanderson electronegativities
* GATS2e: Geary autocorrelation - lag 2 / weighted by Sanderson electronegativities
* GATS3e: Geary autocorrelation - lag 3 / weighted by Sanderson electronegativities
* GATS4e: Geary autocorrelation - lag 4 / weighted by Sanderson electronegativities
* GATS5e: Geary autocorrelation - lag 5 / weighted by Sanderson electronegativities
* GATS6e: Geary autocorrelation - lag 6 / weighted by Sanderson electronegativities
* GATS7e: Geary autocorrelation - lag 7 / weighted by Sanderson electronegativities
* GATS8e: Geary autocorrelation - lag 8 / weighted by Sanderson electronegativities
* GATS1p: Geary autocorrelation - lag 1 / weighted by polarizabilities
* GATS2p: Geary autocorrelation - lag 2 / weighted by polarizabilities
* GATS3p: Geary autocorrelation - lag 3 / weighted by polarizabilities
* GATS4p: Geary autocorrelation - lag 4 / weighted by polarizabilities
* GATS5p: Geary autocorrelation - lag 5 / weighted by polarizabilities
* GATS6p: Geary autocorrelation - lag 6 / weighted by polarizabilities
* GATS7p: Geary autocorrelation - lag 7 / weighted by polarizabilities
* GATS8p: Geary autocorrelation - lag 8 / weighted by polarizabilities
* GATS1i: Geary autocorrelation - lag 1 / weighted by first ionization potential
* GATS2i: Geary autocorrelation - lag 2 / weighted by first ionization potential
* GATS3i: Geary autocorrelation - lag 3 / weighted by first ionization potential
* GATS4i: Geary autocorrelation - lag 4 / weighted by first ionization potential
* GATS5i: Geary autocorrelation - lag 5 / weighted by first ionization potential
* GATS6i: Geary autocorrelation - lag 6 / weighted by first ionization potential
* GATS7i: Geary autocorrelation - lag 7 / weighted by first ionization potential
* GATS8i: Geary autocorrelation - lag 8 / weighted by first ionization potential
* GATS1s: Geary autocorrelation - lag 1 / weighted by I-state
* GATS2s: Geary autocorrelation - lag 2 / weighted by I-state
* GATS3s: Geary autocorrelation - lag 3 / weighted by I-state
* GATS4s: Geary autocorrelation - lag 4 / weighted by I-state
* GATS5s: Geary autocorrelation - lag 5 / weighted by I-state
* GATS6s: Geary autocorrelation - lag 6 / weighted by I-state
* GATS7s: Geary autocorrelation - lag 7 / weighted by I-state
* GATS8s: Geary autocorrelation - lag 8 / weighted by I-state

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_Autocorrelation3D

Autocorrelation3D 3D PaDEL descriptor

The following features are calculated:

* TDB1u: 3D topological distance based autocorrelation - lag 1 / unweighted
* TDB2u: 3D topological distance based autocorrelation - lag 2 / unweighted
* TDB3u: 3D topological distance based autocorrelation - lag 3 / unweighted
* TDB4u: 3D topological distance based autocorrelation - lag 4 / unweighted
* TDB5u: 3D topological distance based autocorrelation - lag 5 / unweighted
* TDB6u: 3D topological distance based autocorrelation - lag 6 / unweighted
* TDB7u: 3D topological distance based autocorrelation - lag 7 / unweighted
* TDB8u: 3D topological distance based autocorrelation - lag 8 / unweighted
* TDB9u: 3D topological distance based autocorrelation - lag 9 / unweighted
* TDB10u: 3D topological distance based autocorrelation - lag 10 / unweighted
* TDB1m: 3D topological distance based autocorrelation - lag 1 / weighted by mass
* TDB2m: 3D topological distance based autocorrelation - lag 2 / weighted by mass
* TDB3m: 3D topological distance based autocorrelation - lag 3 / weighted by mass
* TDB4m: 3D topological distance based autocorrelation - lag 4 / weighted by mass
* TDB5m: 3D topological distance based autocorrelation - lag 5 / weighted by mass
* TDB6m: 3D topological distance based autocorrelation - lag 6 / weighted by mass
* TDB7m: 3D topological distance based autocorrelation - lag 7 / weighted by mass
* TDB8m: 3D topological distance based autocorrelation - lag 8 / weighted by mass
* TDB9m: 3D topological distance based autocorrelation - lag 9 / weighted by mass
* TDB10m: 3D topological distance based autocorrelation - lag 10 / weighted by mass
* TDB1v: 3D topological distance based autocorrelation - lag 1 / weighted by van der Waals volumes
* TDB2v: 3D topological distance based autocorrelation - lag 2 / weighted by van der Waals volumes
* TDB3v: 3D topological distance based autocorrelation - lag 3 / weighted by van der Waals volumes
* TDB4v: 3D topological distance based autocorrelation - lag 4 / weighted by van der Waals volumes
* TDB5v: 3D topological distance based autocorrelation - lag 5 / weighted by van der Waals volumes
* TDB6v: 3D topological distance based autocorrelation - lag 6 / weighted by van der Waals volumes
* TDB7v: 3D topological distance based autocorrelation - lag 7 / weighted by van der Waals volumes
* TDB8v: 3D topological distance based autocorrelation - lag 8 / weighted by van der Waals volumes
* TDB9v: 3D topological distance based autocorrelation - lag 9 / weighted by van der Waals volumes
* TDB10v: 3D topological distance based autocorrelation - lag 10 / weighted by van der Waals volumes
* TDB1e: 3D topological distance based autocorrelation - lag 1 / weighted by Sanderson electronegativities
* TDB2e: 3D topological distance based autocorrelation - lag 2 / weighted by Sanderson electronegativities
* TDB3e: 3D topological distance based autocorrelation - lag 3 / weighted by Sanderson electronegativities
* TDB4e: 3D topological distance based autocorrelation - lag 4 / weighted by Sanderson electronegativities
* TDB5e: 3D topological distance based autocorrelation - lag 5 / weighted by Sanderson electronegativities
* TDB6e: 3D topological distance based autocorrelation - lag 6 / weighted by Sanderson electronegativities
* TDB7e: 3D topological distance based autocorrelation - lag 7 / weighted by Sanderson electronegativities
* TDB8e: 3D topological distance based autocorrelation - lag 8 / weighted by Sanderson electronegativities
* TDB9e: 3D topological distance based autocorrelation - lag 9 / weighted by Sanderson electronegativities
* TDB10e: 3D topological distance based autocorrelation - lag 10 / weighted by Sanderson electronegativities
* TDB1p: 3D topological distance based autocorrelation - lag 1 / weighted by polarizabilities
* TDB2p: 3D topological distance based autocorrelation - lag 2 / weighted by polarizabilities
* TDB3p: 3D topological distance based autocorrelation - lag 3 / weighted by polarizabilities
* TDB4p: 3D topological distance based autocorrelation - lag 4 / weighted by polarizabilities
* TDB5p: 3D topological distance based autocorrelation - lag 5 / weighted by polarizabilities
* TDB6p: 3D topological distance based autocorrelation - lag 6 / weighted by polarizabilities
* TDB7p: 3D topological distance based autocorrelation - lag 7 / weighted by polarizabilities
* TDB8p: 3D topological distance based autocorrelation - lag 8 / weighted by polarizabilities
* TDB9p: 3D topological distance based autocorrelation - lag 9 / weighted by polarizabilities
* TDB10p: 3D topological distance based autocorrelation - lag 10 / weighted by polarizabilities
* TDB1i: 3D topological distance based autocorrelation - lag 1 / weighted by first ionization potential
* TDB2i: 3D topological distance based autocorrelation - lag 2 / weighted by first ionization potential
* TDB3i: 3D topological distance based autocorrelation - lag 3 / weighted by first ionization potential
* TDB4i: 3D topological distance based autocorrelation - lag 4 / weighted by first ionization potential
* TDB5i: 3D topological distance based autocorrelation - lag 5 / weighted by first ionization potential
* TDB6i: 3D topological distance based autocorrelation - lag 6 / weighted by first ionization potential
* TDB7i: 3D topological distance based autocorrelation - lag 7 / weighted by first ionization potential
* TDB8i: 3D topological distance based autocorrelation - lag 8 / weighted by first ionization potential
* TDB9i: 3D topological distance based autocorrelation - lag 9 / weighted by first ionization potential
* TDB10i: 3D topological distance based autocorrelation - lag 10 / weighted by first ionization potential
* TDB1s: 3D topological distance based autocorrelation - lag 1 / weighted by I-state
* TDB2s: 3D topological distance based autocorrelation - lag 2 / weighted by I-state
* TDB3s: 3D topological distance based autocorrelation - lag 3 / weighted by I-state
* TDB4s: 3D topological distance based autocorrelation - lag 4 / weighted by I-state
* TDB5s: 3D topological distance based autocorrelation - lag 5 / weighted by I-state
* TDB6s: 3D topological distance based autocorrelation - lag 6 / weighted by I-state
* TDB7s: 3D topological distance based autocorrelation - lag 7 / weighted by I-state
* TDB8s: 3D topological distance based autocorrelation - lag 8 / weighted by I-state
* TDB9s: 3D topological distance based autocorrelation - lag 9 / weighted by I-state
* TDB10s: 3D topological distance based autocorrelation - lag 10 / weighted by I-state
* TDB1r: 3D topological distance based autocorrelation - lag 1 / weighted by covalent radius
* TDB2r: 3D topological distance based autocorrelation - lag 2 / weighted by covalent radius
* TDB3r: 3D topological distance based autocorrelation - lag 3 / weighted by covalent radius
* TDB4r: 3D topological distance based autocorrelation - lag 4 / weighted by covalent radius
* TDB5r: 3D topological distance based autocorrelation - lag 5 / weighted by covalent radius
* TDB6r: 3D topological distance based autocorrelation - lag 6 / weighted by covalent radius
* TDB7r: 3D topological distance based autocorrelation - lag 7 / weighted by covalent radius
* TDB8r: 3D topological distance based autocorrelation - lag 8 / weighted by covalent radius
* TDB9r: 3D topological distance based autocorrelation - lag 9 / weighted by covalent radius
* TDB10r: 3D topological distance based autocorrelation - lag 10 / weighted by covalent radius

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_BCUT

BCUT PaDEL descriptor

The following features are calculated:

* BCUTw-1l: nhigh lowest atom weighted BCUTS 
* BCUTw-1h: nlow highest atom weighted BCUTS 
* BCUTc-1l: nhigh lowest partial charge weighted BCUTS 
* BCUTc-1h: nlow highest partial charge weighted BCUTS 
* BCUTp-1l: nhigh lowest polarizability weighted BCUTS 
* BCUTp-1h: nlow highest polarizability weighted BCUTS 

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_BPol

BPol PaDEL descriptor

The following features are calculated:

* bpol: Sum of the absolute value of the difference between atomic polarizabilities of all bonded atoms in the molecule (including implicit hydrogens)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_BaryszMatrix

BaryszMatrix PaDEL descriptor

The following features are calculated:

* SpAbs_DzZ: Graph energy from Barysz matrix / weighted by atomic number
* SpMax_DzZ: Leading eigenvalue from Barysz matrix / weighted by atomic number
* SpDiam_DzZ: Spectral diameter from Barysz matrix / weighted by atomic number
* SpAD_DzZ: Spectral absolute deviation from Barysz matrix / weighted by atomic number
* SpMAD_DzZ: Spectral mean absolute deviation from Barysz matrix / weighted by atomic number
* EE_DzZ: Estrada-like index from Barysz matrix / weighted by atomic number (ln(1+x))
* SM1_DzZ: Spectral moment of order 1 from Barysz matrix / weighted by atomic number
* VE1_DzZ: Coefficient sum of the last eigenvector from Barysz matrix / weighted by atomic number
* VE2_DzZ: Average coefficient sum of the last eigenvector from Barysz matrix / weighted by atomic number
* VE3_DzZ: Logarithmic coefficient sum of the last eigenvector from Barysz matrix / weighted by atomic number
* VR1_DzZ: Randic-like eigenvector-based index from Barysz matrix / weighted by atomic number
* VR2_DzZ: Normalized Randic-like eigenvector-based index from Barysz matrix / weighted by atomic number
* VR3_DzZ: Logarithmic Randic-like eigenvector-based index from Barysz matrix / weighted by atomic number
* SpAbs_Dzm: Graph energy from Barysz matrix / weighted by mass
* SpMax_Dzm: Leading eigenvalue from Barysz matrix / weighted by mass
* SpDiam_Dzm: Spectral diameter from Barysz matrix / weighted by mass
* SpAD_Dzm: Spectral absolute deviation from Barysz matrix / weighted by mass
* SpMAD_Dzm: Spectral mean absolute deviation from Barysz matrix / weighted by mass
* EE_Dzm: Estrada-like index from Barysz matrix / weighted by mass (ln(1+x))
* SM1_Dzm: Spectral moment of order 1 from Barysz matrix / weighted by mass
* VE1_Dzm: Coefficient sum of the last eigenvector from Barysz matrix / weighted by mass
* VE2_Dzm: Average coefficient sum of the last eigenvector from Barysz matrix / weighted by mass
* VE3_Dzm: Logarithmic coefficient sum of the last eigenvector from Barysz matrix / weighted by mass
* VR1_Dzm: Randic-like eigenvector-based index from Barysz matrix / weighted by mass
* VR2_Dzm: Normalized Randic-like eigenvector-based index from Barysz matrix / weighted by mass
* VR3_Dzm: Logarithmic Randic-like eigenvector-based index from Barysz matrix / weighted by mass
* SpAbs_Dzv: Graph energy from Barysz matrix / weighted by van der Waals volumes
* SpMax_Dzv: Leading eigenvalue from Barysz matrix / weighted by van der Waals volumes
* SpDiam_Dzv: Spectral diameter from Barysz matrix / weighted by van der Waals volumes
* SpAD_Dzv: Spectral absolute deviation from Barysz matrix / weighted by van der Waals volumes
* SpMAD_Dzv: Spectral mean absolute deviation from Barysz matrix / weighted by van der Waals volumes
* EE_Dzv: Estrada-like index from Barysz matrix / weighted by van der Waals volumes (ln(1+x))
* SM1_Dzv: Spectral moment of order 1 from Barysz matrix / weighted by van der Waals volumes
* VE1_Dzv: Coefficient sum of the last eigenvector from Barysz matrix / weighted by van der Waals volumes
* VE2_Dzv: Average coefficient sum of the last eigenvector from Barysz matrix / weighted by van der Waals volumes
* VE3_Dzv: Logarithmic coefficient sum of the last eigenvector from Barysz matrix / weighted by van der Waals volumes
* VR1_Dzv: Randic-like eigenvector-based index from Barysz matrix / weighted by van der Waals volumes
* VR2_Dzv: Normalized Randic-like eigenvector-based index from Barysz matrix / weighted by van der Waals volumes
* VR3_Dzv: Logarithmic Randic-like eigenvector-based index from Barysz matrix / weighted by van der Waals volumes
* SpAbs_Dze: Graph energy from Barysz matrix / weighted by Sanderson electronegativities
* SpMax_Dze: Leading eigenvalue from Barysz matrix / weighted by Sanderson electronegativities
* SpDiam_Dze: Spectral diameter from Barysz matrix / weighted by Sanderson electronegativities
* SpAD_Dze: Spectral absolute deviation from Barysz matrix / weighted by Sanderson electronegativities
* SpMAD_Dze: Spectral mean absolute deviation from Barysz matrix / weighted by Sanderson electronegativities
* EE_Dze: Estrada-like index from Barysz matrix / weighted by Sanderson electronegativities (ln(1+x))
* SM1_Dze: Spectral moment of order 1 from Barysz matrix / weighted by Sanderson electronegativities
* VE1_Dze: Coefficient sum of the last eigenvector from Barysz matrix / weighted by Sanderson electronegativities
* VE2_Dze: Average coefficient sum of the last eigenvector from Barysz matrix / weighted by Sanderson electronegativities
* VE3_Dze: Logarithmic coefficient sum of the last eigenvector from Barysz matrix / weighted by Sanderson electronegativities
* VR1_Dze: Randic-like eigenvector-based index from Barysz matrix / weighted by Sanderson electronegativities
* VR2_Dze: Normalized Randic-like eigenvector-based index from Barysz matrix / weighted by Sanderson electronegativities
* VR3_Dze: Logarithmic Randic-like eigenvector-based index from Barysz matrix / weighted by Sanderson electronegativities
* SpAbs_Dzp: Graph energy from Barysz matrix / weighted by polarizabilities
* SpMax_Dzp: Leading eigenvalue from Barysz matrix / weighted by polarizabilities
* SpDiam_Dzp: Spectral diameter from Barysz matrix / weighted by polarizabilities
* SpAD_Dzp: Spectral absolute deviation from Barysz matrix / weighted by polarizabilities
* SpMAD_Dzp: Spectral mean absolute deviation from Barysz matrix / weighted by polarizabilities
* EE_Dzp: Estrada-like index from Barysz matrix / weighted by polarizabilities (ln(1+x))
* SM1_Dzp: Spectral moment of order 1 from Barysz matrix / weighted by polarizabilities
* VE1_Dzp: Coefficient sum of the last eigenvector from Barysz matrix / weighted by polarizabilities
* VE2_Dzp: Average coefficient sum of the last eigenvector from Barysz matrix / weighted by polarizabilities
* VE3_Dzp: Logarithmic coefficient sum of the last eigenvector from Barysz matrix / weighted by polarizabilities
* VR1_Dzp: Randic-like eigenvector-based index from Barysz matrix / weighted by polarizabilities
* VR2_Dzp: Normalized Randic-like eigenvector-based index from Barysz matrix / weighted by polarizabilities
* VR3_Dzp: Logarithmic Randic-like eigenvector-based index from Barysz matrix / weighted by polarizabilities
* SpAbs_Dzi: Graph energy from Barysz matrix / weighted by first ionization potential
* SpMax_Dzi: Leading eigenvalue from Barysz matrix / weighted by first ionization potential
* SpDiam_Dzi: Spectral diameter from Barysz matrix / weighted by first ionization potential
* SpAD_Dzi: Spectral absolute deviation from Barysz matrix / weighted by first ionization potential
* SpMAD_Dzi: Spectral mean absolute deviation from Barysz matrix / weighted by first ionization potential
* EE_Dzi: Estrada-like index from Barysz matrix / weighted by first ionization potential (ln(1+x))
* SM1_Dzi: Spectral moment of order 1 from Barysz matrix / weighted by first ionization potential
* VE1_Dzi: Coefficient sum of the last eigenvector from Barysz matrix / weighted by first ionization potential
* VE2_Dzi: Average coefficient sum of the last eigenvector from Barysz matrix / weighted by first ionization potential
* VE3_Dzi: Logarithmic coefficient sum of the last eigenvector from Barysz matrix / weighted by first ionization potential
* VR1_Dzi: Randic-like eigenvector-based index from Barysz matrix / weighted by first ionization potential
* VR2_Dzi: Normalized Randic-like eigenvector-based index from Barysz matrix / weighted by first ionization potential
* VR3_Dzi: Logarithmic Randic-like eigenvector-based index from Barysz matrix / weighted by first ionization potential
* SpAbs_Dzs: Graph energy from Barysz matrix / weighted by I-state
* SpMax_Dzs: Leading eigenvalue from Barysz matrix / weighted by I-state
* SpDiam_Dzs: Spectral diameter from Barysz matrix / weighted by I-state
* SpAD_Dzs: Spectral absolute deviation from Barysz matrix / weighted by I-state
* SpMAD_Dzs: Spectral mean absolute deviation from Barysz matrix / weighted by I-state
* EE_Dzs: Estrada-like index from Barysz matrix / weighted by I-state (ln(1+x))
* SM1_Dzs: Spectral moment of order 1 from Barysz matrix / weighted by I-state
* VE1_Dzs: Coefficient sum of the last eigenvector from Barysz matrix / weighted by I-state
* VE2_Dzs: Average coefficient sum of the last eigenvector from Barysz matrix / weighted by I-state
* VE3_Dzs: Logarithmic coefficient sum of the last eigenvector from Barysz matrix / weighted by I-state
* VR1_Dzs: Randic-like eigenvector-based index from Barysz matrix / weighted by I-state
* VR2_Dzs: Normalized Randic-like eigenvector-based index from Barysz matrix / weighted by I-state
* VR3_Dzs: Logarithmic Randic-like eigenvector-based index from Barysz matrix / weighted by I-state

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_BasicGroupCount

BasicGroupCount PaDEL descriptor

The following features are calculated:

* nBase: Number of basic groups. The list of basic groups is defined by this SMARTS "[$([NH2]-[CX4])]", "[$([NH](-[CX4])-[CX4])]", "[$(N(-[CX4])(-[CX4])-[CX4])]", "[$([*       +       !$(*~[* -])])]", "[$(N=C-N)]", and "[$(N-C=N)]" originally presented in JOELib

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_BondCount

BondCount PaDEL descriptor

The following features are calculated:

* nBonds: Number of bonds (excluding bonds with hydrogen)
* nBonds2: Total number of bonds (including bonds to hydrogens)
* nBondsS: Number of single bonds (including bonds with hydrogen)
* nBondsS2: Total number of single bonds (including bonds to hydrogens, excluding aromatic bonds)
* nBondsS3: Total number of single bonds (excluding bonds to hydrogens and aromatic bonds)
* nBondsD: Number of double bonds
* nBondsD2: Total number of double bonds (excluding bonds to aromatic bonds)
* nBondsT: Number of triple bonds
* nBondsQ: Number of quadruple bonds
* nBondsM: Total number of bonds that have bond order greater than one (aromatic bonds have bond order 1.5).

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_BurdenModifiedEigenvalues

BurdenModifiedEigenvalues PaDEL descriptor

The following features are calculated:

* SpMax1_Bhm: Largest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative mass
* SpMax2_Bhm: Largest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative mass
* SpMax3_Bhm: Largest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative mass
* SpMax4_Bhm: Largest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative mass
* SpMax5_Bhm: Largest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative mass
* SpMax6_Bhm: Largest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative mass
* SpMax7_Bhm: Largest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative mass
* SpMax8_Bhm: Largest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative mass
* SpMin1_Bhm: Smallest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative mass
* SpMin2_Bhm: Smallest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative mass
* SpMin3_Bhm: Smallest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative mass
* SpMin4_Bhm: Smallest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative mass
* SpMin5_Bhm: Smallest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative mass
* SpMin6_Bhm: Smallest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative mass
* SpMin7_Bhm: Smallest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative mass
* SpMin8_Bhm: Smallest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative mass
* SpMax1_Bhv: Largest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative van der Waals volumes
* SpMax2_Bhv: Largest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative van der Waals volumes
* SpMax3_Bhv: Largest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative van der Waals volumes
* SpMax4_Bhv: Largest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative van der Waals volumes
* SpMax5_Bhv: Largest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative van der Waals volumes
* SpMax6_Bhv: Largest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative van der Waals volumes
* SpMax7_Bhv: Largest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative van der Waals volumes
* SpMax8_Bhv: Largest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative van der Waals volumes
* SpMin1_Bhv: Smallest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative van der Waals volumes
* SpMin2_Bhv: Smallest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative van der Waals volumes
* SpMin3_Bhv: Smallest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative van der Waals volumes
* SpMin4_Bhv: Smallest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative van der Waals volumes
* SpMin5_Bhv: Smallest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative van der Waals volumes
* SpMin6_Bhv: Smallest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative van der Waals volumes
* SpMin7_Bhv: Smallest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative van der Waals volumes
* SpMin8_Bhv: Smallest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative van der Waals volumes
* SpMax1_Bhe: Largest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative Sanderson electronegativities
* SpMax2_Bhe: Largest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative Sanderson electronegativities
* SpMax3_Bhe: Largest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative Sanderson electronegativities
* SpMax4_Bhe: Largest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative Sanderson electronegativities
* SpMax5_Bhe: Largest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative Sanderson electronegativities
* SpMax6_Bhe: Largest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative Sanderson electronegativities
* SpMax7_Bhe: Largest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative Sanderson electronegativities
* SpMax8_Bhe: Largest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative Sanderson electronegativities
* SpMin1_Bhe: Smallest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative Sanderson electronegativities
* SpMin2_Bhe: Smallest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative Sanderson electronegativities
* SpMin3_Bhe: Smallest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative Sanderson electronegativities
* SpMin4_Bhe: Smallest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative Sanderson electronegativities
* SpMin5_Bhe: Smallest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative Sanderson electronegativities
* SpMin6_Bhe: Smallest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative Sanderson electronegativities
* SpMin7_Bhe: Smallest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative Sanderson electronegativities
* SpMin8_Bhe: Smallest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative Sanderson electronegativities
* SpMax1_Bhp: Largest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative polarizabilities
* SpMax2_Bhp: Largest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative polarizabilities
* SpMax3_Bhp: Largest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative polarizabilities
* SpMax4_Bhp: Largest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative polarizabilities
* SpMax5_Bhp: Largest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative polarizabilities
* SpMax6_Bhp: Largest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative polarizabilities
* SpMax7_Bhp: Largest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative polarizabilities
* SpMax8_Bhp: Largest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative polarizabilities
* SpMin1_Bhp: Smallest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative polarizabilities
* SpMin2_Bhp: Smallest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative polarizabilities
* SpMin3_Bhp: Smallest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative polarizabilities
* SpMin4_Bhp: Smallest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative polarizabilities
* SpMin5_Bhp: Smallest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative polarizabilities
* SpMin6_Bhp: Smallest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative polarizabilities
* SpMin7_Bhp: Smallest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative polarizabilities
* SpMin8_Bhp: Smallest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative polarizabilities
* SpMax1_Bhi: Largest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative first ionization potential
* SpMax2_Bhi: Largest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative first ionization potential
* SpMax3_Bhi: Largest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative first ionization potential
* SpMax4_Bhi: Largest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative first ionization potential
* SpMax5_Bhi: Largest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative first ionization potential
* SpMax6_Bhi: Largest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative first ionization potential
* SpMax7_Bhi: Largest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative first ionization potential
* SpMax8_Bhi: Largest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative first ionization potential
* SpMin1_Bhi: Smallest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative first ionization potential
* SpMin2_Bhi: Smallest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative first ionization potential
* SpMin3_Bhi: Smallest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative first ionization potential
* SpMin4_Bhi: Smallest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative first ionization potential
* SpMin5_Bhi: Smallest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative first ionization potential
* SpMin6_Bhi: Smallest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative first ionization potential
* SpMin7_Bhi: Smallest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative first ionization potential
* SpMin8_Bhi: Smallest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative first ionization potential
* SpMax1_Bhs: Largest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative I-state
* SpMax2_Bhs: Largest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative I-state
* SpMax3_Bhs: Largest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative I-state
* SpMax4_Bhs: Largest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative I-state
* SpMax5_Bhs: Largest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative I-state
* SpMax6_Bhs: Largest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative I-state
* SpMax7_Bhs: Largest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative I-state
* SpMax8_Bhs: Largest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative I-state
* SpMin1_Bhs: Smallest absolute eigenvalue of Burden modified matrix - n 1 / weighted by relative I-state
* SpMin2_Bhs: Smallest absolute eigenvalue of Burden modified matrix - n 2 / weighted by relative I-state
* SpMin3_Bhs: Smallest absolute eigenvalue of Burden modified matrix - n 3 / weighted by relative I-state
* SpMin4_Bhs: Smallest absolute eigenvalue of Burden modified matrix - n 4 / weighted by relative I-state
* SpMin5_Bhs: Smallest absolute eigenvalue of Burden modified matrix - n 5 / weighted by relative I-state
* SpMin6_Bhs: Smallest absolute eigenvalue of Burden modified matrix - n 6 / weighted by relative I-state
* SpMin7_Bhs: Smallest absolute eigenvalue of Burden modified matrix - n 7 / weighted by relative I-state
* SpMin8_Bhs: Smallest absolute eigenvalue of Burden modified matrix - n 8 / weighted by relative I-state

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_CPSA

CPSA 3D PaDEL descriptor

The following features are calculated:

* PPSA-1: Partial positive surface area -- sum of surface area on positive parts of molecule
* PPSA-2: Partial positive surface area * total positive charge on the molecule 
* PPSA-3: Charge weighted partial positive surface area
* PNSA-1: Partial negative surface area -- sum of surface area on negative parts of molecule
* PNSA-2: Partial negative surface area * total negative charge on the molecule
* PNSA-3: Charge weighted partial negative surface area
* DPSA-1: Difference of PPSA-1 and PNSA-1
* DPSA-2: Difference of FPSA-2 and PNSA-2
* DPSA-3: Difference of PPSA-3 and PNSA-3
* FPSA-1: PPSA-1 / total molecular surface area
* FPSA-2: PPSA-2 / total molecular surface area
* FPSA-3: PPSA-3 / total molecular surface area
* FNSA-1: PNSA-1 / total molecular surface area
* FNSA-2: PNSA-2 / total molecular surface area
* FNSA-3: PNSA-3 / total molecular surface area
* WPSA-1: PPSA-1 * total molecular surface area / 1000
* WPSA-2: PPSA-2 * total molecular surface area /1000
* WPSA-3: PPSA-3 * total molecular surface area / 1000
* WNSA-1: PNSA-1 * total molecular surface area /1000
* WNSA-2: PNSA-2 * total molecular surface area / 1000
* WNSA-3: PNSA-3 * total molecular surface area / 1000
* RPCG: Relative positive charge -- most positive charge / total positive charge
* RNCG: Relative negative charge -- most negative charge / total negative charge
* RPCS: Relative positive charge surface area -- most positive surface area * RPCG
* RNCS: Relative negative charge surface area -- most negative surface area * RNCG
* THSA: Sum of solvent accessible surface areas of atoms with absolute value of partial charges less than 0.2 
* TPSA: Sum of solvent accessible surface areas of atoms with absolute value of partial charges greater than or equal 0.2 
* RHSA: THSA / total molecular surface area 
* RPSA: TPSA / total molecular surface area 

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_CarbonTypes

CarbonTypes PaDEL descriptor

The following features are calculated:

* C1SP1: Triply bound carbon bound to one other carbon 
* C2SP1: Triply bound carbon bound to two other carbons 
* C1SP2: Doubly bound carbon bound to one other carbon 
* C2SP2: Doubly bound carbon bound to two other carbons 
* C3SP2: Doubly bound carbon bound to three other carbons 
* C1SP3: Singly bound carbon bound to one other carbon 
* C2SP3: Singly bound carbon bound to two other carbons 
* C3SP3: Singly bound carbon bound to three other carbons 
* C4SP3: Singly bound carbon bound to four other carbons 

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_ChiChain

ChiChain PaDEL descriptor

The following features are calculated:

* SCH-3: Simple chain, order 3
* SCH-4: Simple chain, order 4
* SCH-5: Simple chain, order 5
* SCH-6: Simple chain, order 6
* SCH-7: Simple chain, order 7
* VCH-3: Valence chain, order 3
* VCH-4: Valence chain, order 4
* VCH-5: Valence chain, order 5
* VCH-6: Valence chain, order 6
* VCH-7: Valence chain, order 7

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_ChiCluster

ChiCluster PaDEL descriptor

The following features are calculated:

* SC-3: Simple cluster, order 3
* SC-4: Simple cluster, order 4
* SC-5: Simple cluster, order 5
* SC-6: Simple cluster, order 6
* VC-3: Valence cluster, order 3
* VC-4: Valence cluster, order 4
* VC-5: Valence cluster, order 5
* VC-6: Valence cluster, order 6

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_ChiPath

ChiPath PaDEL descriptor

The following features are calculated:

* SP-0: Simple path, order 0
* SP-1: Simple path, order 1
* SP-2: Simple path, order 2
* SP-3: Simple path, order 3
* SP-4: Simple path, order 4
* SP-5: Simple path, order 5
* SP-6: Simple path, order 6
* SP-7: Simple path, order 7
* ASP-0: Average simple path, order 0
* ASP-1: Average simple path, order 1
* ASP-2: Average simple path, order 2
* ASP-3: Average simple path, order 3
* ASP-4: Average simple path, order 4
* ASP-5: Average simple path, order 5
* ASP-6: Average simple path, order 6
* ASP-7: Average simple path, order 7
* VP-0: Valence path, order 0
* VP-1: Valence path, order 1
* VP-2: Valence path, order 2
* VP-3: Valence path, order 3
* VP-4: Valence path, order 4
* VP-5: Valence path, order 5
* VP-6: Valence path, order 6
* VP-7: Valence path, order 7
* AVP-0: Average valence path, order 0
* AVP-1: Average valence path, order 1
* AVP-2: Average valence path, order 2
* AVP-3: Average valence path, order 3
* AVP-4: Average valence path, order 4
* AVP-5: Average valence path, order 5
* AVP-6: Average valence path, order 6
* AVP-7: Average valence path, order 7

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_ChiPathCluster

ChiPathCluster PaDEL descriptor

The following features are calculated:

* SPC-4: Simple path cluster, order 4
* SPC-5: Simple path cluster, order 5
* SPC-6: Simple path cluster, order 6
* VPC-4: Valence path cluster, order 4
* VPC-5: Valence path cluster, order 5
* VPC-6: Valence path cluster, order 6

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_Constitutional

Constitutional PaDEL descriptor

The following features are calculated:

* Sv: Sum of atomic van der Waals volumes (scaled on carbon atom)
* Sse: Sum of atomic Sanderson electronegativities (scaled on carbon atom)
* Spe: Sum of atomic Pauling electronegativities (scaled on carbon atom)
* Sare: Sum of atomic Allred-Rochow electronegativities (scaled on carbon atom)
* Sp: Sum of atomic polarizabilities (scaled on carbon atom)
* Si: Sum of first first ionization potentials (scaled on carbon atom)
* Mv: Mean atomic van der Waals volumes (scaled on carbon atom)
* Mse: Mean atomic Sanderson electronegativities (scaled on carbon atom)
* Mpe: Mean atomic Pauling electronegativities (scaled on carbon atom)
* Mare: Mean atomic Allred-Rochow electronegativities (scaled on carbon atom)
* Mp: Mean atomic polarizabilities (scaled on carbon atom)
* Mi: Mean first first ionization potentials (scaled on carbon atom)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_Crippen

Crippen PaDEL descriptor

The following features are calculated:

* CrippenLogP: Crippen's LogP
* CrippenMR: Crippen's molar refractivity

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_DetourMatrix

DetourMatrix PaDEL descriptor

The following features are calculated:

* SpMax_Dt: Leading eigenvalue from detour matrix
* SpDiam_Dt: Spectral diameter from detour matrix
* SpAD_Dt: Spectral absolute deviation from detour matrix
* SpMAD_Dt: Spectral mean absolute deviation from detour matrix
* EE_Dt: Estrada-like index from detour matrix
* VE1_Dt: Coefficient sum of the last eigenvector from detour matrix
* VE2_Dt: Average coefficient sum of the last eigenvector from detour matrix
* VE3_Dt: Logarithmic coefficient sum of the last eigenvector from detour matrix
* VR1_Dt: Randic-like eigenvector-based index from detour matrix
* VR2_Dt: Normalized Randic-like eigenvector-based index from detour matrix
* VR3_Dt: Logarithmic Randic-like eigenvector-based index from detour matrix

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_EStateFP

PaDEL EStateFPfingerprint

Estate fingerprint - E-State fragments

* Number of bits: 79
* Bit prefix: EStateFP


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_EccentricConnectivityIndex

EccentricConnectivityIndex PaDEL descriptor

The following features are calculated:

* ECCEN: A topological descriptor combining distance and adjacency information

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_ElectrotopologicalStateAtomType

ElectrotopologicalStateAtomType PaDEL descriptor

The following features are calculated:

* nHBd: Count of E-States for (strong) Hydrogen Bond donors
* nwHBd: Count of E-States for weak Hydrogen Bond donors
* nHBa: Count of E-States for (strong) Hydrogen Bond acceptors
* nwHBa: Count of E-States for weak Hydrogen Bond acceptors
* nHBint2: Count of E-State descriptors of strength for potential Hydrogen Bonds of path length 2
* nHBint3: Count of E-State descriptors of strength for potential Hydrogen Bonds of path length 3
* nHBint4: Count of E-State descriptors of strength for potential Hydrogen Bonds of path length 4
* nHBint5: Count of E-State descriptors of strength for potential Hydrogen Bonds of path length 5
* nHBint6: Count of E-State descriptors of strength for potential Hydrogen Bonds of path length 6
* nHBint7: Count of E-State descriptors of strength for potential Hydrogen Bonds of path length 7
* nHBint8: Count of E-State descriptors of strength for potential Hydrogen Bonds of path length 8
* nHBint9: Count of E-State descriptors of strength for potential Hydrogen Bonds of path length 9
* nHBint10: Count of E-State descriptors of strength for potential Hydrogen Bonds of path length 10
* nHsOH: Count of atom-type H E-State: -OH
* nHdNH: Count of atom-type H E-State: =NH
* nHsSH: Count of atom-type H E-State: -SH
* nHsNH2: Count of atom-type H E-State: -NH2
* nHssNH: Count of atom-type H E-State: -NH-
* nHaaNH: Count of atom-type H E-State: :NH:
* nHsNH3p: Count of atom-type H E-State: -NH3+
* nHssNH2p: Count of atom-type H E-State: -NH2-+
* nHsssNHp: Count of atom-type H E-State: >NH-+
* nHtCH: Count of atom-type H E-State: #CH
* nHdCH2: Count of atom-type H E-State: =CH2
* nHdsCH: Count of atom-type H E-State: =CH-
* nHaaCH: Count of atom-type H E-State: :CH:
* nHCHnX: Count of atom-type H E-State: CHnX
* nHCsats: Count of atom-type H E-State: H bonded to B, Si, P, Ge, As, Se, Sn or Pb
* nHCsatu: Count of atom-type H E-State: H on C sp3 bonded to unsaturated C
* nHAvin: Count of atom-type H E-State: H on C vinyl bonded to C aromatic
* nHother: Count of atom-type H E-State: H on aaCH, dCH2 or dsCH
* nHmisc: Count of atom-type H E-State: H bonded to B, Si, P, Ge, As, Se, Sn or Pb
* nsLi: Count of atom-type E-State: -Li
* nssBe: Count of atom-type E-State: -Be-
* nssssBem: Count of atom-type E-State: >Be<-2
* nsBH2: Count of atom-type E-State: -BH2
* nssBH: Count of atom-type E-State: -BH-
* nsssB: Count of atom-type E-State: -B<
* nssssBm: Count of atom-type E-State: >B<-
* nsCH3: Count of atom-type E-State: -CH3
* ndCH2: Count of atom-type E-State: =CH2
* nssCH2: Count of atom-type E-State: -CH2-
* ntCH: Count of atom-type E-State: #CH
* ndsCH: Count of atom-type E-State: =CH-
* naaCH: Count of atom-type E-State: :CH:
* nsssCH: Count of atom-type E-State: >CH-
* nddC: Count of atom-type E-State: =C=
* ntsC: Count of atom-type E-State: #C-
* ndssC: Count of atom-type E-State: =C<
* naasC: Count of atom-type E-State: :C:-
* naaaC: Count of atom-type E-State: ::C:
* nssssC: Count of atom-type E-State: >C<
* nsNH3p: Count of atom-type E-State: -NH3+
* nsNH2: Count of atom-type E-State: -NH2
* nssNH2p: Count of atom-type E-State: -NH2-+
* ndNH: Count of atom-type E-State: =NH
* nssNH: Count of atom-type E-State: -NH-
* naaNH: Count of atom-type E-State: :NH:
* ntN: Count of atom-type E-State: #N
* nsssNHp: Count of atom-type E-State: >NH-+
* ndsN: Count of atom-type E-State: =N-
* naaN: Count of atom-type E-State: :N:
* nsssN: Count of atom-type E-State: >N-
* nddsN: Count of atom-type E-State: -N<<
* naasN: Count of atom-type E-State: :N:-
* nssssNp: Count of atom-type E-State: >N<+
* nsOH: Count of atom-type E-State: -OH
* ndO: Count of atom-type E-State: =O
* nssO: Count of atom-type E-State: -O-
* naaO: Count of atom-type E-State: :O:
* naOm: Count of atom-type E-State: :O-0.5
* nsOm: Count of atom-type E-State: -O-
* nsF: Count of atom-type E-State: -F
* nsSiH3: Count of atom-type E-State: -SiH3
* nssSiH2: Count of atom-type E-State: -SiH2-
* nsssSiH: Count of atom-type E-State: >SiH-
* nssssSi: Count of atom-type E-State: >Si<
* nsPH2: Count of atom-type E-State: -PH2
* nssPH: Count of atom-type E-State: -PH-
* nsssP: Count of atom-type E-State: >P-
* ndsssP: Count of atom-type E-State: ->P=
* nddsP: Count of atom-type E-State: -=P=
* nsssssP: Count of atom-type E-State: ->P<
* nsSH: Count of atom-type E-State: -SH
* ndS: Count of atom-type E-State: =S
* nssS: Count of atom-type E-State: -S-
* naaS: Count of atom-type E-State: aSa
* ndssS: Count of atom-type E-State: >S=
* nddssS: Count of atom-type E-State: >S==
* nssssssS: Count of atom-type E-State: >S<<
* nSm: Count of atom-type E-State: -S-
* nsCl: Count of atom-type E-State: -Cl
* nsGeH3: Count of atom-type E-State: -GeH3
* nssGeH2: Count of atom-type E-State: -GeH2-
* nsssGeH: Count of atom-type E-State: >GeH-
* nssssGe: Count of atom-type E-State: >Ge<
* nsAsH2: Count of atom-type E-State: -AsH2
* nssAsH: Count of atom-type E-State: -AsH-
* nsssAs: Count of atom-type E-State: >As-
* ndsssAs: Count of atom-type E-State: ->As=
* nddsAs: Count of atom-type E-State: -=As=
* nsssssAs: Count of atom-type E-State: ->As<
* nsSeH: Count of atom-type E-State: -SeH
* ndSe: Count of atom-type E-State: =Se
* nssSe: Count of atom-type E-State: -Se-
* naaSe: Count of atom-type E-State: aSea
* ndssSe: Count of atom-type E-State: >Se=
* nssssssSe: Count of atom-type E-State: >Se<<
* nddssSe: Count of atom-type E-State: -=Se=-
* nsBr: Count of atom-type E-State: -Br
* nsSnH3: Count of atom-type E-State: -SnH3
* nssSnH2: Count of atom-type E-State: -SnH2-
* nsssSnH: Count of atom-type E-State: >SnH-
* nssssSn: Count of atom-type E-State: >Sn<
* nsI: Count of atom-type E-State: -I
* nsPbH3: Count of atom-type E-State: -PbH3
* nssPbH2: Count of atom-type E-State: -PbH2-
* nsssPbH: Count of atom-type E-State: >PbH-
* nssssPb: Count of atom-type E-State: >Pb<
* SHBd: Sum of E-States for (strong) hydrogen bond donors
* SwHBd: Sum of E-States for weak hydrogen bond donors
* SHBa: Sum of E-States for (strong) hydrogen bond acceptors
* SwHBa: Sum of E-States for weak hydrogen bond acceptors
* SHBint2: Sum of E-State descriptors of strength for potential hydrogen bonds of path length 2
* SHBint3: Sum of E-State descriptors of strength for potential hydrogen bonds of path length 3
* SHBint4: Sum of E-State descriptors of strength for potential hydrogen bonds of path length 4
* SHBint5: Sum of E-State descriptors of strength for potential hydrogen bonds of path length 5
* SHBint6: Sum of E-State descriptors of strength for potential hydrogen bonds of path length 6
* SHBint7: Sum of E-State descriptors of strength for potential hydrogen bonds of path length 7
* SHBint8: Sum of E-State descriptors of strength for potential hydrogen bonds of path length 8
* SHBint9: Sum of E-State descriptors of strength for potential hydrogen bonds of path length 9
* SHBint10: Sum of E-State descriptors of strength for potential hydrogen bonds of path length 10
* SHsOH: Sum of atom-type H E-State: -OH
* SHdNH: Sum of atom-type H E-State: =NH
* SHsSH: Sum of atom-type H E-State: -SH
* SHsNH2: Sum of atom-type H E-State: -NH2
* SHssNH: Sum of atom-type H E-State: -NH-
* SHaaNH: Sum of atom-type H E-State: :NH:
* SHsNH3p: Sum of atom-type H E-State: -NH3+
* SHssNH2p: Sum of atom-type H E-State: -NH2-+
* SHsssNHp: Sum of atom-type H E-State: >NH-+
* SHtCH: Sum of atom-type H E-State: #CH
* SHdCH2: Sum of atom-type H E-State: =CH2
* SHdsCH: Sum of atom-type H E-State: =CH-
* SHaaCH: Sum of atom-type H E-State: :CH:
* SHCHnX: Sum of atom-type H E-State: CHnX
* SHCsats: Sum of atom-type H E-State: H on C sp3 bonded to saturated C
* SHCsatu: Sum of atom-type H E-State: H on C sp3 bonded to unsaturated C
* SHAvin: Sum of atom-type H E-State: H on C vinyl bonded to C aromatic
* SHother: Sum of atom-type H E-State: H on aaCH, dCH2 or dsCH
* SHmisc: Sum of atom-type H E-State: H bonded to B, Si, P, Ge, As, Se, Sn or Pb
* SsLi: Sum of atom-type E-State: -Li
* SssBe: Sum of atom-type E-State: -Be-
* SssssBem: Sum of atom-type E-State: >Be<-2
* SsBH2: Sum of atom-type E-State: -BH2
* SssBH: Sum of atom-type E-State: -BH-
* SsssB: Sum of atom-type E-State: -B<
* SssssBm: Sum of atom-type E-State: >B<-
* SsCH3: Sum of atom-type E-State: -CH3
* SdCH2: Sum of atom-type E-State: =CH2
* SssCH2: Sum of atom-type E-State: -CH2-
* StCH: Sum of atom-type E-State: #CH
* SdsCH: Sum of atom-type E-State: =CH-
* SaaCH: Sum of atom-type E-State: :CH:
* SsssCH: Sum of atom-type E-State: >CH-
* SddC: Sum of atom-type E-State: =C=
* StsC: Sum of atom-type E-State: #C-
* SdssC: Sum of atom-type E-State: =C<
* SaasC: Sum of atom-type E-State: :C:-
* SaaaC: Sum of atom-type E-State: ::C:
* SssssC: Sum of atom-type E-State: >C<
* SsNH3p: Sum of atom-type E-State: -NH3+
* SsNH2: Sum of atom-type E-State: -NH2
* SssNH2p: Sum of atom-type E-State: -NH2-+
* SdNH: Sum of atom-type E-State: =NH
* SssNH: Sum of atom-type E-State: -NH-
* SaaNH: Sum of atom-type E-State: :NH:
* StN: Sum of atom-type E-State: #N
* SsssNHp: Sum of atom-type E-State: >NH-+
* SdsN: Sum of atom-type E-State: =N-
* SaaN: Sum of atom-type E-State: :N:
* SsssN: Sum of atom-type E-State: >N-
* SddsN: Sum of atom-type E-State: -N<<
* SaasN: Sum of atom-type E-State: :N:-
* SssssNp: Sum of atom-type E-State: >N<+
* SsOH: Sum of atom-type E-State: -OH
* SdO: Sum of atom-type E-State: =O
* SssO: Sum of atom-type E-State: -O-
* SaaO: Sum of atom-type E-State: :O:
* SaOm: Sum of atom-type E-State: :O-0.5
* SsOm: Sum of atom-type E-State: -O-
* SsF: Sum of atom-type E-State: -F
* SsSiH3: Sum of atom-type E-State: -SiH3
* SssSiH2: Sum of atom-type E-State: -SiH2-
* SsssSiH: Sum of atom-type E-State: >SiH-
* SssssSi: Sum of atom-type E-State: >Si<
* SsPH2: Sum of atom-type E-State: -PH2
* SssPH: Sum of atom-type E-State: -PH-
* SsssP: Sum of atom-type E-State: >P-
* SdsssP: Sum of atom-type E-State: ->P=
* SddsP: Sum of atom-type E-State: -=P=
* SsssssP: Sum of atom-type E-State: ->P<
* SsSH: Sum of atom-type E-State: -SH
* SdS: Sum of atom-type E-State: =S
* SssS: Sum of atom-type E-State: -S-
* SaaS: Sum of atom-type E-State: aSa
* SdssS: Sum of atom-type E-State: >S=
* SddssS: Sum of atom-type E-State: >S==
* SssssssS: Sum of atom-type E-State: >S<<
* SSm: Sum of atom-type E-State: -S-
* SsCl: Sum of atom-type E-State: -Cl
* SsGeH3: Sum of atom-type E-State: -GeH3
* SssGeH2: Sum of atom-type E-State: -GeH2-
* SsssGeH: Sum of atom-type E-State: >GeH-
* SssssGe: Sum of atom-type E-State: >Ge<
* SsAsH2: Sum of atom-type E-State: -AsH2
* SssAsH: Sum of atom-type E-State: -AsH-
* SsssAs: Sum of atom-type E-State: >As-
* SdsssAs: Sum of atom-type E-State: ->As=
* SddsAs: Sum of atom-type E-State: -=As=
* SsssssAs: Sum of atom-type E-State: ->As<
* SsSeH: Sum of atom-type E-State: -SeH
* SdSe: Sum of atom-type E-State: =Se
* SssSe: Sum of atom-type E-State: -Se-
* SaaSe: Sum of atom-type E-State: aSea
* SdssSe: Sum of atom-type E-State: >Se=
* SssssssSe: Sum of atom-type E-State: >Se<<
* SddssSe: Sum of atom-type E-State: -=Se=-
* SsBr: Sum of atom-type E-State: -Br
* SsSnH3: Sum of atom-type E-State: -SnH3
* SssSnH2: Sum of atom-type E-State: -SnH2-
* SsssSnH: Sum of atom-type E-State: >SnH-
* SssssSn: Sum of atom-type E-State: >Sn<
* SsI: Sum of atom-type E-State: -I
* SsPbH3: Sum of atom-type E-State: -PbH3
* SssPbH2: Sum of atom-type E-State: -PbH2-
* SsssPbH: Sum of atom-type E-State: >PbH-
* SssssPb: Sum of atom-type E-State: >Pb<
* minHBd: Minimum E-States for (strong) Hydrogen Bond donors
* minwHBd: Minimum E-States for weak Hydrogen Bond donors
* minHBa: Minimum E-States for (strong) Hydrogen Bond acceptors
* minwHBa: Minimum E-States for weak Hydrogen Bond acceptors
* minHBint2: Minimum E-State descriptors of strength for potential Hydrogen Bonds of path length 2
* minHBint3: Minimum E-State descriptors of strength for potential Hydrogen Bonds of path length 3
* minHBint4: Minimum E-State descriptors of strength for potential Hydrogen Bonds of path length 4
* minHBint5: Minimum E-State descriptors of strength for potential Hydrogen Bonds of path length 5
* minHBint6: Minimum E-State descriptors of strength for potential Hydrogen Bonds of path length 6
* minHBint7: Minimum E-State descriptors of strength for potential Hydrogen Bonds of path length 7
* minHBint8: Minimum E-State descriptors of strength for potential Hydrogen Bonds of path length 8
* minHBint9: Minimum E-State descriptors of strength for potential Hydrogen Bonds of path length 9
* minHBint10: Minimum E-State descriptors of strength for potential Hydrogen Bonds of path length 10
* minHsOH: Minimum atom-type H E-State: -OH
* minHdNH: Minimum atom-type H E-State: =NH
* minHsSH: Minimum atom-type H E-State: -SH
* minHsNH2: Minimum atom-type H E-State: -NH2
* minHssNH: Minimum atom-type H E-State: -NH-
* minHaaNH: Minimum atom-type H E-State: :NH:
* minHsNH3p: Minimum atom-type H E-State: -NH3+
* minHssNH2p: Minimum atom-type H E-State: -NH2-+
* minHsssNHp: Minimum atom-type H E-State: >NH-+
* minHtCH: Minimum atom-type H E-State: #CH
* minHdCH2: Minimum atom-type H E-State: =CH2
* minHdsCH: Minimum atom-type H E-State: =CH-
* minHaaCH: Minimum atom-type H E-State: :CH:
* minHCHnX: Minimum atom-type H E-State: CHnX
* minHCsats: Minimum atom-type H E-State: H bonded to B, Si, P, Ge, As, Se, Sn or Pb
* minHCsatu: Minimum atom-type H E-State: H on C sp3 bonded to unsaturated C
* minHAvin: Minimum atom-type H E-State: H on C vinyl bonded to C aromatic
* minHother: Minimum atom-type H E-State: H on aaCH, dCH2 or dsCH
* minHmisc: Minimum atom-type H E-State: H bonded to B, Si, P, Ge, As, Se, Sn or Pb
* minsLi: Minimum atom-type E-State: -Li
* minssBe: Minimum atom-type E-State: -Be-
* minssssBem: Minimum atom-type E-State: >Be<-2
* minsBH2: Minimum atom-type E-State: -BH2
* minssBH: Minimum atom-type E-State: -BH-
* minsssB: Minimum atom-type E-State: -B<
* minssssBm: Minimum atom-type E-State: >B<-
* minsCH3: Minimum atom-type E-State: -CH3
* mindCH2: Minimum atom-type E-State: =CH2
* minssCH2: Minimum atom-type E-State: -CH2-
* mintCH: Minimum atom-type E-State: #CH
* mindsCH: Minimum atom-type E-State: =CH-
* minaaCH: Minimum atom-type E-State: :CH:
* minsssCH: Minimum atom-type E-State: >CH-
* minddC: Minimum atom-type E-State: =C=
* mintsC: Minimum atom-type E-State: #C-
* mindssC: Minimum atom-type E-State: =C<
* minaasC: Minimum atom-type E-State: :C:-
* minaaaC: Minimum atom-type E-State: ::C:
* minssssC: Minimum atom-type E-State: >C<
* minsNH3p: Minimum atom-type E-State: -NH3+
* minsNH2: Minimum atom-type E-State: -NH2
* minssNH2p: Minimum atom-type E-State: -NH2-+
* mindNH: Minimum atom-type E-State: =NH
* minssNH: Minimum atom-type E-State: -NH-
* minaaNH: Minimum atom-type E-State: :NH:
* mintN: Minimum atom-type E-State: #N
* minsssNHp: Minimum atom-type E-State: >NH-+
* mindsN: Minimum atom-type E-State: =N-
* minaaN: Minimum atom-type E-State: :N:
* minsssN: Minimum atom-type E-State: >N-
* minddsN: Minimum atom-type E-State: -N<<
* minaasN: Minimum atom-type E-State: :N:-
* minssssNp: Minimum atom-type E-State: >N<+
* minsOH: Minimum atom-type E-State: -OH
* mindO: Minimum atom-type E-State: =O
* minssO: Minimum atom-type E-State: -O-
* minaaO: Minimum atom-type E-State: :O:
* minaOm: Minimum atom-type E-State: :O-0.5
* minsOm: Minimum atom-type E-State: -O-
* minsF: Minimum atom-type E-State: -F
* minsSiH3: Minimum atom-type E-State: -SiH3
* minssSiH2: Minimum atom-type E-State: -SiH2-
* minsssSiH: Minimum atom-type E-State: >SiH-
* minssssSi: Minimum atom-type E-State: >Si<
* minsPH2: Minimum atom-type E-State: -PH2
* minssPH: Minimum atom-type E-State: -PH-
* minsssP: Minimum atom-type E-State: >P-
* mindsssP: Minimum atom-type E-State: ->P=
* minddsP: Minimum atom-type E-State: -=P=
* minsssssP: Minimum atom-type E-State: ->P<
* minsSH: Minimum atom-type E-State: -SH
* mindS: Minimum atom-type E-State: =S
* minssS: Minimum atom-type E-State: -S-
* minaaS: Minimum atom-type E-State: aSa
* mindssS: Minimum atom-type E-State: >S=
* minddssS: Minimum atom-type E-State: >S==
* minssssssS: Minimum atom-type E-State: >S<<
* minSm: Minimum atom-type E-State: -S-
* minsCl: Minimum atom-type E-State: -Cl
* minsGeH3: Minimum atom-type E-State: -GeH3
* minssGeH2: Minimum atom-type E-State: -GeH2-
* minsssGeH: Minimum atom-type E-State: >GeH-
* minssssGe: Minimum atom-type E-State: >Ge<
* minsAsH2: Minimum atom-type E-State: -AsH2
* minssAsH: Minimum atom-type E-State: -AsH-
* minsssAs: Minimum atom-type E-State: >As-
* mindsssAs: Minimum atom-type E-State: ->As=
* minddsAs: Minimum atom-type E-State: -=As=
* minsssssAs: Minimum atom-type E-State: ->As<
* minsSeH: Minimum atom-type E-State: -SeH
* mindSe: Minimum atom-type E-State: =Se
* minssSe: Minimum atom-type E-State: -Se-
* minaaSe: Minimum atom-type E-State: aSea
* mindssSe: Minimum atom-type E-State: >Se=
* minssssssSe: Minimum atom-type E-State: >Se<<
* minddssSe: Minimum atom-type E-State: -=Se=-
* minsBr: Minimum atom-type E-State: -Br
* minsSnH3: Minimum atom-type E-State: -SnH3
* minssSnH2: Minimum atom-type E-State: -SnH2-
* minsssSnH: Minimum atom-type E-State: >SnH-
* minssssSn: Minimum atom-type E-State: >Sn<
* minsI: Minimum atom-type E-State: -I
* minsPbH3: Minimum atom-type E-State: -PbH3
* minssPbH2: Minimum atom-type E-State: -PbH2-
* minsssPbH: Minimum atom-type E-State: >PbH-
* minssssPb: Minimum atom-type E-State: >Pb<
* maxHBd: Maximum E-States for (strong) Hydrogen Bond donors
* maxwHBd: Maximum E-States for weak Hydrogen Bond donors
* maxHBa: Maximum E-States for (strong) Hydrogen Bond acceptors
* maxwHBa: Maximum E-States for weak Hydrogen Bond acceptors
* maxHBint2: Maximum E-State descriptors of strength for potential Hydrogen Bonds of path length 2
* maxHBint3: Maximum E-State descriptors of strength for potential Hydrogen Bonds of path length 3
* maxHBint4: Maximum E-State descriptors of strength for potential Hydrogen Bonds of path length 4
* maxHBint5: Maximum E-State descriptors of strength for potential Hydrogen Bonds of path length 5
* maxHBint6: Maximum E-State descriptors of strength for potential Hydrogen Bonds of path length 6
* maxHBint7: Maximum E-State descriptors of strength for potential Hydrogen Bonds of path length 7
* maxHBint8: Maximum E-State descriptors of strength for potential Hydrogen Bonds of path length 8
* maxHBint9: Maximum E-State descriptors of strength for potential Hydrogen Bonds of path length 9
* maxHBint10: Maximum E-State descriptors of strength for potential Hydrogen Bonds of path length 10
* maxHsOH: Maximum atom-type H E-State: -OH
* maxHdNH: Maximum atom-type H E-State: =NH
* maxHsSH: Maximum atom-type H E-State: -SH
* maxHsNH2: Maximum atom-type H E-State: -NH2
* maxHssNH: Maximum atom-type H E-State: -NH-
* maxHaaNH: Maximum atom-type H E-State: :NH:
* maxHsNH3p: Maximum atom-type H E-State: -NH3+
* maxHssNH2p: Maximum atom-type H E-State: -NH2-+
* maxHsssNHp: Maximum atom-type H E-State: >NH-+
* maxHtCH: Maximum atom-type H E-State: #CH
* maxHdCH2: Maximum atom-type H E-State: =CH2
* maxHdsCH: Maximum atom-type H E-State: =CH-
* maxHaaCH: Maximum atom-type H E-State: :CH:
* maxHCHnX: Maximum atom-type H E-State: CHnX
* maxHCsats: Maximum atom-type H E-State: H bonded to B, Si, P, Ge, As, Se, Sn or Pb
* maxHCsatu: Maximum atom-type H E-State: H on C sp3 bonded to unsaturated C
* maxHAvin: Maximum atom-type H E-State: H on C vinyl bonded to C aromatic
* maxHother: Maximum atom-type H E-State: H on aaCH, dCH2 or dsCH
* maxHmisc: Maximum atom-type H E-State: H bonded to B, Si, P, Ge, As, Se, Sn or Pb
* maxsLi: Maximum atom-type E-State: -Li
* maxssBe: Maximum atom-type E-State: -Be-
* maxssssBem: Maximum atom-type E-State: >Be<-2
* maxsBH2: Maximum atom-type E-State: -BH2
* maxssBH: Maximum atom-type E-State: -BH-
* maxsssB: Maximum atom-type E-State: -B<
* maxssssBm: Maximum atom-type E-State: >B<-
* maxsCH3: Maximum atom-type E-State: -CH3
* maxdCH2: Maximum atom-type E-State: =CH2
* maxssCH2: Maximum atom-type E-State: -CH2-
* maxtCH: Maximum atom-type E-State: #CH
* maxdsCH: Maximum atom-type E-State: =CH-
* maxaaCH: Maximum atom-type E-State: :CH:
* maxsssCH: Maximum atom-type E-State: >CH-
* maxddC: Maximum atom-type E-State: =C=
* maxtsC: Maximum atom-type E-State: #C-
* maxdssC: Maximum atom-type E-State: =C<
* maxaasC: Maximum atom-type E-State: :C:-
* maxaaaC: Maximum atom-type E-State: ::C:
* maxssssC: Maximum atom-type E-State: >C<
* maxsNH3p: Maximum atom-type E-State: -NH3+
* maxsNH2: Maximum atom-type E-State: -NH2
* maxssNH2p: Maximum atom-type E-State: -NH2-+
* maxdNH: Maximum atom-type E-State: =NH
* maxssNH: Maximum atom-type E-State: -NH-
* maxaaNH: Maximum atom-type E-State: :NH:
* maxtN: Maximum atom-type E-State: #N
* maxsssNHp: Maximum atom-type E-State: >NH-+
* maxdsN: Maximum atom-type E-State: =N-
* maxaaN: Maximum atom-type E-State: :N:
* maxsssN: Maximum atom-type E-State: >N-
* maxddsN: Maximum atom-type E-State: -N<<
* maxaasN: Maximum atom-type E-State: :N:-
* maxssssNp: Maximum atom-type E-State: >N<+
* maxsOH: Maximum atom-type E-State: -OH
* maxdO: Maximum atom-type E-State: =O
* maxssO: Maximum atom-type E-State: -O-
* maxaaO: Maximum atom-type E-State: :O:
* maxaOm: Maximum atom-type E-State: :O-0.5
* maxsOm: Maximum atom-type E-State: -O-
* maxsF: Maximum atom-type E-State: -F
* maxsSiH3: Maximum atom-type E-State: -SiH3
* maxssSiH2: Maximum atom-type E-State: -SiH2-
* maxsssSiH: Maximum atom-type E-State: >SiH-
* maxssssSi: Maximum atom-type E-State: >Si<
* maxsPH2: Maximum atom-type E-State: -PH2
* maxssPH: Maximum atom-type E-State: -PH-
* maxsssP: Maximum atom-type E-State: >P-
* maxdsssP: Maximum atom-type E-State: ->P=
* maxddsP: Maximum atom-type E-State: -=P=
* maxsssssP: Maximum atom-type E-State: ->P<
* maxsSH: Maximum atom-type E-State: -SH
* maxdS: Maximum atom-type E-State: =S
* maxssS: Maximum atom-type E-State: -S-
* maxaaS: Maximum atom-type E-State: aSa
* maxdssS: Maximum atom-type E-State: >S=
* maxddssS: Maximum atom-type E-State: >S==
* maxssssssS: Maximum atom-type E-State: >S<<
* maxSm: Maximum atom-type E-State: -S-
* maxsCl: Maximum atom-type E-State: -Cl
* maxsGeH3: Maximum atom-type E-State: -GeH3
* maxssGeH2: Maximum atom-type E-State: -GeH2-
* maxsssGeH: Maximum atom-type E-State: >GeH-
* maxssssGe: Maximum atom-type E-State: >Ge<
* maxsAsH2: Maximum atom-type E-State: -AsH2
* maxssAsH: Maximum atom-type E-State: -AsH-
* maxsssAs: Maximum atom-type E-State: >As-
* maxdsssAs: Maximum atom-type E-State: ->As=
* maxddsAs: Maximum atom-type E-State: -=As=
* maxsssssAs: Maximum atom-type E-State: ->As<
* maxsSeH: Maximum atom-type E-State: -SeH
* maxdSe: Maximum atom-type E-State: =Se
* maxssSe: Maximum atom-type E-State: -Se-
* maxaaSe: Maximum atom-type E-State: aSea
* maxdssSe: Maximum atom-type E-State: >Se=
* maxssssssSe: Maximum atom-type E-State: >Se<<
* maxddssSe: Maximum atom-type E-State: -=Se=-
* maxsBr: Maximum atom-type E-State: -Br
* maxsSnH3: Maximum atom-type E-State: -SnH3
* maxssSnH2: Maximum atom-type E-State: -SnH2-
* maxsssSnH: Maximum atom-type E-State: >SnH-
* maxssssSn: Maximum atom-type E-State: >Sn<
* maxsI: Maximum atom-type E-State: -I
* maxsPbH3: Maximum atom-type E-State: -PbH3
* maxssPbH2: Maximum atom-type E-State: -PbH2-
* maxsssPbH: Maximum atom-type E-State: >PbH-
* maxssssPb: Maximum atom-type E-State: >Pb<
* sumI: Sum of the intrinsic state values I
* meanI: Mean intrinsic state values I
* hmax: Maximum H E-State
* gmax: Maximum E-State
* hmin: Minimum H E-State
* gmin: Minimum E-State
* LipoaffinityIndex: Lipoaffinity index
* MAXDN: Maximum negative intrinsic state di?fference in the molecule (related to the nucleophilicity of the molecule). Using deltaV = (Zv-maxBondedHydrogens) /(atomicNumber-Zv-1). Gramatica, P., Corradi, M., and Consonni, V. (2000). Modelling and prediction of soil sorption coefficients of non-ionic organic pesticides by molecular descriptors. Chemosphere 41, 763-777.
* MAXDP: Maximum positive intrinsic state di?fference in the molecule (related to the electrophilicity of the molecule).  Using deltaV = (Zv-maxBondedHydrogens) /(atomicNumber-Zv-1). Gramatica, P., Corradi, M., and Consonni, V. (2000). Modelling and prediction of soil sorption coefficients of non-ionic organic pesticides by molecular descriptors. Chemosphere 41, 763-777.
* DELS: Sum of all atoms intrinsic state differences (measure of total charge transfer in the molecule).  Using deltaV = (Zv-maxBondedHydrogens) /(atomicNumber-Zv-1). Gramatica, P., Corradi, M., and Consonni, V. (2000). Modelling and prediction of soil sorption coefficients of non-ionic organic pesticides by molecular descriptors. Chemosphere 41, 763-777.
* MAXDN2: Maximum negative intrinsic state di?fference in the molecule (related to the nucleophilicity of the molecule). Using deltaV = Zv-maxBondedHydrogens. Gramatica, P., Corradi, M., and Consonni, V. (2000). Modelling and prediction of soil sorption coefficients of non-ionic organic pesticides by molecular descriptors. Chemosphere 41, 763-777.
* MAXDP2: Maximum positive intrinsic state di?fference in the molecule (related to the electrophilicity of the molecule). Using deltaV = Zv-maxBondedHydrogens. Gramatica, P., Corradi, M., and Consonni, V. (2000). Modelling and prediction of soil sorption coefficients of non-ionic organic pesticides by molecular descriptors. Chemosphere 41, 763-777.
* DELS2: Sum of all atoms intrinsic state differences (measure of total charge transfer in the molecule). Using deltaV = Zv-maxBondedHydrogens. Gramatica, P., Corradi, M., and Consonni, V. (2000). Modelling and prediction of soil sorption coefficients of non-ionic organic pesticides by molecular descriptors. Chemosphere 41, 763-777.

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_ExtFP

PaDEL ExtFPfingerprint

CDK extended fingerprint - Extends the Fingerprinter with additional bits
describing ring features

* Number of bits: 1024
* Bit prefix: ExtFP


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_ExtendedTopochemicalAtom

ExtendedTopochemicalAtom PaDEL descriptor

The following features are calculated:

* ETA_Alpha: Sum of alpha values of all non-hydrogen vertices of a molecule
* ETA_AlphaP: Sum of alpha values of all non-hydrogen vertices of a molecule relative to molecular size
* ETA_dAlpha_A: A measure of count of non-hydrogen heteroatoms
* ETA_dAlpha_B: A measure of count of hydrogen bond acceptor atoms and/or polar surface area
* ETA_Epsilon_1: A measure of electronegative atom count
* ETA_Epsilon_2: A measure of electronegative atom count
* ETA_Epsilon_3: A measure of electronegative atom count
* ETA_Epsilon_4: A measure of electronegative atom count
* ETA_Epsilon_5: A measure of electronegative atom count
* ETA_dEpsilon_A: A measure of contribution of unsaturation and electronegative atom count
* ETA_dEpsilon_B: A measure of contribution of unsaturation
* ETA_dEpsilon_C: A measure of contribution of electronegativity
* ETA_dEpsilon_D: A measure of contribution of hydrogen bond donor atoms
* ETA_Psi_1: A measure of hydrogen bonding propensity of the molecules and/or polar surface area
* ETA_dPsi_A: A measure of hydrogen bonding propensity of the molecules
* ETA_dPsi_B: A measure of hydrogen bonding propensity of the molecules
* ETA_Shape_P: Shape index P
* ETA_Shape_Y: Shape index Y
* ETA_Shape_X: Shape index X
* ETA_Beta: A measure of electronic features of the molecule
* ETA_BetaP: A measure of electronic features of the molecule relative to molecular size
* ETA_Beta_s: A measure of electronegative atom count of the molecule
* ETA_BetaP_s: A measure of electronegative atom count of the molecule relative to molecular size
* ETA_Beta_ns: A measure of electron-richness of the molecule
* ETA_BetaP_ns: A measure of electron-richness of the molecule relative to molecular size
* ETA_dBeta: A measure of relative unsaturation content
* ETA_dBetaP: A measure of relative unsaturation content relative to molecular size
* ETA_Beta_ns_d: A measure of lone electrons entering into resonance
* ETA_BetaP_ns_d: A measure of lone electrons entering into resonance relative to molecular size
* ETA_Eta: Composite index Eta
* ETA_EtaP: Composite index Eta relative to molecular size
* ETA_Eta_R: Composite index Eta for reference alkane
* ETA_Eta_F: Functionality index EtaF
* ETA_EtaP_F: Functionality index EtaF relative to molecular size
* ETA_Eta_L: Local index Eta_local
* ETA_EtaP_L: Local index Eta_local relative to molecular size
* ETA_Eta_R_L: Local index Eta_local for reference alkane
* ETA_Eta_F_L: Local functionality contribution EtaF_local
* ETA_EtaP_F_L: Local functionality contribution EtaF_local relative to molecular size
* ETA_Eta_B: Branching index EtaB
* ETA_EtaP_B: Branching index EtaB relative to molecular size
* ETA_Eta_B_RC: Branching index EtaB (with ring correction)
* ETA_EtaP_B_RC: Branching index EtaB (with ring correction) relative to molecular size

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_FMF

FMF PaDEL descriptor

The following features are calculated:

* FMF: Complexity of a molecule

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_FP

PaDEL FPfingerprint

CDK fingerprint - Fingerprint of length 1024 and search depth of 8

* Number of bits: nan
* Bit prefix: FP


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_FragmentComplexity

FragmentComplexity PaDEL descriptor

The following features are calculated:

* fragC: Complexity of a system

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_GraphFP

PaDEL GraphFPfingerprint

CDK graph only fingerprint - Specialized version of the Fingerprinter which does
not take bond orders into account

* Number of bits: nan
* Bit prefix: GraphFP


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_GravitationalIndex

GravitationalIndex 3D PaDEL descriptor

The following features are calculated:

* GRAV-1: Gravitational index of heavy atoms 
* GRAV-2: Square root of gravitational index of heavy atoms 
* GRAV-3: Cube root of gravitational index of heavy atoms 
* GRAVH-1: Gravitational index - hydrogens included 
* GRAVH-2: Square root of hydrogen-included gravitational index 
* GRAVH-3: Cube root of hydrogen-included gravitational index 
* GRAV-4: Gravitational index of all pairs of atoms (not just bonded pairs) 
* GRAV-5: Square root of gravitational index of all pairs of atoms (not just bonded pairs) 
* GRAV-6: Cube root of gravitational index of all pairs of atoms (not just bonded pairs) 

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_HBondAcceptorCount

HBondAcceptorCount PaDEL descriptor

The following features are calculated:

* nHBAcc: Number of hydrogen bond acceptors (using CDK HBondAcceptorCountDescriptor algorithm)
* nHBAcc2: Number of hydrogen bond acceptors (any oxygen         any nitrogen where the formal charge of the nitrogen is non-positive (i.e. formal charge <= 0) except a non-aromatic nitrogen that is adjacent to an oxygen and aromatic ring, or an aromatic nitrogen with a hydrogen atom in a ring, or an aromatic nitrogen with 3 neighouring atoms in a ring, or a nitrogen with total bond order >=4      any fluorine)
* nHBAcc3: Number of hydrogen bond acceptors (any oxygen         any nitrogen where the formal charge of the nitrogen is non-positive (i.e. formal charge <= 0) except a non-aromatic nitrogen that is adjacent to an oxygen and aromatic ring, or an aromatic nitrogen with a hydrogen atom in a ring, or an aromatic nitrogen with 3 neighouring atoms in a ring, or a nitrogen with total bond order >=4, or a nitrogen in an amide bond      any fluorine)
* nHBAcc_Lipinski: Number of hydrogen bond acceptors (using Lipinski's definition: any nitrogen  any oxygen)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_HBondDonorCount

HBondDonorCount PaDEL descriptor

The following features are calculated:

* nHBDon: Number of hydrogen bond donors (using CDK HBondDonorCountDescriptor algorithm)
* nHBDon_Lipinski: Number of hydrogen bond donors (using Lipinski's definition: Any OH or NH. Each available hydrogen atom is counted as one hydrogen bond donor)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_HybridizationRatio

HybridizationRatio PaDEL descriptor

The following features are calculated:

* HybRatio: Fraction of sp3 carbons to sp2 carbons

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_InformationContent

InformationContent PaDEL descriptor

The following features are calculated:

* IC0: Information content index (neighborhood symmetry of 0-order)
* IC1: Information content index (neighborhood symmetry of 1-order)
* IC2: Information content index (neighborhood symmetry of 2-order)
* IC3: Information content index (neighborhood symmetry of 3-order)
* IC4: Information content index (neighborhood symmetry of 4-order)
* IC5: Information content index (neighborhood symmetry of 5-order)
* TIC0: Total information content index (neighborhood symmetry of 0-order)
* TIC1: Total information content index (neighborhood symmetry of 1-order)
* TIC2: Total information content index (neighborhood symmetry of 2-order)
* TIC3: Total information content index (neighborhood symmetry of 3-order)
* TIC4: Total information content index (neighborhood symmetry of 4-order)
* TIC5: Total information content index (neighborhood symmetry of 5-order)
* SIC0: Structural information content index (neighborhood symmetry of 0-order)
* SIC1: Structural information content index (neighborhood symmetry of 1-order)
* SIC2: Structural information content index (neighborhood symmetry of 2-order)
* SIC3: Structural information content index (neighborhood symmetry of 3-order)
* SIC4: Structural information content index (neighborhood symmetry of 4-order)
* SIC5: Structural information content index (neighborhood symmetry of 5-order)
* CIC0: Complementary information content index (neighborhood symmetry of 0-order)
* CIC1: Complementary information content index (neighborhood symmetry of 1-order)
* CIC2: Complementary information content index (neighborhood symmetry of 2-order)
* CIC3: Complementary information content index (neighborhood symmetry of 3-order)
* CIC4: Complementary information content index (neighborhood symmetry of 4-order)
* CIC5: Complementary information content index (neighborhood symmetry of 5-order)
* BIC0: Bond information content index (neighborhood symmetry of 0-order)
* BIC1: Bond information content index (neighborhood symmetry of 1-order)
* BIC2: Bond information content index (neighborhood symmetry of 2-order)
* BIC3: Bond information content index (neighborhood symmetry of 3-order)
* BIC4: Bond information content index (neighborhood symmetry of 4-order)
* BIC5: Bond information content index (neighborhood symmetry of 5-order)
* MIC0: Modified information content index (neighborhood symmetry of 0-order)
* MIC1: Modified information content index (neighborhood symmetry of 1-order)
* MIC2: Modified information content index (neighborhood symmetry of 2-order)
* MIC3: Modified information content index (neighborhood symmetry of 3-order)
* MIC4: Modified information content index (neighborhood symmetry of 4-order)
* MIC5: Modified information content index (neighborhood symmetry of 5-order)
* ZMIC0: Z-modified information content index (neighborhood symmetry of 0-order)
* ZMIC1: Z-modified information content index (neighborhood symmetry of 1-order)
* ZMIC2: Z-modified information content index (neighborhood symmetry of 2-order)
* ZMIC3: Z-modified information content index (neighborhood symmetry of 3-order)
* ZMIC4: Z-modified information content index (neighborhood symmetry of 4-order)
* ZMIC5: Z-modified information content index (neighborhood symmetry of 5-order)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_KRFP

PaDEL KRFPfingerprint

Klekota-Roth fingerprint - Presence of chemical substructures

* Number of bits: 4860
* Bit prefix: KRFP


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_KRFPC

PaDEL KRFPCfingerprint

Klekota-Roth fingerprint count - Count of chemical substructures

* Number of bits: 4860
* Bit prefix: KRFPC


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_KappaShapeIndices

KappaShapeIndices PaDEL descriptor

The following features are calculated:

* Kier1: First kappa shape index 
* Kier2: Second kappa shape index 
* Kier3: Third kappa (?) shape index 

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_LargestChain

LargestChain PaDEL descriptor

The following features are calculated:

* nAtomLC: Number of atoms in the largest chain

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_LargestPiSystem

LargestPiSystem PaDEL descriptor

The following features are calculated:

* nAtomP: Number of atoms in the largest pi system

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_LengthOverBreadth

LengthOverBreadth 3D PaDEL descriptor

The following features are calculated:

* LOBMAX: The maximum L/B ratio 
* LOBMIN: The L/B ratio for the rotation that results in the minimum area

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_LongestAliphaticChain

LongestAliphaticChain PaDEL descriptor

The following features are calculated:

* nAtomLAC: Number of atoms in the longest aliphatic chain

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_MACCSFP

PaDEL MACCSFPfingerprint

MACCS fingerprint - MACCS keys

* Number of bits: 166
* Bit prefix: MACCSFP


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_MDE

MDE PaDEL descriptor

The following features are calculated:

* MDEC-11: Molecular distance edge between all primary carbons
* MDEC-12: Molecular distance edge between all primary and secondary carbons
* MDEC-13: Molecular distance edge between all primary and tertiary carbons
* MDEC-14: Molecular distance edge between all primary and quaternary carbons 
* MDEC-22: Molecular distance edge between all secondary carbons 
* MDEC-23: Molecular distance edge between all secondary and tertiary carbons
* MDEC-24: Molecular distance edge between all secondary and quaternary carbons 
* MDEC-33: Molecular distance edge between all tertiary carbons
* MDEC-34: Molecular distance edge between all tertiary and quaternary carbons 
* MDEC-44: Molecular distance edge between all quaternary carbons 
* MDEO-11: Molecular distance edge between all primary oxygens 
* MDEO-12: Molecular distance edge between all primary and secondary oxygens 
* MDEO-22: Molecular distance edge between all secondary oxygens 
* MDEN-11: Molecular distance edge between all primary nitrogens
* MDEN-12: Molecular distance edge between all primary and secondary nitrogens 
* MDEN-13: Molecular distance edge between all primary and tertiary niroqens 
* MDEN-22: Molecular distance edge between all secondary nitroqens 
* MDEN-23: Molecular distance edge between all secondary and tertiary nitrogens 
* MDEN-33: Molecular distance edge between all tertiary nitrogens

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_MLFER

MLFER PaDEL descriptor

The following features are calculated:

* MLFER_A: Overall or summation solute hydrogen bond acidity
* MLFER_BH: Overall or summation solute hydrogen bond basicity
* MLFER_BO: Overall or summation solute hydrogen bond basicity
* MLFER_S: Combined dipolarity/polarizability
* MLFER_E: Excessive molar refraction
* MLFER_L: Solute gas-hexadecane partition coefficient

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_MannholdLogP

MannholdLogP PaDEL descriptor

The following features are calculated:

* MLogP: Mannhold LogP

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_McGowanVolume

McGowanVolume PaDEL descriptor

The following features are calculated:

* McGowan_Volume: McGowan characteristic volume

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_MomentOfInertia

MomentOfInertia 3D PaDEL descriptor

The following features are calculated:

* MOMI-X: Moment of inertia along X axis 
* MOMI-Y: Moment of inertia along Y axis 
* MOMI-Z: Moment of inertia along Z axis 
* MOMI-XY: X/Y 
* MOMI-XZ: X/Z 
* MOMI-YZ: Y/Z 
* MOMI-R: Radius of gyration 

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_PathCount

PathCount PaDEL descriptor

The following features are calculated:

* MPC2: Molecular path count of order 2
* MPC3: Molecular path count of order 3
* MPC4: Molecular path count of order 4
* MPC5: Molecular path count of order 5
* MPC6: Molecular path count of order 6
* MPC7: Molecular path count of order 7
* MPC8: Molecular path count of order 8
* MPC9: Molecular path count of order 9
* MPC10: Molecular path count of order 10
* TPC: Total path count (up to order 10)
* piPC1: Conventional bond order ID number of order 1 (ln(1+x)
* piPC2: Conventional bond order ID number of order 2 (ln(1+x)
* piPC3: Conventional bond order ID number of order 3 (ln(1+x)
* piPC4: Conventional bond order ID number of order 4 (ln(1+x)
* piPC5: Conventional bond order ID number of order 5 (ln(1+x)
* piPC6: Conventional bond order ID number of order 6 (ln(1+x)
* piPC7: Conventional bond order ID number of order 7 (ln(1+x)
* piPC8: Conventional bond order ID number of order 8 (ln(1+x)
* piPC9: Conventional bond order ID number of order 9 (ln(1+x)
* piPC10: Conventional bond order ID number of order 10 (ln(1+x)
* TpiPC: Total conventional bond order (up to order 10) (ln(1+x))
* R_TpiPCTPC: Ratio of total conventional bond order (up to order 10) with total path count (up to order 10)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_PetitjeanNumber

PetitjeanNumber PaDEL descriptor

The following features are calculated:

* PetitjeanNumber: Petitjean number

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_PetitjeanShapeIndex

PetitjeanShapeIndex 3D PaDEL descriptor

The following features are calculated:

* geomRadius: Geometrical radius (minimum geometric eccentricity)
* geomDiameter: Geometrical diameter (maximum geometric eccentricity)
* geomShape: Petitjean geometric shape index 

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_PubchemFP

PaDEL PubchemFPfingerprint

Pubchem fingerprint - Pubchem fingerprint

* Number of bits: 881
* Bit prefix: PubchemFP


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_RDF

RDF 3D PaDEL descriptor

The following features are calculated:

* RDF10u: Radial distribution function - 010 / unweighted
* RDF15u: Radial distribution function - 015 / unweighted
* RDF20u: Radial distribution function - 020 / unweighted
* RDF25u: Radial distribution function - 025 / unweighted
* RDF30u: Radial distribution function - 030 / unweighted
* RDF35u: Radial distribution function - 035 / unweighted
* RDF40u: Radial distribution function - 040 / unweighted
* RDF45u: Radial distribution function - 045 / unweighted
* RDF50u: Radial distribution function - 050 / unweighted
* RDF55u: Radial distribution function - 055 / unweighted
* RDF60u: Radial distribution function - 060 / unweighted
* RDF65u: Radial distribution function - 065 / unweighted
* RDF70u: Radial distribution function - 070 / unweighted
* RDF75u: Radial distribution function - 075 / unweighted
* RDF80u: Radial distribution function - 080 / unweighted
* RDF85u: Radial distribution function - 085 / unweighted
* RDF90u: Radial distribution function - 090 / unweighted
* RDF95u: Radial distribution function - 095 / unweighted
* RDF100u: Radial distribution function - 100 / unweighted
* RDF105u: Radial distribution function - 105 / unweighted
* RDF110u: Radial distribution function - 110 / unweighted
* RDF115u: Radial distribution function - 115 / unweighted
* RDF120u: Radial distribution function - 120 / unweighted
* RDF125u: Radial distribution function - 125 / unweighted
* RDF130u: Radial distribution function - 130 / unweighted
* RDF135u: Radial distribution function - 135 / unweighted
* RDF140u: Radial distribution function - 140 / unweighted
* RDF145u: Radial distribution function - 145 / unweighted
* RDF150u: Radial distribution function - 150 / unweighted
* RDF155u: Radial distribution function - 155 / unweighted
* RDF10m: Radial distribution function - 010 / weighted by relative mass
* RDF15m: Radial distribution function - 015 / weighted by relative mass
* RDF20m: Radial distribution function - 020 / weighted by relative mass
* RDF25m: Radial distribution function - 025 / weighted by relative mass
* RDF30m: Radial distribution function - 030 / weighted by relative mass
* RDF35m: Radial distribution function - 035 / weighted by relative mass
* RDF40m: Radial distribution function - 040 / weighted by relative mass
* RDF45m: Radial distribution function - 045 / weighted by relative mass
* RDF50m: Radial distribution function - 050 / weighted by relative mass
* RDF55m: Radial distribution function - 055 / weighted by relative mass
* RDF60m: Radial distribution function - 060 / weighted by relative mass
* RDF65m: Radial distribution function - 065 / weighted by relative mass
* RDF70m: Radial distribution function - 070 / weighted by relative mass
* RDF75m: Radial distribution function - 075 / weighted by relative mass
* RDF80m: Radial distribution function - 080 / weighted by relative mass
* RDF85m: Radial distribution function - 085 / weighted by relative mass
* RDF90m: Radial distribution function - 090 / weighted by relative mass
* RDF95m: Radial distribution function - 095 / weighted by relative mass
* RDF100m: Radial distribution function - 100 / weighted by relative mass
* RDF105m: Radial distribution function - 105 / weighted by relative mass
* RDF110m: Radial distribution function - 110 / weighted by relative mass
* RDF115m: Radial distribution function - 115 / weighted by relative mass
* RDF120m: Radial distribution function - 120 / weighted by relative mass
* RDF125m: Radial distribution function - 125 / weighted by relative mass
* RDF130m: Radial distribution function - 130 / weighted by relative mass
* RDF135m: Radial distribution function - 135 / weighted by relative mass
* RDF140m: Radial distribution function - 140 / weighted by relative mass
* RDF145m: Radial distribution function - 145 / weighted by relative mass
* RDF150m: Radial distribution function - 150 / weighted by relative mass
* RDF155m: Radial distribution function - 155 / weighted by relative mass
* RDF10v: Radial distribution function - 010 / weighted by relative van der Waals volumes
* RDF15v: Radial distribution function - 015 / weighted by relative van der Waals volumes
* RDF20v: Radial distribution function - 020 / weighted by relative van der Waals volumes
* RDF25v: Radial distribution function - 025 / weighted by relative van der Waals volumes
* RDF30v: Radial distribution function - 030 / weighted by relative van der Waals volumes
* RDF35v: Radial distribution function - 035 / weighted by relative van der Waals volumes
* RDF40v: Radial distribution function - 040 / weighted by relative van der Waals volumes
* RDF45v: Radial distribution function - 045 / weighted by relative van der Waals volumes
* RDF50v: Radial distribution function - 050 / weighted by relative van der Waals volumes
* RDF55v: Radial distribution function - 055 / weighted by relative van der Waals volumes
* RDF60v: Radial distribution function - 060 / weighted by relative van der Waals volumes
* RDF65v: Radial distribution function - 065 / weighted by relative van der Waals volumes
* RDF70v: Radial distribution function - 070 / weighted by relative van der Waals volumes
* RDF75v: Radial distribution function - 075 / weighted by relative van der Waals volumes
* RDF80v: Radial distribution function - 080 / weighted by relative van der Waals volumes
* RDF85v: Radial distribution function - 085 / weighted by relative van der Waals volumes
* RDF90v: Radial distribution function - 090 / weighted by relative van der Waals volumes
* RDF95v: Radial distribution function - 095 / weighted by relative van der Waals volumes
* RDF100v: Radial distribution function - 100 / weighted by relative van der Waals volumes
* RDF105v: Radial distribution function - 105 / weighted by relative van der Waals volumes
* RDF110v: Radial distribution function - 110 / weighted by relative van der Waals volumes
* RDF115v: Radial distribution function - 115 / weighted by relative van der Waals volumes
* RDF120v: Radial distribution function - 120 / weighted by relative van der Waals volumes
* RDF125v: Radial distribution function - 125 / weighted by relative van der Waals volumes
* RDF130v: Radial distribution function - 130 / weighted by relative van der Waals volumes
* RDF135v: Radial distribution function - 135 / weighted by relative van der Waals volumes
* RDF140v: Radial distribution function - 140 / weighted by relative van der Waals volumes
* RDF145v: Radial distribution function - 145 / weighted by relative van der Waals volumes
* RDF150v: Radial distribution function - 150 / weighted by relative van der Waals volumes
* RDF155v: Radial distribution function - 155 / weighted by relative van der Waals volumes
* RDF10e: Radial distribution function - 010 / weighted by relative Sanderson electronegativities
* RDF15e: Radial distribution function - 015 / weighted by relative Sanderson electronegativities
* RDF20e: Radial distribution function - 020 / weighted by relative Sanderson electronegativities
* RDF25e: Radial distribution function - 025 / weighted by relative Sanderson electronegativities
* RDF30e: Radial distribution function - 030 / weighted by relative Sanderson electronegativities
* RDF35e: Radial distribution function - 035 / weighted by relative Sanderson electronegativities
* RDF40e: Radial distribution function - 040 / weighted by relative Sanderson electronegativities
* RDF45e: Radial distribution function - 045 / weighted by relative Sanderson electronegativities
* RDF50e: Radial distribution function - 050 / weighted by relative Sanderson electronegativities
* RDF55e: Radial distribution function - 055 / weighted by relative Sanderson electronegativities
* RDF60e: Radial distribution function - 060 / weighted by relative Sanderson electronegativities
* RDF65e: Radial distribution function - 065 / weighted by relative Sanderson electronegativities
* RDF70e: Radial distribution function - 070 / weighted by relative Sanderson electronegativities
* RDF75e: Radial distribution function - 075 / weighted by relative Sanderson electronegativities
* RDF80e: Radial distribution function - 080 / weighted by relative Sanderson electronegativities
* RDF85e: Radial distribution function - 085 / weighted by relative Sanderson electronegativities
* RDF90e: Radial distribution function - 090 / weighted by relative Sanderson electronegativities
* RDF95e: Radial distribution function - 095 / weighted by relative Sanderson electronegativities
* RDF100e: Radial distribution function - 100 / weighted by relative Sanderson electronegativities
* RDF105e: Radial distribution function - 105 / weighted by relative Sanderson electronegativities
* RDF110e: Radial distribution function - 110 / weighted by relative Sanderson electronegativities
* RDF115e: Radial distribution function - 115 / weighted by relative Sanderson electronegativities
* RDF120e: Radial distribution function - 120 / weighted by relative Sanderson electronegativities
* RDF125e: Radial distribution function - 125 / weighted by relative Sanderson electronegativities
* RDF130e: Radial distribution function - 130 / weighted by relative Sanderson electronegativities
* RDF135e: Radial distribution function - 135 / weighted by relative Sanderson electronegativities
* RDF140e: Radial distribution function - 140 / weighted by relative Sanderson electronegativities
* RDF145e: Radial distribution function - 145 / weighted by relative Sanderson electronegativities
* RDF150e: Radial distribution function - 150 / weighted by relative Sanderson electronegativities
* RDF155e: Radial distribution function - 155 / weighted by relative Sanderson electronegativities
* RDF10p: Radial distribution function - 010 / weighted by relative polarizabilities
* RDF15p: Radial distribution function - 015 / weighted by relative polarizabilities
* RDF20p: Radial distribution function - 020 / weighted by relative polarizabilities
* RDF25p: Radial distribution function - 025 / weighted by relative polarizabilities
* RDF30p: Radial distribution function - 030 / weighted by relative polarizabilities
* RDF35p: Radial distribution function - 035 / weighted by relative polarizabilities
* RDF40p: Radial distribution function - 040 / weighted by relative polarizabilities
* RDF45p: Radial distribution function - 045 / weighted by relative polarizabilities
* RDF50p: Radial distribution function - 050 / weighted by relative polarizabilities
* RDF55p: Radial distribution function - 055 / weighted by relative polarizabilities
* RDF60p: Radial distribution function - 060 / weighted by relative polarizabilities
* RDF65p: Radial distribution function - 065 / weighted by relative polarizabilities
* RDF70p: Radial distribution function - 070 / weighted by relative polarizabilities
* RDF75p: Radial distribution function - 075 / weighted by relative polarizabilities
* RDF80p: Radial distribution function - 080 / weighted by relative polarizabilities
* RDF85p: Radial distribution function - 085 / weighted by relative polarizabilities
* RDF90p: Radial distribution function - 090 / weighted by relative polarizabilities
* RDF95p: Radial distribution function - 095 / weighted by relative polarizabilities
* RDF100p: Radial distribution function - 100 / weighted by relative polarizabilities
* RDF105p: Radial distribution function - 105 / weighted by relative polarizabilities
* RDF110p: Radial distribution function - 110 / weighted by relative polarizabilities
* RDF115p: Radial distribution function - 115 / weighted by relative polarizabilities
* RDF120p: Radial distribution function - 120 / weighted by relative polarizabilities
* RDF125p: Radial distribution function - 125 / weighted by relative polarizabilities
* RDF130p: Radial distribution function - 130 / weighted by relative polarizabilities
* RDF135p: Radial distribution function - 135 / weighted by relative polarizabilities
* RDF140p: Radial distribution function - 140 / weighted by relative polarizabilities
* RDF145p: Radial distribution function - 145 / weighted by relative polarizabilities
* RDF150p: Radial distribution function - 150 / weighted by relative polarizabilities
* RDF155p: Radial distribution function - 155 / weighted by relative polarizabilities
* RDF10i: Radial distribution function - 010 / weighted by relative first ionization potential
* RDF15i: Radial distribution function - 015 / weighted by relative first ionization potential
* RDF20i: Radial distribution function - 020 / weighted by relative first ionization potential
* RDF25i: Radial distribution function - 025 / weighted by relative first ionization potential
* RDF30i: Radial distribution function - 030 / weighted by relative first ionization potential
* RDF35i: Radial distribution function - 035 / weighted by relative first ionization potential
* RDF40i: Radial distribution function - 040 / weighted by relative first ionization potential
* RDF45i: Radial distribution function - 045 / weighted by relative first ionization potential
* RDF50i: Radial distribution function - 050 / weighted by relative first ionization potential
* RDF55i: Radial distribution function - 055 / weighted by relative first ionization potential
* RDF60i: Radial distribution function - 060 / weighted by relative first ionization potential
* RDF65i: Radial distribution function - 065 / weighted by relative first ionization potential
* RDF70i: Radial distribution function - 070 / weighted by relative first ionization potential
* RDF75i: Radial distribution function - 075 / weighted by relative first ionization potential
* RDF80i: Radial distribution function - 080 / weighted by relative first ionization potential
* RDF85i: Radial distribution function - 085 / weighted by relative first ionization potential
* RDF90i: Radial distribution function - 090 / weighted by relative first ionization potential
* RDF95i: Radial distribution function - 095 / weighted by relative first ionization potential
* RDF100i: Radial distribution function - 100 / weighted by relative first ionization potential
* RDF105i: Radial distribution function - 105 / weighted by relative first ionization potential
* RDF110i: Radial distribution function - 110 / weighted by relative first ionization potential
* RDF115i: Radial distribution function - 115 / weighted by relative first ionization potential
* RDF120i: Radial distribution function - 120 / weighted by relative first ionization potential
* RDF125i: Radial distribution function - 125 / weighted by relative first ionization potential
* RDF130i: Radial distribution function - 130 / weighted by relative first ionization potential
* RDF135i: Radial distribution function - 135 / weighted by relative first ionization potential
* RDF140i: Radial distribution function - 140 / weighted by relative first ionization potential
* RDF145i: Radial distribution function - 145 / weighted by relative first ionization potential
* RDF150i: Radial distribution function - 150 / weighted by relative first ionization potential
* RDF155i: Radial distribution function - 155 / weighted by relative first ionization potential
* RDF10s: Radial distribution function - 010 / weighted by relative I-state
* RDF15s: Radial distribution function - 015 / weighted by relative I-state
* RDF20s: Radial distribution function - 020 / weighted by relative I-state
* RDF25s: Radial distribution function - 025 / weighted by relative I-state
* RDF30s: Radial distribution function - 030 / weighted by relative I-state
* RDF35s: Radial distribution function - 035 / weighted by relative I-state
* RDF40s: Radial distribution function - 040 / weighted by relative I-state
* RDF45s: Radial distribution function - 045 / weighted by relative I-state
* RDF50s: Radial distribution function - 050 / weighted by relative I-state
* RDF55s: Radial distribution function - 055 / weighted by relative I-state
* RDF60s: Radial distribution function - 060 / weighted by relative I-state
* RDF65s: Radial distribution function - 065 / weighted by relative I-state
* RDF70s: Radial distribution function - 070 / weighted by relative I-state
* RDF75s: Radial distribution function - 075 / weighted by relative I-state
* RDF80s: Radial distribution function - 080 / weighted by relative I-state
* RDF85s: Radial distribution function - 085 / weighted by relative I-state
* RDF90s: Radial distribution function - 090 / weighted by relative I-state
* RDF95s: Radial distribution function - 095 / weighted by relative I-state
* RDF100s: Radial distribution function - 100 / weighted by relative I-state
* RDF105s: Radial distribution function - 105 / weighted by relative I-state
* RDF110s: Radial distribution function - 110 / weighted by relative I-state
* RDF115s: Radial distribution function - 115 / weighted by relative I-state
* RDF120s: Radial distribution function - 120 / weighted by relative I-state
* RDF125s: Radial distribution function - 125 / weighted by relative I-state
* RDF130s: Radial distribution function - 130 / weighted by relative I-state
* RDF135s: Radial distribution function - 135 / weighted by relative I-state
* RDF140s: Radial distribution function - 140 / weighted by relative I-state
* RDF145s: Radial distribution function - 145 / weighted by relative I-state
* RDF150s: Radial distribution function - 150 / weighted by relative I-state
* RDF155s: Radial distribution function - 155 / weighted by relative I-state

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_RingCount

RingCount PaDEL descriptor

The following features are calculated:

* nRing: Number of rings
* n3Ring: Number of 3-membered rings
* n4Ring: Number of 4-membered rings
* n5Ring: Number of 5-membered rings
* n6Ring: Number of 6-membered rings
* n7Ring: Number of 7-membered rings
* n8Ring: Number of 8-membered rings
* n9Ring: Number of 9-membered rings
* n10Ring: Number of 10-membered rings
* n11Ring: Number of 11-membered rings
* n12Ring: Number of 12-membered rings
* nG12Ring: Number of >12-membered rings
* nFRing: Number of fused rings
* nF4Ring: Number of 4-membered fused rings
* nF5Ring: Number of 5-membered fused rings
* nF6Ring: Number of 6-membered fused rings
* nF7Ring: Number of 7-membered fused rings
* nF8Ring: Number of 8-membered fused rings
* nF9Ring: Number of 9-membered fused rings
* nF10Ring: Number of 10-membered fused rings
* nF11Ring: Number of 11-membered fused rings
* nF12Ring: Number of 12-membered fused rings
* nFG12Ring: Number of >12-membered fused rings
* nTRing: Number of rings (includes counts from fused rings)
* nT4Ring: Number of 4-membered rings (includes counts from fused rings)
* nT5Ring: Number of 5-membered rings (includes counts from fused rings)
* nT6Ring: Number of 6-membered rings (includes counts from fused rings)
* nT7Ring: Number of 7-membered rings (includes counts from fused rings)
* nT8Ring: Number of 8-membered rings (includes counts from fused rings)
* nT9Ring: Number of 9-membered rings (includes counts from fused rings)
* nT10Ring: Number of 10-membered rings (includes counts from fused rings)
* nT11Ring: Number of 11-membered rings (includes counts from fused rings)
* nT12Ring: Number of 12-membered rings (includes counts from fused rings)
* nTG12Ring: Number of >12-membered rings (includes counts from fused rings)
* nHeteroRing: Number of rings containing heteroatoms (N, O, P, S, or halogens)
* n3HeteroRing: Number of 3-membered rings containing heteroatoms (N, O, P, S, or halogens)
* n4HeteroRing: Number of 4-membered rings containing heteroatoms (N, O, P, S, or halogens)
* n5HeteroRing: Number of 5-membered rings containing heteroatoms (N, O, P, S, or halogens)
* n6HeteroRing: Number of 6-membered rings containing heteroatoms (N, O, P, S, or halogens)
* n7HeteroRing: Number of 7-membered rings containing heteroatoms (N, O, P, S, or halogens)
* n8HeteroRing: Number of 8-membered rings containing heteroatoms (N, O, P, S, or halogens)
* n9HeteroRing: Number of 9-membered rings containing heteroatoms (N, O, P, S, or halogens)
* n10HeteroRing: Number of 10-membered rings containing heteroatoms (N, O, P, S, or halogens)
* n11HeteroRing: Number of 11-membered rings containing heteroatoms (N, O, P, S, or halogens)
* n12HeteroRing: Number of 12-membered rings containing heteroatoms (N, O, P, S, or halogens)
* nG12HeteroRing: Number of >12-membered rings containing heteroatoms (N, O, P, S, or halogens)
* nFHeteroRing: Number of fused rings containing heteroatoms (N, O, P, S, or halogens)
* nF4HeteroRing: Number of 4-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nF5HeteroRing: Number of 5-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nF6HeteroRing: Number of 6-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nF7HeteroRing: Number of 7-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nF8HeteroRing: Number of 8-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nF9HeteroRing: Number of 9-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nF10HeteroRing: Number of 10-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nF11HeteroRing: Number of 11-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nF12HeteroRing: Number of 12-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nFG12HeteroRing: Number of >12-membered fused rings containing heteroatoms (N, O, P, S, or halogens)
* nTHeteroRing: Number of rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nT4HeteroRing: Number of 4-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nT5HeteroRing: Number of 5-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nT6HeteroRing: Number of 6-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nT7HeteroRing: Number of 7-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nT8HeteroRing: Number of 8-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nT9HeteroRing: Number of 9-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nT10HeteroRing: Number of 10-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nT11HeteroRing: Number of 11-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nT12HeteroRing: Number of 12-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)
* nTG12HeteroRing: Number of >12-membered rings (includes counts from fused rings) containing heteroatoms (N, O, P, S, or halogens)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_RotatableBondsCount

RotatableBondsCount PaDEL descriptor

The following features are calculated:

* nRotB: Number of rotatable bonds, excluding terminal bonds
* RotBFrac: Fraction of rotatable bonds, excluding terminal bonds
* nRotBt: Number of rotatable bonds, including terminal bonds
* RotBtFrac: Fraction of rotatable bonds, including terminal bonds

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_RuleOfFive

RuleOfFive PaDEL descriptor

The following features are calculated:

* LipinskiFailures: Number failures of the Lipinski's Rule Of 5

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_SubFP

PaDEL SubFPfingerprint

Substructure fingerprint - Presence of SMARTS Patterns for Functional Group
Classification by Christian Laggner

* Number of bits: 307
* Bit prefix: SubFP


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_SubFPC

PaDEL SubFPCfingerprint

Substructure fingerprint count - Count of SMARTS Patterns for Functional Group
Classification by Christian Laggner

* Number of bits: 307
* Bit prefix: SubFPC


All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


## Parameters

* size (type: Optional; default: None): Description unavailable.
* search_depth (type: Optional; default: None): Description unavailable.



# padel_TPSA

TPSA PaDEL descriptor

The following features are calculated:

* TopoPSA: Topological polar surface area

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_Topological

Topological PaDEL descriptor

The following features are calculated:

* topoRadius: Topological radius (minimum atom eccentricity)
* topoDiameter: Topological diameter (maximum atom eccentricity)
* topoShape: Petitjean topological shape index 

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_TopologicalCharge

TopologicalCharge PaDEL descriptor

The following features are calculated:

* GGI1: Topological charge index of order 1
* GGI2: Topological charge index of order 2
* GGI3: Topological charge index of order 3
* GGI4: Topological charge index of order 4
* GGI5: Topological charge index of order 5
* GGI6: Topological charge index of order 6
* GGI7: Topological charge index of order 7
* GGI8: Topological charge index of order 8
* GGI9: Topological charge index of order 9
* GGI10: Topological charge index of order 10
* JGI1: Mean topological charge index of order 1
* JGI2: Mean topological charge index of order 2
* JGI3: Mean topological charge index of order 3
* JGI4: Mean topological charge index of order 4
* JGI5: Mean topological charge index of order 5
* JGI6: Mean topological charge index of order 6
* JGI7: Mean topological charge index of order 7
* JGI8: Mean topological charge index of order 8
* JGI9: Mean topological charge index of order 9
* JGI10: Mean topological charge index of order 10
* JGT: Global topological charge index

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_TopologicalDistanceMatrix

TopologicalDistanceMatrix PaDEL descriptor

The following features are calculated:

* SpMax_D: Leading eigenvalue from topological distance matrix
* SpDiam_D: Spectral diameter from topological distance matrix
* SpAD_D: Spectral absolute deviation from topological distance matrix
* SpMAD_D: Spectral mean absolute deviation from topological distance matrix
* EE_D: Estrada-like index from topological distance matrix
* VE1_D: Coefficient sum of the last eigenvector from topological distance matrix
* VE2_D: Average coefficient sum of the last eigenvector from topological distance matrix
* VE3_D: Logarithmic coefficient sum of the last eigenvector from topological distance matrix
* VR1_D: Randic-like eigenvector-based index from topological distance matrix
* VR2_D: Normalized Randic-like eigenvector-based index from topological distance matrix
* VR3_D: Logarithmic Randic-like eigenvector-based index from topological distance matrix

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_VABC

VABC PaDEL descriptor

The following features are calculated:

* VABC: Van der Waals volume calculated using the method proposed in [Zhao, Yuan H. and Abraham, Michael H. and Zissimos, Andreas M., Fast Calculation of van der Waals Volume as a Sum of Atomic and Bond Contributions and Its Application to Drug Compounds, The Journal of Organic Chemistry, 2003, 68:7368-7373]

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_VAdjMa

VAdjMa PaDEL descriptor

The following features are calculated:

* VAdjMat: Vertex adjacency information (magnitude)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_WHIM

WHIM 3D PaDEL descriptor

The following features are calculated:

* L1u: 1st component size directional WHIM index / unweighted
* L2u: 2nd component size directional WHIM index / unweighted
* L3u: 3rd component size directional WHIM index / unweighted
* P1u: 1st component shape directional WHIM index / unweighted
* P2u: 2nd component shape directional WHIM index / unweighted
* E1u: 1st component accessibility directional WHIM index / unweighted
* E2u: 2nd component accessibility directional WHIM index / unweighted
* E3u: 3rd component accessibility directional WHIM index / unweighted
* Tu: T total size index / unweighted
* Au: A total size index / unweighted
* Vu: V total size index / unweighted
* Ku: K global shape index / unweighted
* Du: D total accessibility index / unweighted
* L1m: 1st component size directional WHIM index / weighted by relative mass
* L2m: 2nd component size directional WHIM index / weighted by relative mass
* L3m: 3rd component size directional WHIM index / weighted by relative mass
* P1m: 1st component shape directional WHIM index / weighted by relative mass
* P2m: 2nd component shape directional WHIM index / weighted by relative mass
* E1m: 1st component accessibility directional WHIM index / weighted by relative mass
* E2m: 2nd component accessibility directional WHIM index / weighted by relative mass
* E3m: 3rd component accessibility directional WHIM index / weighted by relative mass
* Tm: T total size index / weighted by relative mass
* Am: A total size index / weighted by relative mass
* Vm: V total size index / weighted by relative mass
* Km: K global shape index / weighted by relative mass
* Dm: D total accessibility index / weighted by relative mass
* L1v: 1st component size directional WHIM index / weighted by relative van der Waals volumes
* L2v: 2nd component size directional WHIM index / weighted by relative van der Waals volumes
* L3v: 3rd component size directional WHIM index / weighted by relative van der Waals volumes
* P1v: 1st component shape directional WHIM index / weighted by relative van der Waals volumes
* P2v: 2nd component shape directional WHIM index / weighted by relative van der Waals volumes
* E1v: 1st component accessibility directional WHIM index / weighted by relative van der Waals volumes
* E2v: 2nd component accessibility directional WHIM index / weighted by relative van der Waals volumes
* E3v: 3rd component accessibility directional WHIM index / weighted by relative van der Waals volumes
* Tv: T total size index / weighted by relative van der Waals volumes
* Av: A total size index / weighted by relative van der Waals volumes
* Vv: V total size index / weighted by relative van der Waals volumes
* Kv: K global shape index / weighted by relative van der Waals volumes
* Dv: D total accessibility index / weighted by relative van der Waals volumes
* L1e: 1st component size directional WHIM index / weighted by relative Sanderson electronegativities
* L2e: 2nd component size directional WHIM index / weighted by relative Sanderson electronegativities
* L3e: 3rd component size directional WHIM index / weighted by relative Sanderson electronegativities
* P1e: 1st component shape directional WHIM index / weighted by relative Sanderson electronegativities
* P2e: 2nd component shape directional WHIM index / weighted by relative Sanderson electronegativities
* E1e: 1st component accessibility directional WHIM index / weighted by relative Sanderson electronegativities
* E2e: 2nd component accessibility directional WHIM index / weighted by relative Sanderson electronegativities
* E3e: 3rd component accessibility directional WHIM index / weighted by relative Sanderson electronegativities
* Te: T total size index / weighted by relative Sanderson electronegativities
* Ae: A total size index / weighted by relative Sanderson electronegativities
* Ve: V total size index / weighted by relative Sanderson electronegativities
* Ke: K global shape index / weighted by relative Sanderson electronegativities
* De: D total accessibility index / weighted by relative Sanderson electronegativities
* L1p: 1st component size directional WHIM index / weighted by relative polarizabilities
* L2p: 2nd component size directional WHIM index / weighted by relative polarizabilities
* L3p: 3rd component size directional WHIM index / weighted by relative polarizabilities
* P1p: 1st component shape directional WHIM index / weighted by relative polarizabilities
* P2p: 2nd component shape directional WHIM index / weighted by relative polarizabilities
* E1p: 1st component accessibility directional WHIM index / weighted by relative polarizabilities
* E2p: 2nd component accessibility directional WHIM index / weighted by relative polarizabilities
* E3p: 3rd component accessibility directional WHIM index / weighted by relative polarizabilities
* Tp: T total size index / weighted by relative polarizabilities
* Ap: A total size index / weighted by relative polarizabilities
* Vp: V total size index / weighted by relative polarizabilities
* Kp: K global shape index / weighted by relative polarizabilities
* Dp: D total accessibility index / weighted by relative polarizabilities
* L1i: 1st component size directional WHIM index / weighted by relative first ionization potential
* L2i: 2nd component size directional WHIM index / weighted by relative first ionization potential
* L3i: 3rd component size directional WHIM index / weighted by relative first ionization potential
* P1i: 1st component shape directional WHIM index / weighted by relative first ionization potential
* P2i: 2nd component shape directional WHIM index / weighted by relative first ionization potential
* E1i: 1st component accessibility directional WHIM index / weighted by relative first ionization potential
* E2i: 2nd component accessibility directional WHIM index / weighted by relative first ionization potential
* E3i: 3rd component accessibility directional WHIM index / weighted by relative first ionization potential
* Ti: T total size index / weighted by relative first ionization potential
* Ai: A total size index / weighted by relative first ionization potential
* Vi: V total size index / weighted by relative first ionization potential
* Ki: K global shape index / weighted by relative first ionization potential
* Di: D total accessibility index / weighted by relative first ionization potential
* L1s: 1st component size directional WHIM index / weighted by relative I-state
* L2s: 2nd component size directional WHIM index / weighted by relative I-state
* L3s: 3rd component size directional WHIM index / weighted by relative I-state
* P1s: 1st component shape directional WHIM index / weighted by relative I-state
* P2s: 2nd component shape directional WHIM index / weighted by relative I-state
* E1s: 1st component accessibility directional WHIM index / weighted by relative I-state
* E2s: 2nd component accessibility directional WHIM index / weighted by relative I-state
* E3s: 3rd component accessibility directional WHIM index / weighted by relative I-state
* Ts: T total size index / weighted by relative I-state
* As: A total size index / weighted by relative I-state
* Vs: V total size index / weighted by relative I-state
* Ks: K global shape index / weighted by relative I-state
* Ds: D total accessibility index / weighted by relative I-state

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_WalkCount

WalkCount PaDEL descriptor

The following features are calculated:

* MWC2: Molecular walk count of order 2 (ln(1+x)
* MWC3: Molecular walk count of order 3 (ln(1+x)
* MWC4: Molecular walk count of order 4 (ln(1+x)
* MWC5: Molecular walk count of order 5 (ln(1+x)
* MWC6: Molecular walk count of order 6 (ln(1+x)
* MWC7: Molecular walk count of order 7 (ln(1+x)
* MWC8: Molecular walk count of order 8 (ln(1+x)
* MWC9: Molecular walk count of order 9 (ln(1+x)
* MWC10: Molecular walk count of order 10 (ln(1+x)
* TWC: Total walk count (up to order 10)
* SRW2: Self-returning walk count of order 2 (ln(1+x)
* SRW3: Self-returning walk count of order 3 (ln(1+x)
* SRW4: Self-returning walk count of order 4 (ln(1+x)
* SRW5: Self-returning walk count of order 5 (ln(1+x)
* SRW6: Self-returning walk count of order 6 (ln(1+x)
* SRW7: Self-returning walk count of order 7 (ln(1+x)
* SRW8: Self-returning walk count of order 8 (ln(1+x)
* SRW9: Self-returning walk count of order 9 (ln(1+x)
* SRW10: Self-returning walk count of order 10 (ln(1+x)
* TSRW: Total self-return walk count (up to order 10) (ln(1+x))

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_Weight

Weight PaDEL descriptor

The following features are calculated:

* MW: Molecular weight
* AMW: Average molecular weight (Molecular weight / Total number of atoms)

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_WeightedPath

WeightedPath PaDEL descriptor

The following features are calculated:

* WTPT-1: Molecular ID
* WTPT-2: Molecular ID / number of atoms
* WTPT-3: Sum of path lengths starting from heteroatoms
* WTPT-4: Sum of path lengths starting from oxygens
* WTPT-5: Sum of path lengths starting from nitrogens

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_WienerNumbers

WienerNumbers PaDEL descriptor

The following features are calculated:

* WPATH: Weiner path number 
* WPOL: Weiner polarity number 

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_XLogP

XLogP PaDEL descriptor

The following features are calculated:

* XLogP: XLogP

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# padel_ZagrebIndex

ZagrebIndex PaDEL descriptor

The following features are calculated:

* Zagreb: Sum of the squares of atom degree over all heavy atoms i

All values are calculated with the [PaDEL_pywrapper Python
package](https://github.com/OlivierBeq/PaDEL_pywrapper) based on
[PaDEL-descriptor](https://doi.org/10.1002/jcc.21707).

> Yap, Chun Wei. “PaDEL-Descriptor: An Open Source Software to Calculate
> Molecular Descriptors and Fingerprints.” Journal of Computational Chemistry
> 32, no. 7 (May 2011): 1466–74. https://doi.org/10.1002/jcc.21707.


# qed

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


# rdkdesc

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


# rdkfp

RDK fingerprint feature calculator.

RDK topological fingerprint calculated with the [RDKit cheminformatics
library](https://www.rdkit.org/docs/source/rdkit.Chem.rdmolops.html#rdkit.Chem.rdmolops.RDKFingerprint

Each feature is a single bit of the feature vector.


## Parameters

* size (type: int; default: 2048): The fingerprint size. It should be 1024, 2048 or 4096.



# secfp

SECFP feature calculator.

SMILES Extended Connectivity Fingerprint f

MinHash Fingerprints (MHFP) / SMILES Extended Connectivity Fingerprints
(SECFP) calculated with [RDKit cheminformatics
library](https://rdkit.org/docs/source/rdkit.Chem.rdMHFPFingerprint.html).

> Probst, Daniel, and Jean-Louis Reymond. “A Probabilistic Molecular
> Fingerprint for Big Data Settings.” Journal of Cheminformatics 10, no. 1
> (December 18, 2018): 66. https://doi.org/10.1186/s13321-018-0321-8.

Each feature is a single bit of the feature vector.


## Parameters

* size (type: int; default: 2048): Description unavailable.



