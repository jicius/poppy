import bottle, poppy, sys

class RollbarBottleReporter(object):
    '''
    A Bottle plugin that reports errors to Rollbar
    All args and kwargs are passed to `poppy.init`
    '''
    name = 'poppy-bottle-reporter'
    api = 2

    def __init__(self, *args, **kwargs):
        if 'exception_level_filters' in kwargs:
            kwargs['exception_level_filters'].append((bottle.BaseResponse, 'ignored'))
        else:
            kwargs['exception_level_filters'] = [(bottle.BaseResponse, 'ignored')]

        poppy.init(*args, **kwargs)

        def hook(request, data):
            data['framework'] = 'bottle'

            if request:
                route = request['bottle.route']
                data['context'] = route.name or route.rule

        poppy.BASE_DATA_HOOK = hook

    def __call__(self, callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception as e:
                poppy.report_exc_info(sys.exc_info(), request=bottle.request)
                raise

        return wrapper


