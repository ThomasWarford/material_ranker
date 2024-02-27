from Ranker import Ranker


ranker = Ranker("model", "You are an AI")


def test_api_requests():
    mat_1 = "mp-66" # diamond
    mat_2 = "mp-1245205" # theoretical material

    assert ranker.get_experimentally_observed(mat_1) == True
    assert ranker.get_experimentally_observed(mat_2) == False

    ## Paper Titles (fails when title enclosed in {{}} )
    expected_paper_titles_1 = ['Influence of the isotope ratio on the lattice constant of diamond', 'Structural and thermodynamic properties of diamond: A path-integral Monte Carlo study', 'Low-temperature phase transformation from graphite to sp3 orthorhombic carbon', 'Precision determination of lattice parameter, coefficient of thermal expansion and atomic weight of carbon in diamond', 'Zinc-blende-Wurtzite polytypism in semiconductors', 'Isotope effect on anharmonic thermal atomic vibration and k-refinemant of 12C and 13C diamond', 'Structure of some crystals', 'Accurate lattice constants from multiple reflection measurements. Lattice constants of germanium, silicon and diamond', 'Calculated x-ray diffraction data for diamond polytypes', 'X-ray study of laboratory-made diamonds', 'Experimental determination of core electron deformation in diamond', 'First-principles study of uranium carbide: accommodation of point defects and of helium, xenon and oxygen impurities', 'Thermal expansion coefficient of synthetic diamond single crystal at low temperatures', 'Structure and stability under pressure of cubic and hexagonal diamond crystals of C, BN and Si from first principles', 'Structural forms of cubic B C2 N', 'Hydrogenated K4 carbon: A new stable cubic gauche structure of carbon hydride', 'Lattice constant of diamond and the C - C single bond']
    assert ranker.get_paper_titles(mat_1) == expected_paper_titles_1

    expected_paper_titles_2 = ['Thermodynamic limit for synthesis of metastable inorganic materials']
    assert ranker.get_paper_titles(mat_2) == expected_paper_titles_2

def test_table():
    df = ranker.create_table(["mp-10101", "mp-1245205"])
    print(df)

