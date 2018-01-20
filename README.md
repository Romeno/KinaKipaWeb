### Web server of [KinaKipa](https://vk.com/kinakipa)  - all movies in belarussian in one place
### All your favorite movies!


### Install
#### Windows
`git clone https://github.com/Romeno/KinaKipaWeb.git`

`pip install -r`

`python manage.py migrate`

`loaddata.bat`

#### Linux server (pythonanywhere)
`git clone https://github.com/Romeno/KinaKipaWeb.git`

`pip3.6 install -r`

`python3.6 manage.py migrate`

`python3.6 ./manage.py loaddata initial_data.json`



install [cygwyn](https://www.cygwin.com/)

install gettext cygwin package


### Usage
`dumpdata.bat`- helper for creating fixtures - data files to populate DB with some starting data during development

`loaddata.bat` - loads all data from fixtures from `fixtures` directory in every app

`makemessages.bat` - helper uses cygwin's or else's gettext to create/populate localisation files 

`compilemessages.bat` - helper to compile message \*.po files into \*.mo files

#### SCSS compilation

When developing and making changes to look and feel of the pages inevitably you change css. 
Project uses scss as the base language so you need to compile it into css code understood by browsers. 
To do that run do the following:

##### Install 
* Ensure you have `node` installed
* `cd` to the project folder and run `npm i`. This should install all project dependencies including `gulp`, `gulp-sass` and other stiff
  * If you encounter errors when installing `gulp-sass` this is probably due to absense of Python27 on you machine. You need to install it along side with Python36.
  * Make sure the `PATH` is like you want it to be so that freshly installed Python27 wont mess things up.

##### Use
* Run `gulp` to compile scss code into css at once. 
* Run `gulp watch` and leave the console waiting to compile scss into css as you make changes into scss as you develop.  


### Structure
`KinaKipaWeb` - project name, settings, urls, etc storage

`KinaKina` - main app

`layout` - has static layout html files

`locale` - localisation files, etc

`templates` - TODO: delete


### "Production" server
Hoseted with [Pythonanywhere](http://pythonanywhere.com) and located at http://kinakipa.pythonanywhere.com

#### *Credentials for Pythonanywhere*
**login**: KinaKipa

**password**: KinaKipa001


#### *Credentials for KinaKipa admin*
**login**: KinaKipa

**password**: admin001


### Other
Some info can be found on [wiki](https://github.com/Romeno/KinaKipaWeb/wiki)
