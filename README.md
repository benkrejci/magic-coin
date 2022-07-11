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

1. You are not allowed to see the initial state of the coins (you cannot see the coins until after your friend has left the room).
1. You and your friend may communicate, but only before your friend enters the room. Once your friend has entered the rom, you effectively never communicate with them again.
1. The only possible action your friend can take is to flip a coin completely (no rotating, moving, marking or the like).
1. No mechanics exist which are not stated in the problem (e.g. you can't stand a coin up on its edge, yell to your friend through the walls, etc.) 

# XOR Solution

See [solution-xor.js](./solution-xor.js) for implementation.

1. Assign an integer index to each coin sequentially (0, 1, 2, ...63).
1. Friend:
   1. Use the bitwise XOR operation with all indices of heads-up coins.
   1. If result is index of magic coin, friend is done.
   1. XOR result with index of magic coin.
   1. Flip the coin with this index.
1. You:
   1. XOR all heads-up indices.
   1. Result is index of magic coin.
