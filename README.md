### Web server of [KinaKipa](https://vk.com/kinakipa)  - all movies in belarussian in one place
### All your favorite movies!


#### Install
`git clone https://github.com/Romeno/KinaKipaWeb.git`

`pip install -r`

install [cygwyn](https://www.cygwin.com/)

install gettext cygwin package


#### Usage
`dumpdata.bat`- helper for creating fixtures - data files to populate DB with some starting data during development

`loaddata.bat` - loads all data from fixtures from `fixtures` directory in every app

`makemessages.bat` - helper uses cygwin's or else's gettext to create/populate localisation files 

`compilemessages.bat` - helper to compile message \*.po files into \*.mo files


#### Structure
`KinaKipaWeb` - project name, settings, urls, etc storage

`KinaKina` - main app

`layout` - has static layout html files

`locale` - localisation files, etc

`templates` - TODO: delete


#### "Production" server
Hoseted with [Pythonanywhere](http://pythonanywhere.com) and located at http://kinakipa.pythonanywhere.com

##### Credentials for Pythonanywhere
**login**: KinaKipa

**password**: KinaKipa001


#### Credentials for KinaKipa admin
**login**: KinaKipa

**password**: admin001


#### Other
Some info can be found on [wiki](https://github.com/Romeno/KinaKipaWeb/wiki)
