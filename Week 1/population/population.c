#include <stdio.h>
#include <cs50.h>

int start_size(void);
int end_size(int start_size);
int calc_years(int start_size, int end_size);


int main(void)
{
    int start = start_size();

    int end = end_size(start);

    int years = calc_years(start, end);

    printf("Years: %i\n", years);
}


// Get the starting size

int start_size(void)
{
    int n;
    do
    {
        n = get_int("Start size: ");
    }
    while (n < 9);

    return n;
}


// Get the ending size

int end_size(int start_size)
{
    int n;
    do
    {
        n = get_int("End size: ");
    }
    while (n < start_size);

    return n;
}


// Find the number of years needed to reach end population

int calc_years(int start_size, int end_size)
{
    int lamas = start_size;
    int years = 0;

    while (lamas < end_size)
    {
        int died = (lamas / 4);
        int born = (lamas / 3);

        lamas = (lamas + born - died);
        years++;
    }

    return years;
}