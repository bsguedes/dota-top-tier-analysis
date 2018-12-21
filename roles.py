class Roles:
	@staticmethod
	def evaluate_roles(match_summary, match_object, match_id):
		lane_role = {1: "safe", 2: "mid", 3: "offlane", 4: "jungle"}
		roles = {1: "hard carry", 2: "mid", 3: "offlane", 4: "support", 5: "hard support"}
		roles = list()
		team_players = match_object['players']
		pnk_players = match_summary['players']
		if match_summary['is_radiant']:
			team_players = team_players[0:5]
		else:
			team_players = team_players[5:10]
		mid_players = [x for x in team_players if x['lane_role'] == 2]
		safe_players = [x for x in team_players if x['lane_role'] == 1]
		off_players = [x for x in team_players if x['lane_role'] == 3]					
		return '%i-%i-%i' % (len(safe_players), len(mid_players), len(off_players))
