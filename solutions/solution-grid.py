""" Python grid-based solution to 
the Magic Golden Coin problem """
import numpy as np

from IPython import embed

def rowcols_grid(grid:np.ndarray, axis:int):
    """ Collapse the values along columns (axis=0) or rows (axis=1)

    An odd number of 1's yields a 1  [yes, opposite what you might think..]

    Args:
        grid (np.ndarray): _description_
        axis (int): _description_

    Returns:
        np.ndarray: 1D array of 0's and 1's for the collapsed rows/columns
    """
    trufalse = ((np.sum(grid, axis=axis)) % 2) == 1
    return trufalse.astype(int)

def ncolrow_to_colrowpos(ncolrow:tuple, ngrid=2):
    """ Convert decimal based row, col into binary format

    The array is padded with 0's to have the full shape
    based on ngrid

    Args:
        ncolrow (tuple): col, row
        ngrid (int, optional): Size of the grid. Defaults to 2.

    Returns:
        tuple: col, row arrays of binary digits
            Confusingly, the first element of the array is the highest
            digit of the binary number.  e.g.  array([0,1,0,0,0,1]) = 17
    """
    npos = int(np.log2(ngrid))

    # Convert to binary and pad to full size
    bincol = bin(ncolrow[0])[2:]
    bincol = '0'*(npos-len(bincol)) + bincol
    binrow = bin(ncolrow[1])[2:]
    binrow = '0'*(npos-len(binrow)) + binrow

    colpos = np.array([int(item) for item in bincol])
    rowpos = np.array([int(item) for item in binrow])

    # These read left to right
    return colpos, rowpos

def colrowpos_to_ncolrow(colpos:np.ndarray, rowpos:np.ndarray):
    """ Convert a binary array into a decimal number

    Args:
        colpos (np.ndarray): binary array specifying the column value, e.g. array([0,1,0,0,0,1])
        rowpos (np.ndarray): binary array specifying the row value, e.g. array([1,1,0,0,0,1])

    Returns:
        tuple: column, row in decimal (int)
    """
    twos = [2**kk for kk in range(len(colpos))]
    twos.reverse()
    nrow = np.sum([two*item for two,item in zip(twos,rowpos.tolist())])
    ncol = np.sum([two*item for two,item in zip(twos,colpos.tolist())])
    # Return
    return ncol, nrow

def flip(cell:int):
    """ Flip the cell value (i.e. the coin)

    Args:
        cell (int): cell value

    Returns:
        int: New cell value
    """
    if cell == 1:
        return 0
    else:
        return 1

def encode(grid:np.ndarray, magic_pos:tuple, ngrid:int=2, debug:bool=False):
    """ Performs the action of the 'friend' who has recevied the board
    and the location of the magic coin and has then flipped one of the coins.

    Args:
        grid (np.ndarray): Grid specifying the state of the coins (0 and 1)
        magic_pos (tuple): col, row of the magic coin position in decimal notation 
        ngrid (int, optional): size of the grid. Defaults to 2.
        debug (bool, optional):

    Returns:
        np.ndarray: New grid which specifies the magic coin position after flipping one coin
    """
    # Convert magic coin position to binary format
    magic_colpos, magic_rowpos = ncolrow_to_colrowpos(
        magic_pos,  ngrid=ngrid)
    # Save a copy of the starting grid
    ogrid = grid.copy()

    # Check if we are correct already
    ogrid_col, ogrid_row = decode(ogrid, ngrid=ngrid)
    if np.all(magic_colpos == ogrid_col) & np.all(magic_rowpos == ogrid_row):
        return grid

    # Brute force me to find the row for the coin to flip
    flip_row = None
    for row in range(ngrid):
        grid = ogrid.copy()
        grid[row,0] = flip(ogrid[row,0])
        grid_col, grid_row = decode(grid, ngrid=ngrid)
        if debug:
            print('row:', grid_row)
        if np.all(magic_rowpos == grid_row):
            flip_row = row
            break

    # Brute force me to find the col for the coin to flip
    flip_col = None
    for col in range(ngrid):
        grid = ogrid.copy()
        grid[0, col] = flip(ogrid[0, col])
        grid_col, grid_row = decode(grid, ngrid=ngrid)
        if debug:
            print('col:', grid_col)
        if np.all(magic_colpos == grid_col):
            flip_col = col
            break

    # Do it
    grid = ogrid.copy()
    try:
        grid[flip_row,flip_col] = flip(ogrid[flip_row,flip_col])
    except ValueError:
        embed(header='There is a bug as we could not find a coin to flip; 70 of coin')

    if debug:
        embed(header='debug: 136 of coin')

    # Return
    return grid

