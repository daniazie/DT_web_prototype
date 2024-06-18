class Community_head:
    @property
    def community_id(self):
        return self.__community_id
    @community_id.setter
    def community_id(self,community_id):
        self.__community_id = community_id

    @property
    def community_name(self):
        return self.__community_name
    @community_name.setter
    def community_name(self,community_name):
        self.__community_name = community_name

    @property
    def community_desc(self):
        return self.__community_desc
    @community_desc.setter
    def community_desc(self,community_desc):
        self.__community_desc = community_desc

    @property
    def number_members(self):
        return self.__number_members
    @number_members.setter
    def number_members(self,number_members):
        self.__number_members = number_members

# ===========================================
    
class Community_post:
    @property
    def c_post_id(self):
        return self.__c_post_id
    @c_post_id.setter
    def c_post_id(self,c_post_id):
        self.__c_post_id = c_post_id

    @property
    def writer(self):
        return self.__writer
    @writer.setter
    def writer(self,writer):
        self.__writer = writer

    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self,date):
        self.__date = date

    @property
    def number_like(self):
        return self.__number_like
    @number_like.setter
    def number_like(self,number_like):
        self.__number_like = number_like

    @property
    def content(self):
        return self.__content
    @content.setter
    def content(self,content):
        self.__content = content

#=========================================================

class Community_post_comment:
    @property
    def writer(self):
        return self.__writer
    @writer.setter
    def writer(self,writer):
        self.__writer = writer

    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self,date):
        self.__date = date

    @property
    def comment(self):
        return self.__comment
    @comment.setter
    def comment(self,comment):
        self.__comment = comment