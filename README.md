# moodle_nbgrader
Basic scripts for Moodle integration with nbgrader (configured for UoG)

## To import students from Moodle 
* Step 1. Export names from the grade book (Gradebook/export/plain text)

    python import_classlist.py <csvfile>

## To collect files from an assignment for marking

* From Moodle, select assignment
* View All Submissions
* Choose "Download All Submissions" from top dropdown (MAKE SURE "Download submissions in folders" is OFF)
* Copy archive into downloaded\<assignment_name>\archive\

    nbgrader zip_collect <assignment_name>


## To create a new assignment
* Create assignment in formgrader
* Edit assignment and validate
* Hit "Generate" in formgrader

    python zip_release.py <assignment_name> # updates the upload/ folder

* Upload zip to Moodle

## Returning feedback and grades

* Run autograder, and perform manual grading and feedback
*  in Moodle, enable offline gradebook and feedback files in the assignment
* Download the (empty) grading worksheet for the submission ("Grading action..." menu at the top)

    python update_gradesheet.csv <assignment_name> <exported_gradesheet.csv>

* Upload exports/<assign>_feedback.zip to Moodle (as the feedback) and exports/<assign>_marks.csv to Moodle (as the gradesheet)


