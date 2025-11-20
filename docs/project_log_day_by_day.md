# Day 1 — Project Log

## Date: 19 Nov 2025

### Summary
Initial setup of the GameDiscountBot project. Core fetch logic, pricing system, 
automatic game list creation, and scoring strategy foundations were established.

### Work Completed

- Created the main project structure:
  - src/main.py
  - src/fetcher.py
  - src/checker.py
  - data/prices.json (initial storage)
  - data/games.json (external game list)

- Implemented Steam price fetcher:
  - Fetches name, original price, discount price, discount percent, currency.
  - Supports BR (Brazil) region via `cc=br`.
  - Includes error handling and fallback cases.

- Implemented review fetcher:
  - Added `fetcher_review_count.py` to retrieve total review count for any Steam game.
  - Confirmed working using Portal 2 (620) test.

- Established the first version of the automatic list builder:
  - Introduced `build_game_list.py`.
  - Fetches discounted games from Steam search AJAX endpoint.
  - Extracts app IDs from HTML.
  - Filters games by total reviews ≥ 10,000.
  - Outputs a clean list to `data/games.json`.

- Updated main.py to:
  - Load app IDs from external `games.json`.
  - Process multiple games instead of a single ID.
  - Output clean discount results for each game.

- Implemented scoring strategy (`scoring.py`):
  - Review weight: 70%
  - Discount weight: 30%
  - Ensures well-known games and strong discounts are ranked fairly.

- Designed posted.json system:
  - Concept only (implementation scheduled for Day 2).
  - Bot will avoid tweeting same game within 7 days unless discount increases.

### Notes
- System is now fully automated for collecting and preparing high-quality game lists.
- Next step: Implement spam-protection layer (posted.json manager) and 
  final decision engine for tweet selection.


# Day 2 — Project Log

## Date: 20 Nov 2025

### Summary
Set up the tweet text system, linked it to the Steam pipeline, and made the bot ready to post daily picks for Brazil.

### Work Completed

- Added `src/format_tweet.py`:
  - Generates tweet text in Brazilian Portuguese.
  - Uses several templates and picks one at random.
  - Tone depends on discount level (big / medium / small).
  - Uses Steam links with Brazil settings: `?cc=br&l=portuguese`.

- Updated `main.py` to:
  - Build a ranked list of discounted Steam games.
  - Select up to 10 games for the day.
  - Call `format_tweet(info)` for each selected game.
  - Print final tweet text to the console (for review).

- Confirmed that the posting guard (`posted_manager.py`) is in use:
  - Avoids posting the same game too often.
  - Updates history after each selected game.

### Notes
- Steam (Brazil) flow is now end-to-end: data fetch → filter → score → select → tweet text.
- Next steps: connect to X (Twitter) API and add a daily schedule.