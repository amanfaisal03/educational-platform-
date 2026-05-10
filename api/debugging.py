def  debugging():
    number1=int(input("Enter a number: "))
    number2=int(input("Enter another number: "))
    result1 =number1 * number2

    for i in range(1, 11):
        if i == 1:
            number1 = 3 * number2
            if number1 < 100 :
                number2=number2 - 3
        elif i == 2:
            number1 = number1 + 5
            if number1 < 100 :
                number2=number2 - 3
        elif i == 3:
            number1 = number1 - 2
            if number1 < 100 :
                number2=number2 - 3
        elif i == 4:
            number1 = number1 * 2
            if number1 < 100 :
                number2=number2 - 3
        elif i == 5:
            number1 = number1 / 2
            if number1 > 100 :
                number2=number2 - 3
        elif i == 6:
            number1 = number1 + 10
            if number1 > 100 :
                number2=number2 - 3
        elif i == 7:
            number1 = number1 - 5
            if number1 > 100 :
                number2=number2 - 3
        elif i == 8:
            number1 = number1 * 3
            if number1 > 100 :
                number2=number2 - 3
        elif i == 9:
            number1 = number1 / 3
            if number1 > 100 :
                number2=number2 - 3
        elif i == 10:
            number1 = number1 + 20
            if number1 > 100 :
                number2=number2 - 3
    print("The final result is:", number1)

if __name__ == '__main__':
    debugging()
