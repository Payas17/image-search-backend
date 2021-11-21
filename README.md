# image-search-backend

## Instalation

### Virtualenv

Create virtual environment:

```
python3 -m venv <virtual_environment_name>
```

### Install dependencies

First open your virtualenv
```
source <virtual_environment_name>/bin/activate
```

Then
```angular2html
pip install -r requirements.txt
```

You'll need to install yolov5 requirements so

```angular2html
pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
```

## Troubleshooting

### Installing OpenCV fails because it cannot find "skbuild"

Try upgrading pip
```angular2html
pip install --upgrade pip
```