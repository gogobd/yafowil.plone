from UserDict import DictMixin
from yafowil.base import factory

class Zope2RequestAdapter(DictMixin):
    
    def __init__(self, request):
        if isinstance(request, self.__class__):
            # for some rare cases this makes sense             
            request = request.request 
        # XXX 
        if not isinstance(request, BaseRequest):
            raise ValueError(\
                'Expecting object based on webob.request.BaseRequest') 
        self.request = request
        
    def __getitem__(self, key):
        value = self.mixed[key]
        # XXX
        if isinstance(value, cgi.FieldStorage):
            fvalue = dict()
            fvalue['file'] = value.file
            fvalue['filename'] = value.filename
            fvalue['mimetype'] = value.type
            fvalue['headers'] = value.headers
            fvalue['original'] = value
            return fvalue
        return value

    def keys(self):
        return self.request.form.keys()
    
    def __setitem__(self, key, item):
        raise AttributeError('read only, __setitem__ is not supported')
    
    def __delitem__(self, key):
        raise AttributeError('read only, __delitem__ is not supported')
    
def zope2_preprocessor(uname, data, properties):
    if not isinstance(data['request'], Zope2RequestAdapter):
        data['request'] = Zope2RequestAdapter(data['request'])
    return data

factory.register_global_preprocessors([zope2_preprocessor])