## Roman numeral date & clock
## Corey Bradshaw
## Flinders University
## April 2022 / updated May 2026

## modified from plotClock in the caroline package
plotClockRoman <- function(hour, minute, second = 0, x0 = 0, y0 = 0, r = 1) {
  circleXY <- caroline::makeElipseCoords(x0 = x0, y0 = y0, b = 1.1 * r, a = 1.1 * r, alpha = 0, pct.range = c(0, 1), len = 50)
  quarHourTickMarksXY <- caroline::makeElipseCoords(x0 = x0, y0 = y0, b = 1.05 * r, a = 1.05 * r, alpha = (pi / 2), pct.range = c((12 * 5 - 1) / (12 * 5), 0), len = 12 * 5)
  hourLabelsXY <- caroline::makeElipseCoords(x0 = x0, y0 = y0, b = 0.9 * r, a = 0.9 * r, alpha = (pi / 2), pct.range = c(11 / 12, 0), len = 12)

  polygon(circleXY)
  if (hour >= 12) {
    roman.seq <- utils::as.roman(c(seq(13, 23), 12))
  } else {
    roman.seq <- utils::as.roman(seq(1, 12))
  }

  text(hourLabelsXY[, 1], hourLabelsXY[, 2], roman.seq, cex = 0.5, vfont = c("serif", "EUC"))
  text(quarHourTickMarksXY[, 1], quarHourTickMarksXY[, 2], ".", col = "dark grey")

  minuteV <- (minute + (second / 60)) / 60
  minuteVXY <- caroline::makeElipseCoords(x0 = x0, y0 = y0, b = r, a = r, alpha = 0, pct.range = (0.25 - rep(minuteV, 2)), len = 1)
  segments(x0, y0, minuteVXY$x[1], minuteVXY$y[1], col = "grey")

  hourV <- hour / 12 + minuteV / 12
  hourVXY <- caroline::makeElipseCoords(x0 = x0, y0 = y0, b = 0.7 * r, a = 0.7 * r, alpha = 0, pct.range = (0.25 - rep(hourV, 2)), len = 1)
  segments(x0, y0, hourVXY$x[1], hourVXY$y[1], lwd = 1.5)

  secondV <- second / 60
  secondVXY <- caroline::makeElipseCoords(x0 = x0, y0 = y0, b = 1.02 * r, a = 1.02 * r, alpha = 0, pct.range = (0.25 - rep(secondV, 2)), len = 1)
  segments(x0, y0, secondVXY$x[1], secondVXY$y[1], col = "firebrick", lwd = 0.8)
  points(x0, y0, pch = 16, cex = 0.4)
}

# set working directory to script's location (from https://gist.github.com/jasonsychau)
stub <- function() {}
thisPath <- function() {
  cmdArgs <- commandArgs(trailingOnly = FALSE)
  if (length(grep("^-f$", cmdArgs)) > 0) {
    # R console option
    normalizePath(dirname(cmdArgs[grep("^-f", cmdArgs) + 1]))[1]
  } else if (length(grep("^--file=", cmdArgs)) > 0) {
    # Rscript/R console option
    normalizePath(dirname(sub("^--file=", "", cmdArgs[grep("^--file=", cmdArgs)])))[1]
  } else if (Sys.getenv("RSTUDIO") == "1") {
    # RStudio
    dirname(rstudioapi::getSourceEditorContext()$path)
  } else if (!is.null(attr(stub, "srcref"))) {
    # 'source'd via R console
    dirname(normalizePath(attr(attr(stub, "srcref"), "srcfile")$filename))
  } else {
    stop("Cannot find file path")
  }
}
setwd(thisPath())

# time as numbers in Latin
load("RomNumNam.RData")

# feriae (Roman festivals)
load("feriae.RData")

