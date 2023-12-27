def main():
    number = input("NUMBER: ")
    length = len(number)

    validity = isvalid(number, length)
    corp = company(number, length)

    if (validity == True) and (corp != None):
        print(corp)
    else:
        print("INVALID")


def isvalid(card, length):

    if length > 16:
        return False

    # Initilizing variables for negative indexing
    n = length * -1
    i = -1

    total_one = 0
    total_two = 0

    while i >= n:
        # Non underlined digits
        if i % 2 == 1:
            total_one += int(card[i])
            i -= 1

        # Multiply underlined digits by 2
        else:
            digit = str(int(card[i]) * 2)

            # Add digits of products to total_two
            for char in digit:
                total_two += int(char)
            i -= 1

    # Add both totals
    grand_total = total_one + total_two

    # Check if last digit is 0
    if grand_total % 10 == 0:
        return True
    else:
        return False



def company(card, length):
    first_two_digits = card[:2]

    # 15 digits and starts with 31 or 37
    if (length == 15) and (first_two_digits in ["31", "37"]):
        return "AMEX"

    # 16 digits and starts with numbers from 51-55
    elif (length == 16) and (50 < int(first_two_digits) < 56):
        return "MASTERCARD"

    # 13 or 16 digits and starts with 4
    elif ((length == 13 or length == 16) and (card[0] == "4")):
        return "VISA"

    else:
        return None

if __name__ == "__main__":
    main()
