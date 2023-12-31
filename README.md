# gradebook Ver. 0.1

## Distinctiveness and Complexity:
--- This project is without question distinct from the projects worked with in this course as well as cs50. This project focuses on functioning as a web-based school Grade system. Ver 0.1 implements the base functionality of creating a school, adding courses and assigning teachers as well as enrolling students. a full gradebook page for teachers to add assignments and grades into the system and to generate the students' overall grades. 
--- this project is also complex with over thirty different routes and 8 models.
--- While my implementation of JavaScript was minimal, this being due to my decision to rework many of what used to be JavaScript API calls to load information into the page all into Django forms as I found that using the Django model forms functioned more efficiently for the number of submissions the site works with. 
--- mobile responsiveness was easily implemented with the use of CSS flexbox

##Files
--- I have chosen to exclude the general Django files I have left untouched from the file breakdown
###/App
---auth.py
----- auth.py abstracts the authorization functions from views.py to clean up the overall project, this file contains a login, registration and logout function with validation
---forms.py
----- contains all of my Django Model forms used throughout the site, again abstracting away from views.py to simplify.
---helpers.py
----- contains a helper function that generates access codes for schools to support other users joining a school as well as course and student codes
---models.py
---- contains all of my data models including, school, students, courses, grades, assignments, course grades and attendance (unutilized in this version)
---urls.py
----- to Django standards, this denotes all of the 30 routes used throughout the site
---user.py
----- abstracted model for user linked to models.py
---views.py
-----includes all view functions for page generation, routing, data generating and form generating and handling
### /static
--- script.js
----- contains a views handler to handle view toggling
--- styles.css
----- all styling for the site
### /templates/app
--- layout.html
----- main Django standard layout page mainly setting up the flexbox frame for the pages and the sidenav
--- index.html
----- front page of the site. loads welcome view and notifications(unimplemented)
--- settings.html
----- page for working with school settings and adds the ability to leave or delete a school
### /templates/app/auth
--- login.html, register.html
----- handles user logins and registrations
### /templates/app/courses
--- addCourse.html
----- site page for adding and editing courses to the school
--- course.html
---- -page for viewing more detailed information on a course with edit, enroll students, unenroll students and gradebook links
--- courses.html
----- page for viewing all teacher and school courses as well as the link for adding courses
--- drop.html
----- handles the dropping of courses
--- enroll.html
----- handles the enrolling of students in courses
--- removeCourse.html
----- handles removing a course from the school
### /templates. /app/gradebook
--- assignment.html
----- page for creating and editing assignments
--- grade.html
----- page for adding and editing student grades for course assignments
--- gradebook.html
----- main gradebook page that generates all the students enrolled in the course as well as overall grades and assignment grades with links to edit assignments and grades
### /school
--- deleteSchool.html
----- page that confirms the user's choice to delete the school profile
--- leaveSchool.html
----- handles users who have joined a school as a secondary user who decide to leave the school
--- setupshool.html
----- contains forms for joining or creating a new school
### /templates/app/students
--- addStudent.html
----- manages adding a student to the school
--- removeStudent.html
----- manages removing a student from the school
--- student.html
----- provides more detailed information of students
--- students.html
----- generates the school and course student lists

## How to run
with Django installed, run
" Python manage.py runserver

## dependencies
Django

## Description
Gradebook is an all-in-one web-based school grade handling webapp that manages school information, courses with enroll and unenroll functions, students' assignments assignment grades and overall grades.
-as Gradebook functions entirely on the web, users who have created the school have the option to share join codes to provide access to the school information to multiple user accounts.
- provides distinctiveness to account types and provieds permissions based on what join code is provided when joining aschool.