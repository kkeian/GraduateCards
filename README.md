# Graduate Cards

[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/kkeian/GraduateCards/blob/main/LICENSE)
[![Rate on AnkiWeb](https://glutanimate.com/logos/ankiweb-rate.svg)](https://ankiweb.net/shared/info/544867715)

Suspend or delete cards if they are past the threshold number of days.

> If you take a break from reviews, Anki this add-on will not be as useful because the threshold is relative to when this add-on runs.

## Installation Options

1. Install from [AnkiWeb](https://ankiweb.net/shared/info/544867715)
2. Clone this repo into your add-ons folder.  
For more information read the Anki Add-Ons Docs.

## Configuration

Tools -> Graduate Cards -> View Config

### Parameters
- **deck_names** - names of the decks to target.  
**Default = ["Default"]**
- **action** - action to take on cards.   
**Default = "Suspend".**
- **threshold_parameter** - the parameter to target card thresholds by.  
**Default = "Due in Days"**
- **threshold** - the number of days the threshold parameter  
should be at before the action is taken.  
**Default = 90**  

## Development/Contributing
- **Python 3.9** is confirmed to work with this add on.
- Confirmed working on **Anki version 25.02.4**  

Fork this repo, make your changes, and open a PR.  
This add-on is pretty complete, so no major functionality changes are planned and are unlikely to be merged.