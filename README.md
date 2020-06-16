# Article parser

This console application allows to parse text files into a proper article files for this
[regional web-encyclopedia](http://85.234.34.14/lerm2014/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine 
for development and testing purposes. See deployment for notes on how to deploy the project 
on a live system.

Just download the project and run application.


You also need to have a folder with a text files in a proper structure
 to work with (see **Installing** section below)

### Prerequisites

A Python (version **3.8** or greater) is required to run this app

### Installing

First of all a folder with a source data should be made. All articles had to be packed into different 
folders, the name of each folder should match the title of a personal article in the encyclopedia.
```
Иванов Иван Иванович/
            text.txt
            image.jpg
```

Note that all files should be in UTF-8 encoding. Also it requires that a user has a permissions 
to create and edit files within the project directory

To run an application on Linux just ``cd`` to the **sample/**  directory and run the following command
```shell script
python3 parser.py
``` 
On Windows 
```shell script
python parser.py
``` 


## Versioning

We use [SemVer](http://semver.org/) for versioning.
 For the versions available, see the [tags on this repository](https://github.com/da070116/py_lermont/tags). 

## Authors

* **Alexander Dubrovin** - *Initial work* - [See on Github](https://github.com/da070116)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

