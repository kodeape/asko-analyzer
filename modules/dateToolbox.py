months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class Date:
    def __init__(self, dateStr): # assuming y-m-d format on dateStr
        self.dateStr = dateStr
        dateList = dateStr.split("-")
        self.y = dateList[0]
        self.y_int = int(self.y)
        self.m = dateList[1]
        self.m_int = int(self.m)
        self.m_name = months[self.m_int-1]
        self.d = dateList[2]
        self.d_int = int(self.d)
        self.dateInt = int("".join(dateList))

    def __str__(self):
        return self.dateStr
    
    def __int__(self):
        return self.dateInt
    
    def __lt__(self, other):
        return self.dateInt < other.dateInt
    
    def __le__(self, other):
        return self.dateInt <= other.dateInt

    def __gt__(self, other):
        return self.dateInt > other.dateInt
    
    def __ge__(self, other):
        return self.dateInt >= other.dateInt

    def __eq__(self, other):
        return self.dateInt == other.dateInt
