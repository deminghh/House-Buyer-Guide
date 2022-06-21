import pandas as pd


data = pd.read_csv('all_merged_scaled_ur.csv', index_col=0)

columns = ['age_avg', 'employment_rate', 'new_building', 'area_new_b', 'rooms_new_b', 'cinema_seat', 'museum',
           'apartment', 'restaurant', 'living_space_1000qm', 'pop_diff', 'house_price_€/m²', 'salary', 'babyboomer_percentage']

default_weights = {'age_avg': 2, 'new_building': 2,
                   'area_new_b': 2, 'rooms_new_b': 2,
                   'cinema_seat': 1, 'salary': 3,
                   'museum': 1, 'apartment': 2,
                   'restaurant': 1, 'employment_rate': 3,
                   'living_space_1000qm': 3,
                   'pop_diff': 1, 'house_price_€/m²': 3, 'babyboomer_percentage': 2}


def calc_score(weights=default_weights):
    data['w_score'] = [0] * 16
    for col in columns:
        data['w_score'] += data['scaled_%s' % col] * weights[col]
    data['avg_score'] = data['w_score'] / sum(weights.values())
    data.w_score = round(data.w_score, 2)
    return data.sort_values(by='avg_score', ascending=False).reset_index()[['state', 'avg_score']]


avg_columns = ['scaled_employment_rate', 'scaled_house_price_€/m²', 'scaled_salary',
               'demographics', 'entertainment', 'new_building', 'scaled_living_space_1000qm', 'scaled_apartment']


def calc_avg_score(weights):
    data['w_score'] = [0] * 16
    for col in avg_columns:
        if weights[col] < 0:
            data['w_score'] += (1 - data[col]) * -weights[col]
        else:
            data['w_score'] += data[col] * weights[col]
    sum_of_weights = sum(map(abs, weights.values()))
    data['avg_score'] = data['w_score'] / sum_of_weights
    data.w_score = round(data.w_score, 2)
    return data.sort_values(by='avg_score', ascending=False).reset_index()[['state', 'avg_score']]
