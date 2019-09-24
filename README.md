
# General info
**List containers:**
sudo docker ps -a

**Build container**
sudo docker build --no-cache . -t agender

**Run container**
sudo docker run -it --rm -p 8080:8080 agender

**If you need login in bash**
docker run -it --rm -p 8080:8080 agender /bin/sh

**Usage**
python server.py default port is 8080

Send a post in url http://localhost:8080/upload with file name **file** with a image file.

response example:
```
[ 
	{'left': 137, 'top': 304, 'right': 284, 'bottom': 451, 'width': 147, 'height': 147, 'gender': 0.4472983, 'age': 39.02036403665261},
	{'left': 36, 'top': 80, 'right': 405, 'bottom': 449, 'width': 369, 'height': 369, 'gender': 0.03139727, 'age': 24.240266015814086}
]
```

**if gender > 0.5 is female**
