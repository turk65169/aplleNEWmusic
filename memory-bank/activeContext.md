# Active Context

## Current Status
- **Recent Content & Branding**:
  - Rebranded the bot from "Humay Music" to "Apple Music" across core files, helper strings, and the setup script.
  - Overhauled and fixed the `/broadcast` command (added `/gcast`, `/broadcast`, `-all` flag, and improved reliability/safety).
  - Added new `/radyo` command with support for popular Turkish radio stations.
  - Fixed support chat link formatting in play command error messages.
  - Updated configuration with new API credentials and support channels.

## Recent Changes (April 12, 2026)
- **CRITICAL FIX** `youtube.py`: Added missing `config` import — was crashing with `NameError` when cookie pool empty
- `admin.py`: Rewrote cookie management — added `/cookies` (status view), `/cookie` (upload fix), `/cookietemizle` (clear all)
- `callbacks.py`: Fixed `AttributeError` crash when `caption` or `text` is `None` in controls callback
- `youtube.py`: Added null-safety to `search()` and `playlist()` — prevents crashes from missing API fields (None duration, empty thumbnails)
- `youtube.py`: Improved `save_cookies()` — handles batbin API failures, validates content size, per-cookie error handling
- `downloader.py`: Fixed progress throttle race condition — per-message tracking instead of shared global state
- `en.json`: Updated `play_log` template to include chat ID, user ID, message link (8-arg format)
- `_utilities.py`: Added `safe_edit()` and `safe_delete()` helpers; hardened `play_log` for None from_user
- `telegram.py`: All edit_text calls now use `utils.safe_edit()` to prevent MESSAGE_ID_INVALID crashes

## Work in Focus
- Stability improvements across all command flows
- Support long-duration films (up to 3 hours) and large file sizes (up to 2 GB)
- Ensuring all features work end-to-end without crashes

## Next Steps
1. Deploy and test `/cookies`, `/cookie`, `/cookietemizle` commands
2. Monitor for any remaining crash patterns in logs
3. Test quiz feature with new song pool
4. Consider adding missing keys to other locale files (ar, de, etc.)
5. Test playlist play command in group chats

## Active Decisions & Patterns
- Use `.get()` with fallback for all locale key access in dynamic contexts
- PyTgCalls now streams audio/video directly from YT URLs instead of downloading locally first, making playback nearly instant.
- Quiz downloads still use local chunk downloads (with timeout protection) as they require FFmpeg slicing.
- All `play_not_found` calls include `.format(config.SUPPORT_CHAT)` argument
- **Stability Pattern**: Use `utils.safe_edit()` and `utils.safe_delete()` for all operations on status/progress messages to prevent `MESSAGE_ID_INVALID` crashes when users delete bot messages.
- **Throttling**: Progress updates are throttled to 3 seconds to avoid Telegram flood waits and redundant network calls.
