import re as _re
import functools as _functools


def _regex_ParsePattern(pattern:str) -> tuple:
    """
    Parses the given regex pattern into its regex pattern and flags.
    
    :param pattern: The regex pattern, with flags following in the format "/pattern/flags".
    :raises Exception: If pattern does not have the format "/pattern/flags".

    :return: A tuple containing the regex pattern and flags.
    """
    flagSplitterPos = pattern.rfind("/")
    if pattern[0] != "/" and flagSplitterPos == -1:
        raise Exception("Pattern need to have format of '/pattern/flags'")
    regexPattern = pattern[1:flagSplitterPos]  # remove first slash
    flags = pattern[flagSplitterPos + 1 :]
    flagLookup = {"i": _re.IGNORECASE, "s": _re.DOTALL, "m": _re.MULTILINE}
    activeFlags = []
    for i in flags:
        activeFlags.append(flagLookup[i])

    if _re.DOTALL not in activeFlags and _re.MULTILINE not in activeFlags:
        activeFlags.append(_re.MULTILINE)

    flagParamValue = _functools.reduce(lambda x, y: x | y, activeFlags)
    return (regexPattern, flagParamValue)


def Replace(pattern: str, replacement: str, message:str) -> str:  
    """
    Replaces all occurrences of the regex pattern in the message with the given replacement.

    :param pattern: The regex pattern, with flags following in the format "/pattern/flags". available flags i=ignorecase, s=dotall
    :param replacement: The replacement string for matches. Back reference to capture groups with \\1...\\100 or \g<1>...\g<100>
    :param message: The string to search for matches in.

    :Return: The message with all matches replaced by the replacement string or same text if not matches

    Example Usage:
    
    >>> RegexReplace(r"/hej (.*?) /i", r"bye \\1 or \g<1> ", "hej v1.0 hej v2.2 hejsan v3.3") 
    "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3"
    """

    regexPattern, flagParamValue = _regex_ParsePattern(pattern)
    return  _re.sub(regexPattern, replacement, message, flags=flagParamValue)

def Match(pattern: str, string: str) -> (list[list[str]] | None):  
    """
    Finds all matches of the regex pattern in the string, default flag is multiline

    :param pattern: The regex pattern, with flags following in the format "/pattern/flags".
    :param string: The string to search for matches in.

    :return:
        list[list[str]] | None: A 2D list of matches and their corresponding capture groups, or None if no matches found.
        Example: [[match1, capture1, capture2][match2, capture1, capture2]]

    Example Usage:
    
    >>> Match(r"/hej (.*?) /is", "hej v1.0 hej v2.2 hejsan v3.3")
    [['hej v1.0 ', 'v1.0'], ['hej v2.2 ', 'v2.2']]
    """

    regexPattern, flagParamValue = _regex_ParsePattern(pattern)
    iterator = _re.finditer(regexPattern, string, flags=flagParamValue)
    results = [[i.group(0), *i.groups()] for i in iterator]
    if len(results) == 0:
        return None
    return results  


############################## Archived Snippets, since they are available in this module instead ###############################

#########
# # @prefix _regex_replace
# # @description 

# # returns string with replacements
#  result = _re.sub(r"hej (.*?) ", r"bye \1 or \g<1> ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE) # result = "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3" 
#########

#########
# # @prefix _regex_match
# # @description 

# # finds first occurence of a match or None, can be used directly in if statements
# # matched object can be accessed through result[0], captured groups can becalmessed by result[1]...result[100]
# result = _re.search(r"hej (.*?) ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE)  # result[0] = "hej v1.0 ", result[1] = "v1.0"
#########


#########
# # @prefix _regex_match
# # @description 

# #no capture groups returns list of string matches
# result1 = _re.findall(r"hej .*? ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE) # result[0] = "hej v1.0 ", result[1] = "hej v2.2 "
# #one capture group returns list of string capture group matches
# result2 = _re.findall(r"hej (.*?) ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE) # result[0] = "v1.0", result[1] = "v2.2"
# #multiple capture groups returns list in list, where the inner list contains captured group
# result3 = _re.findall(r"(hej) (.*?) ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE) # result[0] = ["hej", "v1.0"], result[1] = ["hej", "v2.2"]
#########