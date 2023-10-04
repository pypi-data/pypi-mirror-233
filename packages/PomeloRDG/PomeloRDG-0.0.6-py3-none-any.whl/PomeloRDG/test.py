from Graph import *
from IO import IO
import cyaron 

io = IO("dijstkra_my", 1)
g = Graph.Graph(10000, 5000000, weight = [1, 1000])
io.input_write(g.to_str())

io = cyaron.IO("dijstkra_cyaron1.in")
g = cyaron.Graph.graph(10000, 100000, weight = [1, 1000])
io.input_writeln(1000, 100000)
io.input_write(g.to_str(shuffle = True))

