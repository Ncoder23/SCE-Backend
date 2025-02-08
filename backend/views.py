from django.http import HttpResponse


def home(request):
    routes = [
        '/',
        '/admin/',
        '/api/users/register/',
        '/api/users/login/',
        '/api/users/logout/',
    ]

    route_list = "<br>".join(
        [f"• <a href='{route}'>{route}</a>" for route in routes])
    return HttpResponse(f"<h1>SCE API is running</h1><h2>Available Routes:</h2>{route_list}")
