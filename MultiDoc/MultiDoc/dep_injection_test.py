import time
from unittest import TestCase, main
from Scheduler import Scheduler


class DependencyInjectionTest(TestCase):

    def test_Scheduler_constructor(self):
        scheduler = Scheduler()
        self.assertEquals(scheduler.time, time.time,
                          'Default time function not initialized properly.')
        self.assertEquals(scheduler.sleep, time.sleep,
                          'Default sleep function not initialized properly.')

    def test_schedule(self):
        """
        test Scheduler.schedule method by injecting faked-up dependency 
        """
        class FakeTime(object):
            calls = []

            def time(self):
                self.calls.append('time')
                return 100

            def sleep(self, howLong):
                self.calls.append(('sleep', howLong))

        faketime = FakeTime()
        scheduler = Scheduler(faketime.time, faketime.sleep)

        expectedResult = object()
        def function():
            faketime.calls.append('function')
            return expectedResult

        actualResult = scheduler.schedule(105, function)

        self.assertEquals(
            actualResult, expectedResult,
            'schedule did not return result of calling function'
        )
        self.assertEquals(
            faketime.calls,
            ['time', ('sleep', 5), 'function'],
            'time module and functions called incorrectly.'
        )


if __name__ == '__main__':

    main()