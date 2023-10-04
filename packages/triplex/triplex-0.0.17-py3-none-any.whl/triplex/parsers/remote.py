import requests, pandas

from ..dfas import DFA
from ..parsers.utils import Parser


class RemoteIE(Parser):
    def __init__(self):
        self._url = 'http://165.1.75.234'
        self.server_url = f"{self._url}:5011/text"
        self.model = "gpt-4-0613"

    def parse(self, text: str) -> DFA:
        inputs = {'model': self.model,
                  'text': text,
                  'entities': list()}

        response = requests.post(self.server_url, json=inputs).json()
        df = pandas.DataFrame(response['triplets'])
        triples = list()
        for _, row in df.iterrows():
            triples.append([row["subject"], row["relation"].lower(), row["object"]])

        # triples = clean(triples)
        dfa = DFA(triples, text)

        return dfa
