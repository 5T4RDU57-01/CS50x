#include <cs50.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>

bool key_validation(string key);
void print_ciphertext(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Use the key as a command-line argument!\n");
        return 1;
    }
    if (key_validation(argv[1]) == false)
    {
        printf("Invalid key!\n");
        return 1;
    }
    else
    {
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");
        print_ciphertext(plaintext, argv[1]);
        printf("\n");
    }
}

bool key_validation(string key)
{
    int len = strlen(key);

    if (len != 26)
    {
        return false;
    }

    int frequency[26] = {0};

    for (int i = 0; i < len; i++)
    {
        char x = tolower(key[i]);

        if (x >= 'a' && x <= 'z')
        {
            frequency[x - 'a']++;
        }
        else
        {
            return false;
        }
    }
    for (int j = 0; j < 26; j++)
    {

        if (frequency[j] != 1)
        {
            return false;
        }
    }

    return true;
}

void print_ciphertext(string plaintext, string key)
{
    int len = strlen(plaintext);

    for (int i = 0; i < len; i++)
    {
        if (isalpha(plaintext[i]) != 0)
        {
            if (islower(plaintext[i]) != 0)
            {
                char cipher = tolower(key[plaintext[i] - 'a']);
                printf("%c", cipher);
            }
            else
            {
                char cipher = toupper(key[plaintext[i] - 'A']);
                printf("%c", cipher);
            }
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
}


