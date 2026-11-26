# AutoWA

AutoWA is a simple Python desktop application for scheduling the delivery of a **single WhatsApp message** to a phone number or WhatsApp group at a selected time. The interface is currently presented in Malay and is built with Tkinter.

> Use this application only for lawful communication and with recipients who have agreed to receive messages from you. Avoid spam, bulk unsolicited messages, or any use that violates WhatsApp's terms.

## Features

- Schedule a message for an international phone number or a WhatsApp group.
- Enter a time in 12-hour AM/PM format by typing or using dropdown lists.
- View a live countdown and cancel the schedule before delivery begins.
- Send through WhatsApp Web in Google Chrome with the `pywhatkit` package.
- Launch it from any working directory using the `AutoWA` command after installation.

## Requirements

- Python **3.10 or newer**
- Google Chrome installed
- A WhatsApp account that can access WhatsApp Web
- Tkinter, which is usually included with Python. On some Linux distributions, install the system package `python3-tk` if Tkinter is missing.

## Install once

Clone the repository and install AutoWA as a command-line application. You only need to do this once per Python environment:

```bash
git clone https://github.com/HirokiSpy/AutoWA.git
cd AutoWA
python -m pip install .
```

This installs the Python dependencies and registers the `AutoWA` command. After installation, you can run it from any folder without navigating to the project directory:

```bash
AutoWA
```

On Windows, if the `AutoWA` command is not recognized, add your Python installation's `Scripts` directory to `PATH`, or run the generated `AutoWA.exe` from that directory. Restart the terminal after changing `PATH`.

## Run from source (alternative)

You can also run the app directly from the project directory:

```bash
python -m pip install -r requirements.txt
python AutoWA.py
```

## Usage

1. Choose **Nombor** or **Group** as the target type.
2. Enter a complete international phone number, including the country code (for example, `+60123456789`) or a valid WhatsApp group ID/invite link.
3. Enter the message.
4. Select or type the delivery time in 12-hour AM/PM format.
5. Click **Mula Jadual** to start the countdown.

Keep the application open and the computer running until the scheduled time. WhatsApp Web must be accessible and, when required, you must sign in manually in Chrome.

## Important Notes

- The schedule is not saved after the application is closed.
- If the selected time has already passed on the current day, the application schedules it for the following day.
- You can cancel the schedule before the delivery process begins.
- After a successful send, the application attempts to close Chrome. On Windows and Linux, its process command may close **all running Chrome instances**. Save your work before using AutoWA.
- Delivery depends on internet connectivity, WhatsApp Web availability, and `pywhatkit`; successful delivery is not guaranteed.
- The application does not verify that the recipient consented or that a phone number/group ID is valid. Review target details before scheduling.

## Troubleshooting

- **Tkinter is missing:** install Tkinter support for your Python installation. On Ubuntu/Debian, this is usually:

  ```bash
  sudo apt install python3-tk
  ```

- **`AutoWA` command is not recognized:** confirm the package was installed in the active Python environment and that its Scripts/bin directory is on `PATH`. Restart the terminal after updating `PATH`.
- **Chrome or WhatsApp Web does not open:** verify that Chrome is installed, the internet is available, and you are signed in to WhatsApp Web.
- **Dependency error:** install the project again with `python -m pip install .`.

## Dependencies

- [`pywhatkit`](https://github.com/Ankit404butfound/PyWhatKit) — WhatsApp Web automation
- Tkinter — graphical user interface (Python standard library, subject to system package availability)

## License

This project is licensed under the [MIT License](LICENSE). Copyright (c) 2026 Hiroki.
