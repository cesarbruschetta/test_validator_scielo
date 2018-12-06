from django.http import HttpResponse, JsonResponse

from django.views import View

from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView


from packtools import XMLValidator

class HomePage(View):
    """ class to homePage view """

    def get(self, request, *args, **kwargs):
        """ Home page """
        return HttpResponse('Teste Validador SciELO')
        

class ValideXML(APIView):
    """ class to Validate xml in request """
    
    def get(self, request, *args, **kwargs):
        """ method to show api """
        return Response({"msg": 'Envie um arquivo xml para validar.'})

    def put(self, request, format=None):
        """ method to valid file in request """
        
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        if f.content_type not in ['application/xml', 'text/xml']:
            raise ParseError("Invalid file type")

        try:
            xmlvalidator = XMLValidator.parse(f)
            is_valid, errors = xmlvalidator.validate_all()
            result = {
                'valid': is_valid,
                'errors': []
            }
            
            if not is_valid:
                for error in errors:
                    result['errors'].append(error.message)
                    
            return Response(result)
            
        except Exception as ex:
           raise ParseError("Error: %s" %(ex))
