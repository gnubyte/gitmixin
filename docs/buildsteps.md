# Development

For further development of the gitmixin project, an issue can be opened on Github or a new feature requested there. Additionally [a roadmap is present on github too](https://github.com/gnubyte/gitmixin/projects/1).


## Building the PIP package by hand

### On MacOS/Unix

First generate the distribution packages 
`python3 -m pip install --upgrade build`


Then generate the tar and wheel files required for the source archive and built distribution.
`python3 -m build`


### Uploading the distribution archives

#### On MacOS/Unix

Install Twine, a tool we will use to upload to Pip
`python3 -m pip install --upgrade twine`


Upload the dist package
`twine upload dist/*`