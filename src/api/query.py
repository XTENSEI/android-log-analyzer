def parse_query(query_string):
    params = {}
    if '?' in query_string:
        query_string = query_string.split('?')[1]
    
    for param in query_string.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            params[key] = value
    
    return params

def build_query(params):
    return '&'.join(f"{k}={v}" for k, v in params.items())
