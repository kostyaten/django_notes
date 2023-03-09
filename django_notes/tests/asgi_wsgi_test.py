from django.core.handlers.asgi import ASGIHandler
from django.core.handlers.wsgi import WSGIHandler

from ..asgi import application as application_asgi
from ..wsgi import application as application_wsgi


def test_asgi():
    assert isinstance(application_asgi, ASGIHandler)


def test_wsgi():
    assert isinstance(application_wsgi, WSGIHandler)
