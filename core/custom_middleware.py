from .models import ExceptionLog

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        try:
            response = self.get_response(request)
        except Exception as e:
            # Log the exception
            exception_message = str(e)
            exception_name = e.__class__.__name__
            ExceptionLog.objects.create(message=exception_message, name=exception_name)
            raise  # Re-raise the exception for standard error handling
        return response
