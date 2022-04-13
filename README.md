# Roman numeral calendar and clock

<img align="right" src="www/RomanClockEx.png" alt="Roman Calendar/Clock" width="300" style="margin-top: 20px">

R code to produce a simple date and clock plot in Roman Numerals. Works on a 24-hour system. Clock plot based on a modified version of <code>caroline::plotClock</code>.

## Set-up
1. Install the following libraries in R:
- <code><a href="https://search.r-project.org/CRAN/refmans/caroline/html/plotClock.html">caroline</a></code>
- <code><a href="https://lubridate.tidyverse.org/">lubridate</a></code>

You can do this easily with the following command:
> <code>install.packages(c("caroline", "lubridate"))</code>

2. Simply run the script in R, then you're ready to plot a real-time clock and date in Roman numerals. 

Note that there is no zero in Roman numerals (apparently, the Romans had no need for it). I've therefore just incuded '00' when the hour or minute = zero in the 24-hour clock. Date format is DD.MM.YYYY.
  
<br>
Prof <a href="http://scholar.google.com.au/citations?sortby=pubdate&hl=en&user=1sO0O3wAAAAJ&view_op=list_works">Corey J. A. Bradshaw</a> <br>
<a href="http://globalecologyflinders.com" target="_blank">Global Ecology</a>, <a href="http://flinders.edu.au" target="_blank">Flinders University</a>, Adelaide, Australia <br>
April 2022 <br>
<a href=mailto:corey.bradshaw@flinders.edu.au>e-mail</a> <br>
