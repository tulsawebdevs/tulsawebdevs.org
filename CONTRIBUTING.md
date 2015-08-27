# Contributing


Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/tulsawebdevs/tulsawebdevs.org/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "[bug](https://github.com/tulsawebdevs/tulsawebdevs.org/labels/bug)"
is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "[feature](https://github.com/tulsawebdevs/tulsawebdevs.org/labels/feature)"
is open to whoever wants to implement it.

### Write Documentation

tulsawebdevs.org could always use more documentation, whether as
part of the official Tulsa Web Devs docs, in docstrings, or
even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/tulsawebdevs/tulsawebdevs.org/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up tulsawebdevs.org
for local development.

There are two options, via docker or a local install. For both you'll need to fork and clone the repository. You'll be committing any changes to a branch on your fork and submitting pull requests when your feature or bug fix is done.

1. Fork the `tulsawebdevs.org` repo on GitHub.
2. Clone your fork locally:

   ```bash
   $ git clone git@github.com:your_name_here/tulsawebdevs.org.git
   ```

### Via Docker Compose (OSX only)

1. Install the docker toolbox: https://www.docker.com/toolbox
2. Run the Docker init APP `Applications/Docker/QuickStart Terminal.app`
3. Take note of the IP address the VM is running under
4. Download and install images/containers, run in daemon mode

   ```bash
   $ docker-compose up -d
   $ docker-compose run web python manage.py createsuperuser
   ```
   
5. Enter the information you would like to use for your superuser
6. Visit `<vm ip>:8000/admin/` in your browser, confirm you can login

### Locally

1. Install your local copy into a virtualenv. Assuming you have
   virtualenvwrapper installed, this is how you set up your fork for local
   development:

   ```bash
   $ mkvirtualenv tulsawebdevs.org
   $ cd tulsawebdevs.org/
   $ pip install -r requirements/local.txt
   $ ./manage.py syncdb
   ```
2. Run the server
   ```bash
   $ ./manage.py runserver_plus
   ```
   You should see some output letting you know the location of the server and info about the django install.
   
   ```bash
   Django version 1.8.4, using settings 'config'
   Development server is running at http://127.0.0.1:8000/
   Using the Werkzeug debugger (http://werkzeug.pocoo.org/)
   Quit the server with CONTROL-C.
   Validating models...
   System check identified no issues (0 silenced).
   ```
   
3. Visit the server url to check that everything is running correctly

## Making a change, fixing bugs or adding features

2. Create a branch for local development:

   ```bash
   $ git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

3. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

   ```bash
   $ make qa-all
   ```

6. Commit your changes and push your branch to GitHub:

   ```bash
   $ git add .
   $ git commit -m "Your detailed description of your changes."
   $ git push origin name-of-your-bugfix-or-feature
   ```

7. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.3, and 3.4, and for PyPy. Check
   https://travis-ci.org/tulsawebdevs/tulsawebdevs.org/pull_requests
   and make sure that the tests pass for all supported Python versions.

## Tips

To run a subset of tests:
```bash
$ ./manage.py test events/tests/test_serializers.py
```

To mark failed tests:
```bash
$ ./manage.py test --failed
```

To re-run only the failed tests:
```bash
$ ./manage.py test --failed
```
