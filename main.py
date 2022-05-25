# Rez, Imz and operator have to be separated with space
# In case of only Rez or only Imz, spaces are not allowed
# eg: "5 - 4i", "5 + 4i", "5", "-5i"

def complex_error(number):
    msg = f"Number: ({number}) is invalid "
    raise ValueError(msg)

def try_parsing_to_float(number):
    try:
        float(number)
    except ValueError:
        complex_error(number)

# Conversts user readable number to easy to calculate structure
def parse_to_complex(complex):
    export = {
        "rez": 0,
        "imz": 0,
        "operator": "+"
    }
    # check if has both rez and imz
    if " " in complex:
        complex_sliced = complex.split(" ")
        if len(complex_sliced) != 3:
            complex_error(complex)
        rez = complex_sliced[0]
        if len(complex_sliced[2]) - 1:
            imz = complex_sliced[2].replace("i", "").replace("I", "")
        else:
            imz = 1
        operator = complex_sliced[1]
        if not "+" in operator and not "-" in operator:
            complex_error(complex)
        try_parsing_to_float(rez)
        try_parsing_to_float(imz)
        export["rez"] = float(rez)
        export["imz"] = float(imz)

        if operator == "-":
            operator = "+"
            export["imz"] = -export["imz"]
        export["operator"] = operator

    # check if has imz only
    elif "i" in complex.lower():
        imz = complex.replace("i", "").replace("I", "")
        if not imz:
            imz = "1"
        try_parsing_to_float(imz)
        export["imz"] = float(imz)

    # if has rez only
    else:
        try_parsing_to_float(complex)
        export["rez"] = float(complex)
    return export

# Converts positive number to negative and vice versa
def handle_subtraction(complex_data):
    # print(complex_data["rez"])
    # print(complex_data["imz"])
    complex_data["rez"] = -complex_data["rez"]
    complex_data["imz"] = -complex_data["imz"]
    return complex_data

# takes array of complex numbers prepared for calculations by parse_complex function
def complex_sum(complex_arr):
    rez_sum = 0
    imz_sum = 0
    operator = ""
    for complex_data in complex_arr:
        rez_sum += complex_data["rez"]
        if "+" in complex_data["operator"]:
            imz_sum += complex_data['imz']
        else:
            imz_sum -= complex_data['imz']

    if imz_sum < 0:
        imz_sum = abs(imz_sum)
        operator = "-"
    else:
        operator = "+"

    # convert to int if possible
    if rez_sum != 0 and rez_sum.is_integer():
        rez_sum = int(rez_sum)
    if imz_sum != 0 and imz_sum.is_integer():
        imz_sum = int(imz_sum)

    if rez_sum and imz_sum:
        return f"{rez_sum} {operator} {imz_sum}i"
    if rez_sum and not imz_sum:
        return f"{rez_sum}"
    if imz_sum and not rez_sum:
        if operator == "+":
            return f"{imz_sum}i"
        return f"-{imz_sum}i"

# takes fex: (1 - 4i) + 4 * (2 - 9i)
def parse_raw_data_to_complex_data(data):
    eq = data
    eq_data = []
    buffer = ""
    i = 0
    while i < len(eq):
        if eq[i] == "(":
            i += 1
            while eq[i] != ")":
                buffer += eq[i]
                i += 1
            eq_data.append(buffer)
            buffer = ""
        elif eq[i] == " ":
            i += 1
            while eq[i] != " ":
                buffer += eq[i]
                i += 1
            eq_data.append(buffer)
            buffer = ""
        elif eq[i] != " ":
            while i < len(eq) and eq[i] != " ":
                buffer += eq[i]
                i += 1
            eq_data.append(buffer)
            buffer = ""
        i += 1
    i = 0
    complex_arr = []
    while i < len(eq_data):
        if eq_data[i] == "-":
            i += 1
            complex_arr.append(handle_subtraction(parse_to_complex(eq_data[i])))
            i += 1
        elif eq_data[i] == "+":
            i += 1
            complex_arr.append(parse_to_complex(eq_data[i]))
            i += 1
        elif eq_data[i] == "*":
            raise ValueError("Cant handle multiplication")
        elif eq_data[i] == "/":
            raise ValueError("Cant handle division")
        elif i == 0:
            complex_arr.append(parse_to_complex(eq_data[i]))
            i += 1
        else:
            raise ValueError(f"Something went wrong for item {eq_data[i]} at index {i}")
    return complex_arr

