# Problem

The "Magic Coin" problem:

1. There is a room with a 64x64 grid of coins
1. All coins have a heads and tails side and start in random orientation (~50% heads-up, ~50% tails-up)
1. One coin is the "magic coin" but is indistinguishable from the other coins
1. You have a friend with you who enters the room first and is shown which coin is the magic coin
1. Your friend has the option to flip ONE of the 64<sup>2</sup> coins (or they may flip no coins)
1. Your friend leaves the room (out a back door) and you enter the room
1. You must determine the location of the magic coin

Stipulations:

- You are not allowed to see the initial state of the coins (you cannot see the coins until after your friend has left the room).
- You and your friend may communicate, but only before your friend enters the room. Once your friend has entered the rom, you effectively never communicate with them again.
- The only possible action your friend can take is to flip a coin completely (no rotating, moving, marking or the like).
- No mechanics exist which are not stated in the problem (e.g. you can't stand a coin up on its edge, yell to your friend through the walls, etc.) 

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

TBD
