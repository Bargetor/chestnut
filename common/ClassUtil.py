import traceback
# def get_class_for_full_name(class_full_name):
#     if not class_full_name:
#         return None
#     try:
#         last_point_pos = class_full_name.rindex('.')
#         module_name = class_full_name[0:last_point_pos]
#         print module_name
#         module = __import__(module_name)
#         print module
#         class_name = class_full_name[last_point_pos + 1:]
#         clazz = getattr(module, class_name)
#         return clazz
#     except Exception, e:
#         print e
#         return None

def get_class_for_full_name(class_full_name):
    if not class_full_name:
        return None
    try:
        name_splits = class_full_name.split('.')
        if len(name_splits) < 2:
            return None
        module = None
        for i in range(0,len(name_splits) - 1):
            module = get_module(module, name_splits[i])
        class_name = name_splits[len(name_splits) - 1]
        clazz = getattr(module, class_name)
        return clazz
    except Exception, e:
        print e
        traceback.print_exc()
        return None

def get_module(parent_module, child_module_name):
    try:
        if not  parent_module:
            return __import__(child_module_name)
        return getattr(parent_module, child_module_name)
    except Exception, e:
        print e
        return None
