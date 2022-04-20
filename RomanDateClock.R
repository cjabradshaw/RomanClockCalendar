## Roman numeral date & clock
## Corey Bradshaw
## Flinders University
## April 2022

## modified from plotClock in the caroline package
plotClockRoman <- function (hour, minute, x0 = 0, y0 = 0, r = 1) {
  circleXY <- caroline::makeElipseCoords(x0=x0,y0=y0,b=1.1*r,a=1.1*r,alpha=0,pct.range=c(0,1),len=50)
  quarHourTickMarksXY <- caroline::makeElipseCoords(x0=x0,y0=y0,b=1.05*r,a=1.05*r,alpha=(pi/2),pct.range=c((12*5-1)/(12*5),0),len=12*5)
  hourLabelsXY <- caroline::makeElipseCoords(x0=x0,y0=y0,b=0.9*r,a=0.9*r,alpha=(pi/2),pct.range=c(11/12,0),len=12)
  polygon(circleXY)
  if (hour >= 12) {
        roman.seq <- utils::as.roman(c(seq(13,23),12))
    } else {
        roman.seq <- utils::as.roman(seq(1,12))  
    }
  text(hourLabelsXY[, 1],hourLabelsXY[, 2],roman.seq,cex=0.5,vfont=c("serif","EUC"))
  text(quarHourTickMarksXY[,1],quarHourTickMarksXY[, 2],".", col="dark grey")
  minuteV <- minute/60
  minuteVXY <- caroline::makeElipseCoords(x0=x0,y0=y0,b=r,a=r,alpha=0,pct.range=(0.25-rep(minuteV,2)),len=1)
  segments(x0,y0,minuteVXY$x[1],minuteVXY$y[1],col="grey")
  hourV <- hour/12 + minuteV/12 # adjust hour hand for fractions of the hour by minute
  hourVXY <- caroline::makeElipseCoords(x0=x0,y0=y0,b=0.7*r,a=0.7*r,alpha=0,pct.range=(0.25-rep(hourV,2)),len=1)
  segments(x0, y0, hourVXY$x, hourVXY$y,lwd=1.5)
}

# get current time and date
currentTime <- Sys.time() # current time
date.now <- format(strptime(as.Date(currentTime), format="%Y-%m-%d"), "%d %b %Y")
year.now <- lubridate::year(currentTime)
month.now <- lubridate::month(currentTime)
day.now <-  lubridate::day(currentTime)
hour.now <- sprintf("%02d", lubridate::hour(currentTime))
hour12 <- ifelse(as.numeric(hour.now) > 12, as.numeric(hour.now)-12, as.numeric(hour.now))
min.now <-  sprintf("%02d", lubridate::minute(currentTime))

# Latin date characteristics
LatinWeekday <- c("Dies Lvnae","Dies Martis","Dies Mercvris","Dies Iovis","Dies Veneris", "Dies Satvrni", "Dies Solis")
EnglishWeekday <- c("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
Ldow <- LatinWeekday[which(EnglishWeekday == weekdays(currentTime))]

LatinMonth <- c("Ianvarivs","Febrvarivs","Martivs","Aprilis","Maivs","Ivnivs","Ivlivs","Avgvstvs","September","October","November","December")

# Latin special days
# Ides
Ides <- c(13,13,15,13,15,13,15,13,13,15,13,13) # either 15th (Mar, Jul, Oct,  May) or 13th (every other month)
if (day.now == Ides[month.now]) {
  LatinDateDesc <- paste("Idibvs", LatinMonth[month.now], sep=" ")
}

# Nones
Nones <- Ides - 8 # 8 days earlier than the Ides
if (day.now == Nones[month.now]) {
  LatinDateDesc <- paste("Nonis", LatinMonth[month.now], sep=" ")
}

# Kalends
if (day.now == 1) {
  LatinDateDesc <- paste("Calendas", LatinMonth[month.now], sep=" ")
}

# Other days
if (day.now > 1 & day.now < (Nones[month.now] - 1)) {
  daycount <- as.roman(as.numeric(Nones[month.now] - day.now + 1))
  LatinDateDesc <- paste(daycount, "Nonas", LatinMonth[month.now], sep=" ")
}

if (day.now > Nones[month.now] & day.now < (Ides[month.now] - 1)) {
  daycount <- as.roman(as.numeric(Ides[month.now] - day.now + 1))
  LatinDateDesc <- paste(daycount, "Idvs", LatinMonth[month.now], sep=" ")
}

if (day.now > Ides[month.now]) {
  daycount <- as.roman(as.numeric(lubridate::days_in_month(currentTime)) - day.now + 1)
  if (month.now < 12) {
    LatinDateDesc <- paste(daycount, "Calendas", LatinMonth[month.now+1], sep=" ")
  }
  if (month.now == 12) {
    LatinDateDesc <- paste(daycount, "Calendas", LatinMonth[1], sep=" ")
  }
}

# special day eve
if (day.now == (Nones[month.now] - 1)) {
  LatinDateDesc <- paste("Pridie Nonas", LatinMonth[month.now], sep=" ")
}
if (day.now == (Ides[month.now] - 1)) {
  LatinDateDesc <- paste("Pridie Idus", LatinMonth[month.now], sep=" ")
}
if (day.now == as.numeric(lubridate::days_in_month(currentTime))) {
  LatinDateDesc <- paste("Pridie Calendas", LatinMonth[month.now + 1], sep=" ")
}

# Latin date as text
LDate1 <- paste("Est", Ldow, "ante diem", LatinDateDesc, sep=" ")
LDate2 <- paste(as.roman(year.now + 753), "Ab Vrbe condita", sep=" ") # from the establishment of Rome 753 BC

# Romanise for Gregorian date and 24-hour clock
year.rom <- utils::as.roman(year.now)
month.rom <- utils::as.roman(month.now)
day.rom <- utils::as.roman(day.now)
hour.rom <- utils::as.roman(hour.now)
min.rom <- utils::as.roman(min.now)
if (as.numeric(hour.now) == 0) {
  hour.rom <- sprintf("%02d",0)
}
if (as.numeric(min.now) == 0) {
  min.rom <- sprintf("%02d",0)
}

# plot Gregorian date in Roman numerals, Latin date in Latin, and time in Roman numerals
par(xaxt="n", yaxt="n", pty="s")
plot(0:10,0:10,pch=NULL,col=NULL,xlab="",ylab="")
text(x=5, y=9, labels=paste(day.rom, ".", month.rom, ".", year.rom, sep=""), adj=0.5, cex=2.1, vfont=c("serif", "bold"))
text(x=5, y=8, labels=LDate1, adj=0.5, cex=0.65, vfont=c("serif", "EUC"))
text(x=5, y=7.5, labels=LDate2, adj=0.5, cex=0.65, vfont=c("serif", "EUC"))
text(x=5, y=6, labels=paste(hour.rom, ":", min.rom, sep=""), adj=0.5, cex=1.6, vfont=c("serif", "EUC"))
plotClockRoman(hour=as.numeric(hour.now), minute=as.numeric(min.now), x0 = 5, y0 = 2.5, r = 2)
