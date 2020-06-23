from mathsyStuff import Transformation
from board import Board

"""
 -  a position on the board is modelled by a row vector, with the origin at the board's centre
 -  there are 16 transformations on a board which preserve the boards layout (rotations, reflections, etc),
    since there are 8 different ways an arrow (--->) along the board's top edge can end up,
    and each can be composed with a swap of the players' symbols
 -  these form a group
 -  rotations by 0, 90, 180 and 270, a reflection by 45, the identity, and a piece swap,
    belong to this group, so their compositions (which are 16 elements) 
    make up the group
"""
def standardTransformation(board, playerID):
    swap = playerID != 1
    minTrans = Transformation.identity()

    for angle in [0, 90, 180, 270]:
        for reflectBy45 in [True, False]:
            trans = Transformation.fromProperties(angle, reflectBy45, swap)
            if trans.onBoard(board).encoding() < minTrans.onBoard(board).encoding():
                minTrans = trans
    return minTrans