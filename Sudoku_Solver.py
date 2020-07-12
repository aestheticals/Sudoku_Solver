#sudoku solver

def printGrid( solution ):
    grid = [[0 for a in range( 9 )] for b in range( 9 )]
    for cell in solution:
        grid[cell.data[0]-1] [cell.data[1]-1]  = cell.data[3]
    for x in range( 9 ):
        if( x%3==0 ):
            print( " - - - - - - - - - - - -" )
        for y in range( 0,9,3 ):
            print( " ", end='' )
            print( str( grid[x][y] )   + " ", end='' )
            print( str( grid[x][y+1] ) + " ", end='' )
            print( str( grid[x][y+2] ) + " ", end='' )
            print( "|", end='' )
        print()
    print( " - - - - - - - - - - - -" )

    solved = True
    for x in range( 9 ):
        row_sum=0
        for y in range( 9 ):
            row_sum += grid[x][y]
        if( row_sum!=45 ): solved = False
    for x in range( 9 ):
        col_sum=0
        for y in range( 9 ):
            col_sum += grid[y][x]
        if( col_sum!=45 ): solved = False
    for a in range( 3 ):
        for b in range( 3 ):
            box_sum = 0
            for x in range( 3 ):
                for y in range( 3 ):
                    box_sum += grid[a*3+x][b*3+y]
            #print( box_sum )
            if( box_sum!=45 ): solved = False
    print( "solved: " + str( solved ) )

def getBox( x, y ): #1 to 9
    return ( ( x - 1 ) // 3 ) * 3 + ( y - 1 ) // 3 + 1

class Node:
    def __init__( self, data, header=False ):
        #data = [Row, column, Box, number]
        self.data = data
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        if( header ):
            self.header = self
            self.children = 0
        else:
            self.header = None
    def getLeft( self ):
        return self.left
    def getRight( self ):
        return self.right
    def getUp( self ):
        return self.up
    def getDown( self ):
        return self.down
    def getHeader( self ):
        return self.header

    def setHeader( self, header ):
        self.header = header
    def setLeft( self, left ):
        self.left = left
    def setRight( self, right ):
        self.right = right
    def setUp( self, up ):
        self.up = up
    def setDown( self, down ):
        self.down = down
    def addChild( self ):
        self.children += 1

start = Node( 0, True )
prev = start
#1 of 4 sets of constraints( Row column )
for x in range( 81 ):
    #           row, column, box, number
    curr = Node( [ x // 9 + 1 , x % 9 + 1 , 0 , 0 ], True )
    prev.setRight( curr )
    curr.setLeft( prev )
    prev = curr
#Row Number
for x in range( 81 ):
    curr = Node( [ x // 9 + 1 , 0 , 0 , x % 9 + 1 ], True )
    prev.setRight( curr )
    curr.setLeft( prev )
    prev = curr
#column Number
for x in range( 81 ):
    curr = Node( [ 0 , x // 9 + 1 , 0 , x % 9 + 1 ], True )
    prev.setRight( curr )
    curr.setLeft( prev )
    prev = curr
#Box Number
for x in range( 81 ):
    curr = Node( [ 0 , 0 , x // 9 + 1 , x % 9 + 1 ], True )
    prev.setRight( curr )
    curr.setLeft( prev )
    prev = curr
start.setLeft( prev )
prev.setRight( start )

rows = []
for row in range( 1,10 ):
    for col in range( 1,10 ):
        for num in range( 1,10 ):
            row_list = []
            #each constraint has 9 cells that belong to it( each constraint has two parts )
            curr_header = start.getRight()
            while( curr_header != start ):
                #counts number of matches between constraint and current row
                counter = 0
                if( curr_header.data[0] == row ):
                    counter+=1
                if( curr_header.data[1] == col ):
                    counter+=1
                if( curr_header.data[2] == getBox( row, col ) ):
                    counter+=1
                if( curr_header.data[3] == num ):
                    counter+=1
                #counter will == 2 four times per row
                if( counter == 2 ):
                    curr_row = curr_header
                    #add the new node to the bottom of the column
                    for _ in range( curr_header.children ):
                        curr_row = curr_row.getDown()
                    curr_header.addChild()
                    new_node = Node( [ row , col , getBox( row, col ) , num ] )
                    #every node points to its header
                    new_node.setHeader( curr_header )
                    new_node.setUp( curr_row )
                    curr_row.setDown( new_node )
                    #if children == 9 it is the last node in the column so we link bottom node and header
                    if( curr_header.children == 9 ):
                        new_node.setDown( curr_header )
                        curr_header.setUp( new_node )
                    row_list.append( new_node )
                curr_header = curr_header.getRight()
            #circularly link the rows
            for b in range( len( row_list )-1 ):
                row_list[b].setRight( row_list[b+1] )
                row_list[b+1].setLeft( row_list[b] )
            row_list[0].setLeft( row_list[len( row_list )-1] )
            row_list[len( row_list )-1].setRight( row_list[0] )
            rows.append( row_list )

solution = []
def Solve( depth=0 ):
    if( start.getRight()==start ):
        printGrid( solution )
        #print( "depth: " + str( depth ) )
        exit()
        return
    else:
        col = start.getRight()
        Cover( col )
        row = col.getDown()
        while( row != col ):
            solution.append( row )
            right_node = row.getRight()
            while( right_node != row ):
                Cover( right_node )
                right_node = right_node.getRight()
            Solve( depth+1 )
            solution.remove( row )
            col = row.getHeader()
            left_node = row.getLeft()
            while( left_node != row ):
                Uncover( left_node )
                left_node = left_node.getLeft()
            row = row.getDown()
        Uncover( col )

#take in node, use node.getHeader() to get column
def Cover( node ):
    col = node.getHeader()
    col.getRight().setLeft( col.getLeft() )
    col.getLeft().setRight( col.getRight() )
    col_node = col.getDown()
    while( col_node != col ):
        row_node = col_node.getRight()
        while( row_node != col_node ):
            row_node.getUp().setDown( row_node.getDown() )
            row_node.getDown().setUp( row_node.getUp() )
            row_node = row_node.getRight()
        col_node = col_node.getDown()

def Uncover( node ):
    col = node.getHeader()
    col.getRight().setLeft( col )
    col.getLeft().setRight( col )
    col_node = col.getUp()
    while( col_node != col ):
        row_node = col_node.getLeft()
        while( row_node != col_node ):
            row_node.getUp().setDown( row_node )
            row_node.getDown().setUp( row_node )
            row_node = row_node.getLeft()
        col_node = col_node.getUp()

def createPuzzle( string ):
    for x in range( 81 ):
        if( string[x]=="." or int( string[x] )<1 or int( string[x] )>9 ):
            continue
        else:
            for row in rows:
                data = row[0].data
                if( data[0]==x//9+1 and data[1]==x%9+1 and data[2]==getBox( x//9+1, x%9+1 ) and data[3]==int( string[x] ) ):
                    Cover( row[0] )
                    Cover( row[0].getRight() )
                    Cover( row[0].getRight().getRight() )
                    Cover( row[0].getLeft() )
                    solution.append( row[0] )

#pass in string of length 81. 0 or . = empty
createPuzzle( "080070030260050018000000400000602000390010086000709000004000800810040052050090070" )

Solve()
