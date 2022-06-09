import pandas as pd

data = pd.read_csv('all_merged_scaled_ur.csv', index_col=0)

columns = ['age_avg', 'employment_rate', 'new_building', 'area_new_b', 'rooms_new_b', 'cinema', 'cinema_seat', 'museum',
       'apartment', 'restaurant']

default_weights = dict(zip(columns, [1] * 10))

def calc_score(weights=default_weights):
    data['w_score'] = [0] * 16
    for col in columns:
        data['w_score'] += data['scaled_%s' % col] * weights[col]
    return data[['state', 'w_score']].sort_values(by='w_score', ascending=False)