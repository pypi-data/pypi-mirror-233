# Author: Firas Moosvi, Jake Bobowski, others
# Date: 2021-06-13

import base64
from collections import defaultdict
import numpy as np
import sigfig
import pandas as pd
import importlib.resources
from decimal import Decimal, getcontext, ROUND_HALF_UP
import re

# Set rounding context
round_context = getcontext()
round_context.rounding = ROUND_HALF_UP

## Load data and dictionaries

## Better way of loading data and dictionaries
# Based on this Stack Overflow post: https://stackoverflow.com/questions/65397082/using-resources-module-to-import-data-files

with importlib.resources.open_text("problem_bank_helpers.data", "animals.csv") as file:
    animals = pd.read_csv(file)["Animals"].tolist()

with importlib.resources.open_text("problem_bank_helpers.data", "names.csv") as file:
    names = pd.read_csv(file)["Names"].tolist()

with importlib.resources.open_text("problem_bank_helpers.data", "jumpers.csv") as file:
    jumpers = pd.read_csv(file)["Jumpers"].tolist()

with importlib.resources.open_text("problem_bank_helpers.data", "vehicles.csv") as file:
    vehicles = pd.read_csv(file)["Vehicles"].tolist()

with importlib.resources.open_text("problem_bank_helpers.data", "manual_vehicles.csv") as file:
    manual_vehicles = pd.read_csv(file)["Manual Vehicles"].tolist()

with importlib.resources.open_text("problem_bank_helpers.data", "metals.csv") as file:
    metals = pd.read_csv(file)["Metal"].tolist()

with importlib.resources.open_text("problem_bank_helpers.data", "metals.csv") as file:
    T_c = pd.read_csv(file)["Temp Coefficient"].tolist()

## End Load data

def create_data2():

    nested_dict = lambda: defaultdict(nested_dict)
    return nested_dict()

def sigfigs(x):
    '''Returns the number of significant digits in a number. This takes into account
       strings formatted in 1.23e+3 format and even strings such as 123.450 .
       This has a limit of 16 sigfigs, which can be increased but doesn't seem practical'''
    # if x is negative, remove the negative sign from the string.
    if float(x) < 0:
        x = x[1:]
    # change all the 'E' to 'e'
    x = x.lower()
    if ('e' in x):
        # return the length of the numbers before the 'e'
        myStr = x.split('e')

        return len( myStr[0] ) - (1 if '.' in x else 0) # to compensate for the decimal point
    else:
        # put it in e format and return the result of that
        ### NOTE: because of the 15 below, it may do crazy things when it parses 16 sigfigs
        n = f'{float(x):.15e}'.split('e')
        # remove and count the number of removed user added zeroes. (these are sig figs)
        if '.' in x:
            s = x.replace('.', '')
            #number of zeroes to add back in
            l = len(s) - len(s.rstrip('0'))
            #strip off the python added zeroes and add back in the ones the user added
            n[0] = n[0].rstrip('0') + ''.join(['0' for num in range(l)])
        else:
            #the user had no trailing zeroes so just strip them all
            n[0] = n[0].rstrip('0')
        #pass it back to the beginning to be parsed
    return sigfigs('e'.join(n))


def round_sig(x, sig):
    """
    Round a number to a specified number of significant digits.

    Args:
        x (float or int): The number to be rounded.
        sig (int): The number of significant digits.

    Returns:
        float or int: The rounded number retaining the type of the input.
    """
    from math import log10, floor
    if x == 0:
        y = 0
    else:
        y = sig - int(floor(log10(abs(x)))) - 1
    # avoid precision loss with floats
    decimal_x = round( Decimal(str(x)) , y )

    return type(x)(decimal_x)


# def round_sig(x, sig_figs = 3):
#     """A function that rounds to specific significant digits. Original from SO: https://stackoverflow.com/a/3413529/2217577; adapted by Jake Bobowski

#     Args:
#         x (float): Number to round to sig figs
#         sig_figs (int): Number of significant figures to round to; default is 3 (if unspecified)

