from deepdiff import DeepDiff


def _get_paths_index(path_list):
    """Helper to find 'paths' index in a path list."""
    if 'paths' in path_list:
        return path_list.index('paths')
    return -1


def _process_dictionary_removals(ddiff):
    """Process dictionary item removals to detect endpoint/method removals."""
    differences = []
    if 'dictionary_item_removed' not in ddiff:
        return differences

    for node in ddiff['dictionary_item_removed']:
        path_list = node.path(output_format='list')
        idx = _get_paths_index(path_list)

        if idx == -1:
            continue

        rel_len = len(path_list) - idx
        api_path = path_list[idx+1] if rel_len > 1 else '?'

        # Endpoint removed: ['paths', '/users/{id}']
        if rel_len == 2:
            differences.append({
                'type': 'endpoint-removed',
                'path': api_path,
                'method': '*',
                'severity': 'breaking'
            })
        # Method removed: ['paths', '/users/{id}', 'get']
        elif rel_len == 3:
            method = path_list[idx+2]
            differences.append({
                'type': 'method-removed',
                'path': api_path,
                'method': method,
                'severity': 'breaking'
            })

    return differences


def _process_values_changed(ddiff):
    """Process value changes to detect method swapping."""
    differences = []
    if 'values_changed' not in ddiff:
        return differences

    for node in ddiff['values_changed']:
        path_list = node.path(output_format='list')
        idx = _get_paths_index(path_list)

        if idx == -1:
            continue

        rel_len = len(path_list) - idx
        api_path = path_list[idx+1] if rel_len > 1 else '?'

        if rel_len == 2:
            # The value of the endpoint dict changed.
            # This happens if we swap 'get' for 'delete' completely.
            old_val = node.t1
            new_val = node.t2

            if isinstance(old_val, dict) and isinstance(new_val, dict):
                # check for removed methods
                for method in old_val.keys():
                    if method not in new_val:
                        differences.append({
                            'type': 'method-removed',
                            'path': api_path,
                            'method': method,
                            'severity': 'breaking'
                        })

    return differences


def _process_iterable_removals(ddiff):
    """Process iterable item removals to detect parameter removals."""
    differences = []
    if 'iterable_item_removed' not in ddiff:
        return differences

    for node in ddiff['iterable_item_removed']:
        path_list = node.path(output_format='list')
        p_idx = -1
        if 'parameters' in path_list:
            p_idx = path_list.index('parameters')
        paths_idx = _get_paths_index(path_list)

        if paths_idx != -1 and p_idx != -1 and p_idx > paths_idx:
            api_path = path_list[paths_idx+1]
            method_idx = p_idx - 1
            method = path_list[method_idx] if method_idx > paths_idx else '*'
            differences.append({
                'type': 'parameter-removed',
                'path': api_path,
                'method': method
            })

    return differences


def _process_iterable_additions(ddiff):
    """Process iterable item additions to detect required parameter additions."""
    differences = []
    if 'iterable_item_added' not in ddiff:
        return differences

    for node in ddiff['iterable_item_added']:
        val = node.t2
        path_list = node.path(output_format='list')
        if isinstance(val, dict) and val.get('required') is True:
            if 'parameters' in path_list:
                p_idx = path_list.index('parameters')
                api_path = path_list[1] if len(path_list) > 1 else '?'
                method = path_list[p_idx-1] if p_idx > 1 else '*'

                differences.append({
                    'type': 'parameter-required-added',
                    'path': api_path,
                    'method': method
                })

    return differences


def _process_dictionary_additions(ddiff):
    """Process dictionary additions to detect new required parameters."""
    differences = []
    if 'dictionary_item_added' not in ddiff:
        return differences

    for node in ddiff['dictionary_item_added']:
        path_list = node.path(output_format='list')

        # Check if 'parameters' key was added
        if not path_list or path_list[-1] != 'parameters':
            continue

        val = node.t2
        # val should be a list of parameters
        if not isinstance(val, list):
            continue

        for param in val:
            if isinstance(param, dict) and param.get('required') is True:
                # found required param in new list
                # path_list: ['paths', '/items', 'post', 'parameters']
                paths_idx = _get_paths_index(path_list)
                if paths_idx != -1:
                    api_path = path_list[paths_idx+1]
                    method = path_list[paths_idx+2]

                    differences.append({
                        'type': 'parameter-required-added',
                        'path': api_path,
                        'method': method
                    })

    return differences


def compare_specs(old_spec, new_spec):
    """
    Compare two OpenAPI specifications using DeepDiff and map to change types.
    """
    ddiff = DeepDiff(old_spec, new_spec, ignore_order=True, view='tree')
    differences = []

    # Process different types of changes
    differences.extend(_process_dictionary_removals(ddiff))
    differences.extend(_process_values_changed(ddiff))
    differences.extend(_process_iterable_removals(ddiff))
    differences.extend(_process_iterable_additions(ddiff))
    differences.extend(_process_dictionary_additions(ddiff))

    return {'differences': differences}
