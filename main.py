import json, subprocess, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

APP = "PSP NEXUS"
DATA = Path.home() / "PSP_NEXUS"
DATA.mkdir(exist_ok=True)
CONFIG = DATA / "settings.json"
EXTS = {".iso", ".cso", ".pbp", ".chd"}
BG, PANEL, CYAN, WHITE, MUTED = "#07111f", "#0d1b2d", "#37d9ff", "#eef7ff", "#8da7bd"

class Nexus:
    def __init__(self, root):
        self.root = root
        root.title("PSP NEXUS | Game Center")
        root.geometry("1100x720")
        root.minsize(850, 560)
        root.configure(bg=BG)
        self.settings = {"folder": str(Path.home() / "Games" / "PSP"), "ppsspp": "", "games": []}
        try:
            self.settings.update(json.loads(CONFIG.read_text(encoding="utf-8")))
        except Exception:
            pass
        self.selected = None
        self.build()
        self.scan()

    def save(self):
        CONFIG.write_text(json.dumps(self.settings, indent=2), encoding="utf-8")

    def label(self, parent, text, size=10, color=WHITE, bold=False, **kw):
        return tk.Label(parent, text=text, bg=kw.pop("bg", parent.cget("bg")), fg=color,
                        font=("Segoe UI", size, "bold" if bold else "normal"), **kw)

    def button(self, parent, text, command, primary=False):
        return tk.Button(parent, text=text, command=command, bg=CYAN if primary else "#10243a",
                         fg="#04101b" if primary else WHITE, activebackground="#7be7ff",
                         relief="flat", bd=0, font=("Segoe UI", 10, "bold"),
                         padx=14, pady=9, cursor="hand2")

    def build(self):
        top = tk.Frame(self.root, bg=BG); top.pack(fill="x", padx=25, pady=22)
        self.label(top, "◈", 31, CYAN, True).pack(side="left", padx=(0, 12))
        brand = tk.Frame(top, bg=BG); brand.pack(side="left")
        self.label(brand, "PSP NEXUS", 22, WHITE, True).pack(anchor="w")
        self.label(brand, "YOUR PSP LIBRARY. ONE PLACE.", 8, CYAN, True).pack(anchor="w")
        self.button(top, "⚙ SETTINGS", self.settings_window).pack(side="right", padx=(10, 0))
        self.button(top, "+ ADD GAME", self.add_game, True).pack(side="right")
        hero = tk.Frame(self.root, bg="#0c2940", highlightbackground="#16405a", highlightthickness=1)
        hero.pack(fill="x", padx=25, pady=(0, 18))
        inner = tk.Frame(hero, bg="#0c2940"); inner.pack(fill="x", padx=25, pady=23)
        left = tk.Frame(inner, bg="#0c2940"); left.pack(side="left", fill="x", expand=True)
        self.label(left, "YOUR NEXT ADVENTURE STARTS HERE", 9, CYAN, True).pack(anchor="w")
        self.label(left, "PRESS START.", 29, WHITE, True).pack(anchor="w", pady=(5, 3))
        self.label(left, "Manage your own PSP backups and launch them with PPSSPP.", 10, "#b7cddd").pack(anchor="w", pady=(0, 14))
        self.button(left, "▶ PLAY SELECTED", self.play_selected, True).pack(anchor="w")
        badge = tk.Frame(inner, bg="#123650", padx=20, pady=18); badge.pack(side="right")
        self.label(badge, "NEXUS", 10, CYAN, True).pack()
        self.label(badge, "GAME CENTER", 12, WHITE, True).pack(pady=3)
        self.label(badge, "ISO • CSO • PBP • CHD", 8, MUTED).pack()
        bar = tk.Frame(self.root, bg=BG); bar.pack(fill="x", padx=25, pady=(0, 10))
        self.label(bar, "YOUR LIBRARY", 13, WHITE, True).pack(side="left")
        self.count = self.label(bar, "0 GAMES", 9, CYAN, True); self.count.pack(side="left", padx=12)
        self.query = tk.StringVar()
        self.query.trace_add("write", lambda *_: self.render())
        tk.Entry(bar, textvariable=self.query, bg=PANEL, fg=WHITE, insertbackground=WHITE,
                 relief="flat", font=("Segoe UI", 10), width=25).pack(side="right", ipady=9)
        self.canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        self.scroll = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.area = tk.Frame(self.canvas, bg=BG)
        self.area.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.window = self.canvas.create_window((0, 0), window=self.area, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window, width=e.width))
        self.canvas.pack(side="left", fill="both", expand=True, padx=(25, 0), pady=(0, 12))
        self.scroll.pack(side="right", fill="y", padx=(0, 25), pady=(0, 12))
        foot = tk.Frame(self.root, bg="#050c15"); foot.pack(fill="x", side="bottom")
        self.status = self.label(foot, "● READY", 9, "#53f0b0", True, bg="#050c15")
        self.status.pack(side="left", padx=25, pady=10)
        self.label(foot, "PPSSPP required • Use your own game backups", 9, MUTED, bg="#050c15").pack(side="right", padx=25)

    def scan(self):
        games = set(self.settings.get("games", []))
        folder = Path(self.settings.get("folder", ""))
        if folder.exists():
            try:
                games.update(str(p) for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in EXTS)
            except OSError:
                pass
        self.settings["games"] = sorted(games, key=str.lower)
        self.save(); self.render()

    def add_game(self):
        paths = filedialog.askopenfilenames(title="Add PSP game backups",
            filetypes=[("PSP game files", "*.iso *.cso *.pbp *.chd"), ("All files", "*.*")])
        if paths:
            self.settings["games"] = sorted(set(self.settings["games"] + list(paths)), key=str.lower)
            self.save(); self.render()

    def render(self):
        for child in self.area.winfo_children(): child.destroy()
        q = self.query.get().lower().strip()
        paths = [p for p in self.settings.get("games", []) if q in Path(p).name.lower() and Path(p).exists()]
        self.count.configure(text=f"{len(paths)} GAMES")
        if not paths:
            box = tk.Frame(self.area, bg=PANEL, padx=30, pady=35); box.pack(fill="x", pady=8)
            self.label(box, "◈", 30, CYAN, True).pack()
            self.label(box, "YOUR LIBRARY IS WAITING", 15, WHITE, True).pack(pady=7)
            self.label(box, "Add your own game backup or choose a games folder in Settings.", 10, MUTED).pack(pady=(0, 14))
            self.button(box, "+ ADD YOUR FIRST GAME", self.add_game, True).pack()
            return
        for i, path in enumerate(paths):
            card = tk.Frame(self.area, bg=PANEL, highlightbackground="#18344c", highlightthickness=1, padx=14, pady=13)
            card.grid(row=i//3, column=i%3, sticky="nsew", padx=(0, 12), pady=(0, 12))
            self.area.grid_columnconfigure(i%3, weight=1, uniform="cards")
            art = tk.Frame(card, bg="#0c2b43", height=75); art.pack(fill="x", pady=(0, 10)); art.pack_propagate(False)
            self.label(art, "◈", 30, CYAN, True).pack(expand=True)
            self.label(card, Path(path).stem, 11, WHITE, True, wraplength=230, anchor="w").pack(fill="x")
            self.label(card, f"{Path(path).suffix[1:].upper()} • PSP GAME", 8, CYAN, True, anchor="w").pack(fill="x", pady=(4, 10))
            row = tk.Frame(card, bg=PANEL); row.pack(fill="x")
            self.button(row, "▶ PLAY", lambda p=path: self.play(p), True).pack(side="left")
            self.button(row, "REMOVE", lambda p=path: self.remove(p)).pack(side="right")

    def play_selected(self):
        if self.selected and Path(self.selected).exists(): self.play(self.selected)
        else: messagebox.showinfo("Select a game", "Use PLAY on a game card to start it.")

    def play(self, path):
        exe = self.settings.get("ppsspp", "")
        if not exe or not Path(exe).exists():
            messagebox.showinfo("Set up PPSSPP", "Open Settings and select your PPSSPP executable (.exe).")
            self.settings_window()
            exe = self.settings.get("ppsspp", "")
        if not exe or not Path(exe).exists(): return
        try:
            subprocess.Popen([exe, path], cwd=str(Path(exe).parent))
            self.selected = path
            self.status.configure(text="● LAUNCHING: " + Path(path).stem[:35], fg=CYAN)
        except Exception as e:
            messagebox.showerror("Launch failed", str(e))

    def remove(self, path):
        if messagebox.askyesno("Remove game", "Remove this entry from PSP NEXUS? The actual game file will not be deleted."):
            self.settings["games"] = [p for p in self.settings["games"] if p != path]
            self.save(); self.render()

    def settings_window(self):
        win = tk.Toplevel(self.root); win.title("PSP NEXUS Settings"); win.geometry("650x330")
        win.configure(bg=BG); win.transient(self.root)
        self.label(win, "NEXUS SETTINGS", 18, WHITE, True).pack(anchor="w", padx=24, pady=(22, 6))
        self.label(win, "Choose PPSSPP and the folder containing your PSP backups.", 10, MUTED).pack(anchor="w", padx=24, pady=(0, 18))
        self.label(win, "PPSSPP EXECUTABLE", 9, CYAN, True).pack(anchor="w", padx=24)
        r1 = tk.Frame(win, bg=BG); r1.pack(fill="x", padx=24, pady=(5, 16))
        e1 = tk.Entry(r1, bg=PANEL, fg=WHITE, insertbackground=WHITE, relief="flat"); e1.pack(side="left", fill="x", expand=True, ipady=9)
        e1.insert(0, self.settings.get("ppsspp", ""))
        def browse_exe():
            p = filedialog.askopenfilename(title="Select PPSSPP executable", filetypes=[("Windows app", "*.exe")])
            if p: e1.delete(0, "end"); e1.insert(0, p)
        self.button(r1, "BROWSE", browse_exe).pack(side="left", padx=(8, 0))
        self.label(win, "GAME FOLDER", 9, CYAN, True).pack(anchor="w", padx=24)
        r2 = tk.Frame(win, bg=BG); r2.pack(fill="x", padx=24, pady=(5, 16))
        e2 = tk.Entry(r2, bg=PANEL, fg=WHITE, insertbackground=WHITE, relief="flat"); e2.pack(side="left", fill="x", expand=True, ipady=9)
        e2.insert(0, self.settings.get("folder", ""))
        def browse_folder():
            p = filedialog.askdirectory(title="Choose PSP games folder")
            if p: e2.delete(0, "end"); e2.insert(0, p)
        self.button(r2, "BROWSE", browse_folder).pack(side="left", padx=(8, 0))
        def save():
            self.settings["ppsspp"] = e1.get().strip(); self.settings["folder"] = e2.get().strip()
            self.save(); self.scan(); win.destroy()
        self.button(win, "SAVE SETTINGS", save, True).pack(anchor="e", padx=24, pady=(0, 20))

if __name__ == "__main__":
    root = tk.Tk()
    Nexus(root)
    root.mainloop()