#     Returns:
#         float: Rounded number to specified significant figures.
#     """
#     return round(x, sig_figs-int(np.floor(np.log10(np.abs(x))))-1)

# If the absolute value of the submitted answers are greater than 1e4 or less than 1e-3, write the submitted answers using scientific notation.
# Write the alternative format only if the submitted answers are not already expressed in scientific notation.
# Attempt to keep the same number of sig figs that were submitted.
def sigFigCheck(subVariable, LaTeXstr, unitString):
    if subVariable is not None:
        if (abs(subVariable) < 1e12 and abs(subVariable) > 1e4) or (abs(subVariable) < 1e-3 and abs(subVariable) > 1e-4):
            decStr = "{:." + str(sigfigs(str(subVariable)) - 1) + "e}"
            return("In scientific notation, $" + LaTeXstr + " =$ " + decStr.format(subVariable) + unitString + " was submitted.")
        else:
            return None


# An error-checking function designed to give hints if the submitted answer is:
# (1) correct except for and overall sign or...
# (2) the answer is right expect for the power of 10 multiplier or...
# (3) answer has both a sign and exponent error.
def ErrorCheck(errorCheck, subVariable, Variable, LaTeXstr, tolerance):
    import math, copy
    from math import log10, floor
    if errorCheck == 'true' or errorCheck == 'True' or errorCheck == 't' or errorCheck == 'T':
        if subVariable is not None and subVariable != 0 and Variable != 0:
            if math.copysign(1, subVariable) != math.copysign(1, Variable) and abs((abs(subVariable) - abs(Variable))/abs(Variable)) <= tolerance:
                return("Check the sign of $" + LaTeXstr + "$.")
            elif math.copysign(1, subVariable) == math.copysign(1, Variable) and \
                    (abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable)/10**floor(log10(abs(Variable))))/(abs(Variable)/10**floor(log10(abs(Variable))))) <= tolerance or \
                    abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable/10)/10**floor(log10(abs(Variable))))/(abs(Variable/10)/10**floor(log10(abs(Variable))))) <= tolerance or \
                    abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable*10)/10**floor(log10(abs(Variable))))/(abs(Variable*10)/10**floor(log10(abs(Variable))))) <= tolerance) and \
                    abs((abs(subVariable) - abs(Variable))/abs(Variable)) > tolerance:
                return("Check the exponent of $" + LaTeXstr + "$.")
            elif math.copysign(1, subVariable) != math.copysign(1, Variable) and \
                    (abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable)/10**floor(log10(abs(Variable))))/(abs(Variable)/10**floor(log10(abs(Variable))))) <= tolerance or \
                    abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable/10)/10**floor(log10(abs(Variable))))/(abs(Variable/10)/10**floor(log10(abs(Variable))))) <= tolerance or \
                    abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable*10)/10**floor(log10(abs(Variable))))/(abs(Variable*10)/10**floor(log10(abs(Variable))))) <= tolerance) and \
                    abs((abs(subVariable) - abs(Variable))/abs(Variable)) > tolerance:
                return("Check the sign and exponent of $" + LaTeXstr + "$.")
            else:
                return None
        else:
            return None
    else:
        return None

# def attribution(TorF, source = 'original', vol = 0, chapter = 0):
#     if TorF == 'true' or TorF == 'True' or TorF == 't' or TorF == 'T':
#         if source == 'OSUP':
#             return('<hr></hr><p><font size="-1">From chapter ' + str(chapter) + ' of <a href="https://openstax.org/books/university-physics-volume-' + str(vol) + \
#                     '/pages/' + str(chapter) + '-introduction" target="_blank">OpenStax University Physics volume ' + str(vol) + \
#                     '</a> licensed under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC BY 4.0</a>.</font><br> <font size="-1">Download for free at <a href="https://openstax.org/details/books/university-physics-volume-' + str(vol) + \
#                     '" target="_blank">https://openstax.org/details/books/university-physics-volume-' + str(vol) + \
#                     '</a>.</font><br> <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank"><pl-figure file-name="by.png" directory="clientFilesCourse" width="100px" inline="true"></pl-figure></a></p>')
#         elif source == 'original':
#             return('<hr></hr><p><font size="-1">Licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">CC BY-NC-SA 4.0</a>.</font><br><a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank"><pl-figure file-name="byncsa.png" directory="clientFilesCourse" width="100px" inline="true"></pl-figure></a></p>')
#         else:
#             return None
#     else:
#         return None

