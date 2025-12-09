import pandas as pd


# apply filters to the main dataframe
def filterDf(df, states, districts, crops, seasons, years):
    """Return filtered dataframe based on multi-select user inputs."""
    f = df.copy()

    # filter for state
    if states:
        f = f[f["State"].isin(states)]

    # filter for district
    if districts:
        f = f[f["District"].isin(districts)]

    # filter for crop
    if crops:
        f = f[f["Crop"].isin(crops)]

    # filter for season
    if seasons:
        f = f[f["Season"].isin(seasons)]

    # filter for year
    if years:
        f = f[f["Year"].isin(years)]

    return f


# correlation matrix source
def getCorrelationMatrix(df, states, districts, crops, seasons, years):
    """Return correlation matrix for Area, Production and Yield."""
    f = filterDf(df, states, districts, crops, seasons, years)
    return f[["Area", "Production", "Yield"]].corr()


# top producing districts source
def getTopProducingDistricts(df, states, districts, crops, seasons, years):
    """Return aggregated production grouped by district."""
    f = filterDf(df, states, districts, crops, seasons, years)

    g = (
        f.groupby("District", as_index=False)
        .agg({"Production": "sum"})
        .sort_values("Production", ascending=False)
    )

    return g


# yield vs area scatter source
def getYieldVsArea(df, states, districts, crops, seasons, years):
    """Return Area vs Yield values for scatter plot."""
    f = filterDf(df, states, districts, crops, seasons, years)
    return f[["Area", "Yield", "Crop", "District", "Year"]]


# time series for area, production, yield
def getTimeSeries(df, states, districts, crops, seasons, years):
    """Return multi-metric time series for area, production and yield."""
    f = filterDf(df, states, districts, crops, seasons, years)

    g = (
        f.groupby("Year", as_index=False)
        .agg({"Area": "sum", "Production": "sum", "Yield": "mean"})
        .sort_values("Year")
    )

    return g


# crop-wise production trend
def getCropWiseProduction(df, states, districts, crops, seasons, years):
    """Return crop-wise production aggregated by year."""
    f = filterDf(df, states, districts, crops, seasons, years)

    g = pd.crosstab(
        f["Year"],
        f["Crop"],
        values=f["Production"],
        aggfunc="sum",
    ).fillna(0).reset_index()

    return g


# yield choropleth (district-level)
def getYieldByDistrict(df, states, districts, crops, seasons, years):
    """Return district-level yield average."""
    f = filterDf(df, states, districts, crops, seasons, years)

    g = pd.crosstab(
        f["District"],
        f["Year"],
        values=f["Yield"],
        aggfunc="mean",
    ).fillna(0).reset_index()

    return g

# Special Funtions (Not integerated)

# compare district/state crop yield to state average
def getCropVsStateAverageTrend(df, states, districts, crops, seasons, years):
    """Return comparison of local crop yield trend vs state-level average."""
    f = filterDf(df, states, districts, crops, seasons, years)

    # district-level trend
    districtTrend = (
        f.groupby("Year", as_index=False)
        .agg({"Yield": "mean"})
        .rename(columns={"Yield": "DistrictYield"})
    )

    # full state-level trend (ignoring district filter)
    s = df.copy()
    if states:
        s = s[s["State"].isin(states)]
    if crops:
        s = s[s["Crop"].isin(crops)]
    if seasons:
        s = s[s["Season"].isin(seasons)]

    stateTrend = (
        s.groupby("Year", as_index=False)
        .agg({"Yield": "mean"})
        .rename(columns={"Yield": "StateYield"})
    )

    # merge for comparison chart
    merged = districtTrend.merge(stateTrend, on="Year", how="left")

    return merged


# states with >10% yield decline over 5 years
def getStatesWithYieldDecline(df, crop, declinePct=10):
    """Return states where crop yield declines more than X% over last 5 years."""
    f = df[df["Crop"] == crop]

    # compute state-year yield
    g = f.groupby(["State", "Year"], as_index=False).agg({"Yield": "mean"})

    # find first and last year per state
    firstLast = (
        g.sort_values("Year")
        .groupby("State")
        .agg({"Yield": ["first", "last"]})
    )
    firstLast.columns = ["StartYield", "EndYield"]
    firstLast = firstLast.reset_index()

    # compute decline percentage
    firstLast["DeclinePct"] = (
        (firstLast["StartYield"] - firstLast["EndYield"]) / firstLast["StartYield"]
    ) * 100

    # filter states with decline > X%
    result = firstLast[firstLast["DeclinePct"] >= declinePct]

    return result


# state + district trend by season
def getSeasonalTrends(df, states, districts, crops, seasons, years):
    """Return seasonal crop trends split by state/district."""
    f = filterDf(df, states, districts, crops, seasons, years)

    g = (
        f.groupby(["State", "District", "Season", "Year"], as_index=False)
        .agg({"Area": "sum", "Production": "sum", "Yield": "mean"})
        .sort_values(["State", "District", "Season", "Year"])
    )

    return g
