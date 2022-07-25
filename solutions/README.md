# XOR Solution

## Implementation

See [solution-xor.js](./solution-xor.js) for implementation.

1. Assign an integer index to each coin sequentially (0, 1, 2, ...63).
1. Friend:
   1. Use the bitwise XOR operation with all indices of heads-up coins.
   1. XOR result with index of magic coin.
   1. Flip the coin with this index.
1. You:
   1. XOR all heads-up indices.
   1. Result is index of magic coin.

## Test

To test XOR solution, first clone repo and run `npm i` to install dependencies.
### Test solution for a randomly generated grid

```sh
node -e "require('./solution-xor').tryRandomGrid(16)"
```

Output:

<img width="449" alt="image" src="https://user-images.githubusercontent.com/6108440/178316458-04624f7f-9f6e-4244-92bf-0387734231a4.png">


### Test solution for 1 million randomly-generated grids

```sh
node -e "require('./solution-xor').tryRandomGrids(1_000_000, 16)"
```

Output:

<img width="540" alt="image" src="https://user-images.githubusercontent.com/6108440/178313985-647f6c38-2d5a-472f-abbe-f041815a372c.png">

## Notes & Limitations

- This solution only works for grids with power of 2 sizes (2x2, 4x4, 8x8, etc.) as for other grid sizes, the friend may be called upon to flip a coin which does not exist.
- Technically, the friend does not need to flip any coin if the initial heads-up XOR result is the index of the magic coin, but this flip will always be a no-op since the algorithm will instruct the friend to flip the 0-index coin.

# Coordinate Transformations Solution

## Implementation

See [solution-grid.py](./solution-grid.py) for implementation.

1. For a 2^n number specified in binary format, 
 there are 2^n ways to ways to flip the n elements
 that specify the number (including no change).
   1. For example, to change 001010 = 10 into 
   010010 = 18 we must flip the 16's and 8's elements.
   1. This is a 2-flip transformation.
   1. For n=6 (64), there are 0-flip, 1-flip, 2-flip..6-flip transformations.
1. We use the parity of heads/tails in each row and each column to generate two 64-element "transformation" arrays.
1. The location is then specfied by appying all 2^n
transformations to 000000.
1. The solution to the magic coin is then to identify the single transformation that turns the initial random
grid position into the magic coin position.
   1. This is deterministic because there is only 1 
   transformation to take any binary number into another
   1. And we have the 2-degrees of freedom to specify
   the col, row by choosing the coin in the
   specific col, row.


## Alogrithm

1. Start with a random 64x64 grid of coins 
1. Use the parity of each row and column (separately) to generate two 64 element "collapsed" arrays (even number of 1's = 0)
    1. Define how each of these map to a given transformation of the binary number
1. Your friend reads the position of the random grid
    1.  And then loops through the transformations to find the correct coin to flip
    1.  Separately for row and column
1. You receive the modified grid and use the transformations to read off the magic coin row, column.

## Test

At the bottom of the code you can
specify the size of the grid and 
the number of random trials with
the `nrand` and `ngrid` parameters.

Then do 

```sh
python solution-grid.py
```

This will: 

1. Generate a random grid
1. Generate a random coin posiiton
1. Have your friend flip one coin based on these.
1. Read the new grid and check the position against the known one

## Notes & Limitations

As with the XOR algorithm, this method can only 
be applied to grids with 2^n x 2^n size.
