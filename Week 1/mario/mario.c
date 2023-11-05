#include <stdio.h>
#include "cs50.h"

int get_height(void);
void pyramid(int size);


int main(void)
{
    int size = get_height();

    pyramid(size);
}


int get_height(void)
{
    int height;

    do
    {
        height = get_int("Height: ");
    } 
    while ((height < 0) || (height > 8));
    
    printf("\n");

    return height;
}


void pyramid(int size)
{
    for (int i = 1; i <= size; i++)
    {
        int space = (size - i);
        
        for (int j = 0; j < space; j++)
        {
            printf(" ");
        }
        
        for (int n = 1; n <= i; n++)
        {
            printf("#");
        }
        
        printf("  ");
        
        for (int x = 1; x <= i; x++)
        {
            printf("#");
        }
    }   
}