def matrix_input():
    print("Eg input: 4 - 9i")
    tl_complex = input("Top-Left number: ")
    tr_complex = input("Top-Right number: ")
    bl_complex = input("Bottom-Left number: ")
    br_complex = input("Bottom-right number: ")
    tl_space = "     "
    tr_space = ""
    bl_space = "     "
    br_space = ""
    if len(tl_complex) >= len(bl_complex):
        bl_space = bl_space + " " * (len(tl_complex) - len(bl_complex))
    else:
        tl_space = tl_space + " " * (len(bl_complex) - len(tl_complex))
    if len(tr_complex) >= len(br_complex):
        br_space = br_space + " " * (len(tr_complex) - len(br_complex))
    else:
        tr_space = tr_space + " " * (len(br_complex) - len(tr_complex))
    print(f"""
    Matrix  ==  | {tl_complex}{tl_space}{tr_complex}{tr_space} |
                | {bl_complex}{bl_space}{br_complex}{br_space} |
                """)
    return [tl_complex, tr_complex, bl_complex, br_complex]

# takes 2 x complex datatype
def complex_multiplication(x, y):
    a, b, c, d = 0, 0, 0, 0
    if x["rez"]:
        if y["rez"]:
            a = x["rez"] * y["rez"]
        if y["imz"]:
            b = x["rez"] * y["imz"]
    if x["imz"]:
        if y["rez"]:
            c = x["imz"] * y["rez"]
        if y["imz"]:
            d = x["imz"] * y["imz"]
    rez, imz = 0, 0
    if a:
        rez += a
    if b:
        imz += b
    if c:
        imz += c
    if d:
        rez += -d

    if rez and imz > 0:
        return f"{rez} + {imz}i"
    if rez and imz < 0:
        return f"{rez} - {-imz}i"
    if not rez:
        return f"{imz}i"
    return f"{rez}"

def matrix2d_calculator():
    data = matrix_input()
    tl = parse_to_complex(data[0])
    tr = parse_to_complex(data[1])
    bl = parse_to_complex(data[2])
    br = parse_to_complex(data[3])

    left = parse_to_complex(complex_multiplication(tl, br))
    right = handle_subtraction(parse_to_complex(complex_multiplication(tr, bl)))
    return complex_sum([left, right])

def part_of_admittance(R, XL, XC):
    if not "i" in XL.lower() and XL != "0":
        raise ValueError("XL provided has no i number")
    if not "i" in XC.lower() and XC != "0":
        raise ValueError("XC provided has no i number")

    a = parse_to_complex(XL)
    b = handle_subtraction(parse_to_complex(XC))
    imzZ = complex_sum([a, b])

    if not imzZ:
        try:
            y = round((1/float(R)), 4)
            return y
        except ValueError:
            raise ValueError("R provided is invalid")

    z = complex_sum([parse_to_complex(R), parse_to_complex(imzZ)])
    z = parse_to_complex(z)
    if z["imz"]:
        imz = z["imz"]
        zz = parse_to_complex(f"{z['rez']} {z['operator']} {-z['imz']}i")

        denominator = complex_multiplication(z, zz)
        if not denominator:
            raise ValueError("Denominator is 0")
        denominator = parse_to_complex(denominator)
        numerator = z
        # print(numerator, "/", denominator)
        rez, imz = 0, 0
        if numerator['rez']:
            rez = numerator['rez']/denominator['rez']
        if numerator['imz']:
            imz = numerator['imz']/denominator['rez']

        rez = round(rez, 4)
        imz = round(imz, 4)
        if rez and imz > 0:
            return f"{rez} + {imz}i"
        if rez and imz < 0:
            return f"{rez} - {abs(imz)}i"
        if rez:
            return f"{rez}"
        if imz:
            return f"{imz}i"
    else:
        adm = round((1/z["rez"]), 4)
        return f"{adm}"

def main():
    while True:
        x = input("Choose an option (or type help): ")
        if x == "help":
            print("1 - Admittance calculator")
            print("2 - 2D matrix calculator")
            print("3 - Complex sum calculator")
            print("0 - Exit")
        elif x == "0":
            return
        elif x == "1":
            print("Admittance calculator, please enter values below")
            r = input("Resistance (ex: 12): ")
            xl = input("XL (ex: 15i): ")
            xc = input("XC (ex: 15i): ")
            x = part_of_admittance(r, xl, xc)
            print(x)
        elif x == "2":
            print("2D matrix calculator")
            x = matrix2d_calculator()
            if not x:
                x = 0
            print(x)
        elif x == "3":
            print("Sum calculator")
            x = parse_raw_data_to_complex_data(input("Ex input (2 - 4i) + 9i - (-2 + 2i) + 3: "))
            x = complex_sum(x)
            print(x)

main()



