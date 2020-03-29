import argparse
import datetime
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(description='Extract and transform game log stats to CSV files')
    parser.add_argument('game_log_path', type=str, help='Path of the game log file containing stats')
    parser.add_argument('raw_csv_path', type=str, help='Path of the output file with extracted raw stats')
    parser.add_argument('factories_csv_path', type=str, help='Path of the output file with total factory number stats')
    return parser.parse_args()


def game_log_to_df(game_log_path):
    df_pol = pd.DataFrame()
    df_mil = pd.DataFrame()
    df_eco = pd.DataFrame()
    with open(game_log_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    for line in lines:
        if 'STATSPOL' in line:
            stats_pol = line[(line.find('STATSPOL') + 12):].split(';')[:-1]
            stats_pol[0] = (pd.to_datetime(stats_pol[0]) - datetime.timedelta(days=1)).strftime('%m-%Y')
            df_pol = pd.concat((df_pol, pd.DataFrame([stats_pol])), axis=0, ignore_index=True)
        elif 'STATSMIL' in line:
            stats_mil = line[(line.find('STATSMIL') + 12):].split(';')[:-1]
            stats_mil[0] = (pd.to_datetime(stats_mil[0]) - datetime.timedelta(days=1)).strftime('%m-%Y')
            df_mil = pd.concat((df_mil, pd.DataFrame([stats_mil])), axis=0, ignore_index=True)
        elif 'STATSECO' in line:
            stats_eco = line[(line.find('STATSECO') + 12):].split(';')[:-1]
            stats_eco[0] = (pd.to_datetime(stats_eco[0]) - datetime.timedelta(days=1)).strftime('%m-%Y')
            df_eco = pd.concat((df_eco, pd.DataFrame([stats_eco])), axis=0, ignore_index=True)
    df_pol.columns = ['Date', 'Tag', 'Country', 'Ideology', 'Faction']
    df_mil.columns = ['Date', 'Tag', 'ManpowerK', 'Battalions', 'Planes', 'Ships']
    df_eco.columns = ['Date', 'Tag', 'CivFactory', 'MilFactory', 'NavyFactory']
    res = pd.merge(df_pol, df_mil, on=['Date', 'Tag'])
    res = pd.merge(res, df_eco, on=['Date', 'Tag'])
    return res


def create_df_factory_nb(raw_df):
    raw_df['CivFactory'] = pd.to_numeric(raw_df['CivFactory'])
    raw_df['MilFactory'] = pd.to_numeric(raw_df['MilFactory'])
    raw_df['NavyFactory'] = pd.to_numeric(raw_df['NavyFactory'])
    raw_df['FactoryNb'] = raw_df['CivFactory'] + raw_df['MilFactory'] + raw_df['NavyFactory']
    df_factory_nb = raw_df[['Date', 'Country', 'FactoryNb']].set_index('Country')
    df_factory_nb = df_factory_nb.pivot(index=df_factory_nb.index, columns='Date')['FactoryNb']
    new_col = list()
    for col in df_factory_nb.columns:
        new_col.append(pd.to_datetime(col).strftime('%b-%Y'))
    df_factory_nb.columns = new_col
    df_factory_nb = df_factory_nb.fillna(0)
    df_faction = raw_df[['Country', 'Faction']].drop_duplicates().set_index('Country')
    df_faction['Faction'] = df_faction['Faction'].replace('', 'Not aligned')
    df_faction = df_faction[~df_faction.index.duplicated(keep='last')]
    return df_faction.join(df_factory_nb)


if __name__ == '__main__':
    args = get_args()
    df = game_log_to_df(args.game_log_path)
    df.to_csv(args.raw_csv_path)
    df2 = create_df_factory_nb(df)
    df2.to_csv(args.factories_csv_path)