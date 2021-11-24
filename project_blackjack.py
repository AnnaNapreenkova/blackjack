import random
import numpy as np

class Game(object):

        def __init__(self, player, funds=100):	
                self.dealer = Dealer()
                self.player = Player(player, funds)
                self.deck = Deck()

                self.setup()
                self.check_winner()
                self.end_game()
        
        
        def deal_card(self, player):
                card = self.deck.stack.pop()
                player.hand.append(card)
		
		
        def setup(self):
                self.deck.shuffle()
                self.bet = self.player.place_bet()
		
                for i in range(2):
                        self.deal_card(self.player)
                        self.deal_card(self.dealer)
			
                self.deck.total_up(self.player)
                self.deck.total_up(self.dealer)               
                print()
                print(self)
                
                
        def calc(self, dealer, player):   ##TODO: улучшить вывод результатов    
                 
            if self.deck.total_up(dealer) == 21:
                if self.deck.total_up(player) != 21:
                    self.player.score = -1                    
                else:
                    self.player.score = 0 
                return self.player.score   
                 
            else:
                if self.deck.total_up(player) == 21:
                    self.player.score = 1
                    return self.player.score                
                else:
                    while(self.player.choice() and self.deck.total_up(player)<21):
                        self.deal_card(self.player)
                        print()
                        print(self)    
                        if self.deck.total_up(player) > 21:
                            self.player.score = -1                        
                            return self.player.score 
                        if False:
                            break
                while self.deck.total_up(dealer) < 17:
                        self.deal_card(self.dealer)
                        print()
                        print(self) 
            
            if self.deck.total_up(dealer) > 21 and self.deck.total_up(player) <= 21:
                if self.player.score != -1:
                    self.player.score = 1
                    return self.player.score 
            else:
                if self.deck.total_up(player) > self.deck.total_up(dealer):
                    if self.deck.total_up(player) <= 21:
                        self.player.score = 1
                        return self.player.score 
                    elif self.deck.total_up(player) == self.deck.total_up(dealer):
                        self.player.score = 0
                        return self.player.score
                    elif self.deck.total_up(player) < self.deck.total_up(dealer):
                        self.player.score = -1
                        return self.player.score    
                    else:
                        self.player.score = -1
                        return self.player.score          
				
        def check_winner(self):
                self.calc(self.dealer,self.player)          
                
                if self.player.score == -1:
                        print('Dealer wins')
                        self.end_game()
                elif self.player.score == 0:
                        print('It a tie')
                        self.end_game()
                elif self.player.score == 1:
                        print('{} wins'.format(self.player.name))
                        self.player.payout()
                        print("{}'s bank has been increased: {}.".format(self.player.name, self.player.funds))
                        self.end_game()
            
        def end_game(self):
                bank = self.player.funds
                if bank >= 10:
                        again = input("Do you want to play again (Y/N)? ")
                        if again.lower().startswith('y'):
                                self.__init__(self.player.name, funds=self.player.funds)
                        elif again.lower().startswith('n'):
                                exit(1)
                elif bank < 10:
                        print("You're all out of money!  Come back with some more dough, good luck next time!")
                        exit(2)
						
        def __str__(self): 
                dealer_hand = [card for card, value in self.dealer.hand]
                player_hand = [card for card, value in self.player.hand]

                print("Dealer hand : {}".format(dealer_hand))
                print("Dealer score : {}".format(self.deck.total_up(self.dealer)))
                print()
                print("{}'s hand : {}".format(self.player.name, player_hand))
                print("{}'s score : {}".format(self.player.name, self.deck.total_up(self.player)))
                print()
                print(("{}'s current bet: {}.".format(self.player.name, self.player.bet)))
                print("{}'s current bank: {}.".format(self.player.name, self.player.funds))
                print("-" * 40)
                return ''




class Dealer(object):

    def __init__(self):
    
        self.name = "Dealer"
        self.score = 0
        self.hand = []
        
class Player(Dealer):

    def __init__(self, name, funds, bet=0):
        super().__init__()
        self.name = name
        self.funds = funds
        self.bet = bet
    
    def place_bet(self, amount=10):    
        #amount = input("Enter amount of your bet:")  TODO: разобраться с ручными ставками
        self.funds -= amount
        self.bet += amount
        
    def payout(self, amount=10 ):
        prize = amount * 2
        self.funds += prize
        self.bet = 0
     
    @staticmethod 
    def choice():
        while True:
            choice = input("Do you want another card (Y/N)?:")
            if choice.lower().startswith('y'):
                return True
            elif choice.lower().startswith('n'):
                return False
            else:
                print('Incorrect answer')
                continue

class Deck(object): 

        def __init__(self):        
                self.stack = [('A','A'), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
                      ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
                      ('J', 10), ('Q', 10), ('K', 10)] * 4
                self.shuffle()            
                
        def shuffle(self):
                random.shuffle(self.stack)
        def deal_card(self):
                card = self.stack.pop()
                return card               
                
        def get_ace_values(self, temp_list):     ##функция подсчета стоимости тузов
                sum_array = np.zeros((2**len(temp_list), len(temp_list)))  
                # Этот цикл получает комбинации
                for i in range(len(temp_list)):  
                        n = len(temp_list) - i  
                        half_len = int(2**n * 0.5)  
                        for rep in range(int(sum_array.shape[0]/half_len/2)):  
                                sum_array[rep*2**n : rep*2**n+half_len, i]=1  
                                sum_array[rep*2**n+half_len : rep*2**n+half_len*2, i]=11  
                return list(set([int(s) for s in np.sum(sum_array, axis=1)\
                             if s<=21]))  # Конвертация num_aces, int в list                       

        def ace_values(self, num_aces):  
                temp_list = []  
                for i in range(num_aces):  
                        temp_list.append([1,11])  
                return self.get_ace_values(temp_list)

        def total_up(self, p):  ##функция подсчета очков
                aces = 0
                total = 0
		
                for card in p.hand:
                        if card[1] != 'A':
                                total += int(card[1])
                        else:
                                aces +=1
				
                ace_value_list = self.ace_values(aces)
                final_totals = [i+total for i in ace_value_list if i+total<=21]
		
                if final_totals == []:
                    p.score = min(ace_value_list) + total                  
			
                else:
                    p.score = max(final_totals)
                return p.score
					
def main():

    player_name = input("Welcome to the casino!  What's your name? ")
    Game(player_name)


if __name__ == '__main__':

    main()
