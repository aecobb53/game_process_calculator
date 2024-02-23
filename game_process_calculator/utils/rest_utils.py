
from urllib.parse import parse_qs as parse_query_string
# from urllib.parse import urlencode as encode_query_string

"""
https://fastapi.tiangolo.com/reference/request/
    scope
    app
    url
    base_url
    headers
    query_params
    path_params
    cookies
    client
    session         SessionMiddleware
    auth            AuthenticationMiddleware
    user            AuthenticationMiddleware
    state
    method
    receive

    url_for
    stream
    body
    json
    form
    close
    is_disconnected
    send_push_promise
"""

def parse_query_params(request, query_class=None, body_class=None):
    """
    Parse query arguments from request
    :param request: request object
    :return: dict of query arguments
    """
    query_params = parse_query_string(str(request.query_params))
    # print(f"Query params: {query_params}")
    # print(f"Query class: {query_class}")
    if query_class:
        query_params = query_class(**query_params)
    # print(f"Query params: {query_params}")
    return query_params
