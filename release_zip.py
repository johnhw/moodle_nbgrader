import os, shutil

if __name__=="__main__":
    if len(sys.args)!=2:
        print("""
        Usage:
        
            build_zips.py <assign>
            
        Zips up the assignment folder in release/<assign> and puts it in uploads/<assign.zip>
        
        """)
        exit(-1)
        
    assign = sys.args[1]
    fullpath = os.path.join('release',assign)
    if os.path.isdir(fullpath):
        shutil.make_archive('upload/%s' % file, 'zip', fullpath, verbose=True)        
    