

class Interaction:

    def __init__(self, session_id=None, time=None, responses=[],
                 device_id=None, user_id=None):
        self.session_id = session_id
        self.responses = responses
        self.time = time
        self.device_id = None
        self.user_id = user_id

    def update_response(self, response):
        self.responses.append(response)

    def print_interaction(self):
        print("Device ID: ", self.device_id)
        print("User ID:", self.user_id)
        print("Session: ", self.session_id)
        print("Time : ", self.time)
        for x in self.responses:
            print(x)

        print()

    def get_session(self):
        return self.session_id

    def get_user(self):
        return self.user_id
