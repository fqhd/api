import pandas as pd
import json

df = pd.read_csv('champions.csv')

def create_champion_to_id():
	with open('champion.json', encoding='utf-8') as f:
		champion = json.load(f)
	champion = champion['data']
	dic = {}
	for c in champion.keys():
		dic[champion[c]['name']] = c
	return dic

champ_name_to_id = create_champion_to_id()

def get_champ_vec(champ_name):
	arr = []
	champ_name = champ_name_to_id[champ_name]
	row = df.loc[df['Champion'] == champ_name].iloc[0]
	for i in range(1, 16):
		if i == 7:
			if row.iloc[i] == 1:
				arr.append(1)
				arr.append(0)
				arr.append(0)
			elif row.iloc[i] == 2:
				arr.append(0)
				arr.append(1)
				arr.append(0)
			elif row.iloc[i] == 3:
				arr.append(0)
				arr.append(0)
				arr.append(1)
		else:
			arr.append(row.iloc[i] / 10)
	return arr

def parse_state(frame):
	drake_names = ['EARTH_DRAGON', 'WATER_DRAGON', 'FIRE_DRAGON', 'HEXTECH_DRAGON', 'AIR_DRAGON', 'CHEMTECH_DRAGON']
	data = []
	for t in frame['teams']:
		for p in t['players']:
			data += get_champ_vec(p['champion'])
			data.append(p['kills'] / 20)
			data.append(p['deaths'] / 16)
			data.append(p['assists'] / 40)
			data.append(p['baronTimer'] / (3 * 60))
			data.append(p['elderTimer'] / (3 * 60))
			data.append(p['deathTimer'] / 79)
			data.append(p['level'] / 18)
			data.append(p['creepscore'] / 400)
		for d in t['drakes'][:4]:
			oh_drake = [0, 0, 0, 0, 0, 0] # one hot encoded drake
			if d != 'ELDER_DRAGON':
				oh_drake[drake_names.index(d)] = 1
			data += oh_drake
		remaining_drakes = max(4 - len(t['drakes']), 0)
		for _ in range(remaining_drakes):
			oh_drake = [0, 0, 0, 0, 0, 0] # one hot encoded drake
			data += oh_drake
		data.append(t['barons'] / 2)
		data.append(t['elders'] / 2)
		data.append(t['rifts'] / 2)
		data += t['turrets']
		data.append(t['inhibs'][0] / 300)
		data.append(t['inhibs'][1] / 300)
		data.append(t['inhibs'][2] / 300)
	data.append(frame['time'] / (30 * 60))
	return data