def roundp(*args,**kwargs):
    """ Wrapper function for the sigfig.round package. Also deals with case if requested sig figs is more than provided.

    Args:
        num (number): Number to round or format.

    Returns:
        float/str: Rounded number output to correct significant figures.
    """
    a = [item for item in args]
    kw = {item:v for item,v in kwargs.items() if item in ['sigfigs', 'decimals']}

    num_str = str(float(a[0]))

    # Create default sigfigs if necessary
    if kw.get('sigfigs',None) != None:
        z = kw['sigfigs']
    elif kw.get('decimals', None) != None:
        z = kw['decimals']
    else:
        z = 3 # Default sig figs
        kwargs['sigfigs'] = z

    # Handle big and small numbers carefully
    if abs(float(num_str)) < 1e-4 or abs(float(num_str)) > 1e15:
        power = int(abs(float(num_str))).as_integer_ratio()[1].bit_length() - 1
        if power < 0:
            power = 0
        num_str = format(float(num_str), f".{power}e")
        kwargs['notation'] = 'sci'
    else:
        num_str = num_str + str(0)*z*2

    # Add trailing zeroes if necessary
    if z > sigfigs(num_str):
        split_string = num_str.split("e")
        if "." not in split_string[0]:
            split_string[0] = split_string[0] + "."
        split_string[0] = split_string[0] + ("0"*(z - sigfigs(num_str)))
        num_str = "e".join(split_string)

    # sigfig.round doesn't like zero
    if abs(float(num_str)) == 0:
        result = num_str
        print("num is zero: " + result + "\n")
    else:
        result = sigfig.round(num_str,**kwargs)

    # Switch back to the original format if it was a float
    if isinstance(a[0],float):
        return float(result.replace(",", "")) # Note, sig figs will not be carried through if this is a float
    elif isinstance(a[0],str):
        return result
    elif isinstance(a[0],int):
        return int(float(result.replace(",", "")))
    else:
        return sigfig.round(*args,**kwargs)

def round_str(*args,**kwargs):

    if type(args[0]) is str:
        return args[0]

    if 'sigfigs' not in kwargs.keys() and 'decimals' not in kwargs.keys():
        kwargs['sigfigs'] = 2

    if 'format' not in kwargs.keys():
        if np.abs(args[0]) < 1:
            return roundp(*args,**kwargs,format='std')
        elif np.abs(args[0]) < 1E6:
            return roundp(*args,**kwargs,format='English')
        else:
            return roundp(*args,**kwargs,format='sci')
    else:
        return roundp(*args,**kwargs)

def num_as_str(num, digits_after_decimal = 2):
    """Rounds numbers properly to specified digits after decimal place

    Args:
        num (float): Number that is to be rounded
        digits_after_decimal (int, optional): Number of digits to round to. Defaults to 2.

    Returns:
        str: A string that is correctly rounded (you know why it's not a float!)
    """
    """
    This needs to be heavily tested!!
    WARNING: This does not do sig figs yet!
    """

    # Solution attributed to: https://stackoverflow.com/a/53329223

    if type(num) == str:
        return num
    elif type(num) == dict:
        return num
    else:
        tmp = Decimal(str(num)).quantize(Decimal('1.'+'0'*digits_after_decimal))

        return str(tmp)

def sign_str(number):
    """Returns the sign of the input number as a string.

    Args:
        sign (number): A number, float, etc...

    Returns:
        str: Either '+' or '-'
    """
    if (number < 0):
        return " - "
    else:
        return " + "

################################################
#
# Feedback and Hint Section
#
################################################

