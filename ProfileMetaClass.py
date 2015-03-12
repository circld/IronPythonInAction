from System.Diagnostics import Stopwatch
from System.Threading import Thread
from types import FunctionType


timer = Stopwatch()
times = {}


def profiler(function):
    def wrapped(*args, **kwargs):
        if not timer.IsRunning:
            timer.Start()

        start = timer.ElapsedMilliseconds
        ret_val = function(*args, **kwargs)
        time_taken = timer.ElapsedMilliseconds - start

        name = function.__name__
        # this step works bc each func only decorated once
        function_times = times.setdefault(name, [])
        function_times.append(time_taken)

        return ret_val
    return wrapped


class ProfilingMetaClass(type):

    def __new__(meta, className, bases, classDict):
        for name, item in classDict.items():
            if isinstance(item, FunctionType):
                classDict[name] = profiler(item)
        return type.__new__(meta, className, bases, classDict)


class Test(object):

    __metaclass__ = ProfilingMetaClass

    def __init__(self):
        counter = 0
        while counter < 100:
            counter += 1
            self.method()

    def method(self):
        Thread.CurrentThread.Join(20)


if __name__ == '__main__':
    t = Test()
    y = Test()

    for name, calls in times.items():
        print 'Function: %s' % name
        print 'Called: %s times' % len(calls)
        print 'Total time taken: %s second' % (sum(calls) / 1000.0)
        avg = (sum(calls) / float(len(calls)))
        print 'Max: %sms, Min: %sms, Avg: %sms' % (max(calls), min(calls), avg)
