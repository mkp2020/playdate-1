from .user import User

class Matcher:
    def __init__(self, men, women):
        self.men = men
        self.women = women
        #self.women_matched = [False for w in self.women] #but we'd need to import matcher into user??
        for m in self.men:
            m.setAllRankings(self.women)
        for w in self.women:
            w.setAllRankings(self.men)

    #women propose to men, and men reject or accept
    def findTentativeMatch(self):
        for w in self.women:
            w.propose()
        for m in self.men:
            m.acceptProposal()

    #True if everyone matched
    def isStable(self):
        for w in self.women: #women bc all women must be paired off
            if w.current_match == None:
                return False
        return True
        
    def getTotalRankingWeight(self):
        if not self.isStable():
            print("pairs not yet stable")
            return
        total_ranking_weight = 0
        for user in self.men + self.women:
            total_ranking_weight += user.current_match_ranking()
        return total_ranking_weight

    #returns all existing pairs
    def getAllPairs(self):
        return [[m, m.current_match] for m in self.men] #men bc some men may not get matched up if odd number
