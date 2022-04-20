# Roman numeral date and clock

<img align="right" src="www/RomanClockEx.png" alt="Roman Calendar/Clock" width="300" style="margin-top: 20px">

R code to produce a simple date and clock plot in Roman numerals (Gregorian) and Latin (Roman calendar). Works on a 24-hour system. Clock plot based on a modified version of <code>caroline::<a href="https://search.r-project.org/CRAN/refmans/caroline/html/plotClock.html">plotClock</a></code>.

## Set-up
1. Install the following libraries in R:
- <code><a href="https://cran.r-project.org/web/packages/caroline/index.html">caroline</a></code>
- <code><a href="https://lubridate.tidyverse.org/">lubridate</a></code>

You can do this easily with the following command:
> <code>install.packages(c("caroline", "lubridate"))</code>

2. Run the script <code>RomanDateClock.R</code> in R, then you're ready to plot a real-time date and clock in Roman numerals & Latin. 

- Note that there is no zero in Roman numerals (apparently, the Romans had no need for it). I've therefore just incuded '00' when the hour or minute = zero in the 24-hour clock.
- Top date is the Gregorian date in Roman numeral format (DD.MM.YYYY).
- Also provided is the Roman calendar date in in Latin. Briefly, the date format follows these rules:
    - there are seven days in the week as in the modern week (but in Latin — <em>Dies Lvnae</em>, <em>Dies Martis</em>, <em>Dies Mercvris</em>, <em>Dies Iovis</em>, <em>Dies Veneris</em>, <em>Dies Satvrni</em>, <em>Dies Solis</em>)
    - months are the same as modern months (but in Latin — <em>Ianvarivs</em>, <em>Febrvarivs</em>, <em>Martivs</em>, <em>Aprilis</em>, <em>Maivs</em>, <em>Ivnivs</em>, <em>Ivlivs</em>, <em>Avgvstvs</em>, <em>September</em>, <em>October</em>, <em>November</em>, <em>December</em>)
    - the 1<sup>st</sup> of every month is a <a href="https://www.wordsense.eu/calends/"><strong><em>Kalends</em></strong></a>
    - the 13<sup>th</sup> (Jan, Feb, Apr, Jun, Aug, Sep, Nov, Dec) or the 15<sup>th</sup> (Mar, May, Jul, Oct) are the <a href="https://www.wordsense.eu/ides/"><strong><em>Ides</em></strong></a>
    - the <a href="https://www.wordsense.eu/nones/"><strong><em>Nones</em></strong></a> are 8 days prior to the <strong><em>Ides</em></strong>
    - All other days work backward from the next 'special day' (i.e., <em>Kalends</em>, <em>Nones</em>, or <em>Ides</em>), + 1 to account for the day itself
    - if the date falls on the day before a special day, it receives the precursor <strong><em>Pridie</em></strong> ('the day before') before the name of the relevant special day
    - the reference year is the <a href="https://historycooperative.org/the-founding-of-rome-birth-of-an-empire/">founding of Rome</a> as a city (753 BC)

Some examples:
- '<em>Est Dies Mercvris ante diem XI Calendas Maivs MMDCCLXXV Ab Vrbe condita</em>' means 'Today is Wednesday the 11<sup>th</sup> day before the Kalends of May, 2775 years after the founding (of Rome)' (i.e., 20 April 2022)
- '<em>Est Dies Veneris Pridie Calendas Ianvarivs MMDCCLII Ab Vrbe condita</em>' means 'Today is Friday the day before the Kalends of January, 2752 years after the founding (of Rome)' (i.e., 31 December 1999)
  
<br>
Prof <a href="http://scholar.google.com.au/citations?sortby=pubdate&hl=en&user=1sO0O3wAAAAJ&view_op=list_works">Corey J. A. Bradshaw</a> <br>
<a href="http://globalecologyflinders.com" target="_blank">Global Ecology</a>, <a href="http://flinders.edu.au" target="_blank">Flinders University</a>, Adelaide, Australia <br>
April 2022 <br>
<a href=mailto:corey.bradshaw@flinders.edu.au>e-mail</a> <br>
