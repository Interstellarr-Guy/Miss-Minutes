import datetime
import math
import tkinter as tk


class MissMinutesClock:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("TVA Clock — Miss Minutes")
        self.root.geometry("540x660")
        self.root.resizable(False, False)
        self.root.configure(bg="#140E0A")

        self.size = 440
        self.cx = self.size // 2
        self.cy = self.size // 2
        self.radius = 175

        # Top TVA banner
        header = tk.Frame(root, bg="#140E0A")
        header.pack(pady=(16, 4))

        tk.Label(
            header,
            text="TIME VARIANCE AUTHORITY",
            font=("Courier New", 10, "bold"),
            fg="#F59E0B",
            bg="#140E0A",
        ).pack()

        self.greeting_var = tk.StringVar(value="HEY Y'ALL! IT'S TIME!")
        tk.Label(
            header,
            textvariable=self.greeting_var,
            font=("Trebuchet MS", 16, "bold"),
            fg="#FFF3D6",
            bg="#140E0A",
        ).pack(pady=(2, 0))

        # Main canvas for Miss Minutes & clock face
        self.canvas = tk.Canvas(
            root,
            width=self.size,
            height=self.size,
            bg="#140E0A",
            highlightthickness=0,
        )
        self.canvas.pack()

        # Bottom digital readout & toggle
        footer = tk.Frame(root, bg="#221710", padx=18, pady=10, highlightbackground="#D97706", highlightthickness=1)
        footer.pack(pady=(4, 16))

        self.digital_var = tk.StringVar()
        tk.Label(
            footer,
            textvariable=self.digital_var,
            font=("Courier New", 20, "bold"),
            fg="#FBBF24",
            bg="#221710",
        ).pack(side=tk.LEFT, padx=(0, 14))

        self.use_24h = False
        self.fmt_btn = tk.Button(
            footer,
            text="12H / 24H",
            command=self.toggle_format,
            font=("Courier New", 10, "bold"),
            fg="#140E0A",
            bg="#F59E0B",
            activebackground="#FBBF24",
            activeforeground="#140E0A",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
        )
        self.fmt_btn.pack(side=tk.LEFT)

        self.blink_phase = 0
        self.update_clock()

    def toggle_format(self):
        self.use_24h = not self.use_24h
        self.update_clock()

    def polar_to_xy(self, angle_deg: float, dist: float):
        rad = math.radians(angle_deg - 90)
        return self.cx + dist * math.cos(rad), self.cy + dist * math.sin(rad)

    def draw_face(self, now: datetime.datetime):
        c = self.canvas
        c.delete("all")

        # Subtle outer TVA glow ring
        c.create_oval(
            self.cx - self.radius - 14,
            self.cy - self.radius - 14,
            self.cx + self.radius + 14,
            self.cy + self.radius + 14,
            outline="#92400E",
            width=3,
        )

        # Main clock body (warm amber / orange Miss Minutes tone)
        c.create_oval(
            self.cx - self.radius,
            self.cy - self.radius,
            self.cx + self.radius,
            self.cy + self.radius,
            fill="#F97316",
            outline="#FEF3C7",
            width=4,
        )

        # Inner cream dial ring
        inner_r = self.radius - 28
        c.create_oval(
            self.cx - inner_r,
            self.cy - inner_r,
            self.cx + inner_r,
            self.cy + inner_r,
            fill="#FFFBEB",
            outline="#EA580C",
            width=2,
        )

        # Hour ticks & numbers
        for i in range(60):
            angle = i * 6
            is_hour = i % 5 == 0
            r_outer = inner_r - 4
            r_inner = inner_r - (14 if is_hour else 8)
            x1, y1 = self.polar_to_xy(angle, r_inner)
            x2, y2 = self.polar_to_xy(angle, r_outer)
            c.create_line(
                x1, y1, x2, y2,
                fill="#7C2D12" if is_hour else "#D97706",
                width=3 if is_hour else 1,
            )

            if is_hour:
                num = 12 if i == 0 else i // 5
                nx, ny = self.polar_to_xy(angle, inner_r - 28)
                c.create_text(
                    nx, ny,
                    text=str(num),
                    font=("Trebuchet MS", 13, "bold"),
                    fill="#431407",
                )

        # Miss Minutes eyes & smile (shifted slightly toward second hand for liveliness)
        sec_angle = (now.second + now.microsecond / 1_000_000) * 6
        look_dx = math.cos(math.radians(sec_angle - 90)) * 4
        look_dy = math.sin(math.radians(sec_angle - 90)) * 3

        is_blinking = (now.second % 5 == 0) and (now.microsecond < 160_000)
        for side in (-1, 1):
            ex = self.cx + side * 42 + look_dx * 0.4
            ey = self.cy - 42 + look_dy * 0.4
            if is_blinking:
                c.create_line(ex - 14, ey, ex + 14, ey, fill="#1C1917", width=3, capstyle=tk.ROUND)
            else:
                c.create_oval(ex - 15, ey - 18, ex + 15, ey + 18, fill="#FFFFFF", outline="#1C1917", width=2)
                c.create_oval(
                    ex + look_dx - 6,
                    ey + look_dy - 8,
                    ex + look_dx + 6,
                    ey + look_dy + 8,
                    fill="#1C1917",
                )
                c.create_oval(
                    ex + look_dx - 2,
                    ey + look_dy - 4,
                    ex + look_dx + 2,
                    ey + look_dy,
                    fill="#FFFFFF",
                )

        # Signature friendly grin
        c.create_arc(
            self.cx - 56,
            self.cy - 22,
            self.cx + 56,
            self.cy + 46,
            start=195,
            extent=150,
            style=tk.ARC,
            outline="#1C1917",
            width=3.5,
        )
        # Rosy cheeks
        for side in (-1, 1):
            c.create_oval(
                self.cx + side * 66 - 10,
                self.cy - 8,
                self.cx + side * 66 + 10,
                self.cy + 6,
                fill="#FB7185",
                outline="",
            )

        # Clock hands
        hours_12 = (now.hour % 12) + now.minute / 60.0
        minutes_exact = now.minute + now.second / 60.0

        hour_angle = hours_12 * 30
        min_angle = minutes_exact * 6

        # Hour hand
        hx, hy = self.polar_to_xy(hour_angle, inner_r * 0.48)
        c.create_line(self.cx, self.cy, hx, hy, fill="#1C1917", width=7, capstyle=tk.ROUND)

        # Minute hand
        mx, my = self.polar_to_xy(min_angle, inner_r * 0.72)
        c.create_line(self.cx, self.cy, mx, my, fill="#431407", width=5, capstyle=tk.ROUND)

        # Second hand
        sx, sy = self.polar_to_xy(sec_angle, inner_r * 0.82)
        bx, by = self.polar_to_xy(sec_angle + 180, 22)
        c.create_line(bx, by, sx, sy, fill="#DC2626", width=2.5, capstyle=tk.ROUND)

        # Center cap
        c.create_oval(self.cx - 8, self.cy - 8, self.cx + 8, self.cy + 8, fill="#DC2626", outline="#1C1917", width=2)

    def update_greeting(self, hour: int):
        if 5 <= hour < 12:
            self.greeting_var.set("MORNING, Y'ALL! TIME IS MOVIN'!")
        elif 12 <= hour < 17:
            self.greeting_var.set("AFTERNOON CHECK-IN FROM THE TVA!")
        elif 17 <= hour < 22:
            self.greeting_var.set("EVENIN', FRIEND! EVERY SECOND COUNTS!")
        else:
            self.greeting_var.set("LATE SHIFT ON THE SACRED TIMELINE!")

    def update_clock(self):
        now = datetime.datetime.now()
        self.draw_face(now)
        self.update_greeting(now.hour)

        if self.use_24h:
            self.digital_var.set(now.strftime("%H:%M:%S"))
        else:
            self.digital_var.set(now.strftime("%I:%M:%S %p").lstrip("0"))

        # Smooth ~30 FPS refresh for second hand & eye tracking
        self.root.after(33, self.update_clock)


if __name__ == "__main__":
    root = tk.Tk()
    app = MissMinutesClock(root)
    root.mainloop()