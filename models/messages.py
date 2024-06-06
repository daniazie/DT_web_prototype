class Messages():
    def __str__(self):
        return "msg_id : {0}, sender_id: {1}, recipient_id: {2}, message: {3}, timestamp: {4}, thread_id: {5}, url: {6}".format(self.msg_id, self.sender_id, self.recipient_id, self.message, self.timestamp, self.thread_id, self.url)
    
    @property
    def msg_id(self):
        return self.__msg_id
    @msg_id.setter
    def msg_id(self, msg_id):
        self.__msg_id = msg_id
        
    @property
    def sender_id(self):
        return self.__sender_id
    @sender_id.setter
    def sender_id(self, sender_id):
        self.__sender_id = sender_id
        
    @property
    def recipient_id(self):
        return self.__recipient_id
    @recipient_id.setter
    def recipient_id(self, recipient_id):
        self.__recipient_id = recipient_id
        
    @property
    def message(self):
        return self.__message
    @message.setter
    def message(self, message):
        self.__message = message
        
    @property
    def timestamp(self):
        return self.__timestamp
    @timestamp.setter
    def timestamp(self, timestamp):
        self.__timestamp = timestamp
        
    @property
    def thread_id(self):
        return self.__thread_id
    @thread_id.setter
    def thread_id(self, thread_id):
        self.__thread_id = thread_id
        
    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self, url):
<<<<<<< HEAD
        self.__url = url
=======
        self.__url = url


# class Message_thread:
#     def __str__(self):
#         return "thread_id : {0} | sender : {1}, recipient : {2}"\
#     .format(self.thread_id,self.sender_id,self.recipient_id)

#     @property
#     def thread_id(self):
#         return self.__thread_id
#     @thread_id.setter
#     def thread_id(self, thread_id):
#         self.__thread_id = thread_id
#     @property
#     def sender_id(self):
#         return self.__sender_id
#     @sender_id.setter
#     def sender_id(self, sender_id):
#         self.__sender_id = sender_id

#     @property
#     def recipient_id(self):
#         return self.__recipient_id
#     @recipient_id.setter
#     def recipient_id(self, recipient_id):
#         self.__recipient_id = recipient_id
>>>>>>> ade23fe966ba49c3f00fa1822e0947117ffe9362
