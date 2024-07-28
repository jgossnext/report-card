import logging

import requests
import pandas as pd

class ReportCard:
    def __init__(self):
        self.grade = '4'
        self.year = '2022'
        self.stattype = 'ALC:AB'
        self.variable = 'TOTAL'
        self.subject = 'mathematics'
        self.subscale = 'MRPRCM'

        self.url = f"""https://www.nationsreportcard.gov/DataService/GetAdhocData.aspx?type=data&grade={self.grade}&year={self.year}&stattype={self.stattype}&variable={self.variable}&subject={self.subject}"""
        self.states = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA",
          "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO",
          "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK",
          "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI",
          "WV", "WY", "DC"]
    def get_report_card(self, state: str = 'NT') -> dict:
        formatted_url = self.url + f'&jurisdiction={state}'
        print(formatted_url)
        response = requests.get(formatted_url)
        return response.json()

    @staticmethod
    def clean_report_card(response_object: dict) -> dict:
        res = response_object['result'][0]
        return res

    def compile_math_prof(self) -> pd.DataFrame:
        all_responses = []
        for state in self.states:
            try:
                res = self.get_report_card(state=state)
            except Exception as e:
                logging.warning(f'Failed to retrieve data for {state}, {e}')
                continue
            clean_res = self.clean_report_card(res)
            all_responses.append(clean_res)

        return pd.DataFrame(all_responses)