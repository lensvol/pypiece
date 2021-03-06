pypiece
=======

Wrapper around pip for use with flaky connections.

Basic idea behind it is that default behaviour of `pip` to download all packages at once
and compile them can get pretty frustrating in situations, where single error in 
downloading or installing a package can result in repeating whole process all
over again.

`pypiece` tries to get around that by trying to download and install each package
separately, by calling `pip` for each line of requirements.txt. In the end it
outputs list of successfully installed packages and ones that failed.

Usage
-----

    pypiece < requirements file > < -- PIP options >

Available options:
  
 - `--pip` - specify pip binary to use
 -  `--retries <N>` - try to reinstall failing package _N_ times (default: 3).
 -  `--venv <name>` - install to virtualenvwrapper created virtual environment _name_.

pip arguments
-------------
If `--` is found in command line, then all arguments
after it will be passed unchanged to `pip` executable on every call.

For example: 

    pypiece requirements.txt -- -i https://my.pypi.repo

Last line is equivalent to: 

    pip install -r requirements.txt -i https://my.pypi.repo

Examples
--------

Try to install every package found in _requirements.txt_ one by one:

    pypiece requirements.txt

Install requirements using `pip` from virtualenv _test_:

    pypiece --venv test requirements.txt

Install requirements using specified `pip` binary:

    pypiece --pip my_env/bin/pip requirements.txt

Feedback
--------

Send your bug reports and suggestions to [lensvol@gmail.com][1]


  [1]: mailto:lensvol@gmail.com
