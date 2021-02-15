class Resolution:
    """A dictionary-like class to organize a resolution"""
    def resoFind(self, start, end, key="", offset='default', text=""):
        if len(text) < 1:
            text = self.workingText
        if len(key) < 1:
            key = start
        if offset == 'default':
            offset = len(start)

        if text.lower().find(str(start)) > -1 and text.lower().find(str(key)) > -1 and text.lower().find(str(end)) > -1:
            s = text[text.lower().find(str(start), text.lower().find(str(key))) + offset: text.lower().find(str(end), text.lower().find(key) + len(key))]
            index = text.lower().find(str(end), text.lower().find(key))
            return s, index
        return '', 0

    def stripTags(self, s):
        if s.find('<') > -1 and s.find('>') > -1:
            return s[:s.find('<')] + s[s.find('>') + 1:]
        
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

        self.header["forum"] = self.stripTags(self.resoFind("forum:", "\n")[0])
        self.header["questionOf"] = self.stripTags(self.resoFind("question of:", "\n")[0])
        self.header["submittedBy"] = self.stripTags(self.resoFind("submitted by:", "\n")[0])
        self.workingText = self.workingText[self.resoFind("\n", "\n", "submitted by")[1]:].lstrip()
        self.header["committee"] = self.resoFind("", "\n")[0]

        print(self.header)
        self.workingText = self.workingText[self.resoFind("", "\n")[1]:].lstrip()

        while self.workingText.find("1)", 0, 5) == -1: # 1) is not within the first 5 characters of workingText
            self.preambles.append(self.resoFind("<i>", "\n", offset = 0)[0]) # offset = -3 to include <i> tag
            self.workingText = self.workingText[self.resoFind("<i>", "\n", offset = -3)[1]:].lstrip()

        clauseNum = 1
        while len(self.workingText.strip()) > 0:
            clause = {
                "number": clauseNum,
                "clause": "",
                "subClauses": [],
            }
            clause["clause"] = self.resoFind(str(clauseNum) + ")", "\n")[0]
            if len(clause['clause']) == 0:
                clause["clause"] = self.resoFind(str(clauseNum) + ")", ".")[0] # last clause ends with period
                self.workingText = self.workingText[self.resoFind(str(clauseNum) + ")", ".")[1]:].lstrip()
                if len(clause['clause']) == 0: #if still blank, exit
                    break
                else:
                    clause['clause'] += '.'
            else:
                self.workingText = self.workingText[self.resoFind(str(clauseNum) + ")", "\n")[1]:].lstrip()

            if self.workingText.find("a)", 0, 5) > -1: #subclause found
                subClauseNum = 97 # ascii code for a
                while len(self.workingText.strip()) > 0 and self.workingText.find(str(clauseNum + 1) + ")", 0, 5) == -1: # next clause is not within the next 5 chars
                    subclause = {
                        "number": chr(subClauseNum),
                        "subClause": "",
                        "subSubClauses": [],
                    }
                    subclause["subClause"] = self.resoFind(chr(subClauseNum) + ")", "\n", offset = 0)[0]
                    if len(subclause["subClause"]) == 0:
                        subclause["subClause"] = self.resoFind(chr(subClauseNum) + ")", ".", offset = 0)[0]
                        self.workingText = self.workingText[self.resoFind(chr(subClauseNum) + ")", ".")[1]:].lstrip()
                        if len(subclause["subClause"]) == 0: #if still blank, exit
                            break
                        else:
                            subclause["subClause"] += '.'
                    else:
                        self.workingText = self.workingText[self.resoFind(chr(subClauseNum) + ")", "\n")[1]:].lstrip()


                    if self.workingText.find("i)", 0, 5) > -1: #subclause found
                        subSubClauseNum = 1 # ascii code for a
                        romansymbs = ['0', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv'] # probably no more than 15 sub sub clauses
                        while len(self.workingText.strip()) > 0 and self.workingText.find(chr(subClauseNum + 1) + ")", 0, 5) == -1: # next subclause is not within the next 5 chars
                            subSubClause = {
                                "number": romansymbs[subSubClauseNum],
                                "subSubClause": "",
                            }
                            subSubClause["subSubClause"] = self.resoFind(romansymbs[subSubClauseNum] + ")", "\n", offset = 0)[0]
                            if len(subSubClause["subSubClause"]) == 0:
                                subSubClause["subSubClause"] = self.resoFind(romansymbs[subSubClauseNum] + ")", ".", offset = 0)[0]
                                self.workingText = self.workingText[self.resoFind(romansymbs[subSubClauseNum] + ")", ".")[1]:].lstrip()
                                if len(subSubClause["subSubClause"]) == 0: #if still blank, exit
                                     break
                                else:
                                    subSubClause["subSubClause"] += '.'
                            else:
                                self.workingText = self.workingText[self.resoFind(romansymbs[subSubClauseNum] + ")", "\n")[1]:].lstrip()


                            subclause["subSubClauses"].append(subSubClause)
                            subSubClauseNum += 1
                    clause["subClauses"].append(subclause)
                    subClauseNum += 1
            self.clauses.append(clause)
            print(self.clauses[:10])
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


