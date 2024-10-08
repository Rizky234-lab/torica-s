furniture.py
from menuitem import MenuItem

class furniture(MenuItem):
    def __init__(self, name, price, color):
        super().__init__(name, price)
        self.color = color
    
    def info(self):
        return self.name + ': $' + str(self.price) + ' (' + str(self.color) + 'lame)'
    
    def color_info(self):
        print('lame: ' + str(self.color_info))
