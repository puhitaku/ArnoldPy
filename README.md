PynoldC
=======
*An ArnoldC translator / executor written in Python3*

The purpose of this repo is just to build an implementation of ArnoldC in Python3.

It's not completed to develop and I'm a beginner of Python so please feel free to issue problems or to send me pull requests.

### Progress of this project

- Translator ... *WIP*

Implementation tasks     | Status
-------------------------|-------
Expression interpretation|Done!
Abstract syntax model    |Done!
Concrete syntax model    |Done!
Ops/Args analyzer        |Done!
Deal with variables      |Done!
Deal with loops          |Done!
Input integer            |WIP
Method declaration       |WIP
Method call              |Not yet

- Real-time interpreter ... Discontinued

I used to think of an INTERPRETER of ArnoldC but I thought it'll take too many hours to implement this while this language is just a joke.

### Usage

`python ./main.py file_to_run.arnoldc`

e.g. `python ./main.py 10.arnoldc`

### Method

