from __future__ import annotations

import os
import sys
from pathlib import Path

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent

    return base_path / relative_path
    
import csv
import math
from calendar import monthrange
from dataclasses import dataclass
from datetime import datetime

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, QUrl
from PySide6.QtGui import QColor, QDesktopServices, QFont, QFontMetrics, QImage, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import QApplication, QWidget

NUMBER_NAMES_PATH = resource_path("data/roman_number_names.csv")
FESTIVALS_PATH = resource_path("data/roman_festivals.csv")
FESTIVAL_LINKS_PATH = resource_path("data/roman_festival_links.csv")
COIN_PORTRAIT_PATH = resource_path("data/roman_coin_portrait.png")

LATIN_WEEKDAYS = (
    "Dies Lvnae",
    "Dies Martis",
    "Dies Mercvris",
    "Dies Iovis",
    "Dies Veneris",
    "Dies Satvrni",
    "Dies Solis",
)
LATIN_MONTHS = (
    "Ianvarivs",
    "Febrvarivs",
    "Martivs",
    "Aprilis",
    "Maivs",
    "Ivnivs",
    "Ivlivs",
    "Avgvstvs",
    "September",
    "October",
    "November",
    "December",
)
IDES = (13, 13, 15, 13, 15, 13, 15, 13, 13, 15, 13, 13)
NONES = tuple(day - 8 for day in IDES)


@dataclass(frozen=True)
class RomanClockState:
    day_roman: str
    month_roman: str
    year_roman: str
    hour_roman: str
    minute_roman: str
    second_roman: str
    latin_date_line_one: str
    latin_date_line_two: str
    latin_hour: str
    latin_minute: str
    latin_second: str
    festival_text: str
    festival_url: str | None
    hour: int
    minute: int
    second: int


def int_to_roman(number: int) -> str:
    numerals = (
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    )
    if number <= 0:
        raise ValueError("Roman numerals require a positive integer")

    parts: list[str] = []
    remainder = number
    for value, symbol in numerals:
        while remainder >= value:
            parts.append(symbol)
            remainder -= value
    return "".join(parts)


