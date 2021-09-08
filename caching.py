import pickle
from time import time
import os
from config import Config


class CacheData:
    def __init__(self):
        self.config = Config()

    def get_data(self, key):
        # Variable is initialized to avoid looking up the config object
        caching_type = self.config.CACHING_TYPE
        timeout = int(self.config.CACHE_TIMEOUT)
        try:
            # If the key is blank, return None
            if key is '':
                return None

            print('Loading from {}.'.format(caching_type))
            # Log Timings of getting from Cache. The cache can be pickled or memcached

            start_step = time()

            if caching_type == 'pickle':

                # If the caching_type is pickle, then and only then load if from the pickle.load library
                # The pickle file always needs a '.p' extension
                filename = 'pickle/' + key + '.p'

                # Get the time when the cached file was last modified
                filetime = os.path.getmtime(filename)
                now = time()
                delta = int(now - filetime)

                print('File is {} seconds old'.format(delta))

                # If the last modified date of the file is more than the threshold value, delete the file
                if delta > timeout:
                    print('File too old to read --> {} mins. Making fresh copy of {} in pickle'
                          .format(delta / 60, key))
                    result = None
                else:
                    result = pickle.load(file=open(filename, mode='rb'), encoding='utf-8')

            elif caching_type == 'memcache':
                # Initialize the Memcache Object iff the caching_type is memcache
                import pylibmc
                cache = pylibmc.Client(['{}:{}'.format(self.config.MEMSERVER, self.config.MEMPORT)])
                result = cache.get(key)

            else:
                raise Exception('Invalid Caching Type configured. Caching Type should only be pickle or memcached')

            print('Reading from {} took {:.2f} seconds '.format(caching_type, time() - start_step))
        except Exception as ex:
            result = None
            print('An Error occurred while loading data from {}. Error is {}.'.format(caching_type, ex))
        return result

    def set_data(self, key, value):
        # Variable is initialized to avoid looking up the config object
        caching_type = self.config.CACHING_TYPE
        timeout = int(self.config.CACHE_TIMEOUT)
        try:
            # If the key is blank, return None
            if key is '':
                return None

            print('Loading from {}.'.format(caching_type))
            # Log Timings of getting from Cache. The cache can be pickled or memcached

            start_step = time()

            if caching_type == 'pickle':
                # If the caching_type is pickle, then and only then load if from the pickle.load library
                # The pickle file always needs a '.p' extension
                pickle.dump(obj=value, file=open('pickle/' + key + '.p', mode='wb'))

            elif caching_type == 'memcache':
                # Initialize the Memcache Object iff the caching_type is memcache
                import pylibmc
                cache = pylibmc.Client(['{}:{}'.format('127.0.0.1', 11211)])
                cache.set(key, value, timeout)

            else:
                raise Exception('Invalid Caching Type configured. Caching Type should only be pickle or memcached')

            print('Writing to {} took {:.2f} seconds '.format(caching_type, time() - start_step))
        except Exception as ex:
            print(ex)
            print('An Error occurred while writing data to {}. Error is {}.'.format(caching_type, ex))
        return True
