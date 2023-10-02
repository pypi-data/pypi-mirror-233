"""

Sorry for messy code...
This was just made as a project in my free time for fun, so my objective was just to get it working.

Will be adding as many mathimatical operators/functions as possible

"""

import copy

_division_by_0_error = f"(# / 0) is not definable"

def _remove_following_0(value : str) -> str:
    if not "." in value:
        value = f"{value}."

    integer, decimal = value.split(".")[0], value.split(".")[-1]

    for i in range(1, len(integer) + 1):
        int_slice = integer[0:len(integer) - i]
        if int_slice == len(int_slice) * "0":
            return f"{integer[len(integer) - i:len(integer)]}.{decimal}"

def _remove_trailing_0(value : str) -> str:
    if not "." in value:
        return value

    integer, decimal = value.split(".")[0], value.split(".")[-1]

    for i in range(1, len(decimal) + 1):
        dec_slice = decimal[0:len(decimal) - i]
        if dec_slice == len(dec_slice) * "0":
            return f"{integer}.{decimal[len(decimal) - i:len(decimal)]}"

def _guess(value1 : str, value2 : str) -> list:
    # out {operation} value2 
    # #d = definite
    #v 28 * 8 <= 259
    branches = {
        "5" : {"<" : "9", "=" : "5d", ">" : "1"},
        "1" : {"<" : "3", "=" : "1d", ">" : "0d"},
        "9" : {"<" : "9d", "=" : "9d", ">" : "7"},
        # lower branch
        "3" : {"<" : "4", "=" : "3d", ">" : "2"},
        "4" : {"<" : "4d", "=" : "4d", ">" : "3d"},
        "2" : {"<" : "2d", "=" : "2d", ">" : "1d"},
        # higher branch
        "7" : {"<" : "8", "=" : "7d", ">" : "6"},
        "6" : {"<" : "6d", "=" : "6d", ">" : "5d"},
        "8" : {"<" : "8d", "=" : "8d", ">" : "7d"}
    }
    value1, value2 = value1.replace(".",""), value2.replace(".","")

    carry_over = "0"
    i = 0
    while True:
        i += 1
        if i == 1:
            carry_over = "5"

        if "d" in carry_over:
            carry_over = carry_over.replace("d", "")
            return carry_over, multiplication(f"{value1}{carry_over}", carry_over).replace(".", "")

        out = multiplication(f"{value1}{carry_over}", carry_over).replace(".", "")
        if int(out) < int(value2):
            carry_over = branches[carry_over]["<"]
        elif int(out) == int(value2):
            carry_over = branches[carry_over]["="]
        else:
            carry_over = branches[carry_over][">"]

def _guess_square(value : str) -> list:
    branches = [81, 64, 49, 36, 25, 16, 9, 4, 1]
    for x in range(0, 9):
        if branches[x] <= int(value):
            return str(9 - x), str(branches[x])
    return "0", "0"
        
def addition(value1 : str, value2 : str) -> str:
    # value_1 is the largest integer in terms of length or if = (>=).
    final_value = ""

    val1_sign = "-" if "-" in value1 else ""
    val2_sign = "-" if "-" in value2 else ""
    sign = ""

    if val1_sign == "-" and val2_sign == "-":
        sign = "-"
    elif val1_sign == "-" and val2_sign == "":
        return subtraction(value2, value1.replace("-",""))
    elif val1_sign == "" and val2_sign == "-":
        return subtraction(value1, value2.replace("-",""))

    value1, value2 = value1.replace("-", ""), value2.replace("-", "")

    if not "." in value1: value1 = f"{value1}."
    if not "." in value2: value2 = f"{value2}."

    value1_int, value1_dec = value1.split(".")[0], value1.split(".")[-1]
    value2_int, value2_dec = value2.split(".")[0], value2.split(".")[-1]

    if len(value1_dec) < len(value2_dec):
        value1_dec = value1_dec + "0" * (len(value2_dec) - len(value1_dec))
    elif len(value2_dec) < len(value1_dec):
        value2_dec = value2_dec + "0" * (len(value1_dec) - len(value2_dec))

    if len(value1_int) < len(value2_int):
        value1_int = "0" * (len(value2_int) - len(value1_int)) + value1_int
    elif len(value2_int) < len(value1_int):
        value2_int = "0" * (len(value1_int) - len(value2_int)) + value2_int

    value1 = f"{value1_int}.{value1_dec}"
    value2 = f"{value2_int}.{value2_dec}"
    reg1, reg2, reg3, reg4 = 0,0,0,0

    # addition
    for x in range(1, len(value1) + 1):
        if value1[len(value1) - x] == ".":
            final_value = f".{final_value}"
            continue

        reg1 = int(value1[len(value1) - x])
        reg2 = int(value2[len(value2) - x])

        reg4 = reg1 + reg2 + reg3
        reg3 = 0
        # carry over
        if reg4 >= 10:
            reg3 = 1
            reg4 -= 10

        final_value = f"{reg4}{final_value}"
    if reg3 > 0:
        final_value = f"{reg3}{final_value}"

    if final_value[len(final_value) - 1] == ".":
        final_value = final_value.removesuffix(".")
    return f"{sign}{final_value}"

