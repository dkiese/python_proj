'''
Created on Apr 9, 2021

@author: danki
'''

import csv
import json
import sys

from Courses import Courses
from Marks import Marks
from Student import Student 
from Tests import Tests


studentList = []
testList = []
markList = []
courseList = []
courseAverages = []
courseWeights = []
cindex = 0

def printStudent(index,end):
    # there are more students to print
    if(end == 0):
        st = f'{{\n   "id": {studentList[index].studentId},\n   "name": "{studentList[index].name}",\n   "totalAverage": {studentList[index].totalAverage},\n   "courses": [\n{printCourses(index)}\t]\n   }},\n' 
    # no more students to print
    else:
        st = f'{{\n   "id": {studentList[index].studentId},\n   "name": "{studentList[index].name}",\n   "totalAverage": {studentList[index].totalAverage},\n   "courses": [\n{printCourses(index)}\t]\n  }}\n ]\n}}'
    return st

def printCourses(index):
    global cindex
    done = 0
    length = len(studentList[index].courseList)
    st = ""
    for course in studentList[index].courseList:
        # the course can be printed
        if(courseWeights[cindex] == 100):
            if(done == length-1):
                st += f'  \t{{\n   \t"id": {course.courseId},\n \t"name": "{course.name}",\n   \t"teacher": "{course.teacher}",\n   \t"courseAverage": {courseAverages[cindex]}\n  \t}}\n' 
            else:
                st += f'  \t{{\n   \t"id": {course.courseId},\n   \t"name": "{course.name}",\n   \t"teacher": "{course.teacher}",\n   \t"courseAverage": {courseAverages[cindex]}\n  \t}},\n' 
        else:
            if(done == length-1):
                st += f'  \t{{\n   \t"error": "Invalid course weights"\n   \t}}\n'
            else:
                st += f'  \t{{\n   \t"error": "Invalid course weights"\n   \t}},\n'
        done +=1
        cindex +=1
    return st

def takeId(elem):
    return elem.studentId

def populateStudent():
    # reading out specific csv file
    try:
        with open(sys.argv[2], mode='r') as csv_file:
        # creating the csv reader
            csv_reader = csv.DictReader(csv_file)
        
            # for every line in the csv file
            for row in csv_reader:
            # make a new student
                student = Student()
                # updating students name 
                student.name = row['name'].strip() # remove any trailing/leading whitespace
                # update students ID
                student.studentId = row['id'].strip()
                # update the courseList
                for course in courseList:
                    taken = 0
                    for test in course.testList:
                        for marks in test.markList:
                            if(marks.studentId == student.studentId):
                                if(taken == 0):
                                    taken = 1
                                    student.courseList.append(course)
                studentList.append(student)
        # sort the list by studentId
        studentList.sort(key=takeId)
    except:
        exit(f'Error opening file, {sys.argv[2]}')
        
def populateTest():
    try:   
        # reading out specific csv file
        with open(sys.argv[3], mode='r') as csv_file:
            # creating the csv reader
            csv_reader = csv.DictReader(csv_file)
            
            # for every line in the csv file
            for row in csv_reader:
                # make a new test
                test = Tests()
                # updating the testid 
                test.testId = row['id'].strip() # remove any trailing/leading whitespace
                # update the courseId
                test.courseId = row['course_id'].strip()
                # update the weight
                test.weight = row['weight'].strip()
                # update markList
                for mark in markList:
                    # this mark is for this test
                    if(mark.testId == test.testId):
                        test.markList.append(mark)
                testList.append(test)   
    except:
        exit(f'Error opening file, {sys.argv[3]}')    

def populateMark():
    try:
        # reading out specific csv file
        with open(sys.argv[4], mode='r') as csv_file:
            # creating the csv reader
            csv_reader = csv.DictReader(csv_file)
            
            # for every line in the csv file
            for row in csv_reader:
                # make a new test
                mark = Marks()
                # updating the testId 
                mark.testId = row['test_id'].strip() # remove any trailing/leading whitespace
                # update the studentId
                mark.studentId = row['student_id'].strip()
                # update the marks
                mark.mark = row['mark'].strip()
                # updates the list
                markList.append(mark)   
    except:
        exit(f'Error opening file, {sys.argv[4]}')
            
def writeToFile(file):
    try:
        f = open(f"{sys.argv[5]}", "w")
        f.write(file)
    except:
        exit(f'Error writing to file, {sys.argv[5]}')
    finally:
        f.close() 

def populateCourse():
    try:
            # reading out specific csv file
        with open(sys.argv[1], mode='r') as csv_file:
            # creating the csv reader
            csv_reader = csv.DictReader(csv_file)
            
            # for every line in the csv file
            for row in csv_reader:
                # make a course
                course = Courses()
                # updating the courseId
                course.courseId = row['id'].strip() # remove any trailing/leading whitespace
                # update the course name
                course.name = row['name'].strip()
                # update the teacher
                course.teacher = row['teacher'].strip()
                # update the testlist
                for test in testList:
                    if(test.courseId == course.courseId):
                        course.testList.append(test)
                courseList.append(course)
    except:
        exit(f'Error opening file {sys.argv[1]}')
        
def calculateAverage():
    # this is for the course Average
    for student in studentList:
        totalAvg = 0
        length = len(student.courseList)
    # for every course this student is taking
        for course in student.courseList:
            avg = 0
            weight = 0
            # for every test in this course
            for test in course.testList:
                #make sure the weight adds up to 100 and if it does calculate the average mark
                #get every mark for this particular test
                weight = weight + int(test.weight)
                for mark in test.markList:
                    if(mark.studentId == student.studentId):
                        avg = avg + (int(mark.mark) * (int(test.weight)/100))
                                                     
            courseWeights.append(weight)                                                    
            avg = round(avg, 2)
            course.courseAverage = avg
            totalAvg = totalAvg + avg
            courseAverages.append(avg)
            
        totalAvg = totalAvg / length
        totalAvg = round(totalAvg, 2)
        student.totalAverage = totalAvg

n = len(sys.argv)
print("Total arguments passed:", n)
if(n != 6):
    exit("please use the correct file format: \n\t{path-to-courses-file} {path-to-students-file} {path-to-tests-file} {path-to-marks-file} {path-to-output-file}")
    
    
populateMark()
populateTest()
populateCourse()
populateStudent()
calculateAverage()

# keep track of what student we are on
lineNumber = 0
st = ""
while(lineNumber < len(studentList)):
    # the first student
    if(lineNumber == 0):
        st += f'{{\n "students": [\n'
    if(lineNumber == len(studentList)-1):
        st += f'  {printStudent(lineNumber,1)} '
    else:
        st += f'  {printStudent(lineNumber,0)} '
    lineNumber+=1
    
writeToFile(json.loads(json.dumps(st))) 