def automatic_feedback(data,string_rep = None,rtol = None):

    # In grade(date), put: data = automatic_feedback(data)

    if string_rep is None:
        string_rep = list(data['correct_answers'].keys())
    if rtol is None:
        rtol = 0.03

    for i,ans in enumerate(data['correct_answers'].keys()):
        data["feedback"][ans] = ErrorCheck(data['submitted_answers'][ans],
                                           data['correct_answers'][ans],
                                           string_rep[i],
                                           rtol)

    return data


# An error-checking function designed to give hints if the submitted answer is:
# (1) correct except for and overall sign or...
# (2) the answer is right expect for the power of 10 multiplier or...
# (3) answer has both a sign and exponent error.
def ErrorCheck(subVariable, Variable, LaTeXstr, tolerance):
    import math
    from math import log10, floor

    if subVariable is not None and subVariable != 0 and Variable != 0:
        if math.copysign(1, subVariable) != math.copysign(1, Variable) and abs((abs(subVariable) - abs(Variable))/abs(Variable)) <= tolerance:
            return("Check the sign of $" + LaTeXstr + "$.")
        elif math.copysign(1, subVariable) == math.copysign(1, Variable) and \
                (abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable)/10**floor(log10(abs(Variable))))/(abs(Variable)/10**floor(log10(abs(Variable))))) <= tolerance or \
                abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable/10)/10**floor(log10(abs(Variable))))/(abs(Variable/10)/10**floor(log10(abs(Variable))))) <= tolerance or \
                abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable*10)/10**floor(log10(abs(Variable))))/(abs(Variable*10)/10**floor(log10(abs(Variable))))) <= tolerance) and \
                abs((abs(subVariable) - abs(Variable))/abs(Variable)) > tolerance:
            return("Check the exponent of $" + LaTeXstr + "$.")
        elif math.copysign(1, subVariable) != math.copysign(1, Variable) and \
                (abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable)/10**floor(log10(abs(Variable))))/(abs(Variable)/10**floor(log10(abs(Variable))))) <= tolerance or \
                abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable/10)/10**floor(log10(abs(Variable))))/(abs(Variable/10)/10**floor(log10(abs(Variable))))) <= tolerance or \
                abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable*10)/10**floor(log10(abs(Variable))))/(abs(Variable*10)/10**floor(log10(abs(Variable))))) <= tolerance) and \
                abs((abs(subVariable) - abs(Variable))/abs(Variable)) > tolerance:
            return("Check the sign and exponent of $" + LaTeXstr + "$.")
        elif math.copysign(1, subVariable) == math.copysign(1, Variable) and abs((abs(subVariable) - abs(Variable))/abs(Variable)) <= tolerance:
            return("Nice work, $" + LaTeXstr + "$ is correct!")
        else:
            return None
    else:
        return None

def backticks_to_code_tags(data):
    """
    Converts backticks to <code> tags, and code fences to <pl-code> tags for a filled PrairieLearn question data dictionary.
    Note: this only makes replacements multiple choice (and other similar question) answer options.

    Args:
        html (str): The HTML to convert
    """
    params = data["params"]
    for param, param_data in params.items():
        if not param.startswith("part"):
            continue
        for answer, answer_data in param_data.items():
            if any(opt in answer for opt in {"ans", "statement", "option"}):
                if isinstance(value := answer_data["value"], str):
                    value = re.sub(
                        r"```(?P<language>\w+)?(?(language)(\{(?P<highlighting>[\d,-]*)\})?|)(?P<Code>[^`]+)```",
                        r'<pl-code language="\g<language>" highlight-lines="\g<highlighting>">\g<Code></pl-code>',
                        value,
                        flags=re.MULTILINE,
                    )
                    value = value.replace(' language=""', "")  # Remove empty language attributes
                    value = value.replace(
                        ' highlight-lines=""', ""
                    )  # Remove empty highlight-lines attributes
                    value = re.sub(r"(?<!\\)`(?P<Code>[^`]+)`", r"<code>\g<Code></code>", value)
                    value = value.replace("\\`", "`")  # Replace escaped backticks
                    data["params"][param][answer]["value"] = value

