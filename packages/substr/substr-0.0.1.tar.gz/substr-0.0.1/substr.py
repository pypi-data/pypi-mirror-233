#!/usr/bin/env python3

'''
Get all substrings from string argument.
    Returns None if no substrings.
    Returns only one substring if there's only one.
    Returns all substrings in a list if there's more than one.
'''
def get_substring(string):
    if (type(string) is not str):
        raise TypeError('The string argument must be a str.')
    
    if (len(string.replace(' ', '')) == 0):
        raise ValueError('The string argument may not be empty.')
    
    if (string.replace(' ', '').isalnum() == False):
        raise ValueError('The string argument must be alphanumeric.')
    
    length = len(string)
    substrings = []

    # Iterate unto every index for the total length of the string argument.
    for i in range(length):

        # Interate unto every index from i to the total length of the string argument.
        for j in range(i, length):

            # Slice the string, creating a substring from index i to index j + 1
            substring = string[i : j + 1]

            # Append the substring to list if it's not just whitespace.
            if (substring != ' '):
                substrings.append(substring)

    total_substrings = len(substrings)

    if(total_substrings == 0):
        return None
    elif(total_substrings == 1):
        return substrings[0]
    else:
        return substrings

'''
Find substrings in argument string containing all characters in argument list.
    Returns None if no matching substrings.
    Returns only one matching substring if there's only one.
    Returns all matching substrings in a list if there's more than one.
'''
def get_matching_substring(string, compare_values):
    if (type(string) is not str):
        raise TypeError('The string argument must be a str.')
    
    if (len(string.replace(' ', '')) == 0):
        raise ValueError('The string argument may not be empty.')
    
    if (string.replace(' ', '').isalnum() == False):
        raise ValueError('The string argument must be alphanumeric.')
    
    if (type(compare_values) is not list):
        raise TypeError('The compare_values argument must be a list.')
    
    if (len(compare_values) == 0):
        raise ValueError('The compare_values argument may not be empty.')
    
    for i in compare_values:
        if (type(i) is not str):
            raise ValueError("The compare_values argument may contain only str.")

    substrings = get_substring(string)
    matching_substrings = []

    for substring in substrings:

        # If all characters in parameter compare_values exist in the substring, append the substring to matching_substrings list.
        if (all(i in substring for i in compare_values)):
            matching_substrings.append(substring)

    total_substrings = len(matching_substrings)

    if(total_substrings == 0):
        return None
    elif(total_substrings == 1):
        return matching_substrings[0]
    else:
        return matching_substrings

'''
Find smallest substring in argument string containing all characters in argument list.
'''
def get_small_matching_substring(string, compare_values):
    if (type(string) is not str):
        raise TypeError("The string argument must be a str.")
    
    if (len(string.replace(' ', '')) == 0):
        raise ValueError('The string argument may not be empty.')
    
    if (string.replace(' ', '').isalnum() == False):
        raise ValueError('The string argument must be alphanumeric.')
    
    if (type(compare_values) is not list):
        raise TypeError("The compare_values argument must be a list.")
    
    if (len(compare_values) == 0):
        raise ValueError('The compare_values argument may not be empty.')
    
    for i in compare_values:
        if (type(i) is not str):
            raise ValueError("The compare_values argument contain only str.")
    
    substrings = get_matching_substring(string, compare_values)
    if (substrings == None):
        return None
    
    length = len(substrings)
    if (length >= 1):
        small_substring = substrings[0]
    else:
        small_substring = ''

    if (length > 1):
        for i in range(1, length):
            
            # Check if the length of substrings[i] is less than current assigned small_substring, if so reassign small_substring to substrings[i].
            if (len(substrings[i]) < len(small_substring)):
                small_substring = substrings[i]

    return small_substring