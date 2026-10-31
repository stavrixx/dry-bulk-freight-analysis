Does iron ore explain dry bulk freight rates?

I did a shipbroking internship at Hellaschart in July 2026 and kept hearing that dry bulk rates basically follow commodity demand, especially iron ore. I wanted to see if that actually shows up in the data, so I compared the Baltic Dry Index (BDI) with the iron ore price from 2010 to 2026.

What I found
In levels the two look related (correlation of about 0.52 on the logs), but a lot of that is probably just both of them going up and down with the same big cycles (2015-16 low, 2020-21 spike).
Looking at monthly % changes instead, the correlation is basically 0 (0.02) and R-squared is 0.00. So month to month, iron ore doesn't explain the BDI.
The only thing that showed up was a small correlation of 0.19 when iron ore leads the BDI by 2 months. I tested lags from 0 to 6 months and picked the best one, so this could easily be luck. I wouldn't say it's a real result.
The relationship also isn't stable. The correlation of changes goes from -0.08 (2010-14) to 0.09 (2015-19), 0.09 (2020-22) and -0.20 (2023-26).
Why I think it's so weak
The BDI is only about 40% Capesize, and Capesize is the part that carries iron ore. Panamax and Supramax carry things like coal and grain.
Freight depends on how much gets shipped and on supply (fleet size, port congestion), not just on the price of the cargo.
I used monthly averages, which smooths out a lot.
Data
data/iron_ore.csv: IMF global iron ore price (USD per tonne, monthly), from FRED (series PIORECRUSDM).
BDI: daily history from Investing.com. I didn't upload it because the BDI belongs to the Baltic Exchange. If you want to run the code, download it from Investing.com (Historical Data, Aug 2010 to now) and save it as data/bdi.csv.
How to run
pip install pandas numpy matplotlib
python analysis.py

Results are saved in output/ (results.txt and two charts).

Things I'd do next
Use Capesize rates only, since that's the iron ore segment
Add iron ore import volumes or Chinese steel output instead of just the price
Try quarterly changes instead of monthly
