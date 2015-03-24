# Moscargo, your Munki repo browser! #

Moscargo is a [Munki(2)](https://www.munki.org/munki/) repo browser to aid in finding the most current version of the packages you curate, and makes them available for ad-hoc download, with the version number as the download link.

![Screen Shot 2015-03-18 at 11.58.37 AM.png](https://raw.githubusercontent.com/arubdesu/Moscargo/master/static/readmeScreenshot.png)

It's written in flask, loosely wrapped in bootstrap, and inspired greatly by [Margarita](https://github.com/jessepeterson/margarita). It was thrown together by a novice ([me](http://resume.aru-b.com)) very quickly, so it may very well not work for you. However, feel free to file issues with the understanding that I may not be able to (or honestly be interested in) do(ing) much more work on this, since more full-fledged solutions like [Sal](http://salsoftware.com), [MunkiWebAdmin](https://github.com/munki/munkiwebadmin), [MunkiReport](https://github.com/munkireport/munkireport-php), and [MunkiServer](https://github.com/jnraine/munkiserver)(among others) are available and staffed by more capable devs.

###How it does what it does: 
A bootstrap html template gets filled in with info from a python script. That script checks the 'all' catalog(you can change it in the script if you'd like to limit it to a specific catalog), generates a list of dictionaries for each item it finds (except for Apple Update Metadata pkginfos, since those wouldn't have download links). It caps each description to the length of a tweet, and performs a set of checks to be able to make smart choices about icons: 
- if it's a configuration profile(new in munki as of [2.2](https://github.com/munki/munki/releases/tag/v.2.2.3)) it'll use a default image for that file type, (provided)
- if it has 'icon_name' set, it will use the designated icon
- if no 'icon_name' is set, it checks for a path in icons that has the short product name, and uses that if found
- if all else fails, it uses the (also provided_ generic 'packages.png'

It then reverse-sorts this list of dict-per-catalog-entry by the version, creates a set to throw out duplicates (leaving the highest numerical version), and sorts again by name for ease of scrolling-lookup. (I could get fancier with bootstrap widgets and toolbars, but eff it, ship it. Maybe v.3) 
## Installation
To install, first check out or otherwise grab this code. I'd recommend setting up a virtualenv (using ```easy_install pip``` and then use pip to install virtualenv) wherever you'd like on the same server running your munki repo, and install flask as per their instructions. (If you use git and or git fat to sync around your repo, setting up a new web serving instance anywhere just for this purpose may make sense, too.) In the moscargo.py file, fill in the variable for the full path to the munki repo, and override the 'all' catalog if you'd like. ```cd``` into the included static folder and make symlinks pointing to your icons and packages folders. Optionally, modify the last line of moscargo.py as appropriate to meet your desired setup, if you want to limit to a specific IP for instance - see the flask docs for more info. 

Test by first activating the virtualenv and running the moscargo.py file directly and navigate to http://localhost:5000. For better performance(you could be serving hundreds of megs on top of the regular munki repo load) and ease of 'prod' deployment, you may also want to use pip to install mod_wsgi, which is the simplest way I've found to get this running in Apache on a Mac with the included mos.wsgi script, it also leaves any pre-existing Apache config as-is. If all seems good, run the mod_wsgi-express script, preferably as a restricted service user and make sure that works as well, which would move it to port 8000 by default. (A launchd plist or other pleaserun method of init'ing the webservice is left as an exercise for you, see the Margarita and MunkiWebAdmin docs for some hints.)

Sorry that this probably isn't the friendliest setup ever, but even if you're not familiar with python and web apps, I'm sure you'll learn a lot if you tried giving this a go. (Heck, some enterprising individual may even go ahead and throw this in a Docker container for ease of tinkering, who knows?)
Just remember, as the saying goes, if you break your system YOU get to keep the pieces.
