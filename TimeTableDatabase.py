import sqlite3, sys, os
from sqlite3 import Error

def OpenDatabase():
    try:
        Timetable_Database = sqlite3.connect('TimeTableDatabase.sqlite')
        cursor = Timetable_Database.cursor()
        print("Database Opened Successfully")

        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS Lectures(
             LectureID TEXT NOT NULL,
             LectureType TEXT NOT NULL,
             LectureStartTime TEXT NOT NULL,
             LectureEndTime TEXT NOT NULL,
             LectureDuration TEXT NOT NULL,
             LectureWeek TEXT NOT NULL,
             Lecturer TEXT NOT NULL,
             LectureLocation TEXT NOT NULL,
             LectureDay TEXT NOT NULL
             );''')

            print("Created database table")
            Timetable_Database.close()
        except Error as e:
            print("Database Error")
            ExceptionInfo()
            print(e)

        Timetable_Database.close()

    except Error as e:
        print("Database Error")
        ExceptionInfo()
        print(e)


def ClearDB():
        try:
            Timetable_Database = sqlite3.connect('TimeTableDatabase.sqlite')
            cursor = Timetable_Database.cursor()
            print("Database Opened Successfully")

            try:
                TimeTableContentCheck = "SELECT * FROM Lectures"
                cursor.execute(TimeTableContentCheck)
                Check = cursor.fetchone() # Checks if lecture timetable is empty, if not empties it out (To prevent repeated results)

                if len(Check) > 0:
                    print("Deleting table")
                    cursor.execute("DROP TABLE Lectures")
            except:
                print("Lecture table doesn't exist yet")

            try:
                cursor.execute('''CREATE TABLE IF NOT EXISTS Lectures(
                 LectureID TEXT NOT NULL,
                 LectureType TEXT NOT NULL,
                 LectureStartTime TEXT NOT NULL,
                 LectureEndTime TEXT NOT NULL,
                 LectureDuration TEXT NOT NULL,
                 LectureWeek TEXT NOT NULL,
                 Lecturer TEXT NOT NULL,
                 LectureLocation TEXT NOT NULL,
                 LectureDay TEXT NOT NULL
                 );''')

                print("Created database table")
                Timetable_Database.close()
            except Error as e:
                print("Database Error")
                ExceptionInfo()
                print(e)
        except:
            pass



def ExceptionInfo():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

def CommitToDatabase(values, columns):
    if columns == "all":
        columns = ["LectureID", "LectureType", "LectureStartTime", "LectureEndTime", "LectureDuration", "LectureWeek", "Lecturer", "LectureLocation", "LectureDay"]

    if len(values) != len(columns):
        print("Not enough values in list provided to be committed to database")
        return None

    try:
        Timetable_Database = sqlite3.connect('TimeTableDatabase.sqlite')
        cursor = Timetable_Database.cursor()
        #ClearDB()

    except Error as e:
        print("Database Error")
        ExceptionInfo()
        print(e)


    try:
        sql = 'insert into Lectures({}) values({})'.format(
                ', '.join(columns),
                ', '.join('?' for _ in columns),
                )
        cursor.execute(sql, values)
        Timetable_Database.commit()
        Timetable_Database.close()


        print("Committed values to Database")
    except Error as e:
        print("Database Error...")
        ExceptionInfo()
        print(e)


        #failure to commit to database
def GetSpecificClassType(type, day):
        try:
            Timetable_Database = sqlite3.connect('TimeTableDatabase.sqlite')
            cursor = Timetable_Database.cursor()
            print("Database Opened Successfully")

        except Error as e:

            print("Database error...")
            ExceptionInfo()
            print(e)

        try:

            print("Fetching Lectures on " + str(day))
            cursor.execute("SELECT * FROM Lectures WHERE LectureType='{columnchoice}' AND LectureDay='{daychoice}'".\
            format(columnchoice = type, daychoice = day)) #(day,).\
            #format(columnchoice = type))
            all_rows = cursor.fetchall()
            print(all_rows)
            Timetable_Database.close()
            return(all_rows)

        except Error as e:

            print("Database error...")
            ExceptionInfo()
            print(e)
            Timetable_Database.close()
            return ""

        Timetable_Database.close()


def GetLecturesOnDay(day):
    #Query DB for lectures w/ result of {day} on LectureDay column
    #Rank them by starting date

    try:
        Timetable_Database = sqlite3.connect('TimeTableDatabase.sqlite')
        cursor = Timetable_Database.cursor()
        print("Database Opened Successfully")

    except Error as e:

        print("Database error...")
        ExceptionInfo()
        print(e)

    try:

        print("Fetching Lectures on " + str(day))
        cursor.execute('SELECT * FROM Lectures WHERE LectureDay= ?', (day,)) #{daychosen}#.\
            #format(daychosen = day))
        all_rows = cursor.fetchall()
        print(all_rows)
        Timetable_Database.close()
        return(all_rows)

    except Error as e:

        print("Database error...")
        ExceptionInfo()
        print(e)
        Timetable_Database.close()
        return ""

    #Timetable_Database.commit()
    Timetable_Database.close()

def parse_results(listofvalues):
    #Parses results from GetLecturesOnDay
    #Returns only simple values, i.e. Lecture Name/Type/ Start & End + Place
    ListOfValuesToReturn = []

    valuestoinclude = [0, 1, 2, 3, 7] #Index values according to DB structure
    try:
        for i in range(0, len(listofvalues)):
            ListOfValuesToReturn.append([])
            for x in range(0, len(list(listofvalues[i]))): #range(0, len(listofvalues[i])):
                if x in valuestoinclude:
                    ListOfValuesToReturn[i].append(str(listofvalues[i][x]))
    except:
        print("Parsing results error")
        ExceptionInfo()

    #print(ListOfValuesToReturn)
    return ListOfValuesToReturn



OpenDatabase()
#GetLecturesOnDay("Monday")
