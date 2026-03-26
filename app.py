import random
import string
import secrets
import customtkinter as ctk
import pyperclip
import zxcvbn

# ── Appearance ──────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Colour palette ───────────────────────────────────────────────────────────
BG        = "#0f0f13"
CARD      = "#1a1a24"
ACCENT    = "#7c5cfc"
ACCENT2   = "#a78bfa"
SUCCESS   = "#22c55e"
WARN      = "#f59e0b"
DANGER    = "#ef4444"
TEXT_PRI  = "#f1f5f9"
TEXT_SEC  = "#94a3b8"

# ── Strength helpers ──────────────────────────────────────────────────────────
STRENGTH_LABELS = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
STRENGTH_COLORS = [DANGER, DANGER, WARN, SUCCESS, SUCCESS]
STRENGTH_FG     = ["#ef444433", "#ef444433", "#f59e0b33", "#22c55e33", "#22c55e33"]


class PassGenApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PassGen")
        self.geometry("560x720")
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self._build_ui()

    # ── UI construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=(36, 0), padx=40, fill="x")

        ctk.CTkLabel(
            header,
            text="🔐  PassGen",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=ACCENT2,
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Secure password generator",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_SEC,
        ).pack(side="left", padx=(12, 0), pady=(8, 0))

        # ── Password display card ─────────────────────────────────────────────
        display_card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=16)
        display_card.pack(pady=24, padx=40, fill="x", ipady=10)

        self.password_var = ctk.StringVar(value="Click 'Generate' to start")

        self.password_entry = ctk.CTkEntry(
            display_card,
            textvariable=self.password_var,
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            text_color=ACCENT2,
            fg_color="transparent",
            border_width=0,
            state="readonly",
            height=44,
            justify="center",
        )
        self.password_entry.pack(padx=20, pady=(12, 0), fill="x")

        # Strength bar + label
        self.strength_frame = ctk.CTkFrame(display_card, fg_color="transparent")
        self.strength_frame.pack(padx=20, pady=(6, 0), fill="x")

        self.strength_bar = ctk.CTkProgressBar(
            self.strength_frame,
            height=6,
            corner_radius=4,
            progress_color=DANGER,
            fg_color="#2a2a3a",
        )
        self.strength_bar.set(0)
        self.strength_bar.pack(fill="x")

        self.strength_label = ctk.CTkLabel(
            display_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=DANGER,
        )
        self.strength_label.pack(pady=(4, 10))

        # ── Copy feedback label
        self.copy_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=SUCCESS,
        )
        self.copy_label.pack()

        # ── Settings card ─────────────────────────────────────────────────────
        settings_card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=16)
        settings_card.pack(pady=4, padx=40, fill="x", ipady=10)

        ctk.CTkLabel(
            settings_card,
            text="Settings",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=TEXT_SEC,
        ).pack(anchor="w", padx=20, pady=(14, 4))

        # ── Length slider section
        length_row = ctk.CTkFrame(settings_card, fg_color="transparent")
        length_row.pack(padx=20, pady=(4, 0), fill="x")

        ctk.CTkLabel(
            length_row,
            text="Length",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_PRI,
        ).pack(side="left")

        self.length_display = ctk.CTkLabel(
            length_row,
            text="16",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=ACCENT2,
        )
        self.length_display.pack(side="right")

        self.length_var = ctk.IntVar(value=16)
        self.slider = ctk.CTkSlider(
            settings_card,
            from_=6,
            to=64,
            variable=self.length_var,
            width=480,
            progress_color=ACCENT,
            button_color=ACCENT2,
            button_hover_color=ACCENT,
            command=self._on_slider,
        )
        self.slider.pack(padx=20, pady=(4, 10), fill="x")

        # ── Character options ─────────────────────────────────────────────────
        opts_label = ctk.CTkFrame(settings_card, fg_color="transparent")
        opts_label.pack(padx=20, pady=(4, 4), fill="x")
        ctk.CTkLabel(
            opts_label,
            text="Include",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_PRI,
        ).pack(anchor="w")

        checks_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        checks_frame.pack(padx=20, pady=(0, 14), fill="x")

        self.use_upper = ctk.BooleanVar(value=True)
        self.use_lower = ctk.BooleanVar(value=True)
        self.use_digits = ctk.BooleanVar(value=True)
        self.use_symbols = ctk.BooleanVar(value=False)

        options = [
            ("Uppercase  (A-Z)", self.use_upper),
            ("Lowercase  (a-z)", self.use_lower),
            ("Numbers    (0-9)", self.use_digits),
            ("Symbols   (!@#$)",  self.use_symbols),
        ]

        for col, (label, var) in enumerate(options):
            cb = ctk.CTkCheckBox(
                checks_frame,
                text=label,
                variable=var,
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=TEXT_PRI,
                fg_color=ACCENT,
                hover_color=ACCENT2,
                checkmark_color=TEXT_PRI,
                border_color="#555",
            )
            cb.grid(row=col // 2, column=col % 2, sticky="w", padx=(0, 24), pady=3)

        # ── Action buttons ────────────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20, padx=40, fill="x")

        self.gen_btn = ctk.CTkButton(
            btn_frame,
            text="⚡  Generate",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=48,
            corner_radius=12,
            fg_color=ACCENT,
            hover_color=ACCENT2,
            command=self.generate_password,
        )
        self.gen_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.copy_btn = ctk.CTkButton(
            btn_frame,
            text="📋  Copy",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=48,
            corner_radius=12,
            fg_color="#2a2a3a",
            hover_color="#3a3a4a",
            border_width=1,
            border_color=ACCENT,
            command=self.copy_password,
        )
        self.copy_btn.pack(side="right", expand=True, fill="x", padx=(8, 0))

        # ── Footer tip ────────────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="💡 Use symbols for the strongest passwords",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXT_SEC,
        ).pack(pady=(0, 20))

    # ── Callbacks ─────────────────────────────────────────────────────────────
    def _on_slider(self, value):
        self.length_display.configure(text=str(int(value)))

    def generate_password(self):
        length = self.length_var.get()

        charset = ""
        pools = []
        if self.use_upper.get():
            charset += string.ascii_uppercase
            pools.append(string.ascii_uppercase)
        if self.use_lower.get():
            charset += string.ascii_lowercase
            pools.append(string.ascii_lowercase)
        if self.use_digits.get():
            charset += string.digits
            pools.append(string.digits)
        if self.use_symbols.get():
            symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
            charset += symbols
            pools.append(symbols)

        if not charset:
            self.password_var.set("⚠ Select at least one option!")
            self.strength_label.configure(text="")
            self.strength_bar.set(0)
            return

        # Guarantee at least one char from each selected pool
        mandatory = [secrets.choice(pool) for pool in pools]
        remaining = [secrets.choice(charset) for _ in range(length - len(mandatory))]
        password_list = mandatory + remaining
        secrets.SystemRandom().shuffle(password_list)
        password = "".join(password_list)

        self.password_var.set(password)
        self._update_strength(password)
        self.copy_label.configure(text="")

    def _update_strength(self, password: str):
        result = zxcvbn.zxcvbn(password)
        score = result["score"]  # 0-4

        label = STRENGTH_LABELS[score]
        color = STRENGTH_COLORS[score]

        self.strength_bar.set((score + 1) / 5)
        self.strength_bar.configure(progress_color=color)
        self.strength_label.configure(text=f"Strength: {label}", text_color=color)

    def copy_password(self):
        pwd = self.password_var.get()
        if not pwd or pwd.startswith("⚠") or pwd == "Click 'Generate' to start":
            return
        pyperclip.copy(pwd)
        self.copy_label.configure(text="✅  Copied to clipboard!", text_color=SUCCESS)
        self.after(2500, lambda: self.copy_label.configure(text=""))


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = PassGenApp()
    app.mainloop()
