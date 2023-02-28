import pandas as pd
import time
import sys
from IPython.display import clear_output
from datetime import date, datetime

# Counts when the definition this is attached to is used and then adds to the counter that is to be used for the Part 10: Terminate Feature
def count_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    wrapper.__name__ = func.__name__
    return wrapper

# Initializes the txt file for the previous requests that is to be accessed in Part 8: Previous Requests Feature
def featureRequests(feature:str, stdID:int):
    with open(f"std{stdID}PreviousRequests.txt", "a") as f:
        date_now = date.today().strftime("%d/%m/%Y")
        time_now = datetime.now().strftime("%H:%M %p")
        text =f"\n{feature}\t\t{date_now}\t\t{time_now}\t" 
        f.write(text)
        f.close()

# Part 1: Start Feature
# Presents the option for the user to choose whether they are U, G, or B (Undergraduate, Graduate, or Both)
# And also M, D, or B0 (Master, Doctorate, or Both), then the system sleeps before redirecting to the menu window

def startFeature():

    # Asks the user whether they are undergraduate, graduate, or both
    stdLevel = input("Select what level you are in (i.e U, G, B): ")
    # The user picks "Both"
    if stdLevel == "B":
        stdLevel = ["U","G"]
        if stdLevel == ["U","G"]:

            # Asks the user if they are in their masters, doctorate, or both)
            stdDegree = input("Specify what degree are you in (i.e M, D, B0): ")

            # The user picks "Both"
            if stdDegree == "B0":
                stdDegree = ["B","M","D"]

            # The user picks "Master"
            elif stdDegree == "M":
                stdDegree = ["B","M"]

            # The user picks "Doctorate"
            elif stdDegree == "D":
                stdDegree = ["B","D"]

    # The user picks "Undergraduate"
    elif stdLevel == "U":
        stdLevel = "U"
        stdDegree = "B"

    # The user picks "Graduate"
    elif stdLevel == "G":
        stdLevel = "G"
        if stdLevel == "G":
            stdDegree = input("Specify what degree are you in (i.e M, D, B0): ")

            # The user picks "Both"
            if stdDegree == "B0":
                stdDegree = ["M","D"]

            # The user picks "Master"
            elif stdDegree == "M":
                stdDegree = "M"

            # The user picks "Doctorate"
            elif stdDegree == "D":
                stdDegree = "D"

    # Asks the user for their student ID
    stdID = int(input("Enter Student ID (i.e. 202006000): "))

    # Checks whether the user's input of student ID is in the database
    dataFrame = pd.read_csv("studentDetails.csv")
    df_results = dataFrame[dataFrame["stdID"] == stdID]

    # Tells the user if their student ID is invalid which means that their student ID is not in the databas
    if df_results.empty:
        print("Invalid ID")
        return stdID

    # Returns to the menu feature after sleeping
    return menuFeature(stdLevel, stdDegree, stdID)
    time.sleep(4)

