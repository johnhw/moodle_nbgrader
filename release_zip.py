import os, shutil
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            """
        Usage:
        
            build_zips.py <assign>
            
        Zips up the assignment folder in release/<assign> and puts it in uploads/<assign.zip>
        
        """
        )
        exit(-1)

    assign = sys.argv[1]
    fullpath = os.path.join("release", assign)
    if os.path.isdir(fullpath):
        print("Creating archive upload/%s.zip" % assign)
        shutil.make_archive("upload/%s" % assign, "zip", fullpath, verbose=True)
    shutil.unpack_archive("upload/%s.zip" % assign, "tests/%s" % assign)

