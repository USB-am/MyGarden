# -*- coding: utf-8 -*-

import json


def main():
	name = 'tonel_old'
	with open('%s.json' % name, mode='r', encoding='utf-8') as map_file:
		old_map = json.load(map_file)
		new_map = []
		for row in old_map:
			r = []
			for col in row:
				r.append(col)
			new_map.append(r)

	with open('%s_new.json' % name, mode='w', encoding='utf-8') as map_file:
		json.dump(new_map, map_file)


if __name__ == '__main__':
	main()