# Part 2: Menu Feature
# Shows the menu window with the 8 features (Student Details, Statistics, Transcript based on Major Courses,
# Transcript based on Minor Courses, Full Transcript, Previous Transcript Requests, Select Another Student,
# and Terminate the System) as a selection with assigned numbers for the user to choose from
def menuFeature(stdLevel, stdDegree, stdID):

    # Initializes the amount of requests

    feature_requested = 0

    # Shows the selection
    print(
        """Student Transcript Generation System
        ===================================================
        1. Student details
        2. Statistics
        3. Transcript based on major courses
        4. Transcript based on minor courses
        5. Full transcript
        6. Previous transcript requests
        7. Select Another student
        8. Terminate the system
        ===================================================
        """)
    
    feature = int(input("Enter your feature selected: "))

    # The user chooses the option 1 "Student Details" and then brings them to the said feature
    # Adds 1 to the feature requested counter
    if feature == 1:
        featureRequests("Details", stdID)
        detailsFeature(stdID, stdLevel, stdDegree)

    # The user chooses the option 2 "Statistics" and then brings them to the said feature
    # Adds 1 to the feature requested counter
    elif feature == 2:
        featureRequests("Statistics", stdID)
        statisticFeature(stdID, stdDegree, stdLevel)

    # The user chooses the option 3 "Transcript based on Major Courses" and then shows the said feature
    # Adds 1 to the feature requested counter
    elif feature == 3:
        featureRequests("Major Transcript", stdID)
        majorTranscriptFeature(stdID, stdDegree, stdLevel)

    # The user chooses the option 4 "Transcript based on Minor Courses" and then shows the said feature
    # Adds 1 to the feature requested counter
    elif feature == 4:
        featureRequests("Minor Transcript", stdID)
        minorTranscriptFeature(stdID, stdDegree, stdLevel)

    # The user chooses the option 5 "Full Transcript" and then shows the said feature
    # Adds 1 to the feature requested counter
    elif feature == 5:
        featureRequests("Full Transcript", stdID)
        fullTranscriptFeature(stdID, stdDegree, stdLevel)

    # The user chooses the option 6 "Previous Transcript Requests" and then shows the said feature
    # Adds 1 to the feature requested counter
    elif feature == 6:
        featureRequests("Previous Requests", stdID)
        previousRequestsFeature(stdID, stdDegree, stdLevel)

    # The user chooses the option 7 "Select Another Student" and then runs the said feature
    # Adds 1 to the feature requested counter
    elif feature == 7:
        featureRequests("New Student", stdID)
        newStudentFeature()

    # The user chooses the option 8 "Terminate the System" and then runs the said feature
    # Adds 1 to the feature requested counter
    elif feature == 8:
        terminateFeature(feature_requested)

    # Happens if the user inputs a number outside the range of 1 to 8
    else:
        print("Input out of range")

# Part 3: Details Feature
# Shows the details of the student who owns the entered student ID which is then stored to a txt file
@count_calls
def detailsFeature(stdID, stdLevel, stdDegree):

    # Reads the csv file and is then entered as the value of the variable dataFrame
    dataFrame = pd.read_csv("studentDetails.csv")
    stdDetail = dataFrame[dataFrame["stdID"] == stdID]

    # Initializes the txt file
    stdDetail_txt = """"""

    #Initializes term text to be displayed
    term = ""
    rowLen = len(stdDegree)
        
    for i in range(rowLen):
        if i == 0:
            term += str(stdDetail.Terms.iloc[0])
        if i != 0:
            term += ", " + str(stdDetail.Terms.iloc[i])
    # Inputs information to the txt file
    stdDetail_txt+=(f"""    Name: {stdDetail.Name.iloc[0]}
    stdID: {stdID}
    Level(s): {stdLevel}
    Number of Terms: {term}
    College(s): {stdDetail.College.iloc[0]}
    Department(s): {stdDetail.Department.iloc[0]}
    """)

    print(stdDetail_txt)

    with open(f"std{stdID}details.txt", "w") as f:
        f.write(stdDetail_txt)
        f.close()

    # Clears the screen followed by a short sleep and then proceeds to the menu feature again
    clear_output(wait=True)
    time.sleep(4)
    menuFeature(stdLevel, stdDegree, stdID)

