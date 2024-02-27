from Ranker import Ranker


ranker = Ranker("model", "You are an AI")


def test_api_requests():
    mat_1 = "mp-10101"
    mat_2 = "mp-1245205"

    assert ranker.get_experimentally_observed(mat_1) == True
    assert ranker.get_experimentally_observed(mat_2) == False

    expected_paper_titles_1 = ['Novel ternary alkali metal silver acetylides M(1) Ag C2 (M(1)= Li, Na, K, Rb, Cs)']
    assert ranker.get_paper_titles(mat_1) == expected_paper_titles_1

    expected_paper_titles_2 = ['Thermodynamic limit for synthesis of metastable inorganic materials']
    assert ranker.get_paper_titles(mat_2) == expected_paper_titles_2

def test_table():
    df = ranker.create_table(["mp-10101", "mp-1245205"])
    print(df)

