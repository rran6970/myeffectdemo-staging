import json
from django.http import HttpResponseServerError, HttpResponseForbidden, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

class GenericRequest(object):
    """
    All request classes should extend this class.
    """
    def __init__(self, request):
        """
        Subclasses may override the init method to initialize additional parameters.
        """
        self.params = {}
        self.http_request = request

    def parse_request_params(self):
        """
        This method populate the self.params dictionary object from the HTTP request
        """
        print type(self.http_request.POST), self.http_request.GET, '#'*20
        if self.http_request.method == "POST":
            try:
                for key, value in json.loads(self.http_request.body).iteritems():
                    self.params.__setitem__(key, value)
                print self.params
            except:
                self.parse_error = "Invalid json input in request."
        elif self.http_request.method == "GET":
            try:
                for item in self.http_request.GET:
                    self.params.update({item: self.http_request.GET[item]})
            except:
                self.parse_error = "Invalid json input in request."
        else:
            self.parse_error = "Request is neither GET nor POST."


class GenericResponse(object):
    """
    All response classes should extend this class.
    """
    def __init__(self):
        """
        Subclasses may override the init method to initialize additional parameters.
        """
        self.response = {}

    def dump_response_to_json(self):
        """
        This method returns the converts the object's response dictionary to JSON.
        """
        return json.dumps(self.response, cls=DjangoJSONEncoder)

    def send_json_response(self):
        """
        This method sends the HTTPResponse as json.
        """
        return HttpResponse(self.dump_response_to_json(), "application/json")

    def render_to_template(self, template, request, *args, **kwargs):
        """
        This function will render the request context and extra context to the template name passed.
        """
        return render_to_response(template, self.response, context_instance=RequestContext(request))

    def create_response(self, request_obj, *args, **kwargs):
        """
        Sub-Classes *should* override this method to return a HTTPResponse object.
        """
        pass

def send_server_error(msg, **kwargs):
    """
    Returns a 500 Http error.
    """
    if kwargs and type(kwargs['data']) is dict:
        if kwargs['data']:
            error_dict = {}
        else:
            error_dict = {}
    else:
        error_dict = {}
    if type(msg) is list:
        error_dict['errorMessages'] = [x for x in msg]
    else:
        error_dict['errorMessages'] = [msg]
    error_dict['status'] = -1
    return HttpResponseServerError(json.dumps(error_dict), "application/json")


class ResponseDic(GenericResponse):
    def __init__(self):
        super(ResponseDic, self).__init__()
        self.response = {
            'data': {},
            'errorMessages': [],
            'status': 1
        }


def send_server_forbidden(msg):
    """
    Returns a 403 Http error.
    """
    error_dict = {'data': None}
    if type(msg) is list:
        error_dict['errorMessages'] = [x for x in msg]
    else:
        error_dict['errorMessages'] = [msg]
    error_dict['status'] = -1
    return HttpResponseForbidden(json.dumps(error_dict), "application/json")


def remove_cache(function):

    def add_cache_control_header(request, *args, **kwargs):
        response = function(request)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 0
        return response

    return add_cache_control_header


def clean_inputs(iparams, inputs, required):
    if [i for i in inputs if i not in iparams]: 
        return "Missing Input params"
    if [i for i in required if not iparams[i]]:
        return "required feild cannot be null"

def check_post(function):
    """
    Decorator function to check if the request is done with POST.
    """
    def is_post(request, *args, **kwargs):
        if request.method != "POST":
            return send_server_forbidden("Request is not POST.")
        else:
            return function(request, *args, **kwargs)
    return is_post


def createResponse(returnDict):
    """
    Method to create a json http response with success status code
    @param returnDict: a dict of values to be returned for the ajax call
    """
    response = HttpResponse()
    response.status_code = 200
    response.write(json.dumps(returnDict))
    response['Content-Type'] = 'application/json'
    return response