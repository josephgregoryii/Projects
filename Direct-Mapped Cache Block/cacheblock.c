//
//  cacheblock.c
//  
//
//  Created by Joseph Gregory - Groechelli on 3/13/18.
//  Copyright © 2018 Joseph Gregory - Groechelli. All rights reserved.
//
/*
                                                            Cache Block
                                                    _____________________________
 2) direct-mapped cache                             | Byte | Byte | Byte | Byte |
    s = 16 = 2^4                                    |   0  |   1  |   2  |   3  |
 m = # of bits in memory address = 32bits       000 -----------------------------
                                                011
    t = 26 |    s=4   |   b= 31-26-4=2  |       102
 ________________________________________       113
 |m-1 = 31 |set index | byte offset into|           unsigned int input = x3210a233; = 0011 0001 0000 0110 0010 0011 0011
 |tag bits |bits      | our cache block |           unsigned int tag = input >> 6;//leave input the same, dont alter input
 ________________________________________           unsigned into setId = ______;
                                                    unsigned int byteoffset = ______;
 00110 0001 0000 0110 0010 0011 0011
                             \   /\
                              \ /  \
                              1100  \
                                |    unsigned int byteoffset = 3
                    unsigned into setId = 12
 
 struct {                           _________________________________
 int c;  \                          |                               |
 int m;   \ 16 bytes                |   16 bites    |   16 bites    |   32 bites
 int y;   /                         |                               |
 int k;  /                          ---------------------------------
                                    | square[0][1]  |  square[0][0]
 for (i = 0; i < 16; i++){
    for ( j = 0; j< 16; j++){
 'miss'  square[i][j].c = 1;
 'hit'   square[i][j].m = 0;
 'hit'   ''        ''.y = 0;
 'hit'   ''        ''.k = 0;
    }
 }
 
 */

#include <stdio.h>
#include <stdlib.h>

typedef struct cache_block cache_block;
struct cache_block{
    unsigned char valid;
    unsigned int tag;
    unsigned char value[4];
};

unsigned int getOffset(unsigned int address)
{
    /* returns the byte offset of the address within its cache block */
    unsigned offset;
    offset = (address << 30);
    return offset >> 30;
}

unsigned int getSet(unsigned int address)
{
    /* returns the cache set for the address */
    unsigned int set;
    set = address << 26;    //eliminate tag bits
    return set >> 28;       //shift back the set plus an extra 2 bits to remove offset
}
                          
unsigned int getTag(unsigned int address)
{
    /* returns the cache tag for the address */
    unsigned int tag;
    tag = address >> 6; //shif 4bit block and 2bit offset
    return tag;
}

