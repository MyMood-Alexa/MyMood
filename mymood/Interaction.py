

class Interaction:
    
    def __init__(self, session_id=None, time=None, responses=[]):
        self.session_id = session_id
        self.responses = responses
        self.time = time
    
        
    def update_response(self, response):
        self.responses.append(response)
        
    
    def print_interaction(self):
        print("Session: ", self.session_id)
        print("Time : ", self.time)
        for x in self.responses:
            print(x)
            
        print()
    
    def get_session(self):
        return self.session_id
