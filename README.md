# HoI IV statistics

## Installation

I recommend you to install a Python environment with conda, virtualenv or pipenv.

##### Conda
For example with conda, 
[download and install miniconda](https://docs.conda.io/en/latest/miniconda.html)

Create a conda environment
```
conda create -n hoi_stats python=3.6
```

Activate the conda environment
```
activate hoi_stats
```

Install dependencies
```
conda install pandas==0.20.3
conda install pillow==4.2.1
```

## Usage

#### Gather data

* Copy-paste the content of the `mod` directory into your Hearts of Iron IV mod directory
(something like `Documents\Paradox Interactive\Hearts of Iron IV\mod`).
* Activate the mod `Statistics` in the game launcher
* Play
* After playing, do a copy of the `game.log` file which is in the `logs` directory 
(something like `Documents\Paradox Interactive\Hearts of Iron IV\logs`).
**If you don't do that you will lose your statistics at the next game!**

#### Extract and transform data

Run the Python script game_log_to_csv.

```
python src/game_log_to_csv.py <...>\Documents\Paradox Interactive\Hearts of Iron IV\logs\game.log <...>\Documents\raw.csv <...>\Documents\ 
```

Some csv files have been created in the `Documents` directory.
## Tests

Go to the tests directory and run unittest
```
cd tests
python -m unittest discover
```

## License

The project has an [MIT license](Licence.md).
