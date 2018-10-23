# AutoMovieConverter

This Project search and converts movies files on your filesystem.
The settings converts each movie file into .mkv with x264 and mp3.
Its also double check if the file is converted correctly.
With an option your are able to delete the orign file.

for mor information visit LPL-mind.de.

## Prerequisites
```
apt-get install FFMpeg python
```

## Installing

Clone the Git repository and runf teh file

```
git clone https://github.com/lukaspupkalipinski/AutoMovieConverter
```

Please run the following comands, if you wish to install this too on your system.
This will execute the srcipt on each startup. The script will continue the task.

```
cd AutoMovieConverter
mv AutoMovieConverter.py /usr/share/automovieconverter/automovieconverter.py
mv automovieconverter /etc/init.d/automovieconverter
update-rc.d automovieconverter defaults
update-rc.d automovieconverter enable
```

make sure you change the folder path to your file system in /etc/init.d/automovieconverter

```
DAEMON_ARGS="/usr/share/automovieconverter/automovieconverter.py <your-folder-path> R"
```

## Get started

```
python automovieconverter.py -h
```

## Versioning

We use SemVer for versioning. For the versions available, see the tags on this repository.
## Authors

    Lukas Pupka-Lipinski

