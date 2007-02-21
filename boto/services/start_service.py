#!/usr/bin/env python
import getopt, sys, imp
from boto.utils import get_instance_userdata

def usage():
    print 'start_service.py -m module -c class_name [-w working_dir] [-i input_queue_name] [-o output_queue_name]'
    sys.exit()

def get_userdata():
    module_name = None
    class_name = None
    s = get_instance_userdata()
    if s:
        l = s.split('|')
        for nvpair in l:
            t = nvpair.split('=')
            if t[0].strip() == 'module_name':
                module_name = t[1].strip()
            elif t[0].strip() == 'class_name':
                class_name = t[1].strip()
    return (module_name, class_name)
    

def find_class(module, class_name):
    modules = module.split('.')
    path = None
    for module_name in modules:
        fp, pathname, description = imp.find_module(module_name, path)
        module = imp.load_module(module_name, fp, pathname, description)
        if hasattr(module, '__path__'):
            path = module.__path__
    return getattr(module, class_name)
  
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:hi:m:o:w:',
                                   ['class', 'help', 'inputqueue',
                                    'outputqueue', 'module', 'working_dir'])
    except:
        usage()
    input_queue = None
    output_queue = None
    wdir = 'work'
    module_name = None
    class_name = None
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        if o in ('-c', '--class'):
            class_name = a
        if o in ('-m', '--module'):
            module_name = a
        if o in ('-w', '--working_dir'):
            wdir = a
        if o in ('-i', '--inputqueue'):
            input_queue = a
        if o in ('-o', '--outputqueue'):
            output_queue = a
    if not class_name or not module_name:
        module_name, class_name = get_userdata()
    if not class_name or not module_name:
        usage()
    cls = find_class(module_name, class_name)
    s = cls(working_dir=wdir, input_queue_name=input_queue,
            output_queue_name=output_queue)
    s.run()

if __name__ == "__main__":
    main()
