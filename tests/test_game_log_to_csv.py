import unittest

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.game_log_to_csv import game_log_to_df, create_df_factory_nb


class TestGameLogToCSV(unittest.TestCase):
    def test_game_log_to_df_one_country(self):
        df = game_log_to_df(os.path.join('data', 'one_country.log'))
        self.assertEqual(2, len(df))
        self.assertEqual(df.loc[0, 'Tag'], 'FRA')
        self.assertEqual(df.loc[1, 'Tag'], 'FRA')
        self.assertEqual(df.loc[0, 'ManpowerK'], '72.694')
        self.assertEqual(df.loc[1, 'ManpowerK'], '73.87')
        self.assertEqual(df.loc[0, 'MilFactory'], '21')
        self.assertEqual(df.loc[1, 'MilFactory'], '21')
        self.assertEqual(df.loc[0, 'Date'], 'Jan-1936')
        self.assertEqual(df.loc[1, 'Date'], 'Feb-1936')

    def test_game_log_to_df_on_noise(self):
        df = game_log_to_df(os.path.join('data', 'real_game.log'))
        self.assertEqual('', df.loc[0, 'Faction'])
        df_FRA = df[df['Tag'] == 'FRA']
        self.assertEqual(6, len(df_FRA))
        self.assertEqual(df_FRA.iloc[0]['ManpowerK'], '128.544')
        self.assertEqual(df_FRA.iloc[3]['ManpowerK'], '85.726')
        self.assertEqual(df_FRA.iloc[0]['CivFactory'], '29')
        self.assertEqual(df_FRA.iloc[3]['CivFactory'], '32')
        self.assertEqual(df_FRA.iloc[0]['Date'], 'Jan-1936')
        self.assertEqual(df_FRA.iloc[3]['Date'], 'Apr-1936')

    def test_create_df_factory_nb(self):
        raw_df = game_log_to_df(os.path.join('data', 'real_game.log'))
        df = create_df_factory_nb(raw_df)
        self.assertEqual(len(raw_df['Country'].unique()), len(df))
        self.assertEqual('Faction', df.columns[0])
        self.assertEqual('Jan-1936', df.columns[1])
        self.assertEqual(59, df.loc['Commune of France']['Jan-1936'])
        self.assertEqual(62, df.loc['Commune of France']['Apr-1936'])
        self.assertEqual(27, df.loc['League of Eight Provinces']['Jan-1936'])
        self.assertEqual(0, df.loc['League of Eight Provinces']['Feb-1936'])
        self.assertEqual(9, df.loc['Nanjing Clique']['Feb-1936'])
        self.assertEqual('Not aligned', df.loc['Switzerland']['Faction'])
