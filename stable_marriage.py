#could use PQ's to make this faster and more elegant?
import heapq as heappq


class User:
    all_interests = ["music", "dance", "nature", "sports", "futurism", "food", "fashion", "film", "reading", 
                    "arts, graphic design", "technology", "history", "futurism", "video games", "public speaking"]
    rankings = {} #DELETE THIS ONCE WE IMPLEMENT DETERMINE RANKINGS; dict of ranking : user
    current_proposals = [] #list of users; replace with PQ?

    def __init__(self, first_name, last_name, major_category, hp_house, interests = []):
        self.first_name = first_name
        self.last_name = last_name
        self.major_category = major_category
        self.hp_house = hp_house
        self.current_match = None
        self.current_proposals = []
        self.interests_dict = self.initializeDict([interests])
        #self.rankings = determineRankings()
    
    def initializeDict(self, interest_list):
        dct = {}
        for user_interest in interest_list:
            dct[user_interest] = 1 if user_interest in self.all_interests else 0
        return dct

    #def determineRankings(): #yo how do we implement this

    #if not matched, propose
    def propose(self, other):
        if self.current_match == None:
            heappq.heappush(other.current_proposals, other)

    #set your match to other
    def proposalAccepted(self, other):
        self.current_match = self.rankings[other]

    #accept or reject proposals
    def acceptProposal(self):
        best_proposal = heappq.heappop(self.current_proposals)
        if self.current_match == None or best_proposal < self.current_match:
            #found someone better so leaving current match
            if self.current_match != None:
                self.current_match.rejected()

            #set each other to each other's matches
            self.current_match = best_proposal
            self.rankings[best_proposal].proposalAccepted(self)
        self.current_proposals.clear()
    
    #your tentative partner left you
    def rejected(self):
        self.current_match = None
    
    def __str__(self):
        return self.first_name + " " + self.last_name


class Matcher:

    def __init__(self, men, women):
        assert len(men) == len(women)
        self.men = men
        self.women = women

    #women propose to men, and men reject or accept
    def findTentativeMatch(self):
        for w in self.women:
            w.propose(heappq.nsmallest(1, w.rankings)[0])
        for m in self.men:
            m.acceptProposal()

    #True if everyone matched
    def isStable(self):
        for m in self.men:
            if m.current_match == None:
                return False
        return True

    #returns all existing pairs
    def getAllPairs(self):
        return [[m, m.rankings[m.current_match]] for m in self.men]

def main():
    match_finder = Matcher([], [])
    while not match_finder.isStable():
        match_finder.findTentativeMatch()
    all_pairs = match_finder.getAllPairs()
    print("here are the pairs: " + str(all_pairs))

main()
