// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Declaring some vars used later

unsigned int word_count;
unsigned int hash_value;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word
    unsigned int word_hash = hash(word);

    // Go to corresponding bucket
    node *arrow = table[word_hash];

    // Move through linked list to look for word
    while (arrow != 0)
    {
        if (strcasecmp(arrow->word, word) == 0)
        {
            return true;
        }
        arrow = arrow->next;
    }


    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Inspiration taken from https://www.geeksforgeeks.org/hash-functions-and-list-types-of-hash-functions/

    // Take the sum of ASCiI values and divide by N, return remainder
    int len = strlen(word);
    int total = 0;

    for (int i = 0; i < len; i++)
    {
        total += tolower(word[i]) + total;
    }

    return (total % N);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the file
    FILE *dict = fopen(dictionary, "r");

    if (dict == NULL)
    {
        return false;
    }

    // Read each word
    char word[LENGTH + 1];

    while (fscanf(dict, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));

        if (new_node == NULL)
        {
            unload();
            return false;
        }
        else
        {
            // Copy the word to its place
            strcpy(new_node->word, word);

            // Get hash value
            hash_value = hash(word);

            // Insert the node at the hash value
            new_node->next = table[hash_value];
            table[hash_value] = new_node;

            // Append word count
            word_count++;
        }
    }
    // Close file and return True :333
    fclose(dict);
    return true;

}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (word_count > 0)
    {
        return word_count;
    }

    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        // Create cursor (arrow :33)
        node *arrow = table[i];
        // Move through linked list
        while (arrow != NULL)
        {
            // create temp var
            node *temp = arrow;
            // move arrow to next
            arrow = arrow->next;
            // free temp
            free(temp);
        }

        free(arrow);
    }

    return true;
}
