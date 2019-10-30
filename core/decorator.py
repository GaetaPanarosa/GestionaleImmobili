from django.shortcuts import render, redirect


def login_required(func):
    def wrap(request, *args, **kwargs):
        if not request.session.get( 'username' ):
            return redirect( '/login/' )
        else:
            return func( request, *args, **kwargs )

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap
