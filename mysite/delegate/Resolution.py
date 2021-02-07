class Resolution:
    """A dictionary-like class to organize a resolution"""
    def resoFind(self, start, end, key="", offset='default', text=""):
        if len(text) < 1:
            text = self.workingText
        if len(key) < 1:
            key = start
        if offset == 'default':
            offset = len(start)

        s = text[text.find(str(start), text.find(str(key))) + offset: text.find(str(end), text.find(key) + len(key))]
        index = text.find(str(end), text.find(key))
        return s, index
        
    def __init__(self, text):
        self.rawText = text # keep a copy of the unaltered text
        self.workingText = text # deletes sections as it parses
        self.header = {
            "forum": "",
            "questionOf": "",
            "submittedBy": "",
            "committee": "",
        }
        self.preambles = []
        self.clauses = []

        if len(text) < 1:
            return

        self.header["forum"] = self.resoFind("</b>", "\n", "FORUM")[0]
        self.header["questionOf"] = self.resoFind("</b>", "\n", "QUESTION OF")[0]
        self.header["submittedBy"] = self.resoFind("</b>", "\n", "SUBMITTED BY")[0]
        self.workingText = self.workingText[self.resoFind("\n", "\n", "SUBMITTED BY")[1]:].lstrip()
        self.header["committee"] = self.resoFind("", "\n")[0]
        self.workingText = self.workingText[self.resoFind("", "\n")[1]:].lstrip()

        while self.workingText.find("1)", 0, 5) == -1: # 1) is not within the first 5 characters of workingText
            self.preambles.append(self.resoFind("<i>", "\n", offset = 0)[0]) # offset = -3 to include <i> tag
            self.workingText = self.workingText[self.resoFind("<i>", "\n", offset = -3)[1]:].lstrip()

        clauseNum = 1
        while len(self.workingText.strip()) > 0:
            clause = {
                "number": clauseNum,
                "clause": "",
                "sub-clauses": [],
            }
            clause["clause"] = self.resoFind(str(clauseNum) + ")", "\n")[0]
            self.workingText = self.workingText[self.resoFind(str(clauseNum) + ")", "\n")[1]:].lstrip()

            if self.workingText.find("a)", 0, 5) > -1: #subclause found
                subClauseNum = 97 # ascii code for a
                while len(self.workingText.strip()) > 0 and self.workingText.find(str(clauseNum + 1) + ")", 0, 5) == -1: # next clause is not within the next 5 chars
                    subclause = {
                        "number": chr(subClauseNum),
                        "sub-clause": "",
                        "sub-sub-clauses": [],
                    }
                    subclause["sub-clause"] = self.resoFind(chr(subClauseNum) + ")", "\n", offset = 0)[0]
                    self.workingText = self.workingText[self.resoFind(chr(subClauseNum) + ")", "\n")[1]:].lstrip()

                    if self.workingText.find("i)", 0, 5) > -1: #subclause found
                        subSubClauseNum = 1 # ascii code for a
                        romansymbs = ['0', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv'] # probably no more than 15 sub sub clauses
                        while len(self.workingText.strip()) > 0 and self.workingText.find(chr(subClauseNum + 1) + ")", 0, 5) == -1: # next subclause is not within the next 5 chars
                            subSubClause = {
                                "number": romansymbs[subSubClauseNum],
                                "sub-sub-clause": "",
                            }
                            subSubClause["sub-sub-clause"] = self.resoFind(romansymbs[subSubClauseNum] + ")", "\n", offset = 0)[0]
                            self.workingText = self.workingText[self.resoFind(romansymbs[subSubClauseNum] + ")", "\n")[1]:].lstrip()

                            subclause["sub-sub-clauses"].append(subSubClause)
                            subSubClauseNum += 1
                    clause["sub-clauses"].append(subclause)
                    subClauseNum += 1
            self.clauses.append(clause)
            clauseNum += 1
        self.resolution = {
            "header": self.header,
            "preambles": self.preambles,
            "clauses": self.clauses,
        }

    def __str__():
        print(self.header["forum"])
        print(self.header["questionOf"])
        print(self.header["submittedBy"])
        print(self.header["committee"])
        import pprint
        for i in self.clauses:
            pp = pprint.PrettyPrinter(width = 150, indent = 4, compact = True)
            pp.pprint(i)
            print("-------------------------------")


