<p align="center">
    <img alt="Mussel-Python" title="Mussel-Python" src="docs/images/banner_light.png#gh-dark-mode-only" width="450">
    <img alt="Mussel-Python" title="Mussel-Python" src="docs/images/banner.png#gh-light-mode-only" width="450">
</p>
<div align="center">
  <b><i>Python for any environment</i></b>
<hr>

</div>

# Overview

Mussel Python is a versatile tool designed to streamline the process of creating standalone 
Python applications with **pyinstaller** within a standardized environment.

# Features

* **Isolated Build Environment:** Utilize Docker to build standalone Python application (with its dependencies), ensuring a consistent and isolated build environment.

* **Dependency Management:** Easily manage Python package dependencies and versions within your mussel app, avoiding conflicts and ensuring reproducibility.

* **Build Automation:** Streamline the build process, making it easy to share and deploy your Python applications.

* **Portability:** Python application built with mussel-python runs consistently across different operating systems and environments.

# Installation

Install mussel using pip:
```shell
pip install mussel
```

## Expected Binary Compatibility

This section describe compatibility of your python executable after mussel's build.

### Linux

Compatibles Linux distributions : 
* Any distro with GLIBC >= 2.14
  * Ubuntu 14.04 or higher
  * Debian 8 or higher
  * Fedora 20 or higher
  * And many more ...

|                          Command |       Bundled Python*        |
|---------------------------------:|:----------------------------:|
|  `mussel --python 3.8 [OPTIONS]` | 3.8.18 (With OpenSSL 3.1.3)  |
|  `mussel --python 3.9 [OPTIONS]` | 3.9.13 (With OpenSSL 3.1.3)  |
| `mussel --python 3.10 [OPTIONS]` | 3.10.12 (With OpenSSL 3.1.3) |
| `mussel --python 3.11 [OPTIONS]` | 3.11.5 (With OpenSSL 3.1.3)  |

(*) **Bundled Python**: Python distributed inside mussel (pyinstaller) bundled application.

### Windows

|                          Command |        Bundled Python*        | Compatiblity        |
|---------------------------------:|:-----------------------------:|---------------------|
|  `mussel --python 3.8 [OPTIONS]` | 3.8.10 (With OpenSSL 1.1.1n)  | Windows 7 or higher |
|  `mussel --python 3.9 [OPTIONS]` | 3.9.13 (With OpenSSL 1.1.1n)  | Windows 8 or higher |
| `mussel --python 3.10 [OPTIONS]` | 3.10.11 (With OpenSSL 1.1.1n) | Windows 8 or higher |
| `mussel --python 3.11 [OPTIONS]` | 3.11.5 (With OpenSSL 1.1.1n)  | Windows 8 or higher |

### Compatiblity example

Building your application with `mussel --python 3.11` will produce:
* An application running on Python 3.11.5 on Windows & Linux
* Compatible with:
  * Ubuntu 14.04 or higher
  * Windows 8 or higher

# Getting Started

## Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

* Docker ([Install Docker Engine](https://docs.docker.com/engine/install/))
* `mussel`

## Write your first mussel standalone app

### 1. Define your Python application code

Script above will print Python & OpenSSL version

```python
import sys
import ssl

if __name__ == '__main__':
    print("Python", sys.version)
    print(ssl.OPENSSL_VERSION)
```

### 2. Build your standalone app with mussel-python

**Usage**
```shell
mussel --python <VERSION> (--source PATH) [pyinstaller options]
```

For detailed information on pyinstaller options, please reach https://pyinstaller.org/en/stable/usage.html#options

Example below will build a single file standalone executable (`-F`) from a python script `my-app.py`
```bash
$ mussel --python 3.10 -F my-app.py
```

### 3. Run your standalone executable

Executable files are by default created within a `dist` directory.

```shell
$ ./dist/my-app
Python 3.10.12 (main, Sep 29 2023, 07:32:58) [GCC 4.8.4]
OpenSSL 3.1.3 19 Sep 2023

# Try with ubuntu:14.04 container
$ docker run --rm -v ./dist/my-app:/my-app ubuntu:14.04 /my-app
Python 3.10.12 (main, Sep 29 2023, 07:32:58) [GCC 4.8.4]
OpenSSL 3.1.3 19 Sep 2023

# Try with more recent distro... ubuntu:22.04
$ docker run --rm -v ./dist/my-app:/my-app ubuntu:22.04 /my-app
Python 3.10.12 (main, Sep 29 2023, 07:32:58) [GCC 4.8.4]
OpenSSL 3.1.3 19 Sep 2023

# Fedora 40 ?
$ docker run --rm -v ./dist/my-app:/my-app fedora:40 /my-app
Python 3.10.12 (main, Sep 29 2023, 07:32:58) [GCC 4.8.4]
OpenSSL 3.1.3 19 Sep 2023

# alpine ?
$ docker run --rm -v ./dist/my-app:/my-app alpine:latest sh -c "apk add libc6-compat gcompat ; ./my-app"
...
OK: 8 MiB in 19 packages
Python 3.10.12 (main, Sep 29 2023, 07:32:58) [GCC 4.8.4]
OpenSSL 3.1.3 19 Sep 2023

# Windows ?
\> .\dist\my-app.exe
Python 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v1929 64 bit (AMD64)]
OpenSSL 1.1.1n  15 Mar 2022
```

# License

This project is licensed under the MIT License.

# Acknowledgments

* Inspired by the need for standalone & environment agnostic Python application.
* Built with [Docker](https://www.docker.com/) and [pysintaller](https://pyinstaller.org/en/stable/index.html).

# Contact

For questions or feedback, please contact [contact@tmahe.dev](mailto:contact@tmahe.dev).

Happy coding!