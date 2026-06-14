# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:14:48 2026

@author: jaudis
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import mysql.connector
import csv
import re
import os
import sys, importlib, types, threading
from datetime import datetime

# ─────────────────────────────────────────────
#  COULEURS & STYLE
# ─────────────────────────────────────────────
BG_DARK    = "#0f2418"
BG_PANEL   = "#1a3a25"
BG_CARD    = "#1e4a2e"
GREEN_MAIN = "#2ecc71"
GREEN_DARK = "#27ae60"
GREEN_LITE = "#a8e6bc"
GREEN_ACC  = "#00ff88"
TEXT_WHITE = "#f0fff4"
TEXT_GREY  = "#8aaa96"
TEXT_DARK  = "#0f2418"
RED_ERR    = "#e74c3c"
ORANGE_W   = "#f39c12"

FONT_TITLE  = ("Helvetica", 22, "bold")
FONT_SUB    = ("Helvetica", 13, "bold")
FONT_BODY   = ("Helvetica", 11)
FONT_SMALL  = ("Helvetica", 9)
FONT_MONO   = ("Courier", 10)

# ─────────────────────────────────────────────
#  CONNEXION BDD
# ─────────────────────────────────────────────
def get_connection():
    return mysql.connector.connect(host="localhost", user="root", password="", database="sae", port=3306)

def test_connection():
    try:
        conn = get_connection()
        conn.close()
        return True, "Connexion réussie"
    except Exception as e:
        return False, str(e)

# ─────────────────────────────────────────────
#  UTILITAIRES
# ─────────────────────────────────────────────
def changement(date, separateur):
    parts = date.split(separateur)
    if len(parts) == 3:
        jour, mois, annee = parts
        return f"{annee}-{mois}-{jour}"
    return date

def normaliser_nom(nom):
    nom = nom.strip().replace("_", " ").lower()
    return re.sub(r"\s+", " ", nom)

# ─────────────────────────────────────────────
#  WIDGET HELPERS
# ─────────────────────────────────────────────
def styled_button(parent, text, command, color=GREEN_MAIN, fg=TEXT_DARK, width=18):
    btn = tk.Button(parent, text=text, command=command,
                    bg=color, fg=fg, font=("Helvetica", 10, "bold"),
                    relief="flat", bd=0, padx=10, pady=6,
                    activebackground=GREEN_DARK, activeforeground=TEXT_WHITE,
                    cursor="hand2", width=width)
    btn.bind("<Enter>", lambda e: btn.config(bg=GREEN_DARK, fg=TEXT_WHITE))
    btn.bind("<Leave>", lambda e: btn.config(bg=color, fg=fg))
    return btn

def make_treeview(parent, columns, height=16):
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Green.Treeview",
                    background=BG_CARD, foreground=TEXT_WHITE,
                    fieldbackground=BG_CARD, rowheight=26,
                    font=FONT_BODY)
    style.configure("Green.Treeview.Heading",
                    background=BG_PANEL, foreground=GREEN_ACC,
                    font=("Helvetica", 10, "bold"), relief="flat")
    style.map("Green.Treeview",
              background=[("selected", GREEN_DARK)],
              foreground=[("selected", TEXT_WHITE)])

    frame = tk.Frame(parent, bg=BG_DARK)
    tv = ttk.Treeview(frame, columns=columns, show="headings",
                      style="Green.Treeview", height=height)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tv.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tv.xview)
    tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tv.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    for col in columns:
        tv.heading(col, text=col)
        tv.column(col, minwidth=80, width=120, anchor="center")
    return frame, tv

def section_label(parent, text):
    tk.Label(parent, text=text, bg=BG_PANEL, fg=GREEN_ACC,
             font=FONT_SUB).pack(anchor="w", padx=10, pady=(10, 4))

def card_frame(parent, **kwargs):
    return tk.Frame(parent, bg=BG_CARD, relief="flat",
                    highlightbackground=GREEN_DARK, highlightthickness=1, **kwargs)