void read_cache( cache_block* array, unsigned int address){
    unsigned int tag;
    tag = getTag(address);
    
    unsigned int set;
    set = getSet(address);
    
    unsigned int offset;
    offset = getOffset(address);
    
    printf("Looking for set: %d ", set);
    printf("- tag: %d", tag);
    printf("\n");
    
    if(array[set].valid == 1){
        printf("found set: %d ",set);
        printf("- tag: %d ", tag);
        printf("- offset: %d ", offset);
        printf("- valid: %d ", array[set].valid);
        printf("- value: ");
        printf("%.2x \n",array[set].value[0]);
        if (array[set].tag != tag){
            printf("tags don't match - miss!\n");
        }
        else{
            printf("hit!\n");
        }
    }
    else{
        printf("no valid set found - miss!\n");
    }
}
void write_cache( cache_block* array, unsigned int address, unsigned value){
    unsigned int set;
    unsigned int tag;
    unsigned int a,b,c,d;
    
    tag = getTag(address);
    set = getSet(address);
    
    if (array[set].valid == 1){
        printf("evicting block ");
        printf("- set: %d ",set);
        printf("- tag: %d ",array[set].tag);
        printf("- valid: %d ", array[set].valid);
        printf("- value: ");
        int i;
        for(i=0; i< 1; i++){
            printf("%.2x ",array[set].value[i]);
            printf("%.2x ",array[set].value[i+1]);
            printf("%.2x ",array[set].value[i+2]);
            printf("%.2x \n",array[set].value[i+3]);
        }
        a = (value & 0xFF);       //first set of four bits
        b = ((value >> 8) & 0xFF);    // second set of four bits
        c = ((value >> 16) & 0xFF);   // third set of four bits
        d = ((value >> 24) & 0xFF);   // fourth set of four bits
        array[set].valid = 1;
        array[set].value[0] = a;
        array[set].value[1] = b;
        array[set].value[2] = c;
        array[set].value[3] = d;
        array[set].tag = tag;
        
        printf("wrote set: %d ",set);
        printf("- tag: %d ",array[set].tag);
        printf(" - valid: %d",array[set].valid);
        printf(" - value: ");
        for(i=0; i< 1; i++){
            printf("%.2x ",array[set].value[i]);
            printf("%.2x ",array[set].value[i+1]);
            printf("%.2x ",array[set].value[i+2]);
            printf("%.2x \n",array[set].value[i+3]);
        }
        
    }
    else{
        a = (value & 0xFF);
        b = ((value >>8) & 0xFF);
        c = ((value >> 16) & 0xFF);
        d = ((value >> 24) & 0xFF);
        array[set].valid = 1;
        array[set].value[0] = a;
        array[set].value[1] = b;
        array[set].value[2] = c;
        array[set].value[3] = d;
        array[set].tag = tag;
        
        printf("Wrote set : %u ",set);
        printf("- tag: %u ",array[set].tag);
        printf(" - valid: %d",array[set].valid);
        printf(" - value: ");
        int i;
        for(i=0; i< 1; i++){
            printf("%.2x ",array[set].value[i]);
            printf("%.2x ",array[set].value[i+1]);
            printf("%.2x ",array[set].value[i+2]);
            printf("%.2x \n",array[set].value[i+3]);
        }
    }
}

void print_cache( cache_block* array){
    for (int i = 0; i < 16; i++){
        if (array[i].valid == 1){
        //printf("%d\n",array[i].valid);
            
            printf("set: %d ", i);
            printf(" - tag: %d",array[i].tag);
            printf(" - valid: %d", array[i].valid);
            printf(" - value: ");
            for(int j=0; j< 1; j++){
                printf("%.2x ",array[i].value[j]);
                printf("%.2x ",array[i].value[j+1]);
                printf("%.2x ",array[i].value[j+2]);
                printf("%.2x \n",array[i].value[j+3]);
            }
            
        }
    }
}

int main()
{
    cache_block *array;
    array = (cache_block *)malloc(sizeof(cache_block)*16);
    int i, j;
    for(i = 0; i < 16; i++){    //this loop clears the cache at the start
        array[i].tag = 0;
        array[i].valid = 0;
        for(j = 0; j < 1; j++){
            array[i].value[j] = 0;
            array[i].value[j+1] = 0;
            array[i].value[j+2] = 0;
            array[i].value[j+3] = 0;
        }
    }
    char input;
    unsigned int address;
    unsigned int value;
    do {
        printf("Enter 'r' for read, 'w' for write, 'p' to print, 'q' to quit: ");
        scanf(" %c", &input);
        
        if (input == 'r')
        {
            printf("Enter 32-bit unsigned hex address: ");
            scanf("%x", &address);
            read_cache(array, address);
        }
        else if (input == 'w'){
            printf("Enter 32-bit unsigned hex address: ");
            scanf("%x", &address);
            
            printf("Enter 32-bit unsigned hex value: ");
            scanf("%x",&value);
            write_cache(array, address, value);
        }
        else if (input == 'p'){
            print_cache(array);
        }
    }while(input != 'q');
    
    printf("Thanks for a great year in 314 :) \n");
        
    return 0;
}
