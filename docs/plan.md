# Project Plan

## Goal
Build a simple system that checks game prices and reports discounts for the target region.

## Flow
1. Read list of games or store pages
2. Fetch current price
3. Compare with last saved price
4. If a discount exists, prepare a short post
5. Send the post
6. Save new price to a small log file

## Main Files
- src/main.py: runs the bot
- src/fetcher.py: gets prices
- src/checker.py: compares values
- data/prices.json: stores past prices
- docs/plan.md: project notes

## Next Steps
- Add fetcher for Steam
- Add fetcher for Epic Games
- Add simple post function
- Add scheduler to repeat checks