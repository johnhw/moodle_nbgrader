import sys
import csv
from nbgrader.apps import NbGraderAPI


def import_moodle(csvfile):
    api = NbGraderAPI()
    gradebook = api.gradebook
    
    with open(csvfile) as f:
 
        reader = csv.DictReader(f)            
        for line in reader:
            name, surname, matric, email = line['First name'], line['Surname'], line['ID number'], line['Email address']                                
            unique_id = "{0} {1}".format(name, surname) # moodle unique ID
            print("Adding {0}".format(unique_id))
            
            # store the matric as the last name, as we can't get this otherwise
            gradebook.update_or_create_student(unique_id, first_name=name, last_name=matric, email=email)

                
if __name__=="__main__":
     if len(sys.argv)!=2:
            print("""
            Usage:
            
                import_classlist.py <csvfile>
                
            Loads a class list from the Moodle exported Gradebook (the *whole* gradebook for
            the course, not an individual assignment gradesheet -- these have different formats!)
            
            Students will either be created or updated in the database from the import; they will never
            be removed. It is safe to run this command multiple times as the classlist changes.
            
            """)
            exit(-1)
     import_moodle(sys.argv[1])
     
                