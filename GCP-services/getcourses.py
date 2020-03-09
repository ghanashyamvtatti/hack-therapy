def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('okay done', 204, headers)

   
    
    request_json = request.get_json()
    import flask
    import requests
    import json
    url = "https://sandbox.api.it.nyu.edu/course-catalog-exp/courses"
    header1 = {"Authorization": "Bearer 50075d77-fa22-30ae-a9e2-7dd3e527edee"}
    res = requests.get(url,headers=header1).json()

    response = flask.jsonify(res)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.set( 'Access-Control-Allow-Headers', 'Content-Type')
    return response