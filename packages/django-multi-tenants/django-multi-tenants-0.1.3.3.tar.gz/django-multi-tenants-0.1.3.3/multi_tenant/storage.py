from django.contrib.staticfiles.storage import StaticFilesStorage
from django.core.exceptions import SuspiciousOperation
from django.core.files.storage import FileSystemStorage
from django.db import connection
from django.utils._os import safe_join

__all__ = (
    'TenantStorageMixin',
    'TenantFileSystemStorage',
    'TenantStaticFilesStorage',
)


class TenantStorageMixin(object):
    """
    Mixin that can be combined with other Storage backends to colocate media
    for all tenants in distinct subdirectories.
    Using rewriting rules at the reverse proxy we can determine which content
    gets served up, while any code interactions will account for the multiple
    tenancy of the project.
    """
    def path(self, name):
        """
        Look for files in subdirectory of MEDIA_ROOT using the tenant's
        codename value as the specifier.
        """
        if name is None:
            name = ''
        try:
            location = safe_join(self.location, connection.tenant.codename)
        except AttributeError:
            location = self.location
        try:
            path = safe_join(location, name)
        except ValueError:
            raise SuspiciousOperation(f'Attempted access to {name!r} denied.')
        return path


class TenantFileSystemStorage(TenantStorageMixin, FileSystemStorage):
    """
    Implementation that extends core Django's FileSystemStorage.
    """


class TenantStaticFilesStorage(TenantStorageMixin, StaticFilesStorage):
    """
    Implementation that extends core Django's StaticFilesStorage.
    """
