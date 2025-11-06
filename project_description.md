# 1. Project Description: Course Layout and Teaching load Allocations
This project aims to facilitate course layout, planning and teaching load allocations at a university. 
Which involves designing and creating a database and writing and executing several queries that correspond to the operations specified in the following subsections.

## 1.1 Business Overview
The university offers several courses.  
A course may consist of several teaching activities. 
The two most important tasks are
- to plan a course in terms of deciding the hours needed for various teaching activities called “course layout and planning”,
- and actual allocation of teaching activities to the teachers, called “teaching load allocations”.

## 1.2 Detailed Descriptions
### Course Layout
Each course has a unique course code, course name, högskolepoäng (HP), 
minimum and maximum number of students must also be mentioned in the course layout.

Below is an example of a course layout.  

**Table 1**. Course Layout Example. 
This example is only meant to illustrate some teaching activities and other information that may be associated with course layouts, 
it is NOT meant to show any rows or columns of a Table.  

| Course code | Course Name            | HP  | Min Students | Max Students |
|-------------|------------------------|-----|--------------|--------------|
| IV1351      | Data Storage Paradigms | 7.5 | 50           | 250          |
| IX1500      | Discrete Mathematics   | 7.5 | 50           | 150          |

### Course Instances:
A course instance is an instance of a particular course layout given at a particular period of a year, 
for example a course given during period 1 in year 2025 gets a new unique course instance. 
An academic year is divided into four periods, P1, P2, P3 and P4. 
For simplicity, you may assume that the academic year is from January to December. 
A course instance also has the total number of students registered.

### Teaching Activities:
We are mainly interested in the following teaching activities that may be associated with course layouts or course instances :  
Lecture, Lab, Tutorial, Seminar, examination, administration and Others. 
However, the database must be flexible enough to add more activities in the future.

Some teaching activities may require some preparation time for teachers (let's call it a multiplication factor).

Below is an example of multiplication factors for different teaching activities. 

**Table 2**. Multiplication Factors Example. 
This example is only meant to illustrate example of multiplication factors for some teaching activities, 
it is NOT meant to show any rows or columns of a Table. 

| Activity Name | Factor |
|---------------|--------|
| Lecture       | 3.6    | 
| Lab           | 2.4    |
| Tutorial      | 2.4    |
| Seminar       | 1.8    |
For example, for the course IV1351, in the course instance, Table 3, lecture hours are given 20 hours. 
After applying the above rule/multiplication factor, the total hours for the lectures including preparation time would be 72 hours. 
In other words, a teacher actually spends 72 hours for giving 20 hours lecture. 

### Planned Activities:
A course may contain several activities, we are mainly interested in the number of hours needed for the following teaching activities: 
Lectures, Labs, Tutorials, Seminars and Others. It is important to note that some courses may have only some specific teaching activities. 
Each course instance also gets two additional activities that correspond to examination and administration hours which depend on the number of registered students and högskolepoäng (HP).  
Here is an example to calculate the examination and administration hours for a particular course instance (these are derived attributes). 

Examination hour = $32+ 0.725* No. Students$ 

Admin hours = $2*HP+ 28+ 0.2* No. Students$ 

Below is an example of course instances with planned activities.

**Table 3**. Course Instance Example. 
This example is only meant to illustrate some teaching activities and other information that may be associated with course instances, 
it is NOT meant to show any rows or columns of a Table.

| Course code | Course Instance ID | Period | # Students | Lecture Hours | Tutorial Hours | Lab Hours | Seminar Hours | Other Overhead Hours | Admin | Exam |
|-------------|--------------------|--------|------------|---------------|----------------|-----------|---------------|----------------------|-------|------|
| IV1351      | 2025-50273         | 7.5    | 200        | 20            | 80             | 40        | 80            | 650                  | 177   | 83   |
| IX1500      | 2025-50413         | 7.5    | 150        | 44            | 0              | 0         | 64            | 200                  | 141   | 73   |

### Departments: 
There are several departments at the university. 
Each department has a manager who is also a teacher/employee. 

### Teachers/Employees:
Teachers or employees are affiliated with departments.  
They are allocated teaching activities based on their interests or skill sets. 
It is also important to have their contact details and salary, which is later used to calculate the teaching cost of a course or total teaching cost for a department. 
It is also advisable to have their job titles/designations. Each employee has a manager or a supervisor. 

### Allocations:
A teacher can get involved in teaching activities for many course instances, 
and a course instance can have many teachers involved with. 

<span style="color:red">However, a teacher must not be allocated more than four different course instances simultaneously during a particular period.</span>. 

## 1.3 Conceptual Model:
[A conceptual model](https://canvas.kth.se/courses/57087/pages/conceptual-model-2) is provided that describes the requirements above.

Note that the provided conceptual model is an abstract and possibly may not capture all specific details of the system.

Note: Watch the [conceptual model lecture](https://canvas.kth.se/courses/57087/pages/conceptual-model) (only recorded, not given live). 
The conceptual model lecture page contains several videos, which together lasts about three hours.

## 1.4 Requirements on Project Task Application
The database must store all data described above, in sections 1.1 and 1.2, but no other data. 
The database will be used to retrieve reports and statistics of all possible kinds, but a user interface is not required for that purpose. 
It will instead be done by manually querying the database.

The database will not be used for any financial purpose like bookkeeping, salary or bank contacts. 
What is written above regarding salary is only about calculating the total teaching cost of a course instance or a department over a particular period.

# 2. Grading
There are three tasks, which are described below. Each task gives max 10p, and is divided into two parts giving 5p each. 
The first two tasks have a mandatory part (5p) and a higher grade part (5p). 
The third task has two higher grade parts worth 5p each. 
To pass the project all mandatory tasks must be passed. 
The higher grade tasks are optional, and contribute to the final grade as specified in the [Course Layout](https://canvas.kth.se/courses/57087/pages/course-layout). 
No partial score is given, either a part of a task is accepted and gives five points, or it isn't accepted and does not give any points. 
A task is passed when both seminar and written report are passed. 
Reporting is explained in detail below.

# 3. How to Get Help
Questions about the project can be asked these ways:

* At tutorials, tutorials exist only to provide help with project tasks. You are welcome to ask about anything related to project work at tutorials.
* In [Piazza](https://piazza.com/kth.se/fall2025/iv1351ht25/home). Don't send direct emails to teachers, instead post questions in Piazza since then all students can be helped by the answers. 
Mind that posts can be anonymous to peer students in Piazza.

# 4. How to Report
Each solved task shall be reported both in writing and at a seminar. 
A task is passed only when both written report and seminar have been accepted. 
You are encouraged to collaborate and discuss with as many other students as you wish when doing the project, 
group discussions always give a better result than individual work. The assignments are done in groups of three students; 
please sign up for a group with name "Project Groups", which you can find by following the "People" link to the left. 
You are also allowed to work alone, but that is not recommended.  

## 4.1 Written Report

## 4.2 Seminar

### 4.2.1

### 4.2.2