def load_number_names(path: Path) -> dict[int, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return {int(row["Num"]): row["LatinNumName"] for row in reader}


def load_festivals(path: Path) -> dict[tuple[int, int], list[str]]:
    festivals: dict[tuple[int, int], list[str]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            key = (int(row["month"]), int(row["day"]))
            festivals.setdefault(key, []).append(row["holiday"])
    return festivals


def load_festival_links(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return {row["holiday"].strip(): row["url"] for row in reader}


def roman_time_component(value: int) -> str:
    return "N" if value == 0 else int_to_roman(value)


def resolve_latin_date_description(now: datetime) -> tuple[str, bool]:
    month_index = now.month - 1
    day = now.day
    month_name = LATIN_MONTHS[month_index]
    nones_day = NONES[month_index]
    ides_day = IDES[month_index]
    days_this_month = monthrange(now.year, now.month)[1]
    pridie = False
    latin_date_desc = ""

    if day == ides_day:
        latin_date_desc = f"Idibvs {month_name}"

    if day == nones_day:
        latin_date_desc = f"Nonis {month_name}"

    if day == 1:
        latin_date_desc = f"Calendas {month_name}"

    if 1 < day < (nones_day - 1):
        day_count = int_to_roman(nones_day - day + 1)
        latin_date_desc = f"{day_count} Nonis {month_name}"

    if nones_day < day < (ides_day - 1):
        day_count = int_to_roman(ides_day - day + 1)
        latin_date_desc = f"{day_count} Idibvs {month_name}"

    if day > ides_day:
        next_month_name = LATIN_MONTHS[now.month % 12]
        day_count = int_to_roman(days_this_month - day + 1)
        latin_date_desc = f"{day_count} Calendas {next_month_name}"

    if day == (nones_day - 1):
        latin_date_desc = f"Pridie Nonas {month_name}"
        pridie = True

    if day == (ides_day - 1):
        latin_date_desc = f"Pridie Idibvs {month_name}"
        pridie = True

    if day == days_this_month:
        next_month_name = LATIN_MONTHS[now.month % 12]
        latin_date_desc = f"Pridie Calendas {next_month_name}"
        pridie = True

    return latin_date_desc, pridie


def build_clock_state(
    now: datetime,
    number_names: dict[int, str],
    festivals: dict[tuple[int, int], list[str]],
    festival_links: dict[str, str],
) -> RomanClockState:
    latin_date_desc, pridie = resolve_latin_date_description(now)
    weekday_name = LATIN_WEEKDAYS[now.weekday()]
    month_index = now.month - 1

    if now.day == 1 or pridie or now.day == NONES[month_index] or now.day == IDES[month_index]:
        latin_date_line_one = f"Est {weekday_name} {latin_date_desc}"
    else:
        latin_date_line_one = f"Est {weekday_name} ante diem {latin_date_desc}"

    festival_name = festivals.get((now.month, now.day), ["nvllvs"])[0].strip()
    latin_hour = "media nocte" if now.hour == 0 else number_names[now.hour]

    return RomanClockState(
        day_roman=int_to_roman(now.day),
        month_roman=int_to_roman(now.month),
        year_roman=int_to_roman(now.year),
        hour_roman=roman_time_component(now.hour),
        minute_roman=roman_time_component(now.minute),
        second_roman=roman_time_component(now.second),
        latin_date_line_one=latin_date_line_one,
        latin_date_line_two=f"{int_to_roman(now.year + 753)} Ab Vrbe condita",
        latin_hour=latin_hour,
        latin_minute=number_names[now.minute],
        latin_second=number_names[now.second],
        festival_text=festival_name,
        festival_url=festival_links.get(festival_name),
        hour=now.hour,
        minute=now.minute,
        second=now.second,
    )


class RomanClockWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.number_names = load_number_names(NUMBER_NAMES_PATH)
        self.festivals = load_festivals(FESTIVALS_PATH)
        self.festival_links = load_festival_links(FESTIVAL_LINKS_PATH)
        self.coin_portrait = QImage(str(COIN_PORTRAIT_PATH))
        self.state = build_clock_state(datetime.now(), self.number_names, self.festivals, self.festival_links)
        self.festival_link_rect: QRectF | None = None
        self.second_timer = QTimer(self)
        self.second_timer.setInterval(1000)
        self.second_timer.timeout.connect(self.refresh_state)

        self.setWindowTitle("Roman Clock Calendar")
        self.resize(760, 920)
        self.setMinimumSize(700, 900)
        self.setMouseTracking(True)
        self.sync_to_system_clock()

    def sync_to_system_clock(self) -> None:
        self.refresh_state()
        now = datetime.now()
        delay_ms = max(1, 1000 - int(now.microsecond / 1000))
        QTimer.singleShot(delay_ms, self.start_repeating_timer)

    def start_repeating_timer(self) -> None:
        self.refresh_state()
        if not self.second_timer.isActive():
            self.second_timer.start()

    def refresh_state(self) -> None:
        self.state = build_clock_state(datetime.now(), self.number_names, self.festivals, self.festival_links)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.fillRect(self.rect(), QColor("#f5efe2"))

        width = self.width()
        height = self.height()
        centre_x = width / 2

        self.festival_link_rect = None
        clock_centre_y, clock_radius = self.draw_text_block(painter, width, height)
        self.draw_clock_face(painter, centre_x, clock_centre_y, clock_radius)

    def draw_text_block(self, painter: QPainter, width: int, height: int) -> tuple[float, float]:
        centre_x = width / 2
        top_padding = max(24.0, height * 0.03)
        line_gap = max(10.0, height * 0.012)
        block_gap = max(20.0, height * 0.024)
        quote_padding = max(28.0, height * 0.035)
        current_top = top_padding

        def place_line(
            text: str,
            point_size: int,
            *,
            bold: bool = False,
            italic: bool = False,
            colour: QColor | None = None,
            underline: bool = False,
            gap_after: float = line_gap,
        ) -> QRectF:
            nonlocal current_top
            rect = self.draw_text(
                painter,
                centre_x,
                current_top + point_size,
                text,
                point_size,
                bold=bold,
                italic=italic,
                colour=colour,
                underline=underline,
            )
            current_top = rect.bottom() + gap_after
            return rect

        place_line(f"{self.state.day_roman}.{self.state.month_roman}.{self.state.year_roman}", 56, bold=True)
        place_line(self.state.latin_date_line_one, 20)
        place_line(self.state.latin_date_line_two, 20)
        self.festival_link_rect = self.draw_text(
            painter,
            centre_x,
            current_top + 20,
            f"feriatvm : {self.state.festival_text}",
            20,
            colour=QColor("#1d4f91") if self.state.festival_url else QColor("#2d241c"),
            underline=bool(self.state.festival_url),
        )
        current_top = self.festival_link_rect.bottom() + block_gap
        place_line(
            f"{self.state.hour_roman} : {self.state.minute_roman} : {self.state.second_roman}",
            36,
            gap_after=line_gap,
        )
        place_line(
            f"{self.state.latin_hour} {self.state.latin_minute} {self.state.latin_second}",
            20,
            gap_after=block_gap,
        )

        quote_rect = self.draw_text(
            painter,
            centre_x,
            height - quote_padding - 18,
            "nvlla dies vmqvam memori vos eximet aevo",
            18,
            italic=True,
        )

        available_top = current_top
        available_bottom = quote_rect.top() - block_gap
        clock_centre_y = (available_top + available_bottom) / 2
        clock_radius = min(width * 0.22, max(0.0, (available_bottom - available_top) / 2))
        return clock_centre_y, clock_radius

    def draw_clock_face(self, painter: QPainter, centre_x: float, centre_y: float, radius: float) -> None:
        painter.save()
        self.draw_coin_face(painter, centre_x, centre_y, radius)

        self.draw_tick_marks(painter, centre_x, centre_y, radius)
        self.draw_hour_labels(painter, centre_x, centre_y, radius)
        self.draw_hands(painter, centre_x, centre_y, radius)

        painter.restore()

    def draw_coin_face(self, painter: QPainter, centre_x: float, centre_y: float, radius: float) -> None:
        painter.save()

        outer_radius = radius * 1.14
        painter.setPen(QPen(QColor("#705334"), 4))
        painter.setBrush(QColor("#c8a66b"))
        painter.drawEllipse(QPointF(centre_x, centre_y), outer_radius, outer_radius)

        painter.setPen(QPen(QColor("#e0c089"), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(centre_x, centre_y), radius * 1.06, radius * 1.06)

        painter.setOpacity(1.0)
        painter.setPen(QPen(QColor("#8e6a3f"), 2))
        painter.setBrush(QColor("#f8f3e8"))
        painter.drawEllipse(QPointF(centre_x, centre_y), radius * 0.98, radius * 0.98)

        painter.setPen(QPen(QColor("#9d7a4b"), 1))
        for bead in range(48):
            angle = math.pi / 2 - (2 * math.pi * bead / 48)
            bead_point = QPointF(
                centre_x + math.cos(angle) * radius * 1.025,
                centre_y - math.sin(angle) * radius * 1.025,
            )
            painter.setBrush(QColor("#b88f59"))
            painter.drawEllipse(bead_point, max(1.5, radius * 0.016), max(1.5, radius * 0.016))

        self.draw_coin_portrait(painter, centre_x, centre_y, radius)

        painter.restore()

    def draw_coin_portrait(self, painter: QPainter, centre_x: float, centre_y: float, radius: float) -> None:
        painter.save()
        if self.coin_portrait.isNull():
            painter.restore()
            return

        portrait_rect = QRectF(
            centre_x - radius * 0.43,
            centre_y - radius * 0.56,
            radius * 0.90,
            radius * 1.10,
        )
        clip_path = QPainterPath()
        clip_path.addEllipse(portrait_rect.adjusted(radius * 0.00, radius * 0.03, -radius * 0.02, -radius * 0.01))
        painter.setClipPath(clip_path)
        painter.setOpacity(0.78)
        painter.drawImage(portrait_rect, self.coin_portrait)

        painter.setOpacity(0.10)
        painter.fillPath(clip_path, QColor("#b8874a"))

        painter.setClipping(False)
        edge_blend = QRadialGradient(QPointF(centre_x, centre_y), radius * 0.62)
        edge_blend.setColorAt(0.0, QColor(214, 181, 122, 0))
        edge_blend.setColorAt(0.68, QColor(214, 181, 122, 0))
        edge_blend.setColorAt(0.88, QColor(200, 166, 107, 95))
        edge_blend.setColorAt(1.0, QColor(200, 166, 107, 185))
        painter.setOpacity(1.0)
        painter.fillPath(clip_path, edge_blend)

        painter.restore()

    def draw_tick_marks(self, painter: QPainter, centre_x: float, centre_y: float, radius: float) -> None:
        painter.save()
        tick_pen = QPen(QColor("#7e766d"), 2)
        painter.setPen(tick_pen)

        for tick_index in range(60):
            angle = math.pi / 2 - (2 * math.pi * tick_index / 60)
            outer = QPointF(
                centre_x + math.cos(angle) * radius,
                centre_y - math.sin(angle) * radius,
            )
            inner_scale = 0.93 if tick_index % 5 == 0 else 0.97
            inner = QPointF(
                centre_x + math.cos(angle) * radius * inner_scale,
                centre_y - math.sin(angle) * radius * inner_scale,
            )
            painter.drawLine(inner, outer)

        painter.restore()

    def draw_hour_labels(self, painter: QPainter, centre_x: float, centre_y: float, radius: float) -> None:
        painter.save()
        labels = [int_to_roman(value) for value in (list(range(13, 24)) + [12] if self.state.hour >= 12 else range(1, 13))]
        font = QFont("Times New Roman", max(12, int(radius * 0.1)))
        painter.setFont(font)
        painter.setPen(QColor("#2d241c"))
        metrics = QFontMetrics(font)

        for index, label in enumerate(labels):
            angle = math.pi / 2 - (2 * math.pi * (index + 1) / 12)
            x = centre_x + math.cos(angle) * radius * 0.78
            y = centre_y - math.sin(angle) * radius * 0.78
            rect = metrics.boundingRect(label)
            text_rect = QRectF(
                x - rect.width() / 2 - 6,
                y - rect.height() / 2 - 3,
                rect.width() + 12,
                rect.height() + 6,
            )
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, label)

        painter.restore()

    def draw_hands(self, painter: QPainter, centre_x: float, centre_y: float, radius: float) -> None:
        painter.save()

        second_fraction = self.state.second / 60
        minute_fraction = (self.state.minute + second_fraction) / 60
        hour_fraction = ((self.state.hour % 12) + minute_fraction) / 12

        self.draw_hand(painter, centre_x, centre_y, radius * 0.68, hour_fraction, QColor("#2d241c"), 5)
        self.draw_hand(painter, centre_x, centre_y, radius * 0.96, minute_fraction, QColor("#7e766d"), 3)
        self.draw_hand(painter, centre_x, centre_y, radius * 1.0, second_fraction, QColor("#8f2d1f"), 2)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#2d241c"))
        painter.drawEllipse(QPointF(centre_x, centre_y), 5, 5)
        painter.restore()

    def draw_hand(
        self,
        painter: QPainter,
        centre_x: float,
        centre_y: float,
        length: float,
        fraction: float,
        colour: QColor,
        width: int,
    ) -> None:
        angle = math.pi / 2 - (2 * math.pi * fraction)
        end_point = QPointF(
            centre_x + math.cos(angle) * length,
            centre_y - math.sin(angle) * length,
        )
        pen = QPen(colour, width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(QPointF(centre_x, centre_y), end_point)

    def draw_text(
        self,
        painter: QPainter,
        centre_x: float,
        y: float,
        text: str,
        point_size: int,
        *,
        bold: bool = False,
        italic: bool = False,
        colour: QColor | None = None,
        underline: bool = False,
    ) -> QRectF:
        font = QFont("Times New Roman", point_size)
        font.setBold(bold)
        font.setItalic(italic)
        font.setUnderline(underline)
        painter.setFont(font)
        painter.setPen(colour or QColor("#2d241c"))

        rect = QRectF(20, y - point_size * 1.2, self.width() - 40, point_size * 2.4)
        painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, text)

        metrics = QFontMetrics(font)
        text_rect = metrics.boundingRect(text)
        return QRectF(
            centre_x - (text_rect.width() / 2) - 8,
            y - (text_rect.height() / 2) - 6,
            text_rect.width() + 16,
            text_rect.height() + 12,
        )

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if self.festival_link_rect and self.state.festival_url and self.festival_link_rect.contains(event.position()):
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.festival_link_rect
            and self.state.festival_url
            and self.festival_link_rect.contains(event.position())
        ):
            QDesktopServices.openUrl(QUrl(self.state.festival_url))
            event.accept()
            return
        super().mousePressEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self.unsetCursor()
        super().leaveEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    window = RomanClockWidget()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
