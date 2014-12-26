# -*- coding: utf-8 -*-

from functools import wraps
import threading
import time

class TaskCenter(object):
    """docstring for TaskCenter"""
    _instance = None
    _task_set = {}
    task_todo_flag = "__task_todo__"

    def __new__(clz, *args, **kwargs):
        if not clz._instance:
            clz._instance = super(TaskCenter, clz).__new__(clz, *args, **kwargs)
        return clz._instance


    def reg_target_task(self, target_task_class, is_async = False):
        if not is_class(target_task_class) : return
        task = self._task_set.get(target_task_class.__name__)
        if task : return
        task = self.__build_task(target_task_class, is_async)
        self._task_set[target_task_class.__name__] = task
        return task

    def __build_task(self, target_task_class, is_async = False):
        task =  Task(target_task_class)
        task.is_async = is_async
        return task

    def get_task_by_target_class(self, target_task_class):
        if not target_task_class : return None
        task = self._task_set.get(target_task_class.__name__)
        if not task : return None
        # 复制一个任务
        result = self.__build_task(task.task_class, task.is_async)
        return result

    # def reg_todo_method(self, method, is_check = False, goto = None, is_once = True, check_count = 1):
    #     if not method or not is_instance_methon(method) : return
    #     task = self.get_task_by_target_class(method.im_class)
    #     if not task :
    #         task = self.reg_target_task(method.im_class)

    #     if not task : return
    #     task.reg_todo_method(method, is_check, goto, is_once, check_count)

    def mark_todo(self, todo_method, **kwargs):
        setattr(todo_method, self.task_todo_flag, kwargs)

    def build_task(self, task_class):
        task = self.get_task_by_target_class(task_class)
        return task

    def start_task(self, task_class, *args, **kwargs):
        task = self.build_task(task_class, *args, **kwargs)
        task.start(*args, **kwargs)
        return task


class Task(threading.Thread):
    """docstring for Task"""
    def __init__(self, task_class):
        super(Task, self).__init__()
        self.is_stop = False
        self.is_pause = False

        self.task_class = task_class
        self.is_async = False
        self.todo_dict = {}

        self.task_args = ()
        self.task_kwargs = {}

        self.__reg_task_class_instance_method()

    def __reg_task_class_instance_method(self):
        for name, value in self.task_class.__dict__.items():
            if is_instance_method(value) and hasattr(value, TaskCenter.task_todo_flag):
                todo_method_params = getattr(value, TaskCenter.task_todo_flag)
                self.reg_todo_method(value, **todo_method_params)

    def reg_todo_method(self, method, is_check = False, is_once = True, check_count = 1, step_time = 1000, on_check_done = None):
        if not method or not is_instance_method(method) : return
        todo = ToDo(self.task_class, method)
        todo.is_check = is_check
        todo.is_once = is_once
        todo.check_count = check_count
        todo.step_time = step_time
        todo.on_check_done = on_check_done
        self.todo_dict[todo.get_todo_name()] = todo
        return todo

    def start(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs
        if self.is_async:
            super(Task, self).start()
        else:
            self.__run_sync(*self.task_args, **self.task_kwargs)

    def __run_sync(self, *args, **kwargs):
        task_obj = self.task_class(*args, **kwargs)
        for method_name in self.todo_dict.keys():
            self.__check_start()
            if self.is_stop : break
            method = getattr(task_obj, method_name)
            if not method : continue
            method()

    def __check_start(self):
        while self.is_pause:
            time.sleep(0.2)
            if self.is_stop : return

    def run(self):
        self.__run_sync(*self.task_args, **self.task_kwargs)

    def stop(self):
        self.is_stop = True

    def pause(self):
        self.is_pause = True

    def restart(self):
        self.is_pause = False


class ToDo(object):
    """docstring for Task"""
    def __init__(self, task_class, todo_method):
        super(ToDo, self).__init__()
        self.task_class = task_class
        self.todo_method = todo_method

        self.is_check = False
        self.is_once = True
        self.check_count = 1
        self.step_time = 1000
        self.on_check_done = None

    def get_todo_name(self):
        return self.todo_method.__name__


# 标记任务, 同异步
def task(is_async = False):
    #这里主要考虑不带参数的情况
    if is_class(is_async):
        clazz = is_async
        task = TaskCenter().reg_target_task(clazz)
        return clazz

    # 这里带参数的情况
    def task_decorator(target_task_class):
        task = TaskCenter().reg_target_task(target_task_class, is_async)
        return target_task_class
    return task_decorator

# 标记执行，序列号
def todo(todo_method):
    # 由于python对类的加载是先加载内部函数后加载类，所以这里只做标记
    TaskCenter().mark_todo(todo_method)
    @wraps(todo_method)
    def wrapper(*args, **kwargs):
        return todo_method(*args, **kwargs)
    return wrapper

# 标记为验证步， 验证不通过返回执行, 是否只验证一次，循环次数
def todo_check(is_once = False, check_count = 10, step_time = 1000, on_check_done = None):
    def todo_decorator(todo_method):
        TaskCenter().mark_todo(todo_method, is_check = True, is_once = is_once, check_count = check_count, step_time = step_time, on_check_done = on_check_done)
        @wraps(todo_method)
        def wrapper(*args, **kwargs):
            return todo_method(*args, **kwargs)
        return wrapper
    return todo_decorator



def is_class(clazz):
    if not clazz : return False
    return type(clazz).__name__ == 'type'

def is_instance_method(method):
    if not method : return False
    return type(method).__name__ == 'function'






@task(is_async = True)
class Test(object):
    """docstring for Test"""
    def __init__(self, print_str):
        super(Test, self).__init__()
        self.print_str = print_str

    @todo
    def c(self):
        print self.print_str
        print "c"

    @todo
    def b(self):
        print "b"

task = TaskCenter().build_task(Test)
task.pause()
task.start(print_str = 'd')
time.sleep(0.3)
task.restart()
time.sleep(0.6)
task.stop()
