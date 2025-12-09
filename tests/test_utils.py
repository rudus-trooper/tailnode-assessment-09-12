import pandas as pd
import pytest
from dashboard.utils import (
    filterDf,
    getCorrelationMatrix,
    getTopProducingDistricts,
    getYieldVsArea,
    getTimeSeries,
    getCropWiseProduction,
    getYieldByDistrict,
    getCropVsStateAverageTrend,
    getStatesWithYieldDecline,
    getSeasonalTrends,
)

# create dummy dataframe
@pytest.fixture
def df():
    data = {
        "State": [
            "Bihar","Bihar","Bihar","Bihar","Bihar","Bihar","Bihar","Bihar","Bihar",
            "Bihar","Bihar","Bihar","Bihar","Bihar","Bihar","Bihar","Bihar","Bihar",
            "Bihar","Bihar","Bihar","Bihar","Bihar","Bihar"
        ],
        "District": [
            "ARARIA","ARARIA","ARARIA","AURANGABAD","AURANGABAD","AURANGABAD",
            "BANKA","BANKA","BANKA","ARARIA","ARARIA","ARARIA","AURANGABAD",
            "AURANGABAD","AURANGABAD","BANKA","BANKA","BANKA",
            "ARARIA","AURANGABAD","BANKA","ARARIA","AURANGABAD","BANKA"
        ],
        "Crop": [
            "Barley","Barley","Barley","Barley","Barley","Barley","Barley","Barley","Barley",
            "Wheat","Wheat","Wheat","Wheat","Wheat","Wheat","Wheat","Wheat","Wheat",
            "Barley","Barley","Barley","Wheat","Wheat","Wheat"
        ],
        "Year": [
            "2001-02","2002-03","2003-04","2001-02","2002-03","2003-04","2001-02","2002-03","2003-04",
            "2001-02","2002-03","2003-04","2001-02","2002-03","2003-04","2001-02","2002-03","2003-04",
            "2004-05","2004-05","2004-05","2004-05","2004-05","2004-05"
        ],
        "Season": ["Rabi"] * 24,
        "Area": [
            20,23,104,1775,2280,2461,1111,1113,863,
            60210,55849,53697,55528,57409,53655,35815,26260,27157,
            56,1224,595,53828,52479,21538
        ],
        "Area Units": ["Hectare"] * 24,
        "Production": [
            25,27,116,1798,2503,2284,1102,578,886,
            108136,86810,52118,110171,121475,111218,55872,36958,42013,
            59,1264,344,33278,74460,27735
        ],
        "Production Units": ["Tonnes"] * 24,
        "Yield": [
            1.25,1.1739,1.11538,1.0129,1.0978,0.9280,0.9918,0.5193,1.0266,
            1.7959,1.5543,0.9705,1.9840,2.1159,2.0728,1.5600,1.4073,1.5470,
            1.0535,1.0326,0.5781,0.6182,1.4188,1.2877
        ]
    }
    return pd.DataFrame(data)

# filterDf
def test_filterDf_basic(df):
    f = filterDf(df, ["Bihar"], ["ARARIA"], ["Barley"], ["Rabi"], ["2001-02"])
    assert len(f) == 1
    assert f.iloc[0]["Production"] == 25

# getCorrelationMatrix
def test_getCorrelationMatrix_shape(df):
    m = getCorrelationMatrix(df, ["Bihar"], None, None, None, None)
    assert m.shape == (3, 3)

# getTopProducingDistricts
def test_getTopProducingDistricts_order(df):
    t = getTopProducingDistricts(df, ["Bihar"], None, ["Wheat"], ["Rabi"], None)
    top = t.iloc[0]["District"]
    assert top in ["AURANGABAD", "ARARIA", "BANKA"]

# getYieldVsArea
def test_getYieldVsArea_cols(df):
    q = getYieldVsArea(df, None, None, None, None, None)
    assert set(q.columns) == {"Area", "Yield", "Crop", "District", "Year"}

# getTimeSeries
def test_getTimeSeries_years_order(df):
    ts = getTimeSeries(df, None, None, None, None, None)
    years = ts["Year"].tolist()
    assert years == sorted(years)

# getCropWiseProduction
def test_getCropWiseProduction(df):
    c = getCropWiseProduction(df, None, None, None, None, None)
    assert "Barley" in c.columns
    assert "Wheat" in c.columns

# getYieldByDistrict
def test_getYieldByDistrict(df):
    yd = getYieldByDistrict(df, None, None, None, None, None)
    assert "District" in yd.columns

# getCropVsStateAverageTrend
def test_getCropVsStateAverageTrend(df):
    trend = getCropVsStateAverageTrend(df, ["Bihar"], ["ARARIA"], ["Wheat"], ["Rabi"], None)
    assert "DistrictYield" in trend.columns
    assert "StateYield" in trend.columns

# getStatesWithYieldDecline
def test_getStatesWithYieldDecline(df):
    decline = getStatesWithYieldDecline(df, "Barley", declinePct=5)
    assert "State" in decline.columns

# getSeasonalTrends
def test_getSeasonalTrends(df):
    st = getSeasonalTrends(df, None, None, None, ["Rabi"], None)
    assert {"State", "District", "Season", "Year"}.issubset(set(st.columns))
