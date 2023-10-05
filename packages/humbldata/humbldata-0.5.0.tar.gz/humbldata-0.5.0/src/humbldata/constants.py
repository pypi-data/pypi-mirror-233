"""Defining Project-Level Constants"""

# Locking in specific iv_endpoints to choose from
IV_ENDPOINTS: list[str] = [
    "strikesHistory",
    "ivRankHistory",
    "summariesHistory",
    "coreDataHistory",
]

# Columns to select for the vol_premia calculation
IV_COLUMNS: dict[str, list[str]] = {
    "strikesHistory": None,
    "ivRankHistory": ["iv"],
    "summariesHistory": ["iv30d", "exErnIv30d", "fwd60_30"],
    "coreDataHistory": [
        "atmIvM1",
        "atmIvM2",
        "atmIvM3",
        "atmIvM4",
        "iv30d",
    ],
}

RV_COLUMNS: dict[str, list[str]] = {
    "orats_hv": ["clsHv10d", "clsHv20d", "clsHv30d"],
    "std": "Volatility_pct",
    "parkinson": "Volatility_pct",
    "garman_klass": "Volatility_pct",
    "hodges_tompkins": "Volatility_pct",
    "rogers_satchell": "Volatility_pct",
    "yang_zhang": "Volatility_pct",
    "squared_returns": "Volatility_pct",
}

RV_METHODS = (
    "std",
    "parkinson",
    "garman_klass",
    "hodges_tompkins",
    "rogers_satchell",
    "yang_zhang",
    "squared_returns",
    "orats_hv",
)

ORATS_ENDPOINTS: dict[str] = {
    "tickers": "tickers",
    "strikes": "strikes",
    "strikesHistory": "hist/strikes",
    "strikesByOptions": "strikes/options",
    "strikesHistoryByOptions": "hist/strikes/options",
    "moniesImplied": "monies/implied",
    "moniesForecast": "monies/forecast",
    "moniesImpliedHistory": "hist/monies/implied",
    "moniesForecastHistory": "hist/monies/forecast",
    "smvSummaries": "summaries",
    "summariesHistory": "hist/summaries",
    "coreData": "cores",
    "coreDataHistory": "hist/cores",
    "dailyPrice": "hist/dailies",
    "historicalVolatility": "hist/hvs",
    "dividendHistory": "hist/divs",
    "earningsHistory": "hist/earnings",
    "stockSplitHistory": "hist/splits",
    "ivRank": "ivrank",
    "ivRankHistory": "hist/ivrank",
}

ORATS_BASE_URL: str = "https://api.orats.io/datav2/"
