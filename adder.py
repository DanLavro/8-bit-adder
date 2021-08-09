def and_gate(x, y):
    """
    AND| 0 | 1
    --- --- ---
    0  | 0 | 0
    --- --- ---
    1  | 0 | 1
    --- --- ---
    """
    if x and y:
        return 1
    return 0


def or_gate(x, y):
    """
    OR | 0 | 1
    --- --- ---
    0  | 0 | 1
    --- --- ---
    1  | 1 | 1
    --- --- ---
    """
    if x or y:
        return 1
    return 0


def invert(x):
    """
    0 -> 1
    1 -> 0
    """
    return int(not (x))


def nor_gate(x, y):
    """
    NOR| 0 | 1
    --- --- ---
    0  | 1 | 0
    --- --- ---
    1  | 0 | 0
    --- --- ---
    """
    return invert(or_gate(x, y))


def nand_gate(x, y):
    """
    NAND| 0 | 1
    ---- --- ---
    0   | 1 | 1
    ---- --- ---
    1   | 1 | 0
    ---- --- ---
    """
    return invert(and_gate(x, y))


def xor_gate(x, y):
    """
    XOR| 0 | 1
    --- --- ---
    0  | 0 | 1
    --- --- ---
    1  | 1 | 0
    --- --- ---
    """
    return and_gate(or_gate(x, y), nand_gate(x, y))


def half_adder(first_digit, second_digit):
    """
    input: two bits
    output: sum bit and carry bit
    """
    sum_ = xor_gate(first_digit, second_digit)
    carry = and_gate(first_digit, second_digit)
    return sum_, carry


def adder(first_digit, second_digit, carry_in=0):
    """First digit - FD
    Second digit - SD
    Carry in - CI
    Sum - S
    Carry Out - COUT
    FD | SD | CI | S |COUT
    ---------------------
    0  | 0  | 0  | 0 | 0
    ---------------------
    0  | 1  | 0  | 1 | 0
    ---------------------
    1  | 0  | 0  | 1 | 0
    ---------------------
    1  | 1  | 0  | 0 | 1
    ---------------------
    0  | 0  | 1  | 1 | 0
    ---------------------
    0  | 1  | 1  | 0 | 1
    ---------------------
    1  | 0  | 1  | 0 | 1
    ---------------------
    1  | 1  | 1  | 1 | 1
    """
    sum_first, carry_first = half_adder(first_digit, second_digit)
    sum_, carry_second = half_adder(carry_in, sum_first)
    carry = or_gate(carry_first, carry_second)
    return sum_, carry


def adder_8_bit(first_8_bit_number, second_8_bit_number, carry=0):
    """full adder
    contains 2 adders(half adders) and OR gate
    """
    sum_output = []
    for i, j in zip(reversed(first_8_bit_number), reversed(second_8_bit_number)):
        sum_, carry = adder(int(i), int(j), carry)
        sum_output.insert(0, sum_)
    return sum_output, carry


def adder_16_bit(first_16_bit_number, second_16_bit_number, carry=0):
    """two 8-bit adders in a row"""
    first_8_bit_output, carry = adder_8_bit(first_16_bit_number[8:16], second_16_bit_number[8:16])
    second_8_bit_output, carry = adder_8_bit(first_16_bit_number[0:8], second_16_bit_number[0:8], carry)
    return second_8_bit_output + first_8_bit_output, carry


def ones_complement(input, invert_=0):
    """invert 8-bit
    10101010 -> 01010101
    """
    output = ''
    for i in input:
        output += str(xor_gate(int(i), invert_))
    return output


def adder_subtractor_8_bit(first_8_bit_number, second_8_bit_number, sub=0):
    """can also subtract
    :param sub: switch Adder(0)/Subtractor(1), default = 0 (add)
    """
    overflow = 0
    sum_output, carry = adder_8_bit(first_8_bit_number, ones_complement(second_8_bit_number, sub), sub)
    overflow = xor_gate(carry, sub)
    return sum_output, overflow


# ---INPUT/OUTPUT---
def underflow(result):
    return adder_subtractor_8_bit(ones_complement(result, 1), '00000001', 0)


def pre_output(result, overflow, sub):
    if sub == '1' and overflow == 1:
        result = underflow(result)
        return ''.join(str(number) for number in result[0])
    output_string = ''.join(str(number) for number in result)
    if overflow == 1:
        output_string = '1' + output_string
    return output_string


def main():
    exit_program = ''
    print("""All 8 bits of the number must be filled with 0 or 1
Examples:
00000000
11111111
01010101
00000001""")
    while exit_program != 'q':
        first_8_bit_number = input("Enter first 8-bit number")
        second_8_bit_number = input("Enter second 8-bit number")
        sub = input("Enter signal '1' for subtraction, or nothing for addition")

        result, overflow = adder_subtractor_8_bit(first_8_bit_number, second_8_bit_number, sub)
        print(pre_output(result, overflow, sub))

        exit_program = input("Type 'q' to stop this program, or nothing for continue(than 'Enter')")


if __name__ == '__main__':
    main()
