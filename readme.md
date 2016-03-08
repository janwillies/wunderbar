# readme
reads wunderbar temperature from [relayr](https://developer.relayr.io/) mqtt broker and plots on [plot.ly](https://plot.ly)

## cloud access
### tokens
get tokens at
  - [https://plot.ly/settings/api](https://plot.ly/settings/api)
  - [https://developer.relayr.io/dashboard/devices/](https://developer.relayr.io/dashboard/devices/)

and edit  `config.yml`
## docker
```
$ cp config-dist.yml config.yml
$ vim config.yml
$ docker run -it -v $(pwd)/config.yml:/config.yml willies/wunderbar:latest
```
## dev environment
### virtualenv
use `virtualenv rvenv` (python2) or `pyvenv rvenv` to setup virtualenv and `source rvenv/bin/activate` to activate

### config.yml support

```
pip install pyyaml
```
example `config.yml`:
```
---
# how often to update plot.ly in seconds
update_intervall: 60

relayr:
  token: YOUR_TOKEN
  deviceid: TEMPERATURE_SENSOR_DEVICE_ID

plotly:
  user: YOUR_USERNAME
  apikey: YOUR_APIKEY
  stream_ids:
    - asfj8jfadf
    - asdfasdfkl
    - werwerwerw
    - sdfsdfdsfs
```
### relayr

```
pip install relayr
pip install certifi
```

`rvenv/lib/python3.5/site-packages/relayr/dataconnection.py` needs to be patched, see `relayr_ssl.patch` and `relayr_python3.patch`

### plot.ly

```
pip install plotly
```

## execute

```
(rvenv) ➜  wunderbar git:(master) ✗ python temperature.py
https://plot.ly/~jcw/27
2016-03-06 23:03:56: 21.42
2016-03-06 23:04:58: 21.42
2016-03-06 23:05:58: 21.52
[...]
```

and visit the [plot.ly dashboard](https://plot.ly/organize/home)
