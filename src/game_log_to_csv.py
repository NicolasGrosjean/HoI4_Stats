import argparse
import datetime
import os
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(description='Extract and transform game log stats to CSV files')
    parser.add_argument('game_log_path', type=str, help='Path of the game log file containing stats')
    parser.add_argument('raw_csv_path', type=str, help='Path of the output file with extracted raw stats')
    parser.add_argument('pivot_directory', type=str, help='Path of the directory for output files with pivot stats')
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
            stats_pol[0] = (pd.to_datetime(stats_pol[0]) - datetime.timedelta(days=1)).strftime('%Y-%m')
            df_pol = pd.concat((df_pol, pd.DataFrame([stats_pol])), axis=0, ignore_index=True)
        elif 'STATSMIL' in line:
            stats_mil = line[(line.find('STATSMIL') + 12):].split(';')[:-1]
            stats_mil[0] = (pd.to_datetime(stats_mil[0]) - datetime.timedelta(days=1)).strftime('%Y-%m')
            df_mil = pd.concat((df_mil, pd.DataFrame([stats_mil])), axis=0, ignore_index=True)
        elif 'STATSECO' in line:
            stats_eco = line[(line.find('STATSECO') + 12):].split(';')[:-1]
            stats_eco[0] = (pd.to_datetime(stats_eco[0]) - datetime.timedelta(days=1)).strftime('%Y-%m')
            df_eco = pd.concat((df_eco, pd.DataFrame([stats_eco])), axis=0, ignore_index=True)
    df_pol.columns = ['Date', 'Tag', 'Country', 'Ideology', 'Faction']
    df_mil.columns = ['Date', 'Tag', 'ManpowerK', 'Battalions', 'Planes', 'Ships']
    df_eco.columns = ['Date', 'Tag', 'CivFactory', 'MilFactory', 'NavyFactory']
    res = pd.merge(df_pol, df_mil, on=['Date', 'Tag'])
    res = pd.merge(res, df_eco, on=['Date', 'Tag'])
    return res


def create_df_pivot_column(raw_df, column):
    df_column_nb = raw_df[['Date', 'Country', 'Faction', column]].set_index(['Country', 'Faction'])
    df_column_nb = df_column_nb.pivot(index=df_column_nb.index, columns='Date')[column]
    new_col = list()
    for col in df_column_nb.columns:
        new_col.append(pd.to_datetime(col).strftime('%b-%Y'))
    df_column_nb.columns = new_col
    df_column_nb = df_column_nb.fillna(0)
    return df_column_nb


if __name__ == '__main__':
    args = get_args()
    df = game_log_to_df(args.game_log_path)
    df.to_csv(args.raw_csv_path)
    df['Faction'] = df['Faction'].replace('', 'Not aligned')
    df['CivFactory'] = pd.to_numeric(df['CivFactory'])
    df['MilFactory'] = pd.to_numeric(df['MilFactory'])
    df['NavyFactory'] = pd.to_numeric(df['NavyFactory'])
    df['FactoryNb'] = df['CivFactory'] + df['MilFactory'] + df['NavyFactory']
    create_df_pivot_column(df, 'FactoryNb').to_csv(os.path.join(args.pivot_directory, 'factory_nb.csv'))
    create_df_pivot_column(df, 'Battalions').to_csv(os.path.join(args.pivot_directory, 'battalions_nb.csv'))
    create_df_pivot_column(df, 'Planes').to_csv(os.path.join(args.pivot_directory, 'planes_nb.csv'))
    create_df_pivot_column(df, 'Ships').to_csv(os.path.join(args.pivot_directory, 'ships_nb.csv'))
