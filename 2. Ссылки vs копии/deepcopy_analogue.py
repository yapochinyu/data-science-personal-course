def my_deepcopy(obj, memo=None):
    if memo is None:
        memo = {}
    
    obj_id = id(obj)
    if obj_id in memo:
        return memo[obj_id]
    
    if isinstance(obj, list):
        copy = []
        memo[obj_id] = copy
        for item in obj:
            copy.append(my_deepcopy(item, memo))
        return copy
    else:
        return obj