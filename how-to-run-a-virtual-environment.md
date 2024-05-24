# How to Run a Virtual Enviroment

Run `pip3 install virtualenv` to install the virtual environment package

## Creating Virtual Environment

Creation of virtual environment can be done so using the following command (Apple):

```bash
python3 -m venv /path/to/new/virtual/
```

This command creates a virtual environment directory in the designated file path. In the directory, there will a `pyvenv.cfg` file with a `home` key pointing towards the python installation it was ran from. The directory will consist of a subdirectory containing a copy of the Python binary. 

On windows the above command is synonyms to the following:

```bash
c:\>python3 -m venv c:\path\to\myenv

  OR

mkdir ProjectFolder
cd ProjectFolder
python3 -m venv env
```

The `pyvenv.cfg` file will also includes the `include-system-site-packages` key, set to `true` if `venv` is run with the `--system-site-packages` option, `false` otherwise.

The virutal environment can be deactivated using:

```bash
deactivate
```

## How venv Work

Virtual environment may be "activated" using a script in a binary directory. This will allow Python to run the environment (with installed scripts and packages) from the desired directory. The virtual environment can be activated using the following commands:

```bash
CMD		           C:\> <venv>\Scripts\activate.bat
Powershell	    PS C:\> <venv>\Scripts\Activate.ps1
Terminal (mac)	source env/bin/activate
```

An environment does not need to be specifically activated as you can just specify the full path to that environment's Python interperter when invoking Python (using `cd`). Futhermore, all scripts installed in the environment should be runnable without activating it. This is possible as all scripts installed into a virtual environment have a "shebang" line which points to the environment's Python interpreter. This means the script will run regardless of the value of PATH.

When a virtual environment is activated, the `VIRTUAL_ENV` environment variable is set to the path of the environment.

## Packages in Virtual Environment

Once the virtual environment is activated, you can see a list of packages installed using:

```bash
pip3 list
```

If it worked correctly, there should only be two installed packages - `pip` and `setuptools`. A list of all the installed packages can be made using:

```bash
pip3 freeze > requirements.txt
```

This is important as others trying to recreate my development environment will know what packages to install. All the packages can easily be installed using the following command:
	
```bash
pip3 install -r requirements.txt
```

Generally, the env folder should not be shared. Adding the env directory to .gitignore file is **highly recommended**.

## Help Command

```bash
venv [-h] [--system-site-packages] [--symlinks | --copies] [--clear]
          [--upgrade] [--without-pip] [--prompt PROMPT] [--upgrade-deps]
          ENV_DIR [ENV_DIR ...]
```

Creates virtual Python environments in one or more target directories.

```bash
positional arguments:
  ENV_DIR               A directory to create the environment in.

optional arguments:
  -h, --help            show this help message and exit
  --system-site-packages
                        Give the virtual environment access to the system
                        site-packages dir.
  --symlinks            Try to use symlinks rather than copies, when symlinks
                        are not the default for the platform.
  --copies              Try to use copies rather than symlinks, even when
                        symlinks are the default for the platform.
  --clear               Delete the contents of the environment directory if it
                        already exists, before environment creation.
  --upgrade             Upgrade the environment directory to use this version
                        of Python, assuming Python has been upgraded in-place.
  --without-pip         Skips installing or upgrading pip in the virtual
                        environment (pip is bootstrapped by default)
  --prompt PROMPT       Provides an alternative prompt prefix for this
                        environment.
  --upgrade-deps        Upgrade core dependencies: pip setuptools to the
                        latest version in PyPI
```

Once an environment has been created, you may wish to activate it, e.g. by sourcing an activate script in its bin directory.
