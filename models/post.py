POST_TYPE_NORMAL = 0
POST_TYPE_JOB = 1

# =========================================================

class Post:
    def __str__(self):
        return "post_id : {0}, writer : {1}".format(self.post_id, self.writer)

    @property
    def post_id(self):
        return self.__post_id
    @post_id.setter
    def post_id(self,post_id):
        self.__post_id = post_id

    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self,date):
        self.__date = date

    @property
    def type(self):
        return self.__type
    @type.setter
    def type(self,type):
        self.__type = type

    @property
    def writer(self):
        return self.__writer
    @writer.setter
    def writer(self,writer):
        self.__writer = writer

    @property
    def preview(self):
        return self.__preview
    @preview.setter
    def preview(self,preview):
        self.__preview = preview

    @property
    def job_info(self):
        return self.__job_info
    @job_info.setter
    def job_info(self,job_info):
        self.__job_info = job_info

# =========================================================

class Post_job_info:
    @property
    def post_id(self):
        return self.__post_id
    @post_id.setter
    def post_id(self,post_id):
        self.__post_id = post_id

    @property
    def location(self):
        return self.__location
    @location.setter
    def location(self,location):
        self.__location = location

    @property
    def pay(self):
        return self.__pay
    @property
    def pay_formatted(self):
        return f"{self.__pay:,}"
    @pay.setter
    def pay(self,pay):
        self.__pay = pay

    @property
    def time_unit(self):
        return self.__time_unit
    @time_unit.setter
    def time_unit(self,time_unit):
        self.__time_unit = time_unit

    @property
    def lang_level(self):
        return self.__lang_level
    @lang_level.setter
    def lang_level(self,lang_level):
        self.__lang_level = lang_level
    
    @property
    def working_days(self):
        return self.__working_days
    @working_days.setter
    def working_days(self,working_days):
        self.__working_days = working_days

    @property
    def working_hours(self):
        return self.__working_hours
    @working_hours.setter
    def working_hours(self,working_hours):
        self.__working_hours = working_hours

    @property
    def workplace(self):
        return self.__workplace
    @workplace.setter
    def workplace(self,workplace):
        self.__workplace = workplace

# =========================================================

class Post_content:
    def __str__(self) -> str:
        return "{0}({1}) : {2}".format(self.__post_id, self.__language, self.__content)

    @property
    def post_id(self):
        return self.__post_id
    @post_id.setter
    def post_id(self,post_id):
        self.__post_id = post_id

    @property
    def content(self):
        return self.__content
    @content.setter
    def content(self,content):
        self.__content = content

    @property
    def origin(self):
        return self.__origin
    @origin.setter
    def origin(self,origin):
        self.__origin = origin

    @property
    def language(self):
        return self.__language
    @language.setter
    def language(self,language):
        self.__language = language

    @property
    def contributer(self):
        return self.__contributer
    @contributer.setter
    def contributer(self,contributer):
        self.__contributer = contributer

    @property
    def like(self):
        return self.__like
    @like.setter
    def like(self,like):
        self.__like = like

    @property
    def unlike(self):
        return self.__unlike
    @unlike.setter
    def unlike(self,unlike):
        self.__unlike = unlike