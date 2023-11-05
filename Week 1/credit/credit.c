#include <cs50.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

bool validation(long card, int length);
string get_company(long card, int length);
int get_length(long card);


int main(void)
{
    long card = get_long("Number: ");
    int length = get_length(card);

    if ((validation(card, length)) == false)
    {
        printf("INVALID\n");
    }

    else
    {
        string company = get_company(card, length);
        printf("%s\n", company);
    }
}

bool validation(long card, int length)
{
    // Validating the length
    if ((length != 13) && (length != 15) && (length != 16))
    {
        return false;
    }

    // Doing the checksum
    long long j = card;
    int sum1 = 0;
    int remainder1;
    int remainder0;

    // Doubling and adding every other digit
    while (j != 0)
    {
        remainder1 = 2 * ((j % 100) / 10);
        remainder0 = remainder1 % 10 + round(remainder1 / 10);
        sum1 = sum1 + remainder0;
        j = j / 100;
    }

    // Adding the other digits

    long long k = card;
    int sum2 = 0;
    int remainder2;

    while (k != 0)
    {
        remainder2 = k % 10;
        sum2 = sum2 + remainder2;
        k = k / 100;
    }

    int checksum = sum1 + sum2;

    // Checking if last digit is 0
    if ((checksum % 10) == 0)
    {
        return true;
    }
    else
    {
        return false;
    }

}

int get_length(long card)
{
    int length = 0;
    while(card)
    {
        length += 1;
        card /= 10;
    }
    return length;
}

string get_company(long card, int length)
{

    long first_two = card;
    do
    {
        first_two /= 10;
    }
    while (first_two >= 100);

    
    if (((first_two == 34) || (first_two == 37)) && (length == 15))
    {
        return "AMEX";
    }
    else if (((first_two / 10) == 5) && (0 < (first_two % 10) && ((first_two % 10) < 6)) && (length == 16))
    {
        return "MASTERCARD";
    }
    else if ((first_two / 10 == 4) && ((length == 13) || (length == 16)))
    {
        return "VISA";
    }
    else
    {
        return "INVALID";
    }
}