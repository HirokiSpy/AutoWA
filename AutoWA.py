import os
import platform
import threading
import time
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk

import pywhatkit as kit


class AutoWAApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AutoWA")
        self.root.geometry("470x690")
        self.root.resizable(False, False)
        self.root.configure(bg="#120D1D")

        self.target_dt: datetime | None = None
        self.running = False
        self._syncing_time = False

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(
            "Purple.TCombobox",
            fieldbackground="#120D1D",
            background="#261B3D",
            foreground="#F3E8FF",
            arrowcolor="#C084FC",
            bordercolor="#3B2A61",
            lightcolor="#3B2A61",
            darkcolor="#3B2A61",
            selectbackground="#9333EA",
            selectforeground="#FFFFFF",
            padding=4,
        )
        style.map(
            "Purple.TCombobox",
            fieldbackground=[("readonly", "#120D1D")],
            foreground=[("readonly", "#F3E8FF")],
            bordercolor=[("focus", "#A855F7")],
        )

    def _build_ui(self):
        # Header: AutoWA + Dibuat oleh Hiroki
        header = tk.Frame(self.root, bg="#120D1D")
        header.pack(fill="x", pady=(14, 10))

        tk.Label(
            header,
            text="AutoWA",
            font=("Consolas", 28, "bold"),
            fg="#C084FC",
            bg="#120D1D",
        ).pack()

        tk.Label(
            header,
            text="Dibuat oleh Hiroki",
            font=("Segoe UI", 9),
            fg="#A78BFA",
            bg="#120D1D",
        ).pack(pady=(1, 0))

        # Kad Borang Utama
        form_card = tk.Frame(
            self.root,
            bg="#1B142B",
            highlightbackground="#342554",
            highlightthickness=1,
            padx=18,
            pady=14,
        )
        form_card.pack(fill="x", padx=22)

        # Pemilih Jenis Sasaran (Nombor / Group)
        tk.Label(
            form_card,
            text="Jenis Sasaran",
            font=("Segoe UI", 9, "bold"),
            fg="#C4B5FD",
            bg="#1B142B",
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        self.mode_var = tk.StringVar(value="Nombor")
        mode_row = tk.Frame(form_card, bg="#1B142B")
        mode_row.pack(fill="x", pady=(0, 10))

        for mode_name in ("Nombor", "Group"):
            tk.Radiobutton(
                mode_row,
                text=mode_name,
                variable=self.mode_var,
                value=mode_name,
                command=self._on_mode_change,
                font=("Segoe UI", 10, "bold"),
                fg="#F3E8FF",
                bg="#1B142B",
                selectcolor="#2A1E44",
                activebackground="#1B142B",
                activeforeground="#C084FC",
                cursor="hand2",
            ).pack(side="left", padx=(0, 22))

        # 1. Nombor Telephone / Group ID
        self.target_label = tk.Label(
            form_card,
            text="1. Nombor Telephone",
            font=("Segoe UI", 10, "bold"),
            fg="#F5F3FF",
            bg="#1B142B",
            anchor="w",
        )
        self.target_label.pack(fill="x", pady=(2, 4))

        self.target_entry = tk.Entry(
            form_card,
            font=("Consolas", 11),
            bg="#120D1D",
            fg="#FFFFFF",
            insertbackground="#C084FC",
            relief="flat",
            highlightbackground="#3B2A61",
            highlightcolor="#A855F7",
            highlightthickness=1,
        )
        self.target_entry.insert(0, "+60")
        self.target_entry.pack(fill="x", ipady=6, pady=(0, 10))

        # 2. Mesej
        tk.Label(
            form_card,
            text="2. Mesej",
            font=("Segoe UI", 10, "bold"),
            fg="#F5F3FF",
            bg="#1B142B",
            anchor="w",
        ).pack(fill="x", pady=(2, 4))

        self.msg_text = tk.Text(
            form_card,
            height=3,
            font=("Segoe UI", 10),
            bg="#120D1D",
            fg="#FFFFFF",
            insertbackground="#C084FC",
            relief="flat",
            highlightbackground="#3B2A61",
            highlightcolor="#A855F7",
            highlightthickness=1,
            wrap="word",
        )
        self.msg_text.pack(fill="x", pady=(0, 10))

        # 3. Masa AM/PM 12 Jam (Taip terus atau pilih dropdown dengan : di tengah)
        tk.Label(
            form_card,
            text="3. Masa (12 Jam - taip atau pilih)",
            font=("Segoe UI", 10, "bold"),
            fg="#F5F3FF",
            bg="#1B142B",
            anchor="w",
        ).pack(fill="x", pady=(2, 5))

        now = datetime.now()
        default_ampm = "PM" if now.hour >= 12 else "AM"
        default_hour12 = now.hour % 12
        if default_hour12 == 0:
            default_hour12 = 12

        hours = [f"{h:02d}" for h in range(1, 13)]
        minutes = [f"{m:02d}" for m in range(0, 60)]
        ampm_list = ["AM", "PM"]

        self.hour_var = tk.StringVar(value=f"{default_hour12:02d}")
        self.min_var = tk.StringVar(value=f"{now.minute:02d}")
        self.ampm_var = tk.StringVar(value=default_ampm)

        time_row = tk.Frame(form_card, bg="#1B142B")
        time_row.pack(fill="x", pady=(0, 2))

        self.hour_entry = tk.Entry(
            time_row,
            width=3,
            font=("Consolas", 12, "bold"),
            bg="#120D1D",
            fg="#FFFFFF",
            insertbackground="#C084FC",
            relief="flat",
            highlightbackground="#3B2A61",
            highlightcolor="#A855F7",
            highlightthickness=1,
            justify="center",
        )
        self.hour_entry.insert(0, f"{default_hour12:02d}")
        self.hour_entry.pack(side="left", ipady=4)
        self.hour_entry.bind("<KeyRelease>", self._on_manual_hm_typed)
        self.hour_entry.bind("<FocusOut>", self._on_manual_hm_typed)

        tk.Label(
            time_row,
            text=":",
            fg="#C084FC",
            bg="#1B142B",
            font=("Consolas", 14, "bold"),
        ).pack(side="left", padx=5)

        self.min_entry = tk.Entry(
            time_row,
            width=3,
            font=("Consolas", 12, "bold"),
            bg="#120D1D",
            fg="#FFFFFF",
            insertbackground="#C084FC",
            relief="flat",
            highlightbackground="#3B2A61",
            highlightcolor="#A855F7",
            highlightthickness=1,
            justify="center",
        )
        self.min_entry.insert(0, f"{now.minute:02d}")
        self.min_entry.pack(side="left", ipady=4, padx=(0, 10))
        self.min_entry.bind("<KeyRelease>", self._on_manual_hm_typed)
        self.min_entry.bind("<FocusOut>", self._on_manual_hm_typed)

        self.hour_combo = ttk.Combobox(
            time_row,
            values=hours,
            textvariable=self.hour_var,
            width=3,
            state="readonly",
            style="Purple.TCombobox",
            font=("Consolas", 10, "bold"),
        )
        self.hour_combo.pack(side="left")
        self.hour_combo.bind("<<ComboboxSelected>>", self._on_dropdown_change)

        tk.Label(
            time_row,
            text=":",
            fg="#A78BFA",
            bg="#1B142B",
            font=("Consolas", 12, "bold"),
        ).pack(side="left", padx=4)

        self.min_combo = ttk.Combobox(
            time_row,
            values=minutes,
            textvariable=self.min_var,
            width=3,
            state="readonly",
            style="Purple.TCombobox",
            font=("Consolas", 10, "bold"),
        )
        self.min_combo.pack(side="left", padx=(0, 8))
        self.min_combo.bind("<<ComboboxSelected>>", self._on_dropdown_change)

        self.ampm_combo = ttk.Combobox(
            time_row,
            values=ampm_list,
            textvariable=self.ampm_var,
            width=4,
            state="readonly",
            style="Purple.TCombobox",
            font=("Consolas", 10, "bold"),
        )
        self.ampm_combo.pack(side="left")

        # Butang Mula & Batal
        btn_row = tk.Frame(self.root, bg="#120D1D")
        btn_row.pack(fill="x", padx=22, pady=(12, 12))

        self.start_btn = tk.Button(
            btn_row,
            text="Mula Jadual",
            font=("Segoe UI", 10, "bold"),
            bg="#9333EA",
            fg="#FFFFFF",
            activebackground="#A855F7",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.start_schedule,
        )
        self.start_btn.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 6))

        self.cancel_btn = tk.Button(
            btn_row,
            text="Batal",
            font=("Segoe UI", 10, "bold"),
            bg="#261B3D",
            fg="#E9D5FF",
            activebackground="#362657",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            state="disabled",
            command=self.cancel_schedule,
        )
        self.cancel_btn.pack(side="left", fill="x", expand=True, ipady=7, padx=(6, 0))

        # Kad Paparan Bawah: AutoWA
        summary_card = tk.Frame(
            self.root,
            bg="#1B142B",
            highlightbackground="#342554",
            highlightthickness=1,
            padx=18,
            pady=12,
        )
        summary_card.pack(fill="both", expand=True, padx=22, pady=(0, 18))

        tk.Label(
            summary_card,
            text="AutoWA",
            font=("Consolas", 14, "bold"),
            fg="#C084FC",
            bg="#1B142B",
            anchor="w",
        ).pack(fill="x", pady=(0, 6))

        self.info_label = tk.Label(
            summary_card,
            text="Jenis: -\nSasaran: -\nMesej: -\nMasa: -",
            font=("Consolas", 10),
            fg="#E9D5FF",
            bg="#1B142B",
            justify="left",
            anchor="w",
        )
        self.info_label.pack(fill="x", pady=(0, 8))

        self.countdown_label = tk.Label(
            summary_card,
            text="Countdown: --:--:--",
            font=("Consolas", 16, "bold"),
            fg="#D8B4FE",
            bg="#1B142B",
            anchor="w",
        )
        self.countdown_label.pack(fill="x", pady=(2, 4))

        self.status_label = tk.Label(
            summary_card,
            text="Status: Menunggu input anda.",
            font=("Segoe UI", 9),
            fg="#A78BFA",
            bg="#1B142B",
            anchor="w",
            wraplength=385,
            justify="left",
        )
        self.status_label.pack(fill="x", pady=(2, 0))

    def _on_dropdown_change(self, _event=None):
        if self._syncing_time:
            return
        self._syncing_time = True
        try:
            self.hour_entry.delete(0, "end")
            self.hour_entry.insert(0, self.hour_var.get())
            self.min_entry.delete(0, "end")
            self.min_entry.insert(0, self.min_var.get())
        finally:
            self._syncing_time = False

    def _on_manual_hm_typed(self, _event=None):
        if self._syncing_time:
            return
        h_str = self.hour_entry.get().strip()
        m_str = self.min_entry.get().strip()
        if not (h_str.isdigit() and m_str.isdigit()):
            return

        h = int(h_str)
        m = int(m_str)
        if 1 <= h <= 12 and 0 <= m <= 59:
            self._syncing_time = True
            try:
                self.hour_var.set(f"{h:02d}")
                self.min_var.set(f"{m:02d}")
            finally:
                self._syncing_time = False

    def _on_mode_change(self):
        mode = self.mode_var.get()
        current_val = self.target_entry.get().strip()
        self.target_entry.delete(0, "end")

        if mode == "Nombor":
            self.target_label.config(text="1. Nombor Telephone")
            if not current_val or "chat.whatsapp.com" in current_val:
                self.target_entry.insert(0, "+60")
            else:
                self.target_entry.insert(0, current_val)
        else:
            self.target_label.config(text="1. Group ID (kod atau link invite)")
            if current_val != "+60":
                self.target_entry.insert(0, current_val)

    def _clean_group_id(self, raw: str) -> str:
        val = raw.strip()
        if "chat.whatsapp.com/" in val:
            val = val.split("chat.whatsapp.com/")[-1].split("?")[0].strip("/")
        return val

    def _parse_time_to_datetime(self) -> tuple[datetime, str]:
        h_str = self.hour_entry.get().strip()
        m_str = self.min_entry.get().strip()
        ampm = self.ampm_var.get()

        if h_str or m_str:
            if not (h_str.isdigit() and m_str.isdigit()):
                raise ValueError("Jam dan minit mesti nombor (contoh: 09 : 30).")
            hour12 = int(h_str)
            minute = int(m_str)
            if not (1 <= hour12 <= 12 and 0 <= minute <= 59):
                raise ValueError("Jam mesti 01-12 dan minit mesti 00-59.")
        else:
            hour12 = int(self.hour_var.get())
            minute = int(self.min_var.get())

        if ampm == "AM":
            hour24 = 0 if hour12 == 12 else hour12
        else:
            hour24 = 12 if hour12 == 12 else hour12 + 12

        now = datetime.now()
        target = now.replace(hour=hour24, minute=minute, second=0, microsecond=0)
        if target <= now:
            target += timedelta(days=1)

        formatted_12h = f"{hour12:02d}:{minute:02d} {ampm}"
        return target, formatted_12h

    def start_schedule(self):
        mode = self.mode_var.get()
        raw_target = self.target_entry.get().strip()
        msg = self.msg_text.get("1.0", "end").strip()

        if mode == "Nombor":
            target = raw_target
            if not target or not target.startswith("+") or len(target) < 8:
                self.status_label.config(
                    text="Status: Masukkan nombor telefon penuh bermula dengan + (cth: +60123456789).",
                    fg="#F87171",
                )
                return
        else:
            target = self._clean_group_id(raw_target)
            if not target or len(target) < 10:
                self.status_label.config(
                    text="Status: Masukkan Group ID yang sah atau link invite chat.whatsapp.com.",
                    fg="#F87171",
                )
                return

        if not msg:
            self.status_label.config(text="Status: Sila masukkan mesej dahulu.", fg="#F87171")
            return

        try:
            self.target_dt, masa_paparan = self._parse_time_to_datetime()
        except ValueError as err:
            self.status_label.config(text=f"Status: {err}", fg="#F87171")
            return

        self.running = True
        self.start_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")

        mesej_pendek = msg if len(msg) <= 55 else msg[:52] + "..."

        self.info_label.config(
            text=(
                f"Jenis: {mode}\n"
                f"Sasaran: {target}\n"
                f"Mesej: {mesej_pendek}\n"
                f"Masa: {masa_paparan} ({self.target_dt.strftime('%d/%m/%Y')})"
            )
        )
        self.status_label.config(text="Status: Jadual aktif. Biarkan aplikasi terbuka...", fg="#C084FC")
        self._update_countdown()

    def cancel_schedule(self):
        self.running = False
        self.target_dt = None
        self.start_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.countdown_label.config(text="Countdown: --:--:--", fg="#D8B4FE")
        self.status_label.config(text="Status: Jadual dibatalkan.", fg="#FBBF24")

    def _update_countdown(self):
        if not self.running or self.target_dt is None:
            return

        sisa = int((self.target_dt - datetime.now()).total_seconds())

        if sisa <= 0:
            self.countdown_label.config(text="Countdown: 00:00:00", fg="#C084FC")
            self.status_label.config(
                text="Status: Masa tiba! Membuka Chrome & menghantar mesej...",
                fg="#E9D5FF",
            )
            self.running = False
            mode = self.mode_var.get()
            raw_target = self.target_entry.get().strip()
            target = raw_target if mode == "Nombor" else self._clean_group_id(raw_target)
            msg = self.msg_text.get("1.0", "end").strip()
            threading.Thread(
                target=self._send_and_close_chrome, args=(mode, target, msg), daemon=True
            ).start()
            return

        jam = sisa // 3600
        minit = (sisa % 3600) // 60
        saat = sisa % 60
        self.countdown_label.config(text=f"Countdown: {jam:02d}:{minit:02d}:{saat:02d}", fg="#D8B4FE")
        self.root.after(250, self._update_countdown)

    def _close_chrome(self):
        system = platform.system().lower()
        try:
            if "windows" in system:
                os.system("taskkill /im chrome.exe /f >nul 2>&1")
            elif "linux" in system:
                os.system("pkill -f chrome >/dev/null 2>&1")
            elif "darwin" in system:
                os.system('osascript -e \'quit app "Google Chrome"\'')
        except Exception:
            pass

    def _send_and_close_chrome(self, mode: str, target: str, msg: str):
        try:
            if mode == "Nombor":
                kit.sendwhatmsg_instantly(
                    phone_no=target,
                    message=msg,
                    wait_time=15,
                    tab_close=True,
                    close_time=4,
                )
            else:
                kit.sendwhatmsg_to_group_instantly(
                    group_id=target,
                    message=msg,
                    wait_time=15,
                    tab_close=True,
                    close_time=4,
                )
            time.sleep(2)
            self._close_chrome()
            self.root.after(
                0,
                lambda: self._on_done("Status: Mesej dihantar & Chrome ditutup.", "#E9D5FF"),
            )
        except Exception as e:
            self.root.after(0, lambda: self._on_done(f"Status: Ralat - {e}", "#F87171"))

    def _on_done(self, text: str, color: str):
        self.start_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.status_label.config(text=text, fg=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoWAApp(root)
    root.mainloop()