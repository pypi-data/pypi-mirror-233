from PomeloRDG.__init__ import *

class Graph():
    class Graph():
        def __init__(self, nsize, msize, **kwargs):
            self.nsize = nsize
            self.msize = msize if msize > 0 and msize <= (self.nsize) * (self.nsize - 1) // 2 else random.randint(self.nsize, (self.nsize) * (self.nsize - 1) // 2)
            self.directed = kwargs.get("directed", False)
            self.selflp = kwargs.get("selflp", False)
            self.rpedges = kwargs.get("rpedges", False)
            self.wtype = kwargs.get("wtype", Int)
            self.weight = kwargs.get("weight", [Const.INT_MIN, Const.INT_MAX])
            self.value = self.__rand__()
        
        def __rand__(self):
            """
            Generate a legal graph.
            """
            
            n, m, cnt = self.nsize, self.msize, 0
            self.value, used = {}, set()
            for i in range(1, n + 1):
                self.value[i] = []
            while cnt < m:
                u, v = random.randint(1, n), random.randint(1, n)
                w = self.wtype(limit = self.weight).value if self.weight else None
                if (not self.selflp and u == v) or (not self.rpedges and (u, v) in used):
                    continue
                if self.directed:
                    used.add((u, v))
                    self.value[u].append((v, w))
                else:
                    used.add((u, v)); used.add((v, u))
                    self.value[u].append((v, w))
                cnt += 1
            return self.value
            
        def __str__(self):
            return self.to_str()
                        
        def get(self):
            """
            Return the value.
            """
            
            edges = []
            for u in self.value:
                for v in self.value[u]:
                    edges.append((u, v[0], v[1]))
            return (self.nsize, self.msize, edges)
        
        def to_str(self, shuffle = True):
            value = self.get(); n, m, g, res = value[0], value[1], value[2], ""
            res += "{} {}\n".format(str(n), str(m))
            if shuffle:
                random.shuffle(g)
            for _ in g:
                res += str(_[0]) + " " + str(_[1]) + " " + (str((_[2])) if _[2] != None else "") + "\n"
            return res