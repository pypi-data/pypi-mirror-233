from datetime import datetime

class BaseClass:
    ''' 
    Base Class provides Resource Created and Update Date (Automatically)
    '''
    def __self__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()