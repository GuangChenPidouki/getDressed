import logging

class DressType:
    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.mandatory = False
        self.depend_on = []

class Rules:
    @staticmethod
    def dependOn(source, target):
        source.depend_on.append(target)

    @staticmethod
    def required(dress):
        dress.mandatory = True

    @staticmethod
    def not_required(dress):
        dress.mandatory = False


class DressHandler:
    def __init__(self):
        logging.basicConfig(filename='app.log',
                            filemode='a',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')
        self.logger = logging.getLogger('getDressed')
        self.logger.setLevel(logging.DEBUG)
        
        #set of dresses that is required
        self.mand = set()

        #set of all dresses added til now
        self.total = set()

        #all dress info mapping
        self.dress = {}

    def addDressType(self, cur):
        self.dress[cur.index] = cur
        if cur.mandatory:
            self.mand.add(cur.index)

    def runCommand(self, input_s):
        #reset for each test
        self.total.clear()
        self.tmp = self.mand.copy()

        #prepare input and output
        dress_arr = input_s.split()
        output = ""

        self.logger.debug('*****************************************')
        self.logger.debug('start to check if "{}" is able to be dressed'.format(input_s))
        for s in dress_arr:
            #if input is not a dress number, return fail
            try:
                i = int(s)
            except:
                output += "fail"
                self.logger.warning('This input "{}" is not a valid number in "{}"'.format(s, input_s))
                return output

            #if cur dress is not in prepared closet, return fail
            if i not in self.dress:
                output += "fail"
                self.logger.warning('This input "{}" is not a dress number in "{}"'.format(s, input_s))
                return output
            
            #if need to leave directly, do not check more dress
            if i == 6:
                self.logger.debug('"{}" includes 6, so do not check more than that'.format(input_s))
                break

            #check dependency of each dress
            self.logger.debug('start to check if "{}" is able to be dressed'.format(self.dress[i].name))
            if self.isValid(self.dress[i]):
                output += self.dress[i].name + ", "
            else:
                output += "fail"
                return output

        #check if all required dress are put on already
        if len(self.tmp) > 0:
            for left in self.tmp:
                self.logger.warning('Cannot leave as "{}" is required'.format(self.dress[left].name))
            output += "fail"
        else:
            self.logger.debug('finish checking "{}", Confirmed "{}" is able to be dressed'.format(input_s, output[:-2]))
            output += "leave"
        return output
        
    def isValid(self, cur):
        self.total.add(cur.index)
        if cur.mandatory:
            assert(cur.index in self.tmp)
            self.tmp.remove(cur.index)
        for i in cur.depend_on:
            if i.index not in self.total:
                self.logger.warning('"{}" cannot be dressed as "{}" is not dressed'.format(cur.name, i.name))
                return False
        self.logger.debug('"{}" is valid as all prerequisites are dressed'.format(cur.name))
        return True

def main():
    d_hat = DressType(1, "hat")
    d_pants = DressType(2, "pants")
    d_shirts = DressType(3, "shirts")
    d_shoes = DressType(4, "shoes")
    d_socks = DressType(5, "socks")
    d_leave = DressType(6, "leave")

    Rules.dependOn(d_shoes, d_socks)
    Rules.dependOn(d_shoes, d_pants)
    Rules.dependOn(d_hat, d_shirts)

    Rules.required(d_pants)
    Rules.required(d_shirts)
    Rules.required(d_shoes)
    Rules.required(d_socks)

    h = DressHandler()
    h.addDressType(d_hat)
    h.addDressType(d_pants)
    h.addDressType(d_shirts)
    h.addDressType(d_shoes)
    h.addDressType(d_socks)
    h.addDressType(d_leave)

    print(h.runCommand("5 1"))
    print(h.runCommand("5 2 3 4"))
    print(h.runCommand("5 2 3 4 6"))
    print(h.runCommand("5 2 3 6"))
    print(h.runCommand("5 2 3"))
    print(h.runCommand("5 3 4 2"))
    print(h.runCommand("5 3 8"))
    print(h.runCommand("5 3 haha"))
    print(h.runCommand(""))

if __name__ == "__main__":
    main()
