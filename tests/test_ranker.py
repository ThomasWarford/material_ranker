from Ranker import Ranker


ranker = Ranker("model", "You are an AI")
df = ranker.create_table(["mp-10", "mp-100", "mp-1000"])

## Test table creation
def test_table():
    # check for NaNs
    assert df.isna().any(axis=None) == False
    # check table dimensions
    assert df.shape == (3, 1)
