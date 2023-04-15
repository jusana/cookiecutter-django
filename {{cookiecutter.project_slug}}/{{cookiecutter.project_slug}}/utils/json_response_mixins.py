from django.http import JsonResponse


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(self.get_data(context), safe=False, **response_kwargs)

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        return context


# class AjaxResponseMixin:
#     """
#     Mixin allows you to define alternative methods for ajax requests. Similar
#     to the normal get, post, and put methods, you can use get_ajax, post_ajax,
#     and put_ajax.
#     Important: c'est une réécriture du AjaxResponseMixin de django-braces pour l'adapter à django 3.1
#     https://docs.djangoproject.com/fr/3.1/releases/3.1/#id2
#     """

#     def dispatch(self, request, *args, **kwargs):
#         request_method = request.method.lower()

#         if (
#             request.headers.get("x-requested-with") == "XMLHttpRequest"
#             and request_method in self.http_method_names
#         ):
#             handler = getattr(
#                 self, f"{request_method}_ajax", self.http_method_not_allowed
#             )
#             self.request = request
#             self.args = args
#             self.kwargs = kwargs
#             return handler(request, *args, **kwargs)

#         return super().dispatch(request, *args, **kwargs)

#     def get_ajax(self, request, *args, **kwargs):
#         return self.get(request, *args, **kwargs)

#     def post_ajax(self, request, *args, **kwargs):
#         # print("post en ajax")
#         return self.post(request, *args, **kwargs)

#     def put_ajax(self, request, *args, **kwargs):
#         return self.get(request, *args, **kwargs)

#     def delete_ajax(self, request, *args, **kwargs):
#         return self.get(request, *args, **kwargs)