def subtraction(value1 : str, value2 : str) -> str:
    # value_1 is the largest integer in terms of length or if = (>=).
    final_value = ""

    val1_sign = "-" if "-" in value1 else ""
    val2_sign = "-" if "-" in value2 else ""

    if val1_sign == "-" and val2_sign == "":
        return "-"+addition(value1.replace("-",""), value2)
    elif val1_sign == "" and val2_sign == "-":
        return addition(value1, value2.replace("-",""))
        
    value1, value2 = value1.replace("-", ""), value2.replace("-", "")

    if not "." in value1: value1 = f"{value1}."
    if not "." in value2: value2 = f"{value2}."

    value1_int, value1_dec = value1.split(".")[0], value1.split(".")[-1]
    value2_int, value2_dec = value2.split(".")[0], value2.split(".")[-1]

    if len(value1_dec) < len(value2_dec):
        value1_dec = value1_dec + "0" * (len(value2_dec) - len(value1_dec))
    elif len(value2_dec) < len(value1_dec):
        value2_dec = value2_dec + "0" * (len(value1_dec) - len(value2_dec))

    if len(value1_int) < len(value2_int):
        value1_int = "0" * (len(value2_int) - len(value1_int)) + value1_int
    elif len(value2_int) < len(value1_int):
        value2_int = "0" * (len(value1_int) - len(value2_int)) + value2_int

    value1 = f"{value1_int}.{value1_dec}"
    value2 = f"{value2_int}.{value2_dec}"

    sign = ""
    if int(value2.replace(".","")) > int(value1.replace(".","")):
        value1, value2 = value2, value1
        sign = "-"

    reg1, reg2, reg3, reg4 = 0,0,0,0

    # subtract
    for x in range(1, len(value1 if len(value1) > len(value2) else value2) + 1):
        if value1[len(value1) - x] == ".":
            final_value = f".{final_value}"
            continue

        reg1 = int(value1[len(value1) - x]) + reg3
        reg2 = int(value2[len(value2) - x])
        reg3 = 0

        # carry over
        if reg1 < reg2:
            reg1 += 10
            reg3 = -1
        reg4 = reg1 - reg2

        final_value = f"{reg4}{final_value}"

    if final_value[len(final_value) - 1] == ".":
        final_value = final_value.removesuffix(".")

    return f"{sign}{final_value}"

def multiplication(value1 : str, value2 : str) -> str:
    final_value = "0"

    value1 = _remove_following_0(value1)
    value2 = _remove_following_0(value2)

    sign = "-"
    if ("-" in value1) == ("-" in value2):
        sign = ""
    value1, value2 = value1.replace("-", ""), value2.replace("-", "")

    if not "." in value1: value1 = f"{value1}."
    if not "." in value2: value2 = f"{value2}."

    value_dec_places = len(value1.split(".")[-1]) + len(value2.split(".")[-1])    
    
    value1, value2 = value1.replace(".",""), value2.replace(".","")

    if len(value2) > len(value1):
        value1, value2 = value2, value1

    reg1, reg2, reg3, reg4 = 0,0,0,0 

    # multiply
    for x in range(1, len(value1) + 1):
        reg1 = int(value1[len(value1) - x])
        if reg1 == 0:
            continue

        for i in range(1, len(value2) + 1):
            reg2 = int(value2[len(value2) - i])

            if reg2 == 0:
                continue

            reg4 = (reg1 * reg2) + reg3
            reg3 = 0

            if reg4 >= 10 and i != len(value2):
                reg3 = int(str(reg4)[0])
                reg4 = str(reg4)[-1]
    
            final_value = addition(final_value, str(reg4) + ("0" * (x - 1 + (i - 1))))
    if reg3 > 0:
        final_value = f"{reg3}{final_value}"

    return sign + final_value[:len(final_value) - value_dec_places] + "." + final_value[len(final_value) - value_dec_places:]

