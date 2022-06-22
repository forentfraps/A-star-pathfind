class Astar:
    def __init__(self, w, h, destn, start):
        
        self.field  = [[0 for _ in range(h)] for _ in range(w)] 
        self.destn = destn
        self.start = start
        self.costgrid = [[[0,0,0] for _ in range(h)] for _ in range(w)] 
        self.w = w
        self.h = h


    def pf(self):
        """
        Prints field in a fancy way\n
        has colours (use in PowerShell)
        """
        for l in self.field:
            s = ""
            for number in l:
                match number:
                    case 0:
                        s += str(number) + "  "
                    case 1:
                        s += ("\033[96m")+str(number)+str("\033[0m") + "  "
                    case 2:
                        s += str(number) + "  "
                    case 3:
                        s += str(number) + "  "
                    case 4:
                        s += ("\033[1;35;40m")+str(number)+str("\033[0m") + "  "


            print(s)
        print("\n")
        return None
    def mwall(self,  x: list, y: list):
        """
        Takes 2 lists of coordinates for a wall: ex. x = [2], y = [1,2,3,4,5] will make a wall on x == 2 from y == 1 to y == 5 accordingly
        Third input is a field on which the wall will be made
        """
        for y1 in range(len(self.field)):
            for x1 in range(len(self.field[0])):
                if x1 in x and y1 in y:
                    self.field[y1][x1] = 1
        return None

    


    """
    General terms in the algo: 

    Gcost = distance from starting node
    Hcost = distance from end node
    Fcost = Hcost + Gcost
    status (aka field values) = blank/wall/open/close/path (0/1/2/3/4 respectively) depending on the status of the cell
    """

    def cost(self, s0: tuple, s1: tuple) -> int: #could improve min/max with array interactions
        """
        Idea behind the calculations is as follows:\n
        A rectangle could be imagined with s0 and s1 as coordinates of its opposite corners\n
        Therefore we travel diagonally until x or y coordinate is matched, after that the shortest path is vertical / horizontal \n
        14 stands for diagonal distance\n
        10 for vertical/ horizontal
        """
        x0, y0 = s0
        x1, y1 = s1
        r, d = abs(x0 - x1), abs(y0 - y1)
        x = max(r, d)
        n = min(r, d)
        t = n * 14 + (x - n) * 10
        return t
    def hcost(self, s0: tuple) -> int:
        """
        Calculates hcost
        """
        return self.cost(s0, destn)

    def get_adj(self,s0) -> list:
        """
        Gets legal adjesent points around s0
        """
        x, y = s0

        cords = []
        for i in range(9):
            cords.append((i % 3 + x - 1, i//3 + y - 1))
        cords.pop(4)
        real = []
        for cord in cords:
            x1, y1 = cord
            if x1 < 0 or y1 < 0 or x1 > self.w -1 or y1 > self.h -1 :
                continue

            real.append(cord)
        return real

    def collapse(self, pos):
        """
        Closes a given point, updates all the nearby ones
        """
        x,y = pos
        cords_adj = self.get_adj(pos)
        g0 = self.costgrid[y][x][0]
        self.field[y][x] = 3
        for point in cords_adj:
            x1, y1 = point
            diag = 0
            if abs(x1 - x) + abs(y1 - y) == 2:
                diag = 1

            match self.field[y1][x1]:
                case 1:
                    continue
                case 3:
                    continue
                case 0:
                    self.costgrid[y1][x1] = [g0 + 10 +4* diag,self.hcost(point), g0 +10 + 4* diag+self.hcost(point)]
                    self.field[y1][x1] = 2
                case 2:
                    self.costgrid[y1][x1][0] = min(g0 +10 + 4* diag, self.costgrid[y1][x1][0])
                    self.costgrid[y1][x1][2] = sum(self.costgrid[y1][x1][:2])
        return None
        

    def solve(self):
        """
        Collapses a point with the lowest Fcost, while prioritizing lower Hcost
        """
        #collapse start manually cause bad algo ;-)
        x0,y0 = self.start
        self.field[y0][x0] = 2
        self.costgrid[y0][x0] = [0, self.cost(self.start,self.destn), self.cost(self.start,self.destn)]
        self.collapse(self.start)
        while True:

            opens = []
            glm = float("inf")
            for y1 in range(self.h):
                for x1 in range(self.w):
                    if self.field[y1][x1] == 2:
                        if self.costgrid[y1][x1][1] == 0:
                            self.collapse((x1,y1))
                            return
                        opens.append((x1,y1))
                        glm = min(self.costgrid[y1][x1][2], glm)

            glmh = float("inf")
            for point in opens:
                x1, y1 = point
                if self.costgrid[y1][x1][2] == glm and self.costgrid[y1][x1][1] < glmh:
                    rp = point
                    glmh = self.costgrid[y1][x1][1]
            self.collapse(rp)
    def display_path(self):
        """
        Basically outlines the path after start and finish are connected via closed points
        """
        x1, y1 = self.destn
        self.field[y1][x1] = 4
        while True:
            cords_adj = self.get_adj((x1,y1))
            glm = float("inf")
            glmg = float("inf")
            for point in cords_adj:
                x2, y2 = point
                if point == self.start:
                    self.field[y2][x2] = 4
                    return
                if self.field[y2][x2] == 3 and self.costgrid[y2][x2][2] < glm and self.costgrid[y2][x2][0] < glmg :
                    glm = self.costgrid[y2][x2][2]
                    glmg = self.costgrid[y2][x2][0]
                    rp = point
            
            x1, y1 = rp
            self.field[y1][x1] = 4

            
                            
if __name__ == "__main__":
    ## Just some basic example
    destn = (5,5)
    start = (0,0)
    w, h = 6, 6
    field = Astar(w,h,destn, start)
    field.mwall([2],[1,2,3,4])
    field.mwall([3],[1])
    
    
    field.pf()
    field.solve()
    field.display_path()
    field.pf()