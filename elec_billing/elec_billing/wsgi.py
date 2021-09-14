import os
import sys

sys.path.append("/opt/bitnami/projects/elec_billing")
os.environ.setdefault(
    "PYTHON_EGG_CACHE", "/opt/bitnami/projects/elec_billing/egg_cache"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elec_billing.settings")

from django.core.wsgi import get_wsgi_application  # pylint: disable=wrong-import-position

application = get_wsgi_application()

from whitenoise import WhiteNoise  # pylint: disable=wrong-import-position

application = WhiteNoise(application, root="/opt/bitnami/projects/elec_billing/static")
