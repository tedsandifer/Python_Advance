"""
content = assignment
course  = Python Advanced
 
date    = 14.11.2025
email   = contact@alexanderrichtertd.com
"""

# original: logging.init.py

def find_caller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    frame = currentframe()
    
    #On some versions of IronPython, currentframe() returns None if
    #IronPython isn't run with -X:Frames.
    
    if frame == False:
        frame = f.f_back
    
    rv = "(unknown file)", 0, "(unknown function)"
    
    while hasattr(frame, "f_code"):
        co = frame.f_code
        file_name = os.path.normcase(co.co_filename)
        
        if file_name == _srcfile:
            frame = frame.f_back
            continue
        
        rv = (co.co_filename, frame.f_lineno, co.co_name)
        break
    
    return rv

# How can we make this code better?
