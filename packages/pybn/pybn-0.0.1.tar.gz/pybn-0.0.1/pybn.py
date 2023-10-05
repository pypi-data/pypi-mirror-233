#!/usr/bin/env python3

'''
Generates a new build number from an existing build number if provided in the current_build_number argument.
    Build numbers are in the following format:
        'xxx.xxx.xxx'
    The limit argument is the highest number the back two segments of the build number can be before shifting over (Set to 100 by default).
'''
def generate_buildnumber(current_build_number = None, limit = 100):
    if (current_build_number == None):
        return '0.0.1'

    if (type(current_build_number) is not str):
        raise TypeError('The current_build_number argument may only be of str type.')

    if (type(limit) is not int):
        raise TypeError('The limit argument may only be of int type.')

    if (current_build_number.count('.') != 2):
        raise ValueError('The current_build_number argument value of the string must be in the following format: xxx.xxx.xxx')

    segment = current_build_number.split('.')
    alpha = int(segment[0])
    beta = int(segment[1])
    delta = int(segment[2])
    shifted = False

    if (delta >= limit):
        beta += 1
        delta = 0
        shifted = True
    
    if (beta >= limit):
        alpha += 1
        beta = 0
        delta = 0
        shifted = True

    if (shifted == False):
        delta += 1    

    build_number = str(f"{alpha}.{beta}.{delta}")
    return build_number