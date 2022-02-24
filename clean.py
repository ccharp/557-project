import pandas as pd
import os


def clean(output_file):
    wdi_df = pd.read_excel(os.path.join("data", "WDIEXCEL.xlsx"))
    series_df = pd.read_excel(
        os.path.join("data", "WDIEXCEL.xlsx"), sheet_name="Series"
    )

    wdi_merge = pd.merge(
        wdi_df, series_df, how="left", left_on="Indicator Code", right_on="Series Code"
    )
    wdi_final = wdi_merge.drop(
        [
            "Indicator Name_y",
            "Short definition",
            "Long definition",
            "Unit of measure",
            "Periodicity",
            "Base Period",
            "Other notes",
            "Aggregation method",
            "Limitations and exceptions",
            "Notes from original source",
            "General comments",
            "Source",
            "Statistical concept and methodology",
            "Development relevance",
            "Related source links",
            "Other web links",
            "Related indicators",
            "License Type",
            "Series Code",
        ],
        axis=1,
    )
    wdi_final = wdi_final[
        wdi_final["Topic"].isin(
            [
                "Environment: Agricultural production",
                "Environment: Land use",
                "Economic Policy & Debt: Balance of payments: Current account: Goods, services & income",
                "Environment: Energy production & use",
                "Environment: Emissions",
                "Environment: Biodiversity & protected areas",
                "Environment: Density & urbanization",
                "Infrastructure: Transportation",
                "Environment: Freshwater",
                "Public Sector: Government finance: Deficit & financing",
                "Public Sector: Policy & institutions",
                "Public Sector: Defense & arms trade",
                "Economic Policy & Debt: National accounts: US$ at current prices: Expenditure on GDP",
                "Economic Policy & Debt: National accounts: US$ at constant 2015 prices: Expenditure on GDP",
                "Economic Policy & Debt: National accounts: Growth rates",
                "Environment: Natural resources contribution to GDP",
                "Economic Policy & Debt: National accounts: US$ at current prices: Aggregate indicators",
                "Economic Policy & Debt: National accounts: US$ at constant 2015 prices: Aggregate indicators",
                "Health: Mortality",
                "Poverty: Income distribution",
                "Poverty: Poverty rates",
                "Social Protection & Labor: Economic activity",
                "Social Protection & Labor: Migration",
                "Private Sector & Trade: Travel & tourism",
                "Private Sector & Trade: Total merchandise trade",
                "Private Sector & Trade: Imports",
                "Private Sector & Trade: Exports",
                "Health: Population: Structure",
            ]
        )
    ]
    wdi_final = wdi_final[
        wdi_final["Indicator Name_x"].isin(
            [
                "Access to electricity (% of population)",
                "Urban population (% of total population)",
                "Urban population growth (annual %)",
                "Population, total",
                "Population density (people per sq. km of land area)",
                "Population, total",
                "Rural population",
                "Urban population",
                "Employment in agriculture (% of total employment)",
                "GDP (current US$)",
                "GDP growth (annual %)",
                "GDP per capita (constant 2015 US$)",
                "Agricultural land (% of land area)",
                "Arable land (% of land area)",
                "Forest area (% of land area)",
                "Land area (sq. km)",
                "Permanent cropland (% of land area)",
                "Terrestrial and marine protected areas (% of total territorial area)",
            ]
        )
    ]

    wdi_melt_years = pd.melt(
        wdi_final,
        id_vars=[
            "Country Name",
            "Country Code",
            "Indicator Name_x",
            "Indicator Code",
            "Topic",
        ],
        value_vars=map(str, range(1960, 2021)),
        var_name=["Year"],
    )

    wdi_filtered = wdi_melt_years[wdi_melt_years["Year"].astype(int) >= 1990]
    wdi_filtered.to_csv(os.path.join("data", "filtered.csv"))

    wdi_ind_pivot = pd.pivot_table(
        wdi_filtered,
        values="value",
        index=["Country Name", "Year"],
        columns="Indicator Name_x",
    ).reset_index()

    wdi_ind_pivot.to_csv(output_file)
