"""
Integration with Flask
"""

from flask import request
import poppy


def report_exception(app, exception):
    poppy.report_exc_info(request=request)


def _hook(request, data):
    data['framework'] = 'flask'

    if request:
        data['context'] = str(request.url_rule)

poppy.BASE_DATA_HOOK = _hook
