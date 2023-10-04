from PomeloRDG.__init__ import *

class IO():
    def __init__(self, filename, id = 1, insuffix = ".in", outsuffix = ".out"):
        self.filename = filename
        self.infile = str(filename) + str(id) + str(insuffix)
        self.outfile = str(filename) + str(id) + str(outsuffix)
        self.id = id
        self.insuffix = insuffix
        self.outsuffix = outsuffix
        
    def __list_like__(self, data):
        return isinstance(data, tuple) or isinstance(data, list)

    def __getdata__(self, *args, data = []):
        for _ in args:
            if self.__list_like__(_):
                for __ in _:
                    self.__getdata__(__, data = data)
            else:
                data.append(_)
        return data
        
    def input_write(self, *args, sep = " ", end = "\n"):
        file, data = open(self.infile, "w"), self.__getdata__(*args, data = [])
        for _ in data:
            file.write(str(_) + sep)
        file.write(end)
        
    def output_write(self, *args, sep = " ", end = "\n"):
        file, data = open(self.outfile, "w"), self.__getdata__(*args, data = [])
        for _ in data:
            file.write(str(_) + sep)
        file.write(end)
        
    def output_gen(self, cppfile):
        """
        C++ code template:

        const int MAXN = 1e6;

        int main(int argc, char* argv[]){
            char infile[MAXN], outfile[MAXN];
            strcpy(infile, argv[1]), strcpy(outfile, argv[2]);
            freopen(infile, "r", stdin), freopen(outfile, "w", stdout);
            // Your Code
            return 0;
        }
        """
        file = open(self.outfile, "w")
        os.system("g++ -Ofast -std=c++14 {}".format(cppfile))
        os.system("./a.out {}{}.in {}{}.out".format(self.filename, str(self.id), self.filename, str(self.id)))
        os.remove("./a.out")