# Part 4: Statistics Feature
# Presents some statistics about the student's records based on the selected option(s)
@count_calls
def statisticFeature(stdID, stdDegree:list, stdLevel):

    # Reads the csv file for a specific student ID and is then entered as the value of the variable dataFrame
    dataFrame = pd.read_csv(f"{stdID}.csv")
    stat_txt = """"""

    # The user chooses "Undergraduate"
    if stdLevel == "U":
        for degree in stdDegree:
            degDf = dataFrame.loc[dataFrame["Degree"].str.contains(degree)]
            stat_txt+=f"""       
            ======================================================
            ************   Undergraduate Level   ************
            ======================================================
            Overall Average (major and minor) for all terms: {round(degDf.Grade.mean())}
            Average (major and minor) of each term: {round(degDf.Grade.sum()/degDf.creditHours.sum())}"""

            terms = degDf.Term.unique() # getting unique terms
            for i in terms:
                average = round(degDf[degDf["Term"] == i]["Grade"].mean())
                stat_txt += f'\n\tTerm {i}: {average}'

            repeatedCourses = degDf[degDf.courseName.duplicated()] # taking a row where the course is repeated
            if not repeatedCourses.empty:           #then check if we are repeating row or not
                repeated = f"Yes, {repeatedCourses['courseName'].iloc[0]}"
            else:
                repeated = "No" 

            maximumGrade = degDf[degDf["Grade"] == degDf["Grade"].max()] #Getting the row where the max grade is
            minimumGrade = degDf[degDf["Grade"] == degDf["Grade"].min()] #Getting the row where the min grade is
            #Taking the term and grade on the bottom lines
            stat_txt+=f"""
            Maximum grade(s) and in which term(s):Term - {maximumGrade["Term"].iloc[0]}, Grade - {maximumGrade["Grade"].iloc[0]} 
            Minimum grade(s) and in which term(s):Term - {minimumGrade["Term"].iloc[0]}, Grade - {minimumGrade["Grade"].iloc[0]}  
            Do you have any repeated course(s)? {repeated}
            """

    # The user chooses "Graduate" or "Both"
    elif stdLevel == "G" or ["U","G"]:
        for degree in stdDegree:
            degDf = dataFrame.loc[dataFrame["Degree"].str.contains(degree)]
            stat_txt+=f"""       
            ======================================================
            ************   Graduate({degree}) Level   ************
            ======================================================
            Overall Average (major and minor) for all terms: {round(degDf.Grade.mean())}
            Average (major and minor) of each term: {round(degDf.Grade.sum()/degDf.creditHours.sum())}"""

            terms = degDf.Term.unique() # getting unique terms
            for i in terms:
                average = round(degDf[degDf["Term"] == i]["Grade"].mean())
                stat_txt += f'\n\tTerm {i}: {average}'

            repeatedCourses = degDf[degDf.courseName.duplicated()] # taking a row where the course is repeated
            if not repeatedCourses.empty:           #then check if we are repeating row or not
                repeated = f"Yes, {repeatedCourses['courseName'].iloc[0]}"
            else:
                repeated = "No" 

            maximumGrade = degDf[degDf["Grade"] == degDf["Grade"].max()] #Getting the row where the max grade is
            minimumGrade = degDf[degDf["Grade"] == degDf["Grade"].min()] #Getting the row where the min grade is
            #Taking the term and grade on the bottom lines
            stat_txt+=f"""
            Maximum grade(s) and in which term(s):Term - {maximumGrade["Term"].iloc[0]}, Grade - {maximumGrade["Grade"].iloc[0]} 
            Minimum grade(s) and in which term(s):Term - {minimumGrade["Term"].iloc[0]}, Grade - {minimumGrade["Grade"].iloc[0]}  
            Do you have any repeated course(s)? {repeated}
            """

    print(stat_txt)

    with open(f"std{stdID}statistics.txt", "w") as f:
        f.write(stat_txt)
        f.close()

    # Clears the screen followed by a short sleep and then proceeds to the menu feature again
    clear_output(wait=True)
    time.sleep(4)
    menuFeature(stdLevel, stdDegree, stdID)

# Part 5: Major Transcript Feature
# Show the transcript of the student based on the major courses
@count_calls
def majorTranscriptFeature(stdID, stdDegree:list, stdLevel):

    # Reads the csv file for a specific student ID and is then entered as the value of the variable dataFrame
    dataFrame = pd.read_csv(f"{stdID}.csv")

    # Initializes the txt file
    mtf_txt = """"""

    # Initializes the array for frames
    frames = []

    # Appends degree to the frame array
    for degree in stdDegree:
        degDf = dataFrame.loc[dataFrame["Degree"].str.contains(degree)]
        frames.append(degDf)

    resultDf = pd.concat(frames)
    resultDf = resultDf[resultDf["courseType"] == "Major"]

    df1 = pd.read_csv("studentDetails.csv")
    stdDf = df1[df1["stdID"] == stdID]

    for degree in stdDegree[0]:
        stdDetail = stdDf.loc[stdDf["Degree"].str.contains(degree)]
        mtf_txt += f""" Name: {stdDetail.Name.iloc[0]}              stdID: {stdID}
         College: {stdDetail.College.iloc[0]}              Department: {stdDetail.Department.iloc[0]}
         Major: {stdDetail.Major.iloc[0]}              Minor: {stdDetail.Minor.iloc[0]}
         Level: {stdDetail.Level.iloc[0]}              Number of terms: {stdDetail.Terms.iloc[0]}
        """

        terms = resultDf.Term.unique()
    

    for degree in stdDegree:
        stdDetail1 = stdDf.loc[stdDf["Degree"].str.contains(degree)]
        for i in terms:
            termDf = resultDf[resultDf["Term"]==i]
            mtf_txt+=f"""======================================================
            ************      Term {i}     ************
            ======================================================
            course id   course name     credit hours    grade""" 

            for index, td in termDf.iterrows():
                cID = td.courseID
                cName = td.courseName
                cHours = td.creditHours
                grade = td.Grade
                mtf_txt+=f"""\n\t\t{cID}       {cName}        {cHours}       {grade}"""
            
            mAve = round(termDf.Grade.sum() / termDf.creditHours.sum()) # calculate major avg
            tAve = round(termDf.Grade.mean()) # calculate overall avg

            mtf_txt+=f"""\n\t\t\tMajor Average = {mAve}    \t\tOveral Average = {tAve}
            """
        
        mtf_txt+=f"""======================================================
                ************End of Transcript for Level ({stdDetail1.Level.iloc[0]})  ************
                ======================================================
            """

    print(mtf_txt)

    with open(f"std{stdID}MajorTranscript.txt", "w") as f:
        f.write(mtf_txt)
        f.close()

    time.sleep(5) #sleeping system for 5 seconds
    clear_output(wait=True) #clearing terminal
    menuFeature(stdLevel, stdDegree, stdID)

