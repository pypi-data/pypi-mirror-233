from __init__ import *

class Graph():
    class Graph():
        def __init__(self, nsize = Const.INF, msize = Const.INF, nlimit = [0, Const.INT_MAX], value = {}, directed = False, selflp = False, rpedges = False, eweight = False, ewlimit = [Const.INT_MIN, Const.INT_MAX], ewtype = Int):
            self.nlimit = nlimit
            self.nsize = nsize if self.__cknsize__(nsize) else random.randint(self.nlimit[0], self.nlimit[1])
            self.msize = msize if self.__ckmsize__(msize) else random.randint(self.nsize, (self.nsize) * (self.nsize - 1) // 2)
            self.directed = directed
            self.selflp = selflp
            self.rpedges = rpedges
            self.eweight = eweight
            self.ewlimit = ewlimit
            self.ewtype = ewtype
            # self.value = self.__rand__() if not self.__ckvalue__(value) else value
            
        def __ckvalue__(self, x):
            """
            Check if the graph elements are legal.
            """
            
            cnt = 0
            if type(x) != dict:
                return False
            if len(x) != self.nsize:
                return False
            for node in x:
                cnt += len(x[node])
                for _ in x[node]:
                    if (self.eweight and type(_) != self.ewtype) or (len(_) < 0 or len(_) > self.nsize):
                        return False
            self.nsize, self.msize = len(x), cnt
            return True
            
        def __cknsize__(self, x):
            """
            Check if the node size is legal.
            """
            
            if x < self.nlimit[0] or x > self.nlimit[1]:
                return False
            return True
        
        def __ckmsize__(self, x):
            """
            Check if the edge size is legal.
            """
            
            if self.nsize <= 0 or x > (self.nsize) * (self.nsize - 1) // 2:
                return False
            return True
        
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
                w = self.ewtype(limit = self.ewlimit).value if self.eweight else None
                if (not self.selflp and u == v) or (not self.rpedges and (u, v) in used):
                    continue
                if self.directed:
                    used.add((u, v))
                    self.value[u].append((v, w))
                else:
                    used.add((u, v)); used.add((v, u))
                    self.value[u].append((v, w)); self.value[v].append((u, w))
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
                res += str(_[0]) + " " + str(_[1]) + " " + str((_[2])) + "\n"
            return res