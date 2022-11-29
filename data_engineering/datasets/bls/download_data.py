import mechanize
from time import sleep
#Make a Browser (think of this as chrome or firefox etc)
br = mechanize.Browser()

#visit http://stockrt.github.com/p/emulating-a-browser-in-python-with-mechanize/
#for more ways to set up your br browser object e.g. so it look like mozilla
#and if you need to fill out forms with passwords.

# Open your site
br.open('https://www.bls.gov/lau/#tables')

f=open("source.html","wb")
f.write(br.response().read()) #can be helpful for debugging maybe

filetypes=[".xlsx",".txt",".csv"] #you will need to do some kind of pattern matching on your files
myfiles=[]
for l in br.links(): #you can also iterate through br.forms() to print forms on the page!
    for t in filetypes:
        if t in str(l): #check if this link has the file extension we want (you may choose to use reg expressions or something)
            #print(l)
            myfiles.append(l)


def downloadlink(l):
    filename=l.url.split("/")[len(l.url.split("/"))-1]
    print(filename)
    f=open(filename,"wb") #perhaps you should open in a better way & ensure that file doesn't already exist.
    br.click_link(l)
    f.write(br.response().read())
    print(filename," has been downloaded")
    #br.back()

for l in myfiles:
    sleep(1) #throttle so you dont hammer the site
    downloadlink(l)
