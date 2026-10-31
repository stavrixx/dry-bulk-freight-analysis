# What drives dry bulk freight rates? Baltic Dry Index vs. iron ore

**Question:** how much of the movement in dry bulk freight rates (BDI) does the iron ore price explain, and does iron ore lead freight?

## Run it
1. `pip install pandas numpy matplotlib`
2. Download BDI daily history as a CSV from a free source (Investing.com "Baltic Dry Index historical data", or Trading Economics) and save it as `data/bdi.csv`. It needs a date column and a price/close column.
3. `python analysis.py` (iron ore is pulled from FRED, series PIORECRUSDM; if you are offline, save it as `data/iron_ore.csv` with columns date, value).
4. Results appear in `output/results.txt`, charts in `output/levels.png` and `output/scatter.png`.

## Method (one paragraph for your write-up)
BDI daily data is averaged to monthly and merged with the monthly IMF iron ore price (2010 onward). Because both series trend and move in cycles, a regression on levels can look strong without meaning anything (spurious regression), so the main test uses monthly log changes. I also test whether iron ore leads the BDI by 0-6 months and whether the relationship is stable across sub-periods.

## Limits to state honestly
- The BDI is a composite of Capesize, Panamax and Supramax rates, and Capesize (about 40% weight) is the iron ore segment, so the relationship should be strongest there. Say what a Capesize-only series would add.
- Iron ore is one demand driver among several: coal, grains, fleet supply growth, port congestion and bunker costs also matter.
- Monthly averaging smooths short-term spikes; correlation is not causation.

## Note structure (2 pages)
1. The question and why it matters (3 sentences, link to chartering decisions)
2. Data and method (1 paragraph above)
3. Findings: levels vs. changes correlation, R-squared, best lag, stability by period. Only quote numbers from your own `results.txt`.
4. What explains the rest (supply side: fleet growth, congestion; other cargoes)
5. Limits, and what you'd do next (Capesize-only rates, add China steel output)
