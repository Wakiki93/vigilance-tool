from deepdiff import DeepDiff
import sys

def compare_specs(old_spec, new_spec):
    """
    Compare two OpenAPI specifications using DeepDiff and map to change types.
    """
    ddiff = DeepDiff(old_spec, new_spec, ignore_order=True, view='tree')
    differences = []

    # Helper to find 'paths' index
    def get_paths_index(p_list):
        if 'paths' in p_list:
            return p_list.index('paths')
        return -1

    # 1. Removals (Explicit Key Removal)
    if 'dictionary_item_removed' in ddiff:
        for node in ddiff['dictionary_item_removed']:
            path_list = node.path(output_format='list')
            idx = get_paths_index(path_list)
            
            if idx != -1:
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

    # 2. Values Changed (Method Swapping / Complex Changes)
    if 'values_changed' in ddiff:
        for node in ddiff['values_changed']:
            path_list = node.path(output_format='list')
            idx = get_paths_index(path_list)
            
            # Check if this change is ON an endpoint: ['paths', '/users/{id}']
            if idx != -1:
                rel_len = len(path_list) - idx
                api_path = path_list[idx+1] if rel_len > 1 else '?'
                
                if rel_len == 2:
                    # The value of the endpoint dict changed.
                    # This happens if we swap 'get' for 'delete' completely.
                    old_val = node.t1 # Old dict (e.g. {'get': {...}})
                    new_val = node.t2 # New dict (e.g. {'delete': {...}})
                    
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

    # 3. Iterable Item Removed (Parameters)
    if 'iterable_item_removed' in ddiff:
        for node in ddiff['iterable_item_removed']:
            path_list = node.path(output_format='list')
            p_idx = -1
            if 'parameters' in path_list:
                p_idx = path_list.index('parameters')
            paths_idx = get_paths_index(path_list)
            
            if paths_idx != -1 and p_idx != -1 and p_idx > paths_idx:
                api_path = path_list[paths_idx+1]
                method_idx = p_idx - 1
                method = path_list[method_idx] if method_idx > paths_idx else '*'
                differences.append({
                    'type': 'parameter-removed',
                    'path': api_path,
                    'method': method
                })

    # 4. Additions (Required parameter added)
    # Check both iterable_item_added (list) and dictionary_item_added (dict val)
    if 'iterable_item_added' in ddiff:
         for node in ddiff['iterable_item_added']:
            val = node.t2
            path_list = node.path(output_format='list')
            if isinstance(val, dict) and val.get('required') == True:
                 if 'parameters' in path_list:
                     p_idx = path_list.index('parameters')
                     api_path = path_list[1] if len(path_list) > 1 else '?'
                     method = path_list[p_idx-1] if p_idx > 1 else '*'
                     
                     differences.append({
                         'type': 'parameter-required-added',
                         'path': api_path,
                         'method': method
                     })

    # 4b. Dictionary Item Added (New Parameters list)
    if 'dictionary_item_added' in ddiff:
        for node in ddiff['dictionary_item_added']:
            path_list = node.path(output_format='list')
            sys.stderr.write(f"DEBUG: Dict Added path: {path_list}\n")
            
            # Check if 'parameters' key was added
            if path_list and path_list[-1] == 'parameters':
                val = node.t2
                # val should be a list of parameters
                if isinstance(val, list):
                    for param in val:
                         if isinstance(param, dict) and param.get('required') == True:
                             # found required param in new list
                             # path_list: ['paths', '/items', 'post', 'parameters']
                             paths_idx = get_paths_index(path_list)
                             if paths_idx != -1:
                                 api_path = path_list[paths_idx+1]
                                 method = path_list[paths_idx+2]
                                 
                                 differences.append({
                                     'type': 'parameter-required-added',
                                     'path': api_path,
                                     'method': method
                                 })
    
    return {'differences': differences}
