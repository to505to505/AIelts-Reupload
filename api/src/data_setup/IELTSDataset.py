from pathlib import Path
import pandas as pd

class IELTSDataset():
    ''' Class for dataset logic, might get more complex in the future '''
    def __init__(self, name):
        self.name = name

        PROJECT_ROOT = Path(__file__).resolve().parent.parent
        self.url = PROJECT_ROOT / "data" / "speaking.csv"
        self.df = None
        if self.name == 'BetaBase':

            self.df = pd.read_csv(self.url).loc[lambda x: ~x["id"].isin([0, 3, 9, 15, 36, 39, 42, 48, 54, 57, 105, 108, 111, 129, 147]), :]

