import sys
from PIL import Image

class Node():
    def __init__(self, state, parent, action):
        self.state=state
        self.parent=parent
        self.action=action

class Stackfrontier():
    def __init__(self):
        self.frontier=[]
    
    def add(self,node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(state==node.state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier)==0
    
    def remove(self):
        if self.empty():
            raise Exception("Empty stackfrontier")
        else:
            node=self.frontier[-1]
            self.frontier=self.frontier[:-1]
            return node
    

class Queuefrontier(Stackfrontier):

    def remove(self):
        if self.empty():
            raise Exception("Empty queuefrontier")
        else:
            node=self.frontier[0]
            self.frontier=self.frontier[1:]
            return node
        



class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents=f.read()
        contents=contents.splitlines()
            
        self.height=len(contents)
        self.width=max(len(a) for a in contents)
 
        self.walls=[]
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                try:    
                    if(contents[i][j]=='A'):
                        self.start=(i,j)
                        row.append(False)
                    elif contents[i][j]=='B':
                        self.goal=(i,j)
                        row.append(False)
                    elif contents[i][j]==' ':
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution=None 
    
    def print(self):
        solutions=self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█",end="")
                elif (i,j)==self.start:
                    print("A",end="")
                elif (i,j)==self.goal:
                    print("B",end="")
                elif solutions is not None and (i,j) in solutions:
                    print("*",end="")    
                else:
                    print(" ",end="")
            print()
        print()

    def neigbours(self, state):
        row, col=state
        candidates=[
            ("up",(row-1,col)),
            ("down",(row+1,col)),
            ("left",(row,col-1)),
            ("right",(row,col+1))
               
        ]

        result=[]
        for action,(r,c) in candidates:
            if 0<=r<self.height and 0<=c<self.width and not self.walls[r][c]: 
                result.append((action,(r,c)))
        return result
    
    def solve(self):

        self.num_explored=0
        node=Node(self.start,None,None)

        frontier=Queuefrontier()
        frontier.add(node)

        self.explored=set()

        while(True):

            if frontier.empty():
                raise Exception("No solution")
            
            node=frontier.remove()

            if node.state==self.goal:
                actions=[]
                cells=[]
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node=node.parent
                actions.reverse()
                cells.reverse()
                self.solution=(actions,cells)
                return

            

            self.explored.add(node.state)
            self.num_explored+=1

            neighbour=self.neigbours(node.state)
            for action, state in neighbour:
                if not frontier.contains_state(state) and state not in self.explored:
                    child=Node(state,node,action)
                    frontier.add(child)

    def output_image(self, filenaem, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size=50
        cell_border=2

        image=Image.new("RGBA", (cell_size*self.width,cell_size*self.height),"black")
        draw=ImageDraw.Draw(image)

        solutions=self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                if col:
                    f=(50, 50, 50)
                elif (i,j)==self.start:
                    f=(255, 0, 0)
                elif (i,j)==self.goal:
                    f=(0, 171, 28)
                elif solutions is not None and show_solution and (i,j) in solutions:
                    f=(220, 235,  113)
                elif solutions is not None and show_explored and (i,j) in self.explored:
                    f=(212, 97, 85)
                else:
                    f=(237, 240, 252)

                draw.rectangle(
                    ([(j*cell_size+cell_border, i*cell_size+cell_border),
                      ((j+1)*cell_size-cell_border,(i+1)*cell_size-cell_border)]),
                              fill=f)
                
        image.show()

                

            
    
filename=sys.argv[-1]
m=Maze(filename)
m.print()
m.solve()
m.print()
print(m.num_explored)
m.output_image("maze.png", show_explored=True)

                    


