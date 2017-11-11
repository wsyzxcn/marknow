# encoding:utf8
import subprocess
import re
import os
import sys

def hasSetup():
    return True


def setup():
    pass


def updateGitStatus():
    subprocess.Popen("git add -A .", shell=True).wait()


def getNewFileList():
    ret = subprocess.check_output("git status", shell=True)
    newFileList = re.findall("\s*new file:\s*([^\s]*)\s*", ret)
    return newFileList


def commitAndPublish(filelist):
    msg = '新增%s张图片'%len(filelist)
    for f in filelist:
        msg += f+"\n"
    subprocess.Popen('git commit -m "%s"' % msg, shell=True).wait()
    subprocess.Popen('git push origin master', shell=True).wait()
    generateNewHtml(filelist)


def generateNewHtml(filelist):
    body = ''
    rawBaseUrl = getRawBaseUrl()
    for file in filelist:
        body += '<img src="%s"/>\n'%os.path.abspath(file)
        body += '<p>%s</p>\n' % "%s%s"%(rawBaseUrl, file)
    tmplfile = open("tmpl/newfileurl.html")
    tmplcontent = tmplfile.read()
    content = tmplcontent.replace("<?placeholder?>", body)
    fd = os.open("display.html", os.O_CREAT)
    os.close(fd)
    displayfile = open("display.html", "w+")
    displayfile.write(content)

def getRemotePath():
    ret = subprocess.check_output("git remote -v", shell=True)
    mo = re.search("[^\s]*\s*(.*)\(fetch\)", ret)
    if mo:
        return mo.group(1)
    else:
        raise Exception("fail to get remote path")


def getRawBaseUrl():
    reomteUrl = getRemotePath()
    accountname = re.search("github.com/([^/]*)", remoteUrl).group(1)
    reponame = re.search("([^/]*\.git$)", remoteUrl).group(1)
    return "https://raw.githubusercontent.com/%s/%s/master/" % (accountname, reponame)



def main():
    if not hasSetup():
        setup()
    updateGitStatus()
    newFiles = getNewFileList()
    commitAndPublish(newFiles)


if __name__ == '__main__':
    main()

