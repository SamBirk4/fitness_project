import datetime
from doctest import BLANKLINE_MARKER


class Profile:
   
    def __init__(self, user_first, user_last, user_height, user_weight):
        self.user_first = user_first
        self.user_last = user_last
        self.user_height = user_height
        self.user_weights = [int (user_weight)]
        self.new_weight = user_weight
        self.product = self.user_gain_loss()
        self.bmi = self.user_bmi()
        self.gain_loss = 0

    def log_output(self):
        return [self.user_weights, self.gain_loss, int(self.bmi), weigh_date()]
    
    def add_entry(self, new_weight):
        self.new_weight = new_weight
        self.user_weights.append(new_weight)
        self.gain_loss = self.user_gain_loss()
        self.bmi = self.user_bmi()
        
    def user_bmi(self):
        return int(self.new_weight) / (int(self.user_height) ** 2) * 703
    
    def user_gain_loss(self):
        if len(self.user_weights) > 1:
            self.product = int(self.user_weights[-2]) - int(self.new_weight)
            if self.product > 0:
                return("Loss of {}".format(self.product))
            elif self.product < 0:
                return("Gain of {}".format(abs(self.product)))
            else:
                return 0
        else:
            return 0 
        
def weigh_date():
    return datetime.datetime.now().strftime('%m-%d-%Y, %I:%M %p')




          


    

    
       

        