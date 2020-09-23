# Описание программы в файле task1.txt


import traceback


class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1



def match(string, pattern):
    # Функция проверяет, соответствует ли строка шаблону
    letters = [chr(i) for i in range(97, 123)]
    numbers = [chr(i) for i in range(48,58)]

    pattern_dict = {
        ' ' : ' ',
        'd' : numbers,
        'a': letters,
        '*' : letters + numbers
    }

    if len(string) != len(pattern):
        return False

    for p in pattern:
        if p not in pattern_dict: 
            raise ValueError('Invalid value in pattern')
                  
    for i in range(len(string)):
        if string[i] not in pattern_dict[pattern[i]] :
            return False
    else:
        return True


def testMatch():
    runner = TestRunner('match')

    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ',  'a'))

    runner.expectTrue(lambda:  match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda:  match('x', 'w'))

testMatch()