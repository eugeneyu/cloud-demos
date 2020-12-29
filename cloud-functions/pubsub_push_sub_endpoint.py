import sys,json
from flask import escape

def get_message(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    content_type = request.headers['content-type']
    request_msg = ''
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json:
            request_msg = json.dumps(request_json)
        else:
            raise ValueError("JSON is invalid")
    elif content_type == 'application/octet-stream':
        request_msg = request.data
    elif content_type == 'text/plain':
        request_msg = request.data
    elif content_type == 'application/x-www-form-urlencoded':
        request_msg = json.dumps(request.form)
    else:
        raise ValueError("Unknown content type: {}".format(content_type))
    return 'Message:\n {}!\n'.format(escape(request_msg))



def process_request(request):
    #sys.stdout.write("test\n")    
    msg = get_message(request)
    sys.stdout.write(msg)