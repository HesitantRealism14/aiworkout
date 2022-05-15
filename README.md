# Project description
- Description: A computer vision web app I collaborated on that characterizes and provides feedback on workout images according to pose correctness
- Website link: https://aiworkoutassistant.herokuapp.com/

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
aiworkout-run
```
