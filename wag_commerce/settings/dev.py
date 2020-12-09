from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gxhirnnr-n$k(w_!28jmvaqz7*wj=e^#^l9tkv2y(#x1@=37q_'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['greenhouse-master-demo.herokuapp.com', '127.0.0.1'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if DEBUG:
    import mimetypes
    mimetypes.add_type("text/javascript", ".js", True)

try:
    from .local import *
except ImportError:
    pass
