class PT():

    def __init__(self):
        """ Initializes the basic data associated with a PT """
        self.classes = []

        self.email = ""
        self.name = ""

        self.link = ""
        self.office_hours = ""
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    def get_zoom_link(self):
        """ Return the zoom link, if there is any """
        if self.link == "":
            return None

        return self.link

    def get_class(self):
        """ Return a string listing all the classes the PT oversees """
        class_string = [" ".join(pt_class) for pt_class in self.classes]

        return ",".join(class_string)

    def has_office_hours(self, day, hour):
        """ Check if the PT is hosting office hours at a given weekday and hour """
        hours = self.office_hours[self.days.index(day)]

        if len(hours) == 0:
            return False

        for index in range(0, len(hours), 2):
            if hours[index] <= hour <= hours[index+1]:
                return True

        return False

    def add_class(self, code, course, section):
        """ Add a class to the PT's list of classes """
        self.classes.append([code, course, section])

    def add_hours(self, day, start, end):
        """ Add additional hours to list of office hours """
        index = self.days.index(day)

        self.office_hours[index].append(start)
        self.office_hours[index].append(end)

    def update_email(self, email):
        """ Updates the preferred email for contact """
        self.email = email

    def update_name(self, name):
        """ Updates the preferred name to be called by """
        self.name = name

    def update_link(self, link):
        """ Updates the preferred link for online office hours """
        self.link = link

