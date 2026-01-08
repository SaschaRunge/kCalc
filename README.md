# __kcalTracker__
A tracker and calculator for daily caloric intake and intake requirements depending on weight loss/gain goals

## Dependencies
PyYAML: https://pyyaml.org/wiki/PyYAMLDocumentation

## Usage:

### Installation

I'd recommend installing uv, this will handle the dependencies: https://docs.astral.sh/uv/getting-started/installation/
Or run the source directly via python (v3.12). You'll have to have PyYAML installed.

### Data

You can supply your data by placing a input.csv file within ./data/input/. It needs to contain a column of the following datapoints, each of equal length, with the header information date, weight, kcal. For example:

```
date,kcal,weight
2025-04-09,1039,"97,7"
2025-04-10,2528,"96,4"
2025-04-11,3157,"96,4"
2025-04-12,2000,"96,4"
```

Date should probably follow this format, but can be in any format supported by datetime.fromisoformat(). kcal is best kept as integer values without thousands-delimiter.
weight does support comma seperation if in quotes, or you can use the usual decimal notation, e.g. 95.5

If you don't have any data archived you can do so within the program as follows.

### Commands

The CLI currently supports the following commands:

q, quit: Exits the program.
a, add: Adds a datapoint at date. Usage: a (date) (kcal) (weight). Does not support missing values. Example: a 2026-01-08 2000 80
r, remove: Removes at date. Usage: r (date). Example r 2026-01-08
s, show: Shows currently stored values.
re, read: Manually reads from input.
w, write: Writes currently stored values to saved.csv.

### Other

On startup, will show your current weight, your estimated weekly weightloss based on calculation_interval_days specified in config.yaml (defaults to 21/3 weeks).
TDEE will show your maintenance weight based on simple-linear-least-squares over your recorded weights within that intervall, the value within the brackets are an adjusted estimate
based on your weight loss/gain goals specified in config.yaml.

Based on my experience take those values with a grain of salt, as they are theoretical values and can, even over large timespans, fluctuate wildly. In general, consistency is important and you'll likely see results if you follow these numbers daily, since these are kind of self regulatiing (TDEE will drop when you lose less weight than expected). If that
still does not work, increase the goal specified in the config. If that still does not work you are likely tracking your calories wrong.

Usually 500 kcal above or below maintenance is a good value to start at. If you are struggeling with your weight, don't. You got this =).