# Part 6: Minor Transcript Feature
# Show the transcript of the student based on the minor courses
@count_calls
def minorTranscriptFeature(stdID, stdDegree:list, stdLevel):

    # Reads the csv file for a specific student ID and is then entered as the value of the variable dataFrame
    dataFrame = pd.read_csv(f"{stdID}.csv")

    # Initializes the txt file
    mtf_txt = """"""

    frames = []

    for degree in stdDegree:
        degDf = dataFrame.loc[dataFrame["Degree"].str.contains(degree)]
        frames.append(degDf)

    resultDf = pd.concat(frames)
    resultDf = resultDf[resultDf["courseType"] == "Minor"]

    df1 = pd.read_csv("studentDetails.csv")
    stdDf = df1[df1["stdID"] == stdID]

    for degree in stdDegree[0]:
        stdDetail = stdDf.loc[stdDf["Degree"].str.contains(degree)]
        mtf_txt += f""" Name: {stdDetail.Name.iloc[0]}              stdID: {stdID}
         College: {stdDetail.College.iloc[0]}              Department: {stdDetail.Department.iloc[0]}
         Major: {stdDetail.Major.iloc[0]}              Minor: {stdDetail.Minor.iloc[0]}
         Level: {stdDetail.Level.iloc[0]}              Number of terms: {stdDetail.Terms.iloc[0]}
        """

        terms = resultDf.Term.unique()

    for degree in stdDegree:
        stdDetail1 = stdDf.loc[stdDf["Degree"].str.contains(degree)]
        for i in terms:
            termDf = resultDf[resultDf["Term"]==i]
            mtf_txt+=f"""======================================================
            ************      Term {i}     ************
            ======================================================
            course id   course name     credit hours    grade""" 

            for index, td in termDf.iterrows():
                cID = td.courseID
                cName = td.courseName
                cHours = td.creditHours
                grade = td.Grade
                mtf_txt+=f"""\n\t\t{cID}       {cName}        {cHours}       {grade}"""
            
            mAve = round(termDf.Grade.sum() / termDf.creditHours.sum()) # calculate major avg
            tAve = round(termDf.Grade.mean()) # calculate overal avg

            mtf_txt+=f"""\n\t\t\tMinor Average = {mAve}    \t\tOveral Average = {tAve}
            """
        
        mtf_txt+=f"""======================================================
            ************End of Transcript for Level ({stdDetail1.Level.iloc[0]})  ************
            ======================================================
        """

    print(mtf_txt)

    with open(f"std{stdID}MinorTranscript.txt", "w") as f:
        f.write(mtf_txt)
        f.close()

    time.sleep(5) #sleeping system for 5 seconds
    clear_output(wait=True) #clearing terminal
    menuFeature(stdLevel, stdDegree, stdID)

