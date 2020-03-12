from flask import escape, jsonify, send_file
from tceq import API

"""
Main functions start
"""

tceq = API()

def api(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    # request_json = request.get_json(silent=True)

    sites = tceq.get_sites()

    # Format request
    return jsonify(request.path)
