import os
import urlparse

__author__ = 'ajumell'

# Register database schemes in URLs.
urlparse.uses_netloc.append('mysql')

def has_clear_db():
    """
    @return: True if the clear db database url is present in the
    enviroment variables.
    """
    return 'CLEARDB_DATABASE_URL' in os.environ


def parse_clear_db(throw_exception=False, print_exception=False):
    """
    @param throw_exception: Throws the exception if any exception occures.
    @param print_exception: Prints the exception data if any exception occures.
    @return: A dictionary with the clear db database settings.
    """
    try:
        if has_clear_db():
            config = {}
            url = urlparse.urlparse(os.environ['CLEARDB_DATABASE_URL'])

            # Ensure default database exists.

            DB_NAME = url.path[1:]
            i = DB_NAME.find('?')
            if i > 0:
                DB_NAME = DB_NAME[:i]

            # Update with environment configuration.
            config.update({
                'NAME': DB_NAME,
                'USER': url.username,
                'PASSWORD': url.password,
                'HOST': url.hostname,
                'PORT': url.port,
                })

            if url.scheme == 'mysql':
                config['ENGINE'] = 'django.db.backends.mysql'
            return config
        else:
            raise Exception("Clear DB addon not installed.")
    except Exception, data:
        if print_exception:
            print data
        if throw_exception:
            raise
        return None
