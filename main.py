import subprocess
import re
import os
import sys

def hasSetup():
    return True


def setup():
    pass


def updateGitStatus():
    subprocess.Popen("git add -A .", shell=True)


def getNewFileList():
    ret = subprocess.check_output("git status", shell=True)
    newFileList = re.findall("\s*new file:\s*([^\s]*)\s*", ret)
    return newFileList


def commitAndPublish(filelist):
    msg = '新增%s张图片'%len(filelist)
    for f in filelist:
        msg += f+"\n"
    subprocess.Popen('git commit -m "%s"' % msg, shell=True)
    subprocess.Popen('git push origin master')
    generateNewHtml(filelist)


def generateNewHtml(filelist):
    pass

def main():
    if not hasSetup():
        setup()
    updateGitStatus()
    newFiles = getNewFileList()
    commitAndPublish(newFiles)


if __name__ == '__main__':
    main()