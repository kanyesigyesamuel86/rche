from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('access_denied')
    return wrapper

def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type in ['admin', 'manager']:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('access_denied')
    return wrapper