# ─────────────────────────────────────────────
#  CALENDRIER POPUP (natif Tkinter)
# ─────────────────────────────────────────────
class DatePickerPopup(tk.Toplevel):
    """Mini-calendrier popup qui retourne une date YYYY-MM-DD dans un Entry."""

    MONTHS_FR = ["Janvier","Février","Mars","Avril","Mai","Juin",
                 "Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

    def __init__(self, parent, entry_widget):
        super().__init__(parent)
        self.entry = entry_widget
        self.overrideredirect(True)          # pas de barre de titre
        self.configure(bg=BG_PANEL)
        self.attributes("-topmost", True)

        # Date courante
        today = datetime.today()
        # Si l'entry a déjà une date valide, on part de là
        try:
            existing = datetime.strptime(entry_widget.get().strip(), "%Y-%m-%d")
            self._year  = existing.year
            self._month = existing.month
        except Exception:
            self._year  = today.year
            self._month = today.month
        self._today = today

        self._build()
        self._position(parent, entry_widget)
        self.grab_set()
        self.focus_set()
        self.bind("<FocusOut>", lambda e: self._close_if_outside())
        self.bind("<Escape>", lambda e: self.destroy())

    def _position(self, parent, widget):
        self.update_idletasks()
        try:
            x = widget.winfo_rootx()
            y = widget.winfo_rooty() + widget.winfo_height() + 2
        except Exception:
            x, y = 200, 200
        sw = self.winfo_screenwidth()
        w  = self.winfo_reqwidth()
        if x + w > sw:
            x = sw - w - 4
        self.geometry(f"+{x}+{y}")

    def _close_if_outside(self):
        try:
            wx = self.winfo_pointerx()
            wy = self.winfo_pointery()
            rx, ry = self.winfo_rootx(), self.winfo_rooty()
            rw, rh = self.winfo_width(), self.winfo_height()
            if not (rx <= wx <= rx+rw and ry <= wy <= ry+rh):
                self.destroy()
        except Exception:
            self.destroy()

    def _build(self):
        for w in self.winfo_children():
            w.destroy()

        # ── Header navigation
        hdr = tk.Frame(self, bg=BG_PANEL)
        hdr.pack(fill="x", padx=4, pady=4)

        tk.Button(hdr, text="◀", bg=BG_PANEL, fg=GREEN_ACC, relief="flat",
                  font=("Helvetica",11,"bold"), cursor="hand2",
                  command=self._prev_month).pack(side="left")
        tk.Button(hdr, text="◀◀", bg=BG_PANEL, fg=TEXT_GREY, relief="flat",
                  font=("Helvetica",9), cursor="hand2",
                  command=self._prev_year).pack(side="left")

        self._header_lbl = tk.Label(hdr,
            text=f"{self.MONTHS_FR[self._month-1]} {self._year}",
            bg=BG_PANEL, fg=TEXT_WHITE, font=("Helvetica",11,"bold"), width=18)
        self._header_lbl.pack(side="left", expand=True)

        tk.Button(hdr, text="▶▶", bg=BG_PANEL, fg=TEXT_GREY, relief="flat",
                  font=("Helvetica",9), cursor="hand2",
                  command=self._next_year).pack(side="right")
        tk.Button(hdr, text="▶", bg=BG_PANEL, fg=GREEN_ACC, relief="flat",
                  font=("Helvetica",11,"bold"), cursor="hand2",
                  command=self._next_month).pack(side="right")

        # ── Jours de la semaine
        days_hdr = tk.Frame(self, bg=BG_CARD)
        days_hdr.pack(fill="x", padx=4)
        for d in ["Lu","Ma","Me","Je","Ve","Sa","Di"]:
            tk.Label(days_hdr, text=d, bg=BG_CARD, fg=GREEN_ACC,
                     font=("Helvetica",9,"bold"), width=3).pack(side="left", padx=1)

        # ── Grille des jours
        self._grid_frame = tk.Frame(self, bg=BG_PANEL)
        self._grid_frame.pack(padx=4, pady=4)
        self._fill_grid()

        # ── Bouton Aujourd'hui
        tk.Button(self, text="Aujourd'hui", bg=GREEN_DARK, fg=TEXT_WHITE,
                  relief="flat", font=("Helvetica",9,"bold"), cursor="hand2",
                  command=self._pick_today).pack(pady=(0,4))

    def _fill_grid(self):
        for w in self._grid_frame.winfo_children():
            w.destroy()

        import calendar
        cal = calendar.monthcalendar(self._year, self._month)
        today = self._today

        for week in cal:
            row_frame = tk.Frame(self._grid_frame, bg=BG_PANEL)
            row_frame.pack()
            for day in week:
                if day == 0:
                    tk.Label(row_frame, text="  ", bg=BG_PANEL, width=3).pack(side="left", padx=1, pady=1)
                else:
                    is_today = (day == today.day and self._month == today.month and self._year == today.year)
                    bg = GREEN_DARK if is_today else BG_CARD
                    fg = TEXT_WHITE
                    btn = tk.Button(row_frame, text=str(day), width=3,
                                    bg=bg, fg=fg, relief="flat",
                                    font=("Helvetica", 9),
                                    activebackground=GREEN_MAIN,
                                    cursor="hand2",
                                    command=lambda d=day: self._pick(d))
                    btn.pack(side="left", padx=1, pady=1)

    def _prev_month(self):
        self._month -= 1
        if self._month < 1:
            self._month = 12
            self._year -= 1
        self._refresh()

    def _next_month(self):
        self._month += 1
        if self._month > 12:
            self._month = 1
            self._year += 1
        self._refresh()

    def _prev_year(self):
        self._year -= 1
        self._refresh()

    def _next_year(self):
        self._year += 1
        self._refresh()

    def _refresh(self):
        self._header_lbl.config(text=f"{self.MONTHS_FR[self._month-1]} {self._year}")
        self._fill_grid()

    def _pick(self, day):
        date_str = f"{self._year:04d}-{self._month:02d}-{day:02d}"
        self.entry.config(state="normal")
        self.entry.delete(0, "end")
        self.entry.insert(0, date_str)
        self.destroy()

    def _pick_today(self):
        t = self._today
        self._year, self._month = t.year, t.month
        self._pick(t.day)

# ─────────────────────────────────────────────
#  APPLICATION PRINCIPALE
# ─────────────────────────────────────────────
class GreenSDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GreenSD — Gestion Logistique")
        self.geometry("1280x780")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        self._build_header()
        self._build_notebook()
        self._check_connection_startup()

    # ── HEADER ──────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=BG_PANEL, height=60)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🌿 GreenSD", bg=BG_PANEL, fg=GREEN_ACC,
                 font=("Helvetica", 20, "bold")).pack(side="left", padx=20, pady=10)
        tk.Label(hdr, text="Système de Gestion Logistique", bg=BG_PANEL,
                 fg=TEXT_GREY, font=FONT_BODY).pack(side="left", pady=10)
        self.conn_label = tk.Label(hdr, text="● Déconnecté", bg=BG_PANEL,
                                   fg=RED_ERR, font=FONT_SMALL)
        self.conn_label.pack(side="right", padx=20)

    # ── NOTEBOOK ────────────────────────────
    def _build_notebook(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("GreenNB.TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("GreenNB.TNotebook.Tab",
                        background=BG_PANEL, foreground=TEXT_GREY,
                        font=("Helvetica", 11, "bold"), padding=[16, 8])
        style.map("GreenNB.TNotebook.Tab",
                  background=[("selected", BG_CARD)],
                  foreground=[("selected", GREEN_ACC)])

        nb = ttk.Notebook(self, style="GreenNB.TNotebook")
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        # Tabs
        self.tab_data   = self._make_tab(nb, "📋 Données")
        self.tab_crud   = self._make_tab(nb, "✏️ Modifier")
        self.tab_sql    = self._make_tab(nb, "🔍 Requêtes SQL")
        self.tab_views  = self._make_tab(nb, "👁 Vues SQL")
        self.tab_import = self._make_tab(nb, "📥 Import CSV")

        nb.add(self.tab_data,   text="📋  Données")
        nb.add(self.tab_crud,   text="✏️  Modifier")
        nb.add(self.tab_sql,    text="🔍  Requêtes SQL")
        nb.add(self.tab_views,  text="👁  Vues SQL")
        nb.add(self.tab_import, text="📥  Import CSV")

        self._build_tab_data()
        self._build_tab_crud()
        self._build_tab_sql()
        self._build_tab_views()
        self._build_tab_import()

    def _make_tab(self, nb, name):
        f = tk.Frame(nb, bg=BG_DARK)
        return f

    # ── CONNEXION CHECK ─────────────────────
    def _check_connection_startup(self):
        ok, msg = test_connection()
        if ok:
            self.conn_label.config(text="● Connecté (localhost/sae)", fg=GREEN_ACC)
        else:
            self.conn_label.config(text=f"● Erreur : {msg[:50]}", fg=RED_ERR)

    # ══════════════════════════════════════════
    #  ONGLET 1 : DONNÉES (visualisation tables)
    # ══════════════════════════════════════════
    def _build_tab_data(self):
        parent = self.tab_data

        # Sidebar gauche
        sidebar = tk.Frame(parent, bg=BG_PANEL, width=200)
        sidebar.pack(side="left", fill="y", padx=(0, 4), pady=0)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="📋 Tables", bg=BG_PANEL, fg=GREEN_ACC,
                 font=FONT_SUB).pack(pady=(20, 8), padx=10, anchor="w")

        tables = ["client", "livreur", "partenaire", "tournee",
                  "typevehicule", "livraisonentrante", "livraisonsortante",
                  "emissionco2", "collecter"]

        self.data_table_var = tk.StringVar(value=tables[0])

        for tbl in tables:
            rb = tk.Radiobutton(sidebar, text=tbl.capitalize(), variable=self.data_table_var,
                                value=tbl, bg=BG_PANEL, fg=TEXT_WHITE,
                                selectcolor=BG_CARD, activebackground=BG_PANEL,
                                activeforeground=GREEN_ACC, font=FONT_BODY,
                                indicatoron=False, relief="flat",
                                padx=14, pady=6, anchor="w", width=16,
                                command=self._load_table)
            rb.pack(fill="x", padx=8, pady=2)
            rb.bind("<Enter>", lambda e, w=rb: w.config(fg=GREEN_ACC))
            rb.bind("<Leave>", lambda e, w=rb: w.config(fg=TEXT_WHITE))

        # Zone principale
        main = tk.Frame(parent, bg=BG_DARK)
        main.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        # Titre + refresh
        top = tk.Frame(main, bg=BG_DARK)
        top.pack(fill="x", pady=(0, 8))
        self.data_title = tk.Label(top, text="Table : client", bg=BG_DARK,
                                   fg=GREEN_ACC, font=FONT_SUB)
        self.data_title.pack(side="left")
        self.data_count = tk.Label(top, text="", bg=BG_DARK, fg=TEXT_GREY, font=FONT_SMALL)
        self.data_count.pack(side="left", padx=12)
        styled_button(top, "🔄 Rafraîchir", self._load_table, width=14).pack(side="right")

        # Treeview placeholder (rebuilt on load)
        self.data_tv_frame = tk.Frame(main, bg=BG_DARK)
        self.data_tv_frame.pack(fill="both", expand=True)
        self.data_tv = None

        self._load_table()

    def _load_table(self):
        tbl = self.data_table_var.get()
        self.data_title.config(text=f"Table : {tbl}")
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM `{tbl}` LIMIT 500")
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            conn.close()

            # Clear and rebuild treeview
            for w in self.data_tv_frame.winfo_children():
                w.destroy()
            tv_frame, tv = make_treeview(self.data_tv_frame, cols, height=22)
            tv_frame.pack(fill="both", expand=True)
            self.data_tv = tv
            for col in cols:
                tv.heading(col, text=col)
                tv.column(col, width=max(100, len(col)*10), anchor="center")
            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                tv.insert("", "end", values=[str(v) if v is not None else "" for v in row], tags=(tag,))
            tv.tag_configure("even", background=BG_CARD)
            tv.tag_configure("odd",  background=BG_PANEL)
            self.data_count.config(text=f"{len(rows)} ligne(s)")
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    # ══════════════════════════════════════════
    #  ONGLET 2 : CRUD (Insérer / Modifier / Supprimer)
    # ══════════════════════════════════════════
    def _build_tab_crud(self):
        parent = self.tab_crud

        left = tk.Frame(parent, bg=BG_PANEL, width=220)
        left.pack(side="left", fill="y", padx=(0, 4))
        left.pack_propagate(False)

        tk.Label(left, text="✏️ Table cible", bg=BG_PANEL,
                 fg=GREEN_ACC, font=FONT_SUB).pack(pady=(20, 8), padx=10, anchor="w")

        tables = ["client", "livreur", "partenaire", "tournee",
                  "typevehicule", "livraisonentrante", "livraisonsortante",
                  "emissionco2", "collecter"]
        self.crud_table_var = tk.StringVar(value="livreur")

        for tbl in tables:
            rb = tk.Radiobutton(left, text=tbl.capitalize(), variable=self.crud_table_var,
                                value=tbl, bg=BG_PANEL, fg=TEXT_WHITE,
                                selectcolor=BG_CARD, activebackground=BG_PANEL,
                                activeforeground=GREEN_ACC, font=FONT_BODY,
                                indicatoron=False, relief="flat",
                                padx=14, pady=6, anchor="w", width=18,
                                command=self._crud_load_fields)
            rb.pack(fill="x", padx=8, pady=2)

        right = tk.Frame(parent, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        # ── Formulaire INSERT/UPDATE
        form_card = card_frame(right)
        form_card.pack(fill="x", pady=(0, 10), padx=4)

        tk.Label(form_card, text="Formulaire", bg=BG_CARD, fg=GREEN_ACC,
                 font=FONT_SUB).pack(anchor="w", padx=10, pady=(8, 4))

        self.crud_fields_frame = tk.Frame(form_card, bg=BG_CARD)
        self.crud_fields_frame.pack(fill="x", padx=10, pady=4)

        self.crud_entries = {}

        btn_row = tk.Frame(form_card, bg=BG_CARD)
        btn_row.pack(fill="x", padx=10, pady=8)
        styled_button(btn_row, "➕ Insérer", self._crud_insert, width=14).pack(side="left", padx=4)
        styled_button(btn_row, "💾 Modifier", self._crud_update, color=ORANGE_W, fg=TEXT_DARK, width=14).pack(side="left", padx=4)
        styled_button(btn_row, "🗑 Supprimer", self._crud_delete, color=RED_ERR, fg=TEXT_WHITE, width=14).pack(side="left", padx=4)
        styled_button(btn_row, "🔄 Rafraîchir", self._crud_refresh_tv, color=BG_PANEL, fg=TEXT_WHITE, width=14).pack(side="right", padx=4)

        self.crud_pk_label = tk.Label(form_card,
                                      text="Cliquez sur une ligne pour la sélectionner",
                                      bg=BG_CARD, fg=TEXT_GREY, font=FONT_SMALL)
        self.crud_pk_label.pack(anchor="w", padx=10, pady=(0, 6))

        # ── Treeview résultat
        tv_label = tk.Label(right, text="Données actuelles", bg=BG_DARK,
                            fg=TEXT_GREY, font=FONT_SMALL)
        tv_label.pack(anchor="w", padx=4)
        self.crud_tv_container = tk.Frame(right, bg=BG_DARK)
        self.crud_tv_container.pack(fill="both", expand=True, padx=4)
        self.crud_tv = None
        self.crud_selected_pk = None   # valeur PK de la ligne sélectionnée
        self.crud_selected_row = None  # tuple complet

        self._crud_load_fields()

    def _get_columns(self, table):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"DESCRIBE `{table}`")
            cols = cur.fetchall()
            conn.close()
            return cols  # (Field, Type, Null, Key, Default, Extra)
        except:
            return []

    def _crud_load_fields(self):
        tbl = self.crud_table_var.get()
        cols = self._get_columns(tbl)
        for w in self.crud_fields_frame.winfo_children():
            w.destroy()
        self.crud_entries = {}
        self.crud_selected_pk = None
        self.crud_selected_row = None
        if hasattr(self, "crud_pk_label"):
            self.crud_pk_label.config(
                text="Cliquez sur une ligne pour la sélectionner", fg=TEXT_GREY)

        for i, col in enumerate(cols):
            field, ftype, null, key, default, extra = col
            is_date = "date" in str(ftype).lower()
            grid_row = i // 3
            col_idx  = (i % 3) * 2

            lbl = tk.Label(self.crud_fields_frame, text=field,
                           bg=BG_CARD, fg=GREEN_LITE, font=FONT_SMALL)
            lbl.grid(row=grid_row, column=col_idx, sticky="w", padx=(8, 2), pady=4)

            # Conteneur entry + bouton calendrier si date
            cell = tk.Frame(self.crud_fields_frame, bg=BG_CARD)
            cell.grid(row=grid_row, column=col_idx+1, padx=(0, 12), pady=4, sticky="w")

            ent = tk.Entry(cell, bg=BG_DARK, fg=TEXT_WHITE,
                           insertbackground=GREEN_ACC, font=FONT_BODY,
                           relief="flat", bd=4, width=12 if is_date else 16)
            ent.pack(side="left")

            if is_date:
                cal_btn = tk.Button(cell, text="📅", bg=BG_PANEL, fg=GREEN_ACC,
                                    relief="flat", font=("Helvetica", 10),
                                    cursor="hand2", bd=0,
                                    command=lambda e=ent: DatePickerPopup(self, e))
                cal_btn.pack(side="left", padx=(2, 0))
                # Placeholder hint
                ent.insert(0, "YYYY-MM-DD")
                ent.config(fg=TEXT_GREY)
                def _clear_hint(event, e=ent):
                    if e.get() == "YYYY-MM-DD":
                        e.delete(0, "end")
                        e.config(fg=TEXT_WHITE)
                def _restore_hint(event, e=ent):
                    if e.get().strip() == "":
                        e.insert(0, "YYYY-MM-DD")
                        e.config(fg=TEXT_GREY)
                ent.bind("<FocusIn>",  _clear_hint)
                ent.bind("<FocusOut>", _restore_hint)

            if extra == "auto_increment":
                ent.delete(0, "end")
                ent.insert(0, "AUTO")
                ent.config(state="disabled", fg=TEXT_GREY)

            self.crud_entries[field] = (ent, extra, is_date)

        self._crud_refresh_tv()

    def _crud_get_values(self, skip_auto=True):
        vals = {}
        for field, entry_data in self.crud_entries.items():
            ent, extra = entry_data[0], entry_data[1]
            is_date = entry_data[2] if len(entry_data) > 2 else False
            if skip_auto and extra == "auto_increment":
                continue
            v = ent.get().strip()
            # Ignorer le placeholder date
            if is_date and v == "YYYY-MM-DD":
                v = None
            vals[field] = v if v not in ("", "AUTO") else None
        return vals

    def _crud_insert(self):
        tbl = self.crud_table_var.get()
        vals = self._crud_get_values(skip_auto=True)
        if not vals:
            return
        cols_str = ", ".join(f"`{k}`" for k in vals)
        placeholders = ", ".join(["%s"] * len(vals))
        sql = f"INSERT INTO `{tbl}` ({cols_str}) VALUES ({placeholders})"
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(sql, list(vals.values()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", f"✅ Ligne insérée dans {tbl}")
            self._crud_refresh_tv()
        except Exception as e:
            messagebox.showerror("Erreur INSERT", str(e))

    def _get_fk_references(self, tbl, pk_val):
        """Cherche toutes les tables qui référencent la PK de cette ligne."""
        refs = []
        try:
            conn = get_connection()
            cur = conn.cursor()
            pk_col = self._get_columns(tbl)[0][0]
            cur.execute("""
                SELECT kcu.TABLE_NAME, kcu.COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE kcu
                JOIN information_schema.REFERENTIAL_CONSTRAINTS rc
                    ON rc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                    AND rc.CONSTRAINT_SCHEMA = kcu.TABLE_SCHEMA
                WHERE rc.REFERENCED_TABLE_NAME = %s
                  AND kcu.REFERENCED_COLUMN_NAME = %s
                  AND kcu.TABLE_SCHEMA = DATABASE()
            """, (tbl, pk_col))
            fk_rows = cur.fetchall()
            for (child_table, child_col) in fk_rows:
                cur.execute(f"SELECT COUNT(*) FROM `{child_table}` WHERE `{child_col}` = %s", (pk_val,))
                count = cur.fetchone()[0]
                if count > 0:
                    refs.append((child_table, child_col, count))
            conn.close()
        except Exception:
            pass
        return refs

    def _crud_delete(self):
        tbl = self.crud_table_var.get()
        if self.crud_selected_pk is None:
            messagebox.showwarning("Attention", "Cliquez d'abord sur une ligne du tableau pour la sélectionner.")
            return
        cols = self._get_columns(tbl)
        pk_col = cols[0][0]
        pk_val = self.crud_selected_pk

        # Vérifier les références dans d'autres tables
        refs = self._get_fk_references(tbl, pk_val)
        if refs:
            detail = "\n".join(
                f"  • {child_table}.{child_col} : {count} ligne(s) liée(s)"
                for (child_table, child_col, count) in refs
            )
            messagebox.showerror(
                "Suppression impossible",
                f"Cette ligne est référencée dans d'autres tables :\n\n{detail}\n\n"
                "Supprimez d'abord ces lignes liées avant de continuer."
            )
            return

        if not messagebox.askyesno("Confirmer", f"Supprimer la ligne où {pk_col} = {pk_val} ?"):
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM `{tbl}` WHERE `{pk_col}` = %s", (pk_val,))
            conn.commit()
            conn.close()
            self.crud_selected_pk = None
            self.crud_selected_row = None
            self.crud_pk_label.config(text="Cliquez sur une ligne pour la sélectionner", fg=TEXT_GREY)
            messagebox.showinfo("Succès", "Ligne supprimée.")
            self._crud_refresh_tv()
        except Exception as e:
            messagebox.showerror("Erreur DELETE", str(e))

    def _crud_update(self):
        tbl = self.crud_table_var.get()
        if self.crud_selected_pk is None:
            messagebox.showwarning("Attention", "Cliquez d'abord sur une ligne du tableau pour la sélectionner.")
            return
        cols = self._get_columns(tbl)
        pk_col = cols[0][0]
        pk_val = self.crud_selected_pk
        vals = self._crud_get_values(skip_auto=True)
        if not vals:
            return
        set_str = ", ".join(f"`{k}` = %s" for k in vals)
        sql = f"UPDATE `{tbl}` SET {set_str} WHERE `{pk_col}` = %s"
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(sql, list(vals.values()) + [pk_val])
            conn.commit()
            conn.close()
            self.crud_selected_pk = None
            self.crud_selected_row = None
            self.crud_pk_label.config(text="Cliquez sur une ligne pour la sélectionner", fg=TEXT_GREY)
            messagebox.showinfo("Succès", "💾 Ligne modifiée.")
            self._crud_refresh_tv()
        except Exception as e:
            messagebox.showerror("Erreur UPDATE", str(e))

    def _crud_refresh_tv(self):
        tbl = self.crud_table_var.get()
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM `{tbl}` LIMIT 200")
            rows = cur.fetchall()
            cols_info = self._get_columns(tbl)
            cols = [c[0] for c in cols_info]
            conn.close()

            for w in self.crud_tv_container.winfo_children():
                w.destroy()
            tv_frame, tv = make_treeview(self.crud_tv_container, cols, height=10)
            tv_frame.pack(fill="both", expand=True)
            self.crud_tv = tv
            for col in cols:
                tv.heading(col, text=col)
            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                tv.insert("", "end", values=[str(v) if v is not None else "" for v in row], tags=(tag,))
            tv.tag_configure("even", background=BG_CARD)
            tv.tag_configure("odd",  background=BG_PANEL)

            # Clic sur une ligne : stocke la PK et pré-remplit le formulaire
            def on_select(event, tv=tv, cols_info=cols_info):
                sel = tv.selection()
                if not sel:
                    return   # ne jamais effacer la sélection sur un clic vide
                vals = tv.item(sel[0], "values")
                if not vals:
                    return
                self.crud_selected_pk = vals[0]
                self.crud_selected_row = vals
                self.crud_pk_label.config(
                    text=f"✔ Ligne sélectionnée : {cols_info[0][0]} = {vals[0]}",
                    fg=GREEN_ACC)
                for i, col_info in enumerate(cols_info):
                    field = col_info[0]
                    if field in self.crud_entries:
                        entry_data = self.crud_entries[field]
                        ent, extra = entry_data[0], entry_data[1]
                        if extra != "auto_increment":
                            ent.config(state="normal", fg=TEXT_WHITE)
                            ent.delete(0, "end")
                            if i < len(vals):
                                ent.insert(0, vals[i])
            tv.bind("<<TreeviewSelect>>", on_select)
            # Réinitialiser l'indicateur visuel quand on change de table
            self.crud_pk_label.config(
                text="Cliquez sur une ligne pour la sélectionner", fg=TEXT_GREY)
        except Exception as e:
            messagebox.showerror("Erreur DB", str(e))

    # ══════════════════════════════════════════
    #  ONGLET 3 : REQUÊTES SQL
    # ══════════════════════════════════════════
    def _build_tab_sql(self):
        parent = self.tab_sql

        REQUETES = {
            "Nb livraisons par client": """
SELECT C.idClient, C.villeClient, COUNT(LS.idLivraisonS) AS nb_livraisons
FROM Client C
JOIN LivraisonSortante LS ON LS.idClient = C.idClient
GROUP BY C.idClient, C.villeClient
ORDER BY nb_livraisons DESC""",

            "Livreurs avec +3 livraisons": """
SELECT L.idLivreur, L.PrenomLivreur, L.nomLivreur, COUNT(T.idTournee) AS nb_livraisons
FROM Livreur L
JOIN Tournee T ON T.idLivreur = L.idLivreur
GROUP BY L.idLivreur, L.PrenomLivreur, L.nomLivreur
HAVING COUNT(T.idTournee) > 3
ORDER BY nb_livraisons DESC""",

            "Distance totale par tournée": """
SELECT T.idTournee, T.DateTournee, SUM(T.DistanceEstimeeKm) AS distance_totale_km
FROM Tournee T
GROUP BY T.idTournee, T.DateTournee
ORDER BY distance_totale_km DESC""",

            "Marge autonomie vs distance": """
SELECT T.idTournee, T.DateTournee, T.DistanceEstimeeKm,
       TV.LibelleTypeVehicule, TV.AutonomieKm,
       (TV.AutonomieKm - T.DistanceEstimeeKm) AS marge_autonomie_km
FROM Tournee T
JOIN TypeVehicule TV ON TV.idTypeVehicule = T.idTypeVehicule
ORDER BY marge_autonomie_km ASC""",

            "Livreurs sans livraison": """
SELECT idLivreur, PrenomLivreur, nomLivreur
FROM LIVREUR
WHERE idLivreur NOT IN (SELECT idLivreur FROM TOURNEE)""",

            "Émissions CO2 par véhicule/année": """
SELECT TV.LibelleTypeVehicule, EC.annee, SUM(EC.QuantiteCo2) AS total_co2
FROM TYPEVEHICULE TV
JOIN EMISSIONCO2 EC USING (idTypeVehicule)
GROUP BY TV.idTypeVehicule, TV.LibelleTypeVehicule, EC.annee
ORDER BY total_co2 DESC""",

            "Tournées + livreurs associés": """
SELECT L.idLivreur, L.PrenomLivreur, L.nomLivreur,
       T.idTournee, T.DateTournee, T.DistanceEstimeeKm
FROM LIVREUR L
JOIN TOURNEE T ON T.idLivreur = L.idLivreur
ORDER BY L.nomLivreur""",

            "Nb tournées + distance totale / livreur": """
SELECT L.idLivreur, L.PrenomLivreur, L.nomLivreur,
       COUNT(T.idTournee) AS nb_tournees,
       SUM(T.DistanceEstimeeKm) AS distance_totale_km
FROM LIVREUR L
JOIN TOURNEE T ON T.idLivreur = L.idLivreur
GROUP BY L.idLivreur, L.PrenomLivreur, L.nomLivreur
ORDER BY distance_totale_km DESC""",

            "Livraisons entrantes par partenaire": """
SELECT P.nomPartenaire, P.villePartenaire, COUNT(LE.idLivraisonEntrante) AS nb_livraisons,
       SUM(LE.nbColis) AS total_colis
FROM Partenaire P
JOIN LivraisonEntrante LE ON LE.idPartenaire = P.idPartenaire
GROUP BY P.idPartenaire, P.nomPartenaire, P.villePartenaire
ORDER BY total_colis DESC""",

            "Véhicules dépassant leur autonomie": """
SELECT T.idTournee, T.DateTournee, T.DistanceEstimeeKm,
       TV.LibelleTypeVehicule, TV.AutonomieKm
FROM Tournee T
JOIN TypeVehicule TV ON TV.idTypeVehicule = T.idTypeVehicule
WHERE T.DistanceEstimeeKm > TV.AutonomieKm
ORDER BY (T.DistanceEstimeeKm - TV.AutonomieKm) DESC""",
        }

        left = tk.Frame(parent, bg=BG_PANEL, width=230)
        left.pack(side="left", fill="y", padx=(0, 4))
        left.pack_propagate(False)

        tk.Label(left, text="🔍 Requêtes prédéfinies", bg=BG_PANEL,
                 fg=GREEN_ACC, font=("Helvetica", 10, "bold")).pack(pady=(14, 6), padx=10, anchor="w")

        self.sql_query_var = tk.StringVar()

        for name in REQUETES:
            btn = tk.Button(left, text=name, bg=BG_PANEL, fg=TEXT_WHITE,
                            font=FONT_SMALL, relief="flat", anchor="w",
                            padx=10, pady=5, wraplength=200,
                            command=lambda n=name, r=REQUETES: self._sql_load(n, r))
            btn.pack(fill="x", padx=6, pady=2)
            btn.bind("<Enter>", lambda e, w=btn: w.config(bg=BG_CARD, fg=GREEN_ACC))
            btn.bind("<Leave>", lambda e, w=btn: w.config(bg=BG_PANEL, fg=TEXT_WHITE))

        right = tk.Frame(parent, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        # Éditeur SQL
        edit_frame = card_frame(right)
        edit_frame.pack(fill="x", pady=(0, 8))

        tk.Label(edit_frame, text="Éditeur SQL", bg=BG_CARD, fg=GREEN_ACC,
                 font=FONT_SUB).pack(anchor="w", padx=10, pady=(8, 4))

        self.sql_editor = tk.Text(edit_frame, height=7, bg=BG_DARK, fg=GREEN_LITE,
                                  insertbackground=GREEN_ACC, font=FONT_MONO,
                                  relief="flat", padx=8, pady=6,
                                  selectbackground=GREEN_DARK)
        self.sql_editor.pack(fill="x", padx=10, pady=(0, 4))

        btn_row = tk.Frame(edit_frame, bg=BG_CARD)
        btn_row.pack(fill="x", padx=10, pady=(0, 8))
        styled_button(btn_row, "▶ Exécuter", self._sql_run, width=14).pack(side="left", padx=4)
        styled_button(btn_row, "🗑 Effacer", lambda: self.sql_editor.delete("1.0", "end"),
                      color=BG_PANEL, fg=TEXT_WHITE, width=14).pack(side="left", padx=4)

        self.sql_result_label = tk.Label(right, text="", bg=BG_DARK,
                                         fg=TEXT_GREY, font=FONT_SMALL)
        self.sql_result_label.pack(anchor="w", padx=4)

        self.sql_tv_container = tk.Frame(right, bg=BG_DARK)
        self.sql_tv_container.pack(fill="both", expand=True, padx=4)
        self.sql_tv = None

        self.REQUETES = REQUETES

    def _sql_load(self, name, requetes):
        self.sql_editor.delete("1.0", "end")
        self.sql_editor.insert("1.0", requetes[name].strip())
        self.sql_result_label.config(text=f"Requête : {name}")

    def _sql_run(self):
        sql = self.sql_editor.get("1.0", "end").strip()
        if not sql:
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(sql)

            if cur.description:
                rows = cur.fetchall()
                cols = [d[0] for d in cur.description]
                conn.close()

                for w in self.sql_tv_container.winfo_children():
                    w.destroy()
                tv_frame, tv = make_treeview(self.sql_tv_container, cols, height=14)
                tv_frame.pack(fill="both", expand=True)
                self.sql_tv = tv
                for col in cols:
                    tv.heading(col, text=col)
                for i, row in enumerate(rows):
                    tag = "even" if i % 2 == 0 else "odd"
                    tv.insert("", "end", values=[str(v) if v is not None else "" for v in row], tags=(tag,))
                tv.tag_configure("even", background=BG_CARD)
                tv.tag_configure("odd",  background=BG_PANEL)
                self.sql_result_label.config(
                    text=f"✅ {len(rows)} résultat(s)", fg=GREEN_ACC)
            else:
                conn.commit()
                conn.close()
                self.sql_result_label.config(
                    text=f"✅ Requête exécutée ({cur.rowcount} ligne(s) affectée(s))", fg=GREEN_ACC)
        except Exception as e:
            self.sql_result_label.config(text=f"❌ {str(e)[:80]}", fg=RED_ERR)

    # ══════════════════════════════════════════
    #  ONGLET 4 : VUES SQL
    # ══════════════════════════════════════════
    def _build_tab_views(self):
        parent = self.tab_views

        VUES = {
            "Vue_Vehicule_Emissions": {
                "desc": "Émissions CO2 par modèle de véhicule et par année",
                "create": """CREATE OR REPLACE VIEW Vue_Vehicule_Emissions AS
SELECT TV.idTypeVehicule, TV.LibelleTypeVehicule, EC.annee, SUM(EC.QuantiteCo2) AS total_co2
FROM TYPEVEHICULE TV
JOIN EMISSIONCO2 EC USING (idTypeVehicule)
GROUP BY TV.idTypeVehicule, TV.LibelleTypeVehicule, EC.annee""",
                "select": "SELECT * FROM Vue_Vehicule_Emissions ORDER BY annee DESC, total_co2 DESC"
            },
            "Vue_Tournees_Livreurs": {
                "desc": "Association tournées ↔ livreurs avec distances",
                "create": """CREATE OR REPLACE VIEW Vue_Tournees_Livreurs AS
SELECT L.idLivreur, L.PrenomLivreur, L.nomLivreur, T.idTournee, T.DateTournee, T.DistanceEstimeeKm
FROM LIVREUR L
JOIN TOURNEE T ON T.idLivreur = L.idLivreur
GROUP BY L.idLivreur, L.PrenomLivreur, L.nomLivreur, T.idTournee, T.DateTournee, T.DistanceEstimeeKm""",
                "select": """SELECT idLivreur, PrenomLivreur, nomLivreur,
       COUNT(idTournee) AS nb_tournees, SUM(DistanceEstimeeKm) AS distance_totale_km
FROM Vue_Tournees_Livreurs
GROUP BY idLivreur, PrenomLivreur, nomLivreur
ORDER BY distance_totale_km DESC"""
            }
        }

        top = tk.Frame(parent, bg=BG_DARK)
        top.pack(fill="x", padx=12, pady=(12, 6))
        tk.Label(top, text="👁 Vues SQL", bg=BG_DARK, fg=GREEN_ACC, font=FONT_SUB).pack(side="left")

        self.views_tv_container = tk.Frame(parent, bg=BG_DARK)
        self.views_status = tk.Label(parent, text="", bg=BG_DARK, fg=TEXT_GREY, font=FONT_SMALL)
        self.views_status.pack(anchor="w", padx=12)
        self.views_tv_container.pack(fill="both", expand=True, padx=12, pady=4)

        cards_frame = tk.Frame(parent, bg=BG_DARK)
        cards_frame.pack(fill="x", padx=12, pady=8, before=self.views_status)

        for vname, vdata in VUES.items():
            card = card_frame(cards_frame, padx=10, pady=8)
            card.pack(fill="x", pady=4)

            tk.Label(card, text=vname, bg=BG_CARD, fg=GREEN_ACC,
                     font=("Helvetica", 11, "bold")).pack(anchor="w")
            tk.Label(card, text=vdata["desc"], bg=BG_CARD, fg=TEXT_GREY,
                     font=FONT_SMALL).pack(anchor="w", pady=2)

            btn_row = tk.Frame(card, bg=BG_CARD)
            btn_row.pack(anchor="w", pady=4)

            styled_button(btn_row, "▶ Afficher", 
                         lambda v=vdata: self._view_show(v),
                         width=12).pack(side="left", padx=4)
            styled_button(btn_row, "🔧 (Re)créer",
                         lambda v=vdata: self._view_create(v),
                         color=ORANGE_W, fg=TEXT_DARK, width=12).pack(side="left", padx=4)

    def _view_show(self, vdata):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(vdata["select"])
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            conn.close()

            for w in self.views_tv_container.winfo_children():
                w.destroy()
            tv_frame, tv = make_treeview(self.views_tv_container, cols, height=16)
            tv_frame.pack(fill="both", expand=True)
            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                tv.insert("", "end", values=[str(v) if v is not None else "" for v in row], tags=(tag,))
            tv.tag_configure("even", background=BG_CARD)
            tv.tag_configure("odd",  background=BG_PANEL)
            self.views_status.config(text=f"✅ {len(rows)} ligne(s)", fg=GREEN_ACC)
        except Exception as e:
            self.views_status.config(text=f"❌ {str(e)[:80]}", fg=RED_ERR)

    def _view_create(self, vdata):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(vdata["create"])
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "✅ Vue créée / mise à jour.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # ══════════════════════════════════════════
    #  ONGLET 5 : IMPORT CSV
    # ══════════════════════════════════════════
    def _build_tab_import(self):
        parent = self.tab_import

        tk.Label(parent, text="📥 Import des données CSV",
                 bg=BG_DARK, fg=GREEN_ACC, font=FONT_SUB).pack(pady=(30, 8), padx=16, anchor="w")
        tk.Label(parent,
                 text="Lance le script greensd.py qui importe automatiquement tous les fichiers CSV\n"
                      "(partenaire, entree, vehicule_livreur, tournee, livraison) dans la base de données.",
                 bg=BG_DARK, fg=TEXT_GREY, font=FONT_BODY, justify="left").pack(padx=16, anchor="w", pady=(0, 20))

        styled_button(parent, "▶  Lancer l'import", self._import_run, width=22).pack(padx=16, anchor="w")

        self.import_log = tk.Text(parent, height=22, bg=BG_CARD, fg=GREEN_LITE,
                                  font=FONT_MONO, relief="flat", padx=10, pady=8,
                                  state="disabled")
        self.import_log.pack(fill="both", expand=True, padx=16, pady=20)

    def _import_log_line(self, msg):
        self.import_log.config(state="normal")
        self.import_log.insert("end", msg + "\n")
        self.import_log.see("end")
        self.import_log.config(state="disabled")

    def _ask_input_dialog(self, prompt):
        """Affiche une fenêtre de saisie Tkinter et retourne la valeur entrée."""
        result = {"value": None}
        win = tk.Toplevel(self)
        win.title("Information manquante")
        win.configure(bg=BG_PANEL)
        win.grab_set()
        win.resizable(False, False)
        win.geometry("440x180")

        tk.Label(win, text=prompt, bg=BG_PANEL, fg=TEXT_WHITE,
                 font=FONT_BODY, wraplength=400, justify="left").pack(padx=20, pady=(20, 8))
        ent = tk.Entry(win, bg=BG_DARK, fg=TEXT_WHITE, insertbackground=GREEN_ACC,
                       font=FONT_BODY, relief="flat", bd=4, width=36)
        ent.pack(padx=20, pady=4)
        ent.focus_set()

        def validate():
            result["value"] = ent.get().strip()
            win.destroy()

        ent.bind("<Return>", lambda e: validate())
        styled_button(win, "✔ Valider", validate, width=14).pack(pady=12)
        self.wait_window(win)
        return result["value"] or ""

    def _import_run(self):
        """Importe les données en appelant directement les fonctions de greensd.py,
        avec des fenêtres Tkinter à la place des input() console."""

        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "greensd.py")
        if not os.path.exists(script):
            messagebox.showwarning("Fichier introuvable",
                                   f"greensd.py introuvable :\n{script}")
            return

        self.import_log.config(state="normal")
        self.import_log.delete("1.0", "end")
        self.import_log.config(state="disabled")
        self._import_log_line("⏳ Démarrage de l'import...\n")

        def run():
            try:
                # Charger le module sans l'exécuter directement
                spec = importlib.util.spec_from_file_location("greensd", script)
                mod = importlib.util.module_from_spec(spec)

                # Remplacer input() par notre fenêtre Tkinter
                def tk_input(prompt=""):
                    self._import_log_line(f"❓ Saisie requise : {prompt}")
                    result = {"v": ""}
                    done = threading.Event()
                    def ask():
                        result["v"] = self._ask_input_dialog(prompt)
                        done.set()
                    self.after(0, ask)
                    done.wait()
                    self._import_log_line(f"   → Réponse : {result['v']}")
                    return result["v"]

                # Remplacer print() pour loguer dans l'interface
                def tk_print(*args, **kwargs):
                    msg = " ".join(str(a) for a in args)
                    self.after(0, self._import_log_line, msg)

                mod.__builtins__ = dict(vars(__builtins__)) if isinstance(__builtins__, types.ModuleType) else dict(__builtins__)
                mod.__builtins__["input"] = tk_input
                mod.__builtins__["print"] = tk_print

                spec.loader.exec_module(mod)
                self.after(0, self._import_log_line, "\n✅ Import terminé avec succès.")
            except SystemExit:
                self.after(0, self._import_log_line, "\n✅ Import terminé.")
            except Exception as e:
                self.after(0, self._import_log_line, f"\n❌ Erreur : {e}")

        threading.Thread(target=run, daemon=True).start()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = GreenSDApp()
    app.mainloop()
