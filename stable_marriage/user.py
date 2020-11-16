import heapq as heappq

class User:
    all_interests = ["music", "dance", "nature", "sports", "futurism", "food", "fashion", "film", "reading", 
                    "arts, graphic design", "technology", "history", "futurism", "video games", "public speaking"]
    

    def __init__(self, name, major_category, hp_house, user_interests = []):
        self.name = name

        self.major_category = major_category
        self.hp_house = hp_house
        self.interests_dict = self.initializeDict([user_interests])

        self.current_match = None
        self.current_proposals = [] #heap of users
        self.user_to_rankings = {} #dict of user : ranking
        self.rankings_to_user = {} #dict of ranking : user
        self.others_available = [] #heap of users
        

    def initializeDict(self, user_interests):
        dct = {}
        for interest in self.all_interests:
            dct[interest] = 1 if interest in user_interests else 0
        return dct

    def setAllRankings(self, otherGroup): 
        for user in otherGroup:
            ranking = self.findOneRanking(user)
            self.user_to_rankings[user] = ranking
            self.rankings_to_user[ranking] = user
            heappq.heappush(self.others_available, ranking)


    #how much self ranks the other person; each user has a unique rank
    def findOneRanking(self, otherUser):
        if otherUser in self.user_to_rankings:
            return self.user_to_rankings[otherUser]
        ranking = 0
        if self.major_category == otherUser.major_category: #if we were to add LOTS of factors, we could add all of them to a for loop and decide how much to add to rankings using a dict of factor : points
            ranking += 3
        if self.hp_house == otherUser.hp_house:
            ranking += 1
        for selfInterest, otherInterest in zip(self.interests_dict, otherUser.interests_dict):
            if selfInterest == otherInterest:
                ranking += 1
        ranking *= -1

        while ranking in self.rankings_to_user: #can't have duplicate rankings, so make this one slightly worse ranked
            ranking +=  0.001
        return ranking 


    #if not matched, propose
    def propose(self):
        if self.current_match != None or len(self.others_available) == 0:
            return
            
        #choose best ranking option; cannot propose to this person again
        best_proposal_ranking = heappq.heappop(self.others_available)
        best_proposal = self.rankings_to_user[best_proposal_ranking]
        heappq.heappush(best_proposal.current_proposals, best_proposal.user_to_rankings[self])

    #set your match to other
    def proposalAccepted(self, otherUser):
        self.current_match = otherUser

    #accept or reject proposals
    def acceptProposal(self):
        if len(self.current_proposals) == 0: #no one proposed to you
            return
        
        #check if you should accept best proposal
        best_proposal_ranking = heappq.heappop(self.current_proposals)
        if self.current_match == None or best_proposal_ranking < self.user_to_rankings[self.current_match]:
            #found someone better so leaving current match
            if self.current_match != None:
                self.current_match.relationship_ended()

            #set each other to each other's matches
            self.current_match = self.rankings_to_user[best_proposal_ranking]
            self.current_match.proposalAccepted(self)

        #reject everyone else
        self.current_proposals.clear()
    
    #your tentative partner left you
    def relationship_ended(self):
        self.current_match = None

    def current_match_ranking(self):
        return self.user_to_rankings[self.current_match]

    def __repr__(self):
        #if self.current_match != None:
        #    return self.name + " " + str(self.user_to_rankings[self.current_match])
        return self.name
