import json
from datetime import datetime

class Time_manage:

    def __init__(self):
       fileObject = open("week_time.json", "r")
       jsonContent = fileObject.read()
       aList = json.loads(jsonContent)
       
       self.Start_Hour_Monday = float (aList['Start_Hour_Monday'])
       self.End_Hour_Monday = float (aList['End_Hour_Monday'])

       self.Start_Hour_Tuesday = float (aList['Start_Hour_Tuesday'])
       self.End_Hour_Tuesday = float (aList['End_Hour_Tuesday'])

       self.Start_Hour_Wednesday = float (aList['Start_Hour_Wednesday'])
       self.End_Hour_Wednesday = float (aList['End_Hour_Wednesday'])

       self.Start_Hour_Thursday = float (aList['Start_Hour_Thursday'])
       self.End_Hour_Thursday = float (aList['End_Hour_Thursday'])

       self.Start_Hour_Friday = float (aList['Start_Hour_Friday'])
       self.End_Hour_Friday = float (aList['End_Hour_Friday'])

       


    def dow(date):
         days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
         dayNumber=date.weekday()
         out = days[dayNumber]
         return out

    def time():
        today = datetime.now()
        date_time = today.strftime("%d/%m/%Y %H:%M:%S")
        print("date_time:" , date_time)
        minute = '{:02d}'.format(today.minute)
        hour = '{:02d}'.format(today.hour)
        day = Time_manage.dow(today) 
        return [day , hour , minute]
    
    def cal_time():
        
        time_current = Time_manage.time()
        # print ("time_current:" , time_current)

        day = time_current[0]
        hour = time_current[1]
        minute = time_current[2]

        hour = int (hour)
        minute = int (minute)

        print("day:" , day)

        # print("hour:" , hour)
        # print("minute:" , minute)

        hour_start = f'{hour}' + '.' + f'{minute}'
        hour_start = float (hour_start)
        # print ("hour_start:" , hour_start)



        if day == 'Saturday':
            # print("000000")
            return False

        elif day == 'Sunday':  
            # print("111111")
            return False

        elif day == 'Monday' and hour_start >= Time_manage().Start_Hour_Monday and hour_start <= Time_manage().End_Hour_Monday :
            # print("222222")
            return True
            
        elif day == 'Tuesday' and hour_start >= Time_manage().Start_Hour_Tuesday  and hour_start <= Time_manage().End_Hour_Tuesday :
            # print("333333")
            return True

        elif day == 'Wednesday' and hour_start >= Time_manage().Start_Hour_Wednesday and hour_start <= Time_manage().End_Hour_Wednesday :
            # print("444444")
            return True

        elif day == 'Thursday' and hour_start >= Time_manage().Start_Hour_Thursday and hour_start <= Time_manage().End_Hour_Thursday :
            # print("555555")
            return True

        elif day == 'Friday' and hour_start >= Time_manage().Start_Hour_Friday and hour_start <= Time_manage().End_Hour_Friday :
            # print("666666")    
            return True 
                    
        else:
            return False
   