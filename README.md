# SSW 533 Term Project

The goal of this project is to analyze a couple of existing open source projects to understand how the project complexity has evolved over time. 

## Getting Started

The two tools that are currently being used in the script are:
'''
lizard - https://github.com/terryyin/lizard
pmccabe - https://people.debian.org/~bame/pmccabe/overview.html
'''

### Prerequisites

The scripts have been developed to run in a bash envronment. If using a Windows machine suggest running in a virtual machine.

```
git
pmccabe
lizzard
current python 3 distribution - https://python.org
numpy python library - https://numpy.org
matplotlib python library - https://matplotlib.org
```

### Installing

There is no install required for these scripts if the prerequisites are met. Please follow the links above for the analysis tools. It is suggested to obtain the python distribution and packages through the os package manager (apt-get - Ubuntu)

## Running the scripts 

./generate_data.sh repo_source/example_repo.git

### Break down of what is generated

For each commit in the repo mainline history text files are created with the results of the pmccabe tools and lizard tools. A text file is also created to display the number of files that changed between the commits. 

TODO - Update what post processing does. 

## Contributing
 

## Authors

Jacob Christensen
Matt Fuhrmann

## License


## Acknowledgments
