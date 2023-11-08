#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>


int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calculate_grade(int letters, int words, int sentences);

int main(void)
{
    string text = get_string("Text: ");

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    int grade = calculate_grade(letters, words, sentences);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{

    int letters = 0;
    int i = 0;


    while (text[i] != '\0')
    {
         text[i] = toupper(text[i]);

        if ((text[i] > 64) && (text[i] < 91))
        {
            letters++;
        }

        i++;
    }
    return letters;
}

int count_words(string text)
{
    int words = 0;
    int i = 0;

    while (text[i] != '\0')
    {
        if (text[i] == 32)
        {
            words++;
        }

        i++;
    }

    int first_letter = toupper(text[0]);

    if (first_letter > 64 && first_letter < 91)
    {
        words++;
    }
    return words;
}

int count_sentences(string text)
{
    int sentences = 0;
    int i = 0;

    while (text[i] != '\0')
    {
        if ((text[i] == '!') || (text[i] == '.') || (text[i] == '?'))
        {
            sentences++;
        }
        i++;
    }
    return sentences;
}

int calculate_grade(int letters, int words, int sentences)
{
    // index = 0.0588 * L - 0.296 * S - 15.8
    // L = avg no of letters per 100 words
    // S = avg no of sentences per 100 words
    float l = (((float) letters / (float) words) * 100);
    float s = (((float) sentences / (float) words )* 100);

    int grade = round(((0.0588 * l) - (0.296 * s) - 15.8));

    return grade;
}

