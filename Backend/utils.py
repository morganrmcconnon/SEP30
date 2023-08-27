def remove_none_entries(list_of_dicts):
    for d in list_of_dicts:
        keys_to_remove = [key for key, value in d.items() if value is None]
        for key in keys_to_remove:
            del d[key]
    return list_of_dicts

def complete_dict_entries(list_of_dicts):
    all_keys = set()
    for d in list_of_dicts:
        all_keys.update(d.keys())

    for d in list_of_dicts:
        for key in all_keys:
            if key not in d:
                d[key] = None
    return list_of_dicts