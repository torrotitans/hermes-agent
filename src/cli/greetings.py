"""
FN:greetings.py
Greeting message generator for Torro Agent CLI.

Provides random inspiration messages, holiday-specific greetings,
and ASCII art banner.

Functions:
- FN:get_greeting: Get a random greeting message (lines 55-75)
- FN:get_holiday_greeting: Get holiday-specific greeting (lines 78-120)
- FN:get_seasonal_greeting: Get seasonal greeting (lines 123-145)
- FN:get_banner: Get ASCII art banner (lines 148-180)
"""

import random
from datetime import datetime
from typing import Optional


# ANSI color codes
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
}

# ASCII art banner - Pluto themed logo
TORRO_BANNER = f"""{COLORS['cyan']}{COLORS['bold']}
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   {COLORS['dim']}          .--.                                          ║
    ║   {COLORS['dim']}         |o_o |                                          ║
    ║   {COLORS['dim']}         |_  _ |                                         ║
    ║   {COLORS['dim']}        /  ___ \\                                        ║
    ║   {COLORS['dim']}       /  _  _ \\                                       ║
    ║   {COLORS['dim']}      /  | | | \\                                      ║
    ║   {COLORS['dim']}     |   | | |   |                                    ║
    ║   {COLORS['dim']}     |____|_|____|                                   ║
    ║   {COLORS['dim']}        \\_       _/                                  ║
    ║   {COLORS['dim']}         \\_______/                                   ║
    ║                                                          ║
    ║         {COLORS['yellow']}⚡{COLORS['reset']} {COLORS['magenta']}P L U T O{COLORS['reset']} {COLORS['yellow']}⚡{COLORS['reset']}                              ║
    ║         {COLORS['green']}T O R R O   A G E N T{COLORS['reset']}                          ║
    ║         {COLORS['dim']}Autonomous Agent Framework{COLORS['reset']}                       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝{COLORS['reset']}
"""

# General inspiration messages
INSPIRATION_MESSAGES = [
    ("Ready to rock and roll!", "🚀", "green"),
    ("Buckle up, we're launching to Mars!", "🪐", "cyan"),
    ("Systems online. Let's make magic happen!", "✨", "yellow"),
    ("Ready to tackle any challenge you throw my way!", "💪", "green"),
    ("Let's build something extraordinary together!", "🏗️", "magenta"),
    ("Code, create, conquer. Let's go!", "⚡", "yellow"),
    ("Your digital co-pilot is ready for takeoff!", "✈️", "cyan"),
    ("Ready to turn ideas into reality!", "🎯", "green"),
    ("Let's solve some problems and have fun doing it!", "🧩", "yellow"),
    ("Awake and ready to assist! What's our mission?", "🎖️", "cyan"),
    ("Let's make today productive and awesome!", "🌟", "yellow"),
    ("Ready to innovate and create!", "🎨", "magenta"),
    ("Your AI assistant is fully charged and ready!", "🔋", "green"),
    ("Let's push the boundaries of what's possible!", "🌊", "cyan"),
    ("Ready to help you achieve greatness!", "🏆", "yellow"),
]

# Holiday-specific greetings
HOLIDAY_GREETINGS = {
    # January
    "01-01": [("Happy New Year!", "🎆", "yellow"), ("New year, new possibilities!", "🎊", "cyan")],
    # February
    "02-14": [("Happy Valentine's Day!", "💕", "magenta"), ("Let's make someone's day special!", "❤️", "red")],
    # March
    "03-17": [("Happy St. Patrick's Day!", "🍀", "green"), ("May the luck be with you!", "🍀", "green")],
    # April
    "04-01": [("Happy April Fools' Day!", "😄", "yellow"), ("Just kidding, I'm genuinely ready to help!", "🤡", "cyan")],
    # May
    "05-01": [("Happy Labor Day!", "🛠️", "yellow"), ("Let's make something beautiful!", "🌺", "magenta")],
    # June
    "06-15": [("Happy Father's Day!", "👨", "blue"), ("Let's make the most of the season!", "☀️", "yellow")],
    # July
    "07-04": [("Happy Independence Day!", "🎇", "cyan"), ("Time to fire up the engines!", "🇺🇸", "red")],
    # August
    "08-15": [("Happy summer break vibes!", "🏖️", "cyan"), ("Let's make every day count!", "🌞", "yellow")],
    # September
    "09-01": [("Happy New Month!", "📅", "blue"), ("Ready to learn something new!", "📚", "cyan")],
    # October
    "10-31": [("Happy Halloween!", "🎃", "yellow"), ("Don't worry, I'm on your side!", "👻", "magenta")],
    # November
    "11-11": [("Happy Veterans Day!", "🎖️", "green"), ("Let's be grateful for what we have!", "🦃", "yellow")],
    # December
    "12-25": [("Merry Christmas!", "🎄", "green"), ("Happy Holidays!", "🎅", "red"), ("Let's finish the year strong!", "🎆", "cyan")],
    "12-31": [("Happy New Year's Eve!", "🎆", "cyan"), ("Ready to ring in the future!", "🕐", "blue")],
}

# Seasonal greetings
SEASONAL_GREETINGS = {
    "spring": [
        ("Spring is in the air!", "🌸", "magenta"),
        ("Fresh spring vibes!", "🌷", "green"),
        ("Spring cleaning for your code? I'm ready!", "🌱", "green"),
    ],
    "summer": [
        ("Summer mode activated!", "☀️", "yellow"),
        ("Sunny days and code rays!", "🌊", "cyan"),
        ("Summer energy!", "🏖️", "yellow"),
    ],
    "autumn": [
        ("Fall into productivity!", "🍂", "yellow"),
        ("Autumn vibes!", "🍁", "red"),
        ("Cozy coding season!", "📚", "blue"),
    ],
    "winter": [
        ("Winter wonderland mode!", "❄️", "cyan"),
        ("Cold outside, warm inside!", "🌨️", "blue"),
        ("Snowy days and coding ways!", "⛄", "cyan"),
    ],
}


def _get_season() -> str:
    """
    FN:_get_season Determine the current season.

    Returns:
        Season name (spring, summer, autumn, winter)
    """
    month = datetime.now().month
    if month in (3, 4, 5):
        return "spring"
    elif month in (6, 7, 8):
        return "summer"
    elif month in (9, 10, 11):
        return "autumn"
    else:
        return "winter"


def get_holiday_greeting() -> Optional[tuple]:
    """
    FN:get_holiday_greeting Get holiday-specific greeting if today is a holiday.

    Returns:
        Tuple of (message, emoji, color) or None if not a holiday
    """
    today = datetime.now().strftime("%m-%d")
    if today in HOLIDAY_GREETINGS:
        greeting = random.choice(HOLIDAY_GREETINGS[today])
        return greeting
    return None


def get_seasonal_greeting() -> tuple:
    """
    FN:get_seasonal_greeting Get seasonal greeting.

    Returns:
        Tuple of (message, emoji, color)
    """
    season = _get_season()
    return random.choice(SEASONAL_GREETINGS[season])


def get_greeting() -> tuple:
    """
    FN:get_greeting Get a random greeting message.

    Returns:
        Tuple of (message, emoji, color)
    """
    # Check for holiday first
    holiday = get_holiday_greeting()
    if holiday:
        return holiday

    # Check for seasonal greeting (30% chance)
    if random.random() < 0.3:
        return get_seasonal_greeting()

    # Default to inspiration message
    return random.choice(INSPIRATION_MESSAGES)


def get_banner() -> str:
    """
    FN:get_banner Get the ASCII art banner.

    Returns:
        ASCII art banner string
    """
    return TORRO_BANNER
