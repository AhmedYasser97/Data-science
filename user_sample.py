import pandas as pd
import numpy as np

data = pd.read_csv("user_data.csv")
sample = data.sort_values(by=['user_id'])

for index, row in sample.iterrows():
	current_user = row['user_id']
	split_user = current_user.split('_')
	sample['user_id'].replace(current_user,split_user[1], inplace = True)

sample.user_id = sample.user_id.astype('int64')
sample = sample[sample.user_id <= 2200]
final_sample = sample.sort_values(by=['user_id'])

final_sample.to_csv('user_sample.csv', sep=',')