import logging

import requests
import pandas as pd
from bs4 import BeautifulSoup
import plotly_express as px
from ReportCard import ReportCard
from HomePrices import HomePrices

class Analysis:
    def __init__(self):
        self.abbreviation_to_name = {
            # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#States.
            "AK": "Alaska",
            "AL": "Alabama",
            "AR": "Arkansas",
            "AZ": "Arizona",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "IA": "Iowa",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "MA": "Massachusetts",
            "MD": "Maryland",
            "ME": "Maine",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MO": "Missouri",
            "MS": "Mississippi",
            "MT": "Montana",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "NE": "Nebraska",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NV": "Nevada",
            "NY": "New York",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VA": "Virginia",
            "VT": "Vermont",
            "WA": "Washington",
            "WI": "Wisconsin",
            "WV": "West Virginia",
            "WY": "Wyoming",
            # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Federal_district.
            "DC": "District of Columbia",
            # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Inhabited_territories.
            "AS": "American Samoa",
            "GU": "Guam GU",
            "MP": "Northern Mariana Islands",
            "PR": "Puerto Rico PR",
            "VI": "U.S. Virgin Islands",
        }

    def plot_home_prices(self, home_price_df: pd.DataFrame = None):
        name_to_abbreviation = {v: k for k, v in self.abbreviation_to_name.items()}
        home_price_df['state'] = home_price_df['State or territory'].map(name_to_abbreviation)

        fig = px.choropleth(home_price_df,
                            locations='state',
                            locationmode='USA-states',
                            color='amount',
                            hover_name='state',
                            color_continuous_scale='Greens',
                            scope='usa',
                            labels={'amount': 'Median Home Price (US$)'},
                            title='Median Home Price by State')

        fig.show()

    @staticmethod
    def plot_test_scores(report_card_df: pd.DataFrame = None):
        fig = px.choropleth(report_card_df,
                            locations='jurisdiction',
                            locationmode='USA-states',
                            color='value',
                            hover_name='jurisdiction',
                            color_continuous_scale='Blues',
                            scope='usa',
                            labels={'value': '% basic compentency at math'},
                            title='Percent of 4th graders at or above basic math')
        fig.show()

    @staticmethod
    def compute_ratio(report_card_df: pd.DataFrame = None, home_price_df: pd.DataFrame = None):
        analysis_df = report_card_df.merge(home_price_df, left_on='jurisdiction', right_on='state' ,
                             how='inner')
        analysis_df['ratio'] = (analysis_df.value / analysis_df.amount) * 100000
        print(analysis_df.sort_values(by='ratio')[['state', 'ratio']].head(10))
        print(analysis_df.sort_values(by='ratio')[['state', 'ratio']].tail(10))

        fig = px.choropleth(analysis_df,
                            locations='jurisdiction',
                            locationmode='USA-states',
                            color='ratio',
                            hover_name='jurisdiction',
                            color_continuous_scale='Cividis',
                            scope='usa',
                            labels={'ratio': 'math basic competency percentage point per % of home price'},
                            title='Ratio of student math basic competency to median home price')
        fig.show()


if __name__ == '__main__':
    home_prices = HomePrices().compile_homeprices()
    analysis = Analysis()
    analysis.plot_home_prices(home_price_df=home_prices)
    math_df = ReportCard().compile_math_prof()
    analysis.plot_test_scores(report_card_df=math_df)
    analysis.compute_ratio(report_card_df=math_df, home_price_df=home_prices)

