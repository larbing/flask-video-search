import threading

def synchronized(func):
    """线程安全的装饰器"""
    func.__lock__ = threading.Lock()

    def wrapper(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return wrapper

def singleton(cls):
    """单例模式装饰器"""
    instances = {}

    @synchronized
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
