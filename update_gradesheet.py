import nbgrader, csv, codecs, sys, os, shutil
from nbgrader.apps import NbGraderAPI

def unicode_csv_dictreader(path, *args, **kwargs):
    "create a csv dict reader that copes with encoding correctly"
    # utf-8-sig strips off a BOM if it's present
    stream = codecs.open(path, encoding='utf-8-sig')
    return UnicodeCSVDictReader(stream, *args, **kwargs)

class UnicodeCSVDictReader(csv.DictReader):
    def __init__(self, unicode_csvfile, *args, **kwargs):
        decoder = codecs.getdecoder('utf-8')
        self.decoder = lambda v: decoder(v)[0]
        utf8_csvfile = codecs.iterencode(unicode_csvfile, encoding='utf-8')
        # bollicks to csv.DictReader being an oldstyle class
        csv.DictReader.__init__(self, utf8_csvfile, *args, **kwargs)
        self.fieldnames = [self.decoder(f) for f in self.fieldnames] 

    def next(self):
        data = csv.DictReader.next(self)
        return {k: self.decoder(v) for (k,v) in data.iteritems()}


def zip(out, root):
    shutil.make_archive(out, 'zip', root)

def moodle_gradesheet(assignment, csvfile, with_feedback=True):    
    
    api = NbGraderAPI()
    gradebook = api.gradebook        
    reader = unicode_csv_dictreader(csvfile)    
    fname =    "exports/{0}_gradesheet.csv".format(assignment)
    
    if with_feedback:
        try:
            os.mkdir("exports/%s" % assignment)
        except OSError:
            print("Directory already exists")
            
    
    with open(fname, 'wb') as out:
        writer = csv.DictWriter(out, reader.fieldnames)
        writer.writeheader()
        for line in reader:        
            ident, fullname, status, grade, max_grade = line['Identifier'], line['Full name'], line['Status'], line['Grade'], line['Maximum Grade']                        
            try:
                submission = gradebook.find_submission(assignment, fullname)                
            except:
                print("\tNo submission for {0} in assignment {1}".format(fullname,assignment))
            else:
                print("\tProcessing submission for {0} in assignment {1}".format(fullname,assignment))
                if with_feedback:
                    ident = ident[12:]
                    
                    # zip into correct filenaming format
                    zip("exports/{2}/{1}_{0}_assignsubmission_file_{2}_feedback".format(ident, fullname, assignment),  "feedback/{1}/{2}".format(ident, fullname, assignment))
                    print("\t\tFeedback generated...")
            
                line['Grade'] = submission.score
                line['Maximum Grade'] = submission.max_score
                writer.writerow(line)
            
        print("Wrote to {0}".format(fname))
        if with_feedback:
              zip("exports/{0}_feedback".format(assignment),  "exports/{0}".format(assignment))
              print("Created feedback zip file {0}.zip".format(assignment))
                
        
if __name__=="__main__":
    if len(sys.argv)!=3:
            print("""
            Usage:
            
                update_gradesheet.py <assign> <csvfile>
                
            Updates a CSV file gradesheet (which must have be downloaded from
            Moodle with "offline gradesheets" enabled in the assignment settings) with
            the results from grading the assignment <assign>.
            
            The output will be in exports/<assign>_gradesheet.csv
            
            Feedback will be zipped up into the file exports/<assign>_feedback.zip and this
            can be uploaded to Moodle if "Feedback files" is enabled. This uploads all student
            feedback in one go.
            
            """)
            exit(-1)
    
    assignment, csvfile = sys.argv[1], sys.argv[2]
    print("Updating gradesheet for {0}...".format(assignment))
    moodle_gradesheet(assignment, csvfile)
    