def division(value1 : str, value2 : str, precision : int = 100) -> str:
    final_value = ""

    sign = "-"
    if ("-" in value1) == ("-" in value2):
        sign = ""

    value1, value2 = value1.replace("-", ""), value2.replace("-", "")

    if not "." in value1: value1 = f"{value1}."
    if not "." in value2: value2 = f"{value2}."

    dec_pos = len(value1.split(".")[0]) + len(value2.split(".")[-1])
    
    value1, value2 = value1.replace(".",""), value2.replace(".","")

    reg1, reg2, reg3 = "0",0,"0"

    i = -1
    l = 0
    while True:
        i += 1

        if i == dec_pos:
            final_value = f"{final_value}."
        if i >= len(value1):
            if int(reg2) != 0 or int(reg3) != 0:
                l += 1
                value1 = f"{value1}0"
            else:
                break

        reg1 = value1[i - reg2:i + 1]
        if reg3 != "0":
            reg1 = f"{reg3}{reg1}"

        if int(reg1[0:4300]) < int(value2):
            reg2 += 1
            final_value = f"{final_value}0"
            continue

        multiplace = "0"
        revolutions = 0
        # find amount of times this occures
        while True:
            _ = addition(multiplace, value2)
            if int(_) > int(reg1): break

            multiplace = _
            if multiplace == value2 and revolutions > 10:
                return _division_by_0_error
            revolutions += 1
        reg2 = 0
        reg3 = subtraction(reg1, multiplace)

        final_value = f"{final_value}{revolutions}"

        if l >= precision:
            break
    return sign + _remove_following_0(final_value)

def exponential(value1 : str, exp : str) -> str:
    final_value = "1"

    if int(value1.split(".")[-1]) == 0:
        value1 = value1.split(".")[0]

    for x in range(0, int(exp)):
        final_value = multiplication(final_value, value1)
    return final_value

def factorial(value : str) -> str:
    """
    Decimals and negative numbers not currently calculable.
    """
    final_value = "1"

    value = value.split(".")[0]

    for x in range(1, int(value) + 1):
        final_value = multiplication(final_value, str(x))
    return final_value

def sin(value : str, precision : int = 10) -> str:
    """
    Integer values between 0-2pi are recommended. Anything larger will reqiure precision to be higher than 10.
    """
    final_value = value
    # format:
    # x - x^3/3! + x^5/5! - x^7/7! + x^9/9!...
    value = value.replace("-", "")

    if not "." in value: value = f"{value}."

    num, denom = "",""

    for i in range(1, precision + 1):
        num = exponential(value, str(2*i + 1))
        denom = factorial(str(2*i + 1))

        if i % 2 == 1:
            final_value = subtraction(final_value, division(num, denom, precision))
        else:
            final_value = addition(final_value, division(num, denom, precision))
    return final_value

def square_root(value : str, precision : int = 100) -> str:
    final_value = ""
    val_sign = "-" if "-" in value else ""

    value = value.replace("-", "")

    if not "." in value: value = f"{value}."

    dec_pos = len(value.split(".")[0])

    value = value.replace(".","")

    reg1, reg2, reg3, reg4, reg5 = "0","0","0","0","0"

    i = -1
    l = 0
    # if odd then == 1
    offset = int(dec_pos % 2 == 1)
    while True:
        i += 1
        if l > precision or (int(reg3) == 0 and 2*i >= len(value)):
            break

        if 2*i >= len(value):
            l += 1
            value = f"{value}00"
        
        if 2*i == dec_pos + offset:
            final_value = f"{final_value}."

        # if i == 0 and offset then offset - 1
        reg1 = value[2*i - (offset if i > 0 else 0):2*i + 2 - offset]

        if i == 0:
            reg4, reg5 = _guess_square(reg1)

            reg2 = multiplication(reg4, "2").replace(".", "")
            reg3 = subtraction(reg1, reg5)
        else:
            reg4, reg5 = _guess(reg2, f"{reg3}{reg1}")

            reg2 = addition(reg2 + reg4, reg4)
            reg3 = subtraction(f"{reg3}{reg1}", reg5)
        
        final_value = f"{final_value}{reg4}"

    return final_value + ("i" if val_sign == "-" else "")

def round(value : str, decimals : int = 0):
    value_dec = value.split(".")[-1]
    value_int = value.split(".")[0]
    if len(value_dec) < decimals + 1:
        value_dec = value_dec + "0" * (decimals - len(value_dec) + 1)
        value = value.split(".")[0] + "." + value_dec
    if int(value_dec[decimals]) >= 5:
        value = value[:len(value_int) + decimals + 1]
        value = addition(value, "0." + "0"*(decimals - 1) + "1")
    else:
        value = value[:len(value_int) + decimals + 1]

    return value

