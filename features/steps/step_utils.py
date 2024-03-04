

def compare_things(thing1, thing2, verbose=False):
    """Compare two things."""
    if verbose:
        print(f"Comparing {thing1} and {thing2}")
        print(f"Type of thing1: {type(thing1)}")
        print(f"Type of thing2: {type(thing2)}")
    if isinstance(thing1, dict) and isinstance(thing2, dict):
        return compare_dicts(thing1, thing2)

def compare_dicts(dct1, dct2):
    """Compare two dictionaries."""
    errors = []
    keys1 = list(dct1.keys())
    keys2 = list(dct2.keys())

    if len(keys1) != len(keys2):
        errors.append(f"Expected {len(keys1)} keys, but got {len(keys2)} keys")
    for key in keys1:
        if key not in keys2:
            errors.append(f"Expected key [{key}] to be in dict2 but only found [{keys2}]")
        if type(dct1[key]) != type(dct2[key]):
            errors.append(f"Expected key {key} types to match [{dct1[key]}] to be [{dct2[key]}]")
        if isinstance(dct1[key], dict):
            temp_errors = compare_dicts(dct1[key], dct2[key])
            if temp_errors:
                errors.append(f"Exception at key [{key}]")
                errors.extend(temp_errors)
        elif isinstance(dct1[key], list):
            temp_errors = compare_lists(dct1[key], dct2[key])
            if temp_errors:
                errors.append(f"Exception at key [{key}]")
                errors.extend(temp_errors)
        else:
            temp_errors = compare_values(dct1[key], dct2[key])
            if temp_errors:
                errors.append(f"Exception at key [{key}]")
                errors.extend(temp_errors)
    return errors

def compare_lists(list1, list2):
    """Compare two lists."""
    errors = []
    if len(list1) != len(list2):
        errors.append(f"Expected {len(list1)} items, but got {len(list2)} items")
    for index, (item1, item2) in enumerate(zip(list1, list2)):
        if type(item1) != type(item2):
            errors.append(f"Expected item types to match [{item1}] to be [{item2}]")
        if isinstance(item1, dict):
            temp_error = compare_dicts(item1, item2)
            if temp_error:
                errors.append(f'Exception at item index [{index}]')
                errors.extend(temp_error)
        elif isinstance(item1, list):
            temp_error = compare_lists(item1, item2)
            if temp_error:
                errors.append(f'Exception at item index [{index}]')
                errors.extend(temp_error)
        else:
            temp_error = compare_values(item1, item2)
            if temp_error:
                errors.append(f'Exception at item index [{index}]')
                errors.extend(temp_error)
    return errors

def compare_values(value1, value2):
    """Compare two values."""
    if value1 != value2:
        return [f"Expected [{value1}], but got [{value2}]"]
    return []
