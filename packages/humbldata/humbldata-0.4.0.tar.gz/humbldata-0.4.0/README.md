<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">humbldata</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![GitHub Issues](https://img.shields.io/github/issues/jjfantini/humbldata.svg)](https://github.com/jjfantini/humbldata/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/jjfantini/humbldata.svg)](https://github.com/jjfantini/humbldata/pulls)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
  ![License](https://img.shields.io/badge/License-Proprietary-black)
</div>

---

<p align="center"> This package connects the <b>humblfinance</b> project to its data sources and data analytics functions.
</p>
       
## 📝 __Table of Contents__

- [About](#about)
- [Features](#features)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 __About__ <a name = "about"></a>

Write about 1-2 paragraphs describing the purpose of your project.

## __Features__ <a name = "features"></a>

- _ORATS data collection_
- _volatility analysis_
- _rescaled-range analysis_
- _strategy backtest performance_

## 🏁 __Getting Started__ <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

- Conda (miniconda3/anaconda) - env management
- Poetry - package management



### __Installing Package__

When I upload to pip:

```bash
pip install humbldata
```

Current install method:

```bash
pip install git+https://github.com/jjfantini/humbldata.git
```

<details>
<summary><b>Development: Setup Conda Environment (w/Poetry)</b></summary>
<p>

This project uses a conda environment. I have done this to be able to use openbb
package easily. I have followed the instructions on the 
[openbb](https://docs.openbb.co/terminal/installation/pypi) website.

1. I created the environment with a `--prefix` and not a name, to ensure that it installed in my project directory, not the default path. This is executed in the project root dir.

    ```bash
    conda env create --prefix ./obb  --file https://raw.githubusercontent.com/OpenBB-finance/OpenBBTerminal/main/build/conda/conda-3-10-env.yaml
    ```

 2. I didn't want the full path to be displayed when using this env so I changed my `.condarc` file to show the env name as the last directory where the env is located.

    ```bash
    conda config --set env_prompt '({name})'
    ```
 3. Activate the environment

    ```bash
    conda activate ./obb
    ```
 4. Check if poetry is installed

    ```bash
    poetry --version
    # Install with `pip install poetry --upgrade`
    ```
 5. Install Packages from `poetry.lock`

    ```bash
    poetry install
    ```
 6. If you get an error: 
    ```
    EnvCommandError
    
    Command ['c:\\Users\\<user>\\<path>\\obb\\python.exe', '-m', 'pip', 'uninstall', 'charset-normalizer', '-y'] errored with the following return code 2
    ```
    Then run:
    ```
    pip install charset-normalizer --upgrade
    ```
    and re-run!
    ```bash
    poetry install
    ```

</p>
</details>
<details>
<summary><b>Development: Setup Conda Environment (w/o Poetry)</b></summary>
<p>

  If you do not use `poetry` for some weird reason, I keep the updated environment specs in an `environment.yml` and `requirements.txt`file in the root of the project.

  I use keep the env. specs up to date. This is packaged in a file `update_reqs.py`

  ```bash
  conda env export | python -c "import sys; print(''.join(line for line in sys.stdin if 'prefix: ' not in line))" > environment.yml
  # This cmd removes the 'prefix:' line to be platform independent.
  conda list  --export > requirements.txt
  ```

  ### __Setup Conda Env (w/ requirements)__

  This method will be installing dependencies from `requirements.txt || environment.yml`

  ### __Steps__

  There are two methods to recreating the environment:

  * Using requirements.txt

      ```bash
      conda create --name obb --file requirements.txt
      ```

  * Using environment.yml (has my path prefix-check the file to change path prefix)

      ```bash
      conda env create -f environment.yml
      ```
</p>
</details>

## 🔧 Running the tests <a name = "tests"></a>

Explain how to run the automated tests for this system.

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## 🎈 Usage <a name="usage"></a>

Add notes about how to use the system.

## 🚀 Deployment <a name = "deployment"></a>

Add additional notes about how to deploy this on a live system.

## ⛏️ Built Using <a name = "built_using"></a>

- [OpenBB](https://www.openbb.co/) - Data Source
- [PostgreSQL](https://postgresql.com/) - Database
- [Python](https://python.org/) - Programming Language

## ✍️ Authors <a name = "authors"></a>

- [@jjfantini](https://github.com/jjfantini) - Idea & Initial work

See also the list of [contributors](https://github.com/jjfantini/humbldata/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References
