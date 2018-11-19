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

    except Error as e:
        print("Database Error")
        ExceptionInfo()
        print(e)


def ClearDB(Timetable_Database, cursor):
        try:
        #    Timetable_Database = sqlite3.connect('TimeTableDatabase.sqlite')
        #    cursor = Timetable_Database.cursor()
        #    print("Database Opened Successfully")

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
        return

    try:
        Timetable_Database = sqlite3.connect('TimeTableDatabase.sqlite')
        cursor = Timetable_Database.cursor()
        ClearDB(Timetable_Database, cursor)

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

OpenDatabase()

#GetLecturesOnDay("Monday")
