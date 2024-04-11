import threading

from flask import jsonify

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

def error_response(msg,code=1):
    return jsonify({"code":code,"msg":msg})

def success_response(data,extra={}):
    return jsonify({"code":0,"msg":"","data":data,**extra})

def getInt(values,key,default=0):
    value = values.get(key)
    try: 
        return max(int(value),default)
    except:
        return default
