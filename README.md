# Title

## Presentation
What Am i doing???
## Demonstration

[Watch the demonstration](demonstrations/demo.mp4)
## Installation

```bash
git clone <repository-url>

cd <project-folder>


python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Project structure

main.py            Entry point
solver.py          RK4 integrator
polynomial.py      Polynomial utilities
visualization.py   Plotting

## Example

Input polynomial

P(z)=z^5-z^2

The program computes

## Future work

- Faster integration
- Better GUI
- Export animations