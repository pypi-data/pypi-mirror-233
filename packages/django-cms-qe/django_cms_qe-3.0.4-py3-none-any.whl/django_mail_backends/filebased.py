# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_BACKEND = 'django_mail_backends.filebased.EmailBackend'
import datetime
import os

from django.core.mail.backends.filebased import EmailBackend as DjangoEmailBackend


class EmailBackend(DjangoEmailBackend):

    def _get_filename(self):
        """Return a unique file name."""
        if self._fname is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            fname = "%s-%s.eml" % (timestamp, abs(id(self)))
            self._fname = os.path.join(self.file_path, fname)
        return self._fname
