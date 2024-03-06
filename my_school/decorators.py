from django.shortcuts import redirect

def hteacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type == 'headteacher':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('access_denied')
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type in ['admin', 'headteacher']:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('access_denied')
    return wrapper


def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type in ['admin', 'teacher', 'headteacher']:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('access_denied')
    return wrapper