# rand-useragent

An up-to-date simple random user-agent with real world database. 
The collections of user-agent data is pre-downloaded from [techblog.willshouse.com](https://techblog.willshouse.com/2012/01/03/most-common-user-agents/).


## Installation

```shell
$ pip3 install rand-useragent
```

## Usage

Simple usage example, see below for more examples:


```python
from rand_useragent import randua

# Get a random browser user-agent string
print(randua())
```

---

If you want to specify your own browser list, you can do that via the `browsers` 
argument (default is: `["chrome", "edge", "firefox", "safari"]`).  
This example will only return random useragents from Edge and Chrome:

```python
from rand_useragent import randua

# Get a random browser user-agent string
print(randua(browsers=["edge", "chrome"]))
```

---

If you want to specify your own operating systems, 
you can do that via the `os` argument (default is: `["windows", "mac os x", "linux"]`).  
In this example you will only get Linux useragents back:

```python
from rand_useragent import randua

# Get a random browser user-agent string
print(randua(os=["linux"]))
```

---

If you want to return more popular useragent strings, you can play with the `min_percent` 
argument (default is: `0.0`, meaning all useragents will match).  
In this example you get only useragents that have a minimum usage percentage of 10.0% (or higher):

```python
from rand_useragent import randua

# Get a random browser user-agent string
print(randua(min_percent=10.0))
```

---

You can override the fallback string using the `fallback` parameter, in very rare cases something failed:

```python
from rand_useragent import randua

# If something went wrong
print(randua(fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"))
```

## Development

Since GitHub Actions is unable to reach willshouse.com and has Cloudflare protection. 
We can run the script below to automatically scrape the user-agent strings from the external data source. 
The script will copy the [JSONlines](https://jsonlines.org/) file to the `rand_useragent/data` directory. Execute:

```sh
./scripts/update-data.sh
```

The data JSON file is part of the Python package, see [pyproject.toml](pyproject.toml). Read more about [Data files support](https://setuptools.pypa.io/en/latest/userguide/datafiles.html).

---

<!-- [![license](https://img.shields.io/github/license/Neoteroi/blacksheep.svg)](https://github.com/redbugg/random-useragent/blob/main/LICENSE) -->
<p align="center"><i>rand-useragent is a <a href="https://github.com/encode/httpx/blob/master/LICENSE.md">BSD licensed</a> code.</i></p>