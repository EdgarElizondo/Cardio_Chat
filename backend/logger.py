import logging

class log:
    
    logging.basicConfig (format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)    

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        
    def info(self,message):
        self.logger.info(message)
    