def base64_encode_string(string):
    """Encode a string into a base64 representation to act as a file for prarielearn
    """
    # Based off of https://github.com/PrairieLearn/PrairieLearn/blob/2ff7c5cc2435bae80c0ba512631749f9c3eadb43/exampleCourse/questions/demo/autograder/python/leadingTrailing/server.py#L9-L11
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")

def base64_decode_file(file):
    """Decode a base64 string which is a file from prairielearn into a useable string
    """
    # symetrical to base64_encode_string
    return base64.b64decode(to_decode.encode("utf-8")).decode("utf-8")

def string_to_pl_user_file(string, data):
    """Encode a string to base64 and add it as the user submitted code file
    """
    # partially based off of https://github.com/PrairieLearn/PrairieLearn/blob/2ff7c5cc2435bae80c0ba512631749f9c3eadb43/apps/prairielearn/elements/pl-file-upload/pl-file-upload.py#L114C1-L119
    parsed_file = {"name": "user_code.py", "contents": base64_encode_string(answer)}
    if isinstance(data["submitted_answers"].get("_files", None), list):
        data["submitted_answers"]["_files"].append(parsed_file)
    else:
        data["submitted_answers"]["_files"] = [parsed_file]

def create_html_table(table, width="100%", first_row_is_header=True, first_col_is_header=True, wrap_header_latex=False, wrap_nonheader_latex=False, ):
    """
    Convert a python table to HTML\n
    Example usage:\n
    server.py: data["params"]["table1"] = pbh.convert_markdown_table([["a", "b", "c"], ["x", "1"]], wrap_nonheader_latex=True)\n
    markdown: {{{ params.table1 }}}

    Args:
        table (list): A list of lists representing the table
        width (str, optional): The width of the table. Ex. "100%", "500px", etc.
        first_row_is_header (bool, optional): Whether the first row is a header. Defaults to True.
        first_col_is_header (bool, optional): Whether the first column is a header. Defaults to True.
        wrap_nonheader_latex (bool, optional): Whether to wrap all non-header table cells in $ for LaTeX. Defaults to False.
        wrap_header_latex (bool, optional): Whether to wrap all header table cells in $ for LaTeX. Defaults to False.
    """
    def wrap(x):
        return f"${x}$" if wrap_nonheader_latex else x
    def wrap_header(x):
        return f"${x}$" if wrap_header_latex else x

    def choose_el(x, i, j):
        if i == 0 and first_row_is_header:
            return f'<th>{wrap_header(x)}</th>'
        elif j == 0 and first_col_is_header:
            return f'<th>{wrap_header(x)}</th>'
        else:
            return f'<td>{wrap(x)}</td>'


    html = f'<table style="width:{width}">\n'
    for i, row in enumerate(table):
        html += "<tr>\n"
        elements = [choose_el(col, i, j) for j, col in enumerate(row)]
        html += "\n".join(elements)
        html += "\n</tr>"
    html += "\n</table>"
    return html


def template_mc(data, part_num, choices):
    """
    Adds multiple choice to data from dictionary

    Args:
        choices (dict): the multiple-choice dictionary

    Example:
        options = {
            'option1 goes here': ['correct', 'Nice work!'],
            'option2 goes here': ['Incorrect', 'Incorrect, try again!'],
            ....
        }

        template_mc(data2, 1, options)

    """
    for i, (key, value) in enumerate(choices.items()):
        data['params'][f'part{part_num}'][f'ans{i+1}']['value'] = key
        is_correct = value[0].strip().lower() == 'correct'
        data['params'][f'part{part_num}'][f'ans{i+1}']['correct'] = is_correct

        try:
            data['params'][f'part{part_num}'][f'ans{i+1}']['feedback'] = value[1]
        except IndexError:
            data['params'][f'part{part_num}'][f'ans{i+1}']['feedback'] = "Feedback is not available"
