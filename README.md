# Alarm Clock using PYTHON ⏰

## Overview

This is a **Python-based alarm clock** with multiple features such as custom alarm sounds, snooze functionality, countdown display, and support for multiple time formats. It is designed to run on desktops with Python and uses **`pygame`** for sound playback.

The project aims to provide a user-friendly console interface while ensuring reliability and flexibility for scheduling alarms.

---

## Features

* ✅ Accepts **multiple time formats**: `HH:MM` or `HH:MM:SS`
* ✅ Automatically schedules the **next occurrence** if the entered time has already passed today
* ✅ **Snooze functionality** (default: 5 minutes)
* ✅ **Countdown display** showing the remaining time until the alarm
* ✅ Supports **multiple sound formats** (`.mp3`, `.wav`)
* ✅ **Fallback system beep** if no sound file is provided
* ✅ Error handling for invalid input and sound playback

---

## Requirements

* Python **3.10+**

* Libraries (install via pip):

  ```bash
  pip install pygame
  ```

* Optional: Custom sound files (`.mp3` or `.wav`) placed in the project folder

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Aditya-2215/ALARM_CLOCK.git
   ```

2. **Navigate to the project folder**:

   ```bash
   cd "ALARM_CLOCK"
   ```

3. **Create a virtual environment (optional but recommended)**:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # For PowerShell
   ```

4. **Install dependencies**:

   ```bash
   pip install pygame
   ```

---

## Usage

1. **Run the alarm clock script**:

   ```bash
   python alarm_clock.py
   ```

2. **Follow the prompts**:

   * Enter the alarm time in `HH:MM` or `HH:MM:SS` format
   * Optionally, provide a custom alarm sound file path
   * Wait for the countdown to reach zero

3. **When the alarm rings**, you can:

   * **\[S] Snooze** – Delay the alarm by 5 minutes
   * **\[O] Turn off alarm** – Stop the alarm immediately
   * **\[Q] Quit program** – Exit the application

---

## Folder Structure

```
ALARM_CLOCK/
│
├── alarm_clock.py      # Main Python script
├── alarm.mp3           # Example default sound file (optional)
├── alarm.wav           # Example default sound file (optional)
├── README.md           # Project documentation
└── .venv/              # Optional virtual environment folder
```

---

## How It Works

1. The user enters the alarm time.
2. The program calculates whether the alarm is today or tomorrow.
3. A **countdown timer** is displayed in the console.
4. When the alarm triggers:

   * The chosen sound plays using `pygame`
   * Users can snooze, stop, or quit
5. If snoozed, the alarm will re-trigger after 5 minutes.

---

## Future Enhancements

* GUI version with **Tkinter or PyQt**
* Multiple alarms support
* Configurable snooze duration
* Integration with system notifications

---

## License

This project is open-source and available under the **MIT License**.

---

## Author

**Aditya Raj Pandey**
GitHub: [https://github.com/Aditya-2215](https://github.com/Aditya-2215)
