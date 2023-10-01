


def START (PATH_STATUSES):
	STATUS = {
		"PATHS": PATH_STATUSES,
		"STATS": {
			"EMPTY": 0,
			"CHECKS": {
				"PASSES": 0,
				"ALARMS": 0
			}
		}
	}

	for PATH in PATH_STATUSES:
		if ("EMPTY" in PATH and PATH ["EMPTY"] == True):
			STATUS ["STATS"] ["EMPTY"] += 1
			continue;
			
		STATUS ["STATS"] ["CHECKS"] ["PASSES"] += PATH ["STATS"] ["PASSES"]
		STATUS ["STATS"] ["CHECKS"] ["ALARMS"] += PATH ["STATS"] ["ALARMS"]
		

	return STATUS