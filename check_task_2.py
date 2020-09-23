# Описание программы в файле task1.txt
# Код написан с тестирующей функцией

from collections import deque
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

tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}


def findTaskHavingMaxPriorityInGroup(tmp_tasks, group_id):
    # функция проходит по дереву tasks
    # и собирает список задач у которых есть приоритеты (не являются узлами)
    # Далее собирает список всех приоритетов из списка задач и возвращает максимальный
# ------------------------------------------------------------------------------------------------
    deq_tasks = deque([tmp_tasks])
    task_list = []
    parent_group = None
    while len(deq_tasks) > 0:
        while tmp_tasks['id'] != group_id:
            try:
                tmp_tasks = deq_tasks.pop()
                if 'priority' in tmp_tasks:
                    task_list.append(tmp_tasks)
                else:	
                    for task in tmp_tasks['children']:
                        deq_tasks.appendleft(task)
            except IndexError:
                #print('Не удалось найти группу с указанным идентификатором')
                raise Exception# 'Не удалось найти группу с указанным идентификатором'
            
        else:
            parent_group = tmp_tasks
            break  

    deq_tasks.clear()
    task_list = []
    deq_tasks.appendleft(parent_group)
    
    while len(deq_tasks) > 0:
        tmp_tasks = deq_tasks.pop()
        if 'priority' in tmp_tasks:
            task_list.append(tmp_tasks)
        
        else:	
            for task in tmp_tasks['children']:
                deq_tasks.appendleft(task)
    #return parent_group, task_list

    if 'priority' in parent_group:
        raise Exception('Не является группой')
    elif parent_group['children'] == []:
        return None
    else:
        task_list = sorted(task_list, key=lambda task: task['priority'])
        task_with_max_priority = task_list[-1]
        return task_with_max_priority       
# ------------------------------------------------------------------------------------------------


def taskEquals(a, b):
    return (
        not 'children' in a and
        not 'children' in b and
        a['id'] == b['id'] and
        a['name'] == b['name'] and
        a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)


testFindTaskHavingMaxPriorityInGroup()