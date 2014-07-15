
import pytest
from twisted.python import log

from scrapy import optional_features

collect_ignore = ["stats.py"]
if 'django' not in optional_features:
    collect_ignore.append("tests/test_djangoitem/models.py")


class LogObservers:
    """Class for keeping track of log observers across test modules"""

    def __init__(self):
        self.observers = []

    def add(self, logfile='test.log'):
        fileobj = open(logfile, 'wb')
        observer = log.FileLogObserver(fileobj)
        log.startLoggingWithObserver(observer.emit, 0)
        self.observers.append((fileobj, observer))

    def remove(self):
        fileobj, observer = self.observers.pop()
        log.removeObserver(observer.emit)
        fileobj.close()


@pytest.fixture(scope='module')
def log_observers():
    return LogObservers()


@pytest.fixture()
def setlog(request, log_observers):
    """Attach test.log file observer to twisted log, for trial compatibility"""
    log_observers.add()
    request.addfinalizer(log_observers.remove)


@pytest.fixture()
def chdir(tmpdir):
    """Change to pytest-provided temporary directory"""
    tmpdir.chdir()
