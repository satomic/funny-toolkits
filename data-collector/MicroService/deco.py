#coding=utf-8

import multiprocessing.pool
import functools

def timeout(max_timeout):
    """
    timeout decorator, parameter is seconds
    :param max_timeout: 
    :return: 
    """
    def timeout_decorator(item):
        "wrap the orignal function."
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            "closure for function"
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raise a TimeoutError if excution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator

if __name__=="__main__":
    # 限定下面的函数如果在5s内不返回就强制抛Timeout异常
    @timeout(5)
    def slowfunc(sleep_time):
        a = 1
        import time
        time.sleep(sleep_time)
        return a

    print slowfunc(11)