# Part 7: Full Transcript Feature
# Show the transcript of the student based on both their major and minor courses together
@count_calls
def fullTranscriptFeature(stdID, stdDegree:list, stdLevel):

    # Reads the csv file for a specific student ID and is then entered as the value of the variable dataFrame
    dataFrame = pd.read_csv(f"{stdID}.csv")

    # Initializes the txt file
    ftf_txt = """"""

    # Initializes the array for frames
    frames = []

    for degree in stdDegree:
        degDf = dataFrame.loc[dataFrame["Degree"].str.contains(degree)]
        frames.append(degDf)

    for level in stdLevel:
        lvlDf = dataFrame.loc[dataFrame["Level"].str.contains(level)]
        frames.append(lvlDf)

    resultDf = pd.concat(frames)
    resultDf = resultDf[(resultDf["courseType"] == "Minor") | (resultDf["courseType"] == "Major") ]

    df1 = pd.read_csv("studentDetails.csv")
    stdDf = df1[df1["stdID"] == stdID]

    for degree in stdDegree[0]:
        stdDetail = stdDf.loc[stdDf["Degree"].str.contains(degree)]
        dfResult = resultDf.loc[resultDf["Degree"].str.contains(degree)]

        ftf_txt += f""" Name: {stdDetail.Name.iloc[0]}              stdID: {stdID}
         College: {stdDetail.College.iloc[0]}              Department: {stdDetail.Department.iloc[0]}
         Major: {stdDetail.Major.iloc[0]}              Minor: {stdDetail.Minor.iloc[0]}
         Level: {stdDetail.Level.iloc[0]}              Number of terms: {stdDetail.Terms.iloc[0]}
        """

        terms = dfResult.Term.unique()

    for degree in stdDegree:
        stdDetail1 = stdDf.loc[stdDf["Degree"].str.contains(degree)]
        for i in terms:
            termDf = resultDf[resultDf["Term"]==i]
            ftf_txt+=f"""======================================================
            ************      Term {i}     ************
            ======================================================
            course id   course name     credit hours    grade""" 

            for index, td in termDf.iterrows():
                cID = td.courseID
                cName = td.courseName
                cHours = td.creditHours
                grade = td.Grade
                ftf_txt+=f"""\n\t\t{cID}       {cName}        {cHours}       {grade}"""
            
            major_rows = termDf[termDf["courseType"] == "Major"]
            major_avg = round(major_rows.Grade.sum() / major_rows.creditHours.sum()) 
            # calculating minor Average
            minor_rows = termDf[termDf["courseType"] == "Minor"]
            minor_avg = round(minor_rows.Grade.sum() / minor_rows.creditHours.sum()) 
            # calculating term Average
            t_avg = round(termDf.Grade.sum() / len(terms))
            # calculating overal Average
            o_avg = round(termDf.Grade.mean()) 

            ftf_txt+=f"""\n\t\t\tMajor Average = {major_avg}    \tMinor Average = {minor_avg}
            \t\t\tTerm Average = {t_avg}    \t\tOverall Average = {o_avg}
            """
        
        ftf_txt+=f"""======================================================
            ************End of Transcript for Level({stdDetail1.Level.iloc[0]})  ************
            ======================================================
        """

    print(ftf_txt)

    with open(f"std{stdID}FullTranscript.txt", "w") as f:
        f.write(ftf_txt)
        f.close()

    time.sleep(5) #sleeping system for 5 seconds
    clear_output(wait=True) #clearing terminal
    menuFeature(stdLevel, stdDegree, stdID)

# Part 8: Previous Requests Feature
# Shows the user's their previous requests (Major, Minor, or Full transcripts)
@count_calls
def previousRequestsFeature(stdID, stdDegree:list, stdLevel):
    # opening
    with open(f"std{stdID}PreviousRequests.txt") as f:
        text = f.read()
        print(text)
        f.close()
        
    time.sleep(5)
    clear_output(wait=True)
    menuFeature(stdLevel, stdDegree, stdID)

# Part 9: New Student Feature
# Gives access to the new user to start the program again
# The screen sleeps first and then clears the screen before proceeding to showing the start feature again
@count_calls
def newStudentFeature():
    time.sleep(5)
    clear_output(wait=True)
    startFeature()  

# Part 10: Terminate Feature
# The user will be able to close the program and then show the number of requests they had during their use
def terminateFeature(countReqs):
    print(f"Program Closed!\n Feature Requested for "
          f"{detailsFeature.calls + statisticFeature.calls + majorTranscriptFeature.calls + minorTranscriptFeature.calls + fullTranscriptFeature.calls + previousRequestsFeature.calls + newStudentFeature.calls} times")

startFeature()