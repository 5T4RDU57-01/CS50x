from cs50 import get_int

def main():

    while True:
        h = get_int("Height: ")

        if h > 8 or h < 1:
            continue
        else:
            break

    print_pyramid(h)


def print_pyramid(height):
    i = 1
    j = 1

    while i <= height:
        while j <= height:
            spaces = height - i
            print(" " * spaces, end='')
            print("#" * i, end='')
            print(" " * 2, end='')
            print("#" * i, end='')
            print()

            i += 1
            j += 1



if __name__ == "__main__":
    main()
