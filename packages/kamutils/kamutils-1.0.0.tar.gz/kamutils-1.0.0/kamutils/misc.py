#-----------------------------------------------------------------------------------------
# Miscellaneous Functions
#-----------------------------------------------------------------------------------------

# Convert all keys to lowercase recursively
def lower_all_keys(obj):
	if isinstance(obj,dict):
		return {(k.lower() if isinstance(k,str) else k) : lower_all_keys(v) for k, v in obj.items()}
	elif isinstance(obj, (list, set, tuple)):
		t = type(obj)
		return t(lower_all_keys(o) for o in obj)
	else:
		return obj

# Convert first-level keys to lowercase
def lower_first_level_keys(obj):
	if isinstance(obj,dict):
		return {(k.lower() if isinstance(k,str) else k) : v for k, v in obj.items()}
	elif isinstance(obj, (list, set, tuple)):
		t = type(obj)
		return t(lower_first_level_keys(o) for o in obj)
	else:
		return obj
