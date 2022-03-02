from re import I
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
                "GNI per capita, Atlas method (current US$)",
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

    region_map = {
        "East Asian and Pacitif": [
            "American Samoa",
            "Australia",
            "Brunei Darussalam",
            "Cambodia",
            "China",
            "Fiji",
            "French Polynesia",
            "Guam",
            "Hong Kong SAR, China",
            "Indonesia",
            "Japan",
            "Kiribati",
            "Korea, Dem. People's Rep.",
            "Korea, Rep.",
            "Korea Rep.",
            "Lao PDR",
            "Macao SAR, China",
            "Malaysia",
            "Marshall Islands",
            "Micronesia, Fed. Sts.",
            "Mongolia",
            "Myanmar",
            "Nauru",
            "Nauru Ne",
            "New Caledonia",
            "Caledonia",
            "New Zealand",
            "Northern Mariana Islands",
            "Palau",
            "Papua New Guinea",
            "Philippines",
            "Samoa",
            "Singapore",
            "Solomon Islands",
            "Thailand",
            "Timor-Leste",
            "Tonga",
            "Tuvalu",
            "Vanuatu",
            "Vietnam",
        ],
        "Europe and Central Asia": [
            "Albania",
            "Andorra",
            "Armenia",
            "Austria",
            "Azerbaijan",
            "Belarus",
            "Belgium",
            "Bosnia",
            "Bosnia and Herzegovina",
            "Herzegovina",
            "Bulgaria",
            "Channel Islands",
            "Croatia",
            "Cyprus",
            "Czech Republic",
            "Denmark",
            "Estonia",
            "Faroe Islands",
            "Finland",
            "France",
            "Georgia",
            "Germany",
            "Gibraltar",
            "Greece",
            "Greenland",
            "Hungary",
            "Iceland",
            "Ireland",
            "Isle of Man",
            "Italy",
            "Kazakhstan",
            "Kosovo",
            "Kyrgyz Republic",
            "Latvia",
            "Liechtenstein",
            "Lithuania",
            "Luxembourg",
            "Moldova",
            "Monaco",
            "Montenegro",
            "Netherlands",
            "North Macedonia",
            "Norway",
            "Poland",
            "Portugal",
            "Romania",
            "Russian Federation",
            "San Marino",
            "Serbia",
            "Slovak Republic",
            "Slovenia",
            "Spain",
            "Sweden",
            "Switzerland",
            "Tajikistan",
            "Turkey",
            "Turkmenistan",
            "Ukraine",
            "United Kingdom",
            "Uzbekistan",
        ],
        "Latin American and Caribbean": [
            "Antigua",
            "Antigua and Barbuda",
            "Barbuda",
            "Argentina",
            "Aruba",
            "Bahamas, The",
            "Barbados",
            "Belize",
            "Bolivia",
            "Brazil",
            "British",
            "British Virgin Islands",
            "Virgin Islands",
            "Virgin Islands (U.S.)",
            "Cayman Islands",
            "Chile",
            "Colombia",
            "Costa Rica",
            "Cuba",
            "Curacao",
            "Dominica",
            "Dominican Republic",
            "Ecuador",
            "El Salvador",
            "Grenada",
            "Guatemala",
            "Guyana",
            "Haiti",
            "Honduras",
            "Jamaica",
            "Mexico",
            "Nicaragua",
            "Panama",
            "Paraguay",
            "Peru",
            "Puerto Rico",
            "Sint Maarten, Dutch",
            "Sint Maarten (Dutch part)",
            "St. Kitts and Nevis",
            "St. itts Nevis",
            "St. Lucia",
            "St. Martin, (French Part)",
            "St. Martin (French part)",
            "St. Vincent and the Grenadines",
            "St. Vincent",
            "Grenadines",
            "Suriname",
            "Trinidad",
            "Trinidad and Tobago",
            "Tobago",
            "Turks",
            "Caicos Islands",
            "Turks and Caicos Islands",
            "Uruguay",
            "Venezuela, RB",
            "Virgin Islands",
        ],
        "Middle East and North Africa": [
            "Algeria",
            "Bahrain",
            "Djibouti",
            "Egypt, Arab Rep.",
            "Iran, Islamic Rep.",
            "Iraq",
            "Israel",
            "Jordan",
            "Kuwait",
            "Lebanon",
            "Libya",
            "Malta",
            "Morocco",
            "Oman",
            "Qatar",
            "Saudi Arabia",
            "Syrian Arab Republic",
            "Tunisia",
            "United Arab Emirates",
            "West Bank and Gaza",
            "Yemen, Rep.",
        ],
        "North America": ["Bermuda", "Canada", "United States"],
        "South Asia": [
            "Afghanistan",
            "Bangladesh",
            "Bhutan",
            "India",
            "Maldives",
            "Nepal",
            "Pakistan",
            "Sri Lanka",
        ],
        "Sub-Saharan Africa": [
            "Angola",
            "Benin",
            "Botswana",
            "Burkina",
            "Burkina Faso",
            "Faso",
            "Burundi",
            "Cabo Verde",
            "Cameroon",
            "Central African Republic",
            "Chad",
            "Comoros",
            "Congo, Dem. Rep.",
            "Congo, Rep.",
            "Cote d'Ivoire",
            "Equatorial Guinea",
            "Eritrea",
            "Eswatini",
            "Ethiopia",
            "Gabon",
            "Gambia, The",
            "Ghana",
            "Guinea",
            "Guinea-Bissau",
            "Kenya",
            "Lesotho",
            "Liberia",
            "Madagascar",
            "Malawi",
            "Mali",
            "Mauritania",
            "Mauritius",
            "Mozambique",
            "Namibia",
            "Niger",
            "Nigeria",
            "Rwanda",
            "Sao Tome and Principe",
            "Senegal",
            "Seychelles",
            "Sierra Leone",
            "Somalia",
            "South Africa",
            "South Sudan",
            "Sudan",
            "Tanzania",
            "Togo",
            "Uganda",
            "Zambia",
            "Zimbabwe",
        ],
    }

    wdi_ind_pivot["Region"] = ""
    for region_name, countries in region_map.items():
        wdi_ind_pivot["Region"] = wdi_ind_pivot.apply(
            lambda row: region_name
            if row["Country Name"] in countries
            else row["Region"],
            axis=1,
        )

    # TODO remove this line
    # wdi_ind_pivot = pd.read_csv(output_file)

    income_mappings = {}

    def classify_income(country, gni):
        income_class = ""
        if gni > 12696:
            income_class = "High income"
        elif gni > 4096:
            income_class = "Upper middle income"
        elif gni > 1054:
            income_class = "Lower middle income"
        else:
            income_class = "Low income"

        income_mappings[country] = income_class

    wdi_2018 = wdi_ind_pivot[wdi_ind_pivot["Year"] == "2018"]
    wdi_2018.apply(
        lambda row: classify_income(
            row["Country Name"], row["GNI per capita, Atlas method (current US$)"]
        ),
        axis=1,
    )

    wdi_ind_pivot["Income"] = wdi_ind_pivot.apply(
        lambda row: income_mappings[row["Country Name"]],
        axis=1,
    )

    wdi_ind_pivot.to_csv(output_file)