def __calc_lim(parsed_equation : dict, x_goes_towards : str, side, precision : int = 50) -> str:
    x_goes_towards = x_goes_towards[:-1] if (x_goes_towards[-1] == "+" or x_goes_towards[-1] == "-") else x_goes_towards
    lim = calculate(copy.deepcopy(parsed_equation), side(x_goes_towards, "0."+"0"*precision+"1"))
    lim_mprecise = calculate(copy.deepcopy(parsed_equation), subtraction(x_goes_towards, "0."+"0"*(precision + 5)+"1"))

    lim_out = _remove_trailing_0(round(lim, precision))
    lim_out_mprecise = _remove_trailing_0(round(lim_mprecise, precision + 5))
    if len(lim_out_mprecise) > len(lim_out):
        if lim_out[0] == "-": return "-∞"
        else: return "∞"
    else:
        return lim_out 

def limit(equation : str, x_goes_towards : str, precision : int = 50) -> str:
    parsed_equation = parser(equation)

    try:
        t_x_goes_towards = x_goes_towards[:-1] if (x_goes_towards[-1] == "+" or x_goes_towards[-1] == "-") else x_goes_towards
        out = calculate(copy.deepcopy(parsed_equation), t_x_goes_towards)
        if out != _division_by_0_error:
            return out
    except: pass # if undefined


    if x_goes_towards[-1] == "+":
        return __calc_lim(copy.deepcopy(parsed_equation), x_goes_towards, addition, precision)
    elif x_goes_towards[-1] == "-":
        return __calc_lim(copy.deepcopy(parsed_equation), x_goes_towards, subtraction, precision)
    else:
        upper_lim = __calc_lim(copy.deepcopy(parsed_equation), x_goes_towards, addition, precision)
        lower_lim = __calc_lim(copy.deepcopy(parsed_equation), x_goes_towards, subtraction, precision)

        if upper_lim == lower_lim:
            return upper_lim
        else:
            return "DNE"

######################################## EQUATION PARSER ########################################

def parser(expression : str):
    parsed = {}
    parentheses_queue = []
    expression = expression.replace(" ","")

    operators = ["+", "-", "*", "/", "^", "!"]
    functions = ["sqrt(", "sin("]

    parentheses = 0
    extra_val = 0
    # False = <-    ...     True = ->
    cur_side = False

    read_queue = ""
    for char in expression:
        read_queue += char

        if char == "(":
            try:
                old_paren = parentheses_queue[0]
            except: old_paren = parentheses
            parentheses += 1
            parentheses_queue.insert(0, parentheses)
            try:
                if parsed[str(old_paren)][1] != None:
                    parsed[str(old_paren)][-1] = f"dict-{parentheses_queue[0]}"
                else:
                    parsed[str(old_paren)][0] = f"dict-{parentheses_queue[0]}"
            except: pass # no values in dict
            parsed.update({str(parentheses_queue[0]) : [None, None, None]})
            read_queue = ""
        elif char == ")":
            op_index = None
            chosen_op = None
            
            if parsed.get(str(parentheses_queue[0]))[-1] == None:
                right = read_queue.split(parsed.get(str(parentheses_queue[0]))[1])[-1][:-1]
                parsed[str(parentheses_queue[0])][-1] = right

            #szparsed[str(parentheses)][-1] = read_queue[:-1]
            read_queue = ""
            parentheses_queue.pop(0)

        if char in operators:
            if parsed[str(parentheses_queue[0])][0] == None:
                parsed[str(parentheses_queue[0])][0] = read_queue[:-1]
            parsed[str(parentheses_queue[0])][1] = char

    return parsed

def calculate(equation : dict, x_val : str = None) -> str:
    """
    This function is for calculation based off known values. This will not solve for variables.
    """
    operators = {'+' : addition, '-' : subtraction, '*' : multiplication, 
                 '/' : division, '^' : exponential, '!' : factorial}
    current_val = []
    solved_vals = {}
    for x in range(0, len(equation)):
        current_val = equation[str(len(equation) - x)]

        if "x" in current_val:
            if x_val == None:
                raise ValueError("'x_val' must be input if variable 'x' is in the equation")
        for i in range(0, len(current_val)):
            if current_val[i] == "x":
                current_val[i] = str(x_val)
                
            if 'dict' in current_val[i]:
                current_val[i] = solved_vals.get(current_val[i].replace("dict-", ""))

        final_val = operators.get(current_val[1])(current_val[0], current_val[-1])
        solved_vals.update({f"{len(equation) - x}" : final_val})
    return solved_vals["1"] 

def solve(equation : str, x_val : str = None) -> str:
    parsed_equation = parser(equation)
    return calculate(parsed_equation, x_val)