getRomanClockState <- function(currentTime = Sys.time()) {
  year.now <- lubridate::year(currentTime)
  month.now <- lubridate::month(currentTime)
  day.now <- lubridate::day(currentTime)
  hour.now <- lubridate::hour(currentTime)
  min.now <- lubridate::minute(currentTime)
  sec.now <- floor(lubridate::second(currentTime))

  # Latin date characteristics
  LatinWeekday <- c("Dies Lvnae", "Dies Martis", "Dies Mercvris", "Dies Iovis", "Dies Veneris", "Dies Satvrni", "Dies Solis")
  EnglishWeekday <- c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
  Ldow <- LatinWeekday[which(EnglishWeekday == weekdays(currentTime))]

  LatinMonth <- c("Ianvarivs", "Febrvarivs", "Martivs", "Aprilis", "Maivs", "Ivnivs", "Ivlivs", "Avgvstvs", "September", "October", "November", "December")

  # Latin special days
  Ides <- c(13, 13, 15, 13, 15, 13, 15, 13, 13, 15, 13, 13) # either 15th (Mar, Jul, Oct, May) or 13th (every other month)
  Nones <- Ides - 8 # 8 days earlier than the Ides
  Pridie <- FALSE
  LatinDateDesc <- ""

  if (day.now == Ides[month.now]) {
    LatinDateDesc <- paste("Idibvs", LatinMonth[month.now], sep = " ")
  }

  if (day.now == Nones[month.now]) {
    LatinDateDesc <- paste("Nonis", LatinMonth[month.now], sep = " ")
  }

  if (day.now == 1) {
    LatinDateDesc <- paste("Calendas", LatinMonth[month.now], sep = " ")
  }

  if (day.now > 1 && day.now < (Nones[month.now] - 1)) {
    daycount <- as.roman(as.numeric(Nones[month.now] - day.now + 1))
    LatinDateDesc <- paste(daycount, "Nonis", LatinMonth[month.now], sep = " ")
  }

  if (day.now > Nones[month.now] && day.now < (Ides[month.now] - 1)) {
    daycount <- as.roman(as.numeric(Ides[month.now] - day.now + 1))
    LatinDateDesc <- paste(daycount, "Idibvs", LatinMonth[month.now], sep = " ")
  }

  if (day.now > Ides[month.now]) {
    daycount <- as.roman(as.numeric(lubridate::days_in_month(currentTime)) - day.now + 1)
    if (month.now < 12) {
      LatinDateDesc <- paste(daycount, "Calendas", LatinMonth[month.now + 1], sep = " ")
    }
    if (month.now == 12) {
      LatinDateDesc <- paste(daycount, "Calendas", LatinMonth[1], sep = " ")
    }
  }

  # special day eve
  if (day.now == (Nones[month.now] - 1)) {
    LatinDateDesc <- paste("Pridie Nonas", LatinMonth[month.now], sep = " ")
    Pridie <- TRUE
  }
  if (day.now == (Ides[month.now] - 1)) {
    LatinDateDesc <- paste("Pridie Idibvs", LatinMonth[month.now], sep = " ")
    Pridie <- TRUE
  }
  if (day.now == as.numeric(lubridate::days_in_month(currentTime))) {
    if (month.now < 12) {
      LatinDateDesc <- paste("Pridie Calendas", LatinMonth[month.now + 1], sep = " ")
      Pridie <- TRUE
    }
    if (month.now == 12) {
      LatinDateDesc <- paste("Pridie Calendas", LatinMonth[1], sep = " ")
      Pridie <- TRUE
    }
  }

  # Latin date as text
  if (!Pridie) {
    LDate1 <- paste("Est", Ldow, "ante diem", LatinDateDesc, sep = " ")
  }
  if (day.now == 1 || Pridie || day.now == Nones[month.now] || day.now == Ides[month.now]) {
    LDate1 <- paste("Est", Ldow, LatinDateDesc, sep = " ")
  }
  LDate2 <- paste(as.roman(year.now + 753), "Ab Vrbe condita", sep = " ")

  # Romanise for Gregorian date and 24-hour clock
  year.rom <- as.character(utils::as.roman(year.now))
  month.rom <- as.character(utils::as.roman(month.now))
  day.rom <- as.character(utils::as.roman(day.now))
  hour.rom <- if (hour.now == 0) "00" else as.character(utils::as.roman(hour.now))
  min.rom <- if (min.now == 0) "00" else as.character(utils::as.roman(min.now))
  sec.rom <- if (sec.now == 0) "00" else as.character(utils::as.roman(sec.now))

  LatinHr <- if (hour.now == 0) "media nocte" else romNumName$LatinNumName[match(hour.now, romNumName$Num)]
  LatinMn <- romNumName$LatinNumName[match(min.now, romNumName$Num)]
  LatinSc <- romNumName$LatinNumName[match(sec.now, romNumName$Num)]

  feriae.sub <- which(feriae$month == month.now & feriae$day == day.now)
  dies.feriae <- if (length(feriae.sub) > 0) paste(feriae$holiday[feriae.sub], collapse = ", ") else "nvllvs"

  list(
    year.rom = year.rom,
    month.rom = month.rom,
    day.rom = day.rom,
    hour.rom = hour.rom,
    min.rom = min.rom,
    sec.rom = sec.rom,
    LDate1 = LDate1,
    LDate2 = LDate2,
    LatinHr = LatinHr,
    LatinMn = LatinMn,
    LatinSc = LatinSc,
    dies.feriae = dies.feriae,
    hour.now = hour.now,
    min.now = min.now,
    sec.now = sec.now
  )
}

renderRomanClockFrame <- function(currentTime = Sys.time()) {
  clockState <- getRomanClockState(currentTime)

  par(xaxt = "n", yaxt = "n", pty = "s")
  plot(0:10, 0:10, pch = NA, col = NA, xlab = "", ylab = "")
  text(x = 5, y = 9, labels = paste(clockState$day.rom, ".", clockState$month.rom, ".", clockState$year.rom, sep = ""), adj = 0.5, cex = 2.1, vfont = c("serif", "bold"))
  text(x = 5, y = 8, labels = clockState$LDate1, adj = 0.5, cex = 0.65, vfont = c("serif", "EUC"))
  text(x = 5, y = 7.5, labels = clockState$LDate2, adj = 0.5, cex = 0.65, vfont = c("serif", "EUC"))
  text(x = 5, y = 7, labels = paste("feriatvm : ", clockState$dies.feriae, sep = ""), adj = 0.5, cex = 0.65, vfont = c("serif", "EUC"))
  text(x = 5, y = 5.8, labels = paste(clockState$hour.rom, ":", clockState$min.rom, ":", clockState$sec.rom, sep = ""), adj = 0.5, cex = 1.4, vfont = c("serif", "EUC"))
  text(x = 5, y = 5.2, labels = paste(clockState$LatinHr, clockState$LatinMn, clockState$LatinSc, sep = " "), adj = 0.5, cex = 0.6, vfont = c("serif", "EUC"))
  text(x = 5, y = -0.1, labels = "nvlla dies vmqvam memori vos eximet aevo", adj = 0.5, cex = 0.6, vfont = c("serif", "EUC"))
  plotClockRoman(hour = clockState$hour.now, minute = clockState$min.now, second = clockState$sec.now, x0 = 5, y0 = 2.5, r = 2)
}

animateRomanClock <- function() {
  message("Animating Roman clock; press Esc or Ctrl+C to stop.")
  repeat {
    currentTime <- Sys.time()
    renderRomanClockFrame(currentTime)
    Sys.sleep(max(0, 1 - (as.numeric(currentTime) %% 1)))
  }
}

if (interactive()) {
  animateRomanClock()
} else {
  renderRomanClockFrame(Sys.time())
}