def decode(grid:np.ndarray, ngrid=2):
    """ Procedure to read the position of the magic coin

    Args:
        grid (np.ndarray): The grid modified by your friend
        ngrid (int, optional): size of the grid. Defaults to 2.

    Returns:
        tuple: magic coin position in binary format (col, row)
    """
    npos = int(np.log2(ngrid))

    # Prepare for the multi-bit transforms
    transforms = np.arange(ngrid+1).tolist()
    transforms.reverse()

    # Drop the one-bit transformations
    drop_list = [0] + [2**item for item in range(npos+1)]
    for drop in drop_list:
        transforms.remove(drop)

    # Grab the values of the rows and columns based on coin parity
    all_col_pos = rowcols_grid(grid, 0)
    all_row_pos = rowcols_grid(grid, 1)

    # The col and row and saved in the last/first digits
    col_pos = all_col_pos[-npos:]
    row_pos = all_row_pos[0:npos]

    # Transform -- multi-bit modifications to the position
    for tt in range(ngrid-npos-1):
        bint = bin(transforms[tt])[2:]
        bint = '0'*(npos-len(bint)) + bint

        #
        col_trans = all_col_pos[-npos-1-tt]
        if col_trans == 1:
            for kk, tval in enumerate(bint):
                if tval == '1':
                    col_pos[kk] = flip(col_pos[kk])
        # Rows
        row_trans = all_row_pos[npos+tt]
        if row_trans == 1:
            for kk, tval in enumerate(bint):
                if tval == '1':
                    row_pos[kk] = flip(row_pos[kk])
    # Return
    return col_pos, row_pos


if __name__ == '__main__':
    # 4x4
    '''
    ngrid = 4
    rand_grid = np.random.randint(0, high=2, size=(ngrid, ngrid))
    col, row = decode(rand_grid, ngrid=ngrid)
    '''

    # Random trials
    nrand = 50
    ngrid = 64
    for ss in range(nrand):
        # Grid
        rand_grid = np.random.randint(0, high=2, size=(ngrid, ngrid))
        # Coin
        rand_coin = np.random.randint(0, high=ngrid, size=2).tolist()
        
        # Encode
        new_grid = encode(rand_grid, rand_coin, ngrid=ngrid,
                          debug=False)

        # Decode
        col, row = decode(new_grid, ngrid=ngrid)
        ncol, nrow = colrowpos_to_ncolrow(col, row)

        #
        try:
            assert [ncol, nrow] == rand_coin
        except:
            embed(header='124 of coin')
        print(f"passed: ss={ss}")

    '''
    grid = np.array( [[1,0], [0,1]] ) # col=0, row=0
    magic_pos = [0,0]
    new_grid = encode(grid, magic_pos)

    col, row = decode(new_grid)
    ncol, nrow = rowcolpos_to_nrowcol(col, row)

    print(f'Magic coin at col={ncol}, row={nrow}; Ans={magic_pos}')
    embed(header='75 of coin')

    # Test magic pos
    magic_rowcolpos = nrowcol_to_rowcolpos([2,3], ngrid=4)


    # Test translator
    grid = np.array( [[0,1], [0,1]] ) # col=0, row=1

    grid = np.array( [[1,1], [0,1]] ) # col=0, row=0

    #grid = np.array( [[0,0], [1,1]] )

    #grid = np.array( [[0,1], [1,1]] )  # col=0, row=1
    #grid = np.array( [[0,1], [0,1]] )


    col, row = decode(grid)
    print(f'col={col}, row={row}')

    embed(header='25 of coin')
    '''