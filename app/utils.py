import threading
import nltk

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

def error_response(msg,code=1,extra={}):
    return jsonify({"code":code,"msg":msg,**extra})

def success_response(data,extra={}):
    return jsonify({"code":0,"msg":"ok","data":data,**extra})

def getInt(values,key,default=0):
    value = values.get(key)
    try: 
        return max(int(value),default)
    except:
        return default

def getString(values,key,default=None):
    value = values.get(key)
    try: 
        return str(value)
    except:
        return default
    
def string_similarity(str1, str2):
    distance = nltk.edit_distance(str1, str2)
    length = max(len(str1), len(str2))
    similarity = 1 - (distance / length)
    return similarity