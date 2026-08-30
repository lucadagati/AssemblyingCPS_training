#!/usr/bin/env python3
"""Genera i deck PPTX del laboratorio S4T — rendering visivo condiviso."""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

BASE = Path(__file__).resolve().parent
SLIDES_DIR = BASE / "slides"
ASSETS = BASE / "assets"

# --- Brand palette (Assembling Smart CPS / MDSLab-inspired) ---
NAVY = RGBColor(0x0D, 0x2B, 0x45)
NAVY_MID = RGBColor(0x1A, 0x4A, 0x6E)
TEAL = RGBColor(0x00, 0x8B, 0x9A)
TEAL_LIGHT = RGBColor(0xB2, 0xEB, 0xF2)
LAB_GREEN = RGBColor(0x1B, 0x5E, 0x20)
LAB_GREEN_LIGHT = RGBColor(0x2E, 0x7D, 0x32)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
OFF_WHITE = RGBColor(0xF8, 0xFA, 0xFC)
GRAY = RGBColor(0x37, 0x47, 0x4F)
LIGHT_GRAY = RGBColor(0x78, 0x90, 0x9C)
ACCENT_BLUE = RGBColor(0xE3, 0xF2, 0xFD)
WARN_AMBER = RGBColor(0xE6, 0x51, 0x00)
WARN_BG = RGBColor(0xFF, 0xF3, 0xE0)
THEORY_BG = RGBColor(0xF0, 0xF9, 0xFA)
DEMO_BG = RGBColor(0xFF, 0xF8, 0xE1)
DEMO_ACCENT = RGBColor(0xF5, 0x7C, 0x00)
CODE_BG = RGBColor(0x1E, 0x29, 0x3B)
CODE_TEXT = RGBColor(0xE2, 0xE8, 0xF0)
FOOTER_TEXT = RGBColor(0x90, 0xA4, 0xAE)

FONT = "Calibri"
MONO = "Consolas"


def new_prs():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def blank_slide(prs, bg=OFF_WHITE):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = bg
    return slide


def _set_font(p, *, size=18, bold=False, color=GRAY, name=FONT):
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = name


def _footer(slide, module_tag=""):
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(7.05), Inches(12.33), Inches(0.02)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = TEAL_LIGHT
    line.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(0.55), Inches(7.08), Inches(8), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = "Assembling Smart CPS · Stack4Things Training"
    _set_font(p, size=9, color=FOOTER_TEXT)
    if module_tag:
        rt = slide.shapes.add_textbox(Inches(10.2), Inches(7.06), Inches(2.6), Inches(0.35))
        rp = rt.text_frame.paragraphs[0]
        rp.text = module_tag
        _set_font(rp, size=9, color=TEAL, bold=True)
        rp.alignment = PP_ALIGN.RIGHT


def _top_accent_bar(slide, color=TEAL, height=Inches(0.06)):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()


def _pill_badge(slide, text, x, y, w, h, fill, text_color=WHITE, size=11):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    tf = shape.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    _set_font(p, size=size, bold=True, color=text_color)


def _title_card(slide, title, y, color=NAVY, size=28):
    tb = slide.shapes.add_textbox(Inches(0.65), y, Inches(12), Inches(0.95))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    _set_font(p, size=size, bold=True, color=color)
    return y + Inches(1.0)


def _bullet_lines(slide, bullets, top, body_color=GRAY, compact=False, width=11.4):
    card_top = top - Inches(0.08)
    card_h = Inches(6.95) - card_top
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), card_top, Inches(12.2), card_h
    )
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = TEAL_LIGHT
    card.line.width = Pt(0.75)

    body = slide.shapes.add_textbox(Inches(0.85), top + Inches(0.05), Inches(width), card_h - Inches(0.25))
    tf = body.text_frame
    tf.word_wrap = True
    n = len(bullets)
    if compact:
        size_main, size_sub = (16, 15) if n >= 6 else (17, 16)
    else:
        size_main, size_sub = (17, 16) if n >= 6 else (19, 17)
    for i, line in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        raw = line.strip()
        is_cmd = raw.startswith("$ ") or raw.startswith("```")
        is_sub = raw.startswith("    ")
        if is_cmd:
            p.text = raw
            _set_font(p, size=14, color=NAVY, name=MONO)
        else:
            prefix = "    " if is_sub else "▸  "
            p.text = f"{prefix}{raw}" if not raw.startswith("▸") else raw
            _set_font(p, size=size_sub if is_sub else size_main, color=body_color)
        p.space_after = Pt(5 if compact else 8)
        p.line_spacing = 1.15


def add_title_slide(prs, title, subtitle="", footer="", notes=""):
    slide = blank_slide(prs, bg=NAVY)
    # Layered gradient effect
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    band.fill.solid()
    band.fill.fore_color.rgb = NAVY_MID
    band.line.fill.background()
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.18), Inches(7.5))
    accent.fill.solid()
    accent.fill.fore_color.rgb = TEAL
    accent.line.fill.background()

    _pill_badge(slide, "S4T TRAINING", Inches(0.75), Inches(0.55), Inches(2.2), Inches(0.38), TEAL)

    box = slide.shapes.add_textbox(Inches(0.75), Inches(2.0), Inches(11.8), Inches(1.8))
    p = box.text_frame.paragraphs[0]
    p.text = title
    _set_font(p, size=40, bold=True, color=WHITE)

    if subtitle:
        box2 = slide.shapes.add_textbox(Inches(0.75), Inches(3.85), Inches(11.5), Inches(1.4))
        for i, line in enumerate(subtitle.split("\n")):
            p2 = box2.text_frame.paragraphs[0] if i == 0 else box2.text_frame.add_paragraph()
            p2.text = line
            _set_font(p2, size=22, color=TEAL_LIGHT)
            p2.space_after = Pt(4)

    if footer:
        box3 = slide.shapes.add_textbox(Inches(0.75), Inches(6.15), Inches(11.5), Inches(0.6))
        _set_font(box3.text_frame.paragraphs[0], size=14, color=FOOTER_TEXT)
        box3.text_frame.paragraphs[0].text = footer

    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(5.9), Inches(3.5), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = TEAL
    line.line.fill.background()
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def add_content_slide(prs, title, bullets, notes="", hands_on=False, warn=False):
    if hands_on:
        slide = blank_slide(prs, bg=OFF_WHITE)
        _top_accent_bar(slide, TEAL)
        top = _title_card(slide, title, Inches(0.55), color=NAVY, size=30)
        _bullet_lines(slide, bullets, top, body_color=GRAY)
    elif warn:
        slide = blank_slide(prs, bg=WARN_BG)
        _top_accent_bar(slide, WARN_AMBER)
        _pill_badge(slide, "⚠  BOOK ↔ LAB", Inches(0.55), Inches(0.32), Inches(1.55), Inches(0.36), WARN_AMBER)
        top = _title_card(slide, title, Inches(0.78), color=RGBColor(0xBF, 0x36, 0x0C), size=28)
        _bullet_lines(slide, bullets, top, body_color=GRAY, compact=False)
    else:
        slide = blank_slide(prs, bg=OFF_WHITE)
        _top_accent_bar(slide, NAVY_MID)
        top = _title_card(slide, title, Inches(0.55), color=NAVY, size=30)
        _bullet_lines(slide, bullets, top, body_color=GRAY)

    _footer(slide)
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def _slide_badge(slide, text, color, y=Inches(0.32)):
    _pill_badge(slide, text, Inches(0.55), y, Inches(2.2), Inches(0.34), color, WHITE, 11)


def add_section_slide(prs, title, subtitle="", notes=""):
    slide = blank_slide(prs, bg=NAVY)
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(3.35), Inches(13.333), Inches(0.06))
    accent.fill.solid()
    accent.fill.fore_color.rgb = TEAL
    accent.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(2.35), Inches(11.5), Inches(1.2))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    _set_font(p, size=38, bold=True, color=WHITE)
    p.alignment = PP_ALIGN.CENTER

    if subtitle:
        sb = slide.shapes.add_textbox(Inches(0.8), Inches(3.65), Inches(11.5), Inches(0.9))
        sp = sb.text_frame.paragraphs[0]
        sp.text = subtitle
        _set_font(sp, size=22, color=TEAL_LIGHT)
        sp.alignment = PP_ALIGN.CENTER

    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def add_theory_slide(prs, title, bullets, book_ref="", notes=""):
    slide = blank_slide(prs, bg=THEORY_BG)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.12), Inches(7.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL
    bar.line.fill.background()
    _slide_badge(slide, "THEORY", TEAL)
    if book_ref:
        ref = slide.shapes.add_textbox(Inches(8.5), Inches(0.32), Inches(4.5), Inches(0.45))
        rp = ref.text_frame.paragraphs[0]
        rp.text = book_ref[:70]
        _set_font(rp, size=11, color=LIGHT_GRAY)
        rp.alignment = PP_ALIGN.RIGHT
    top = _title_card(slide, title, Inches(0.78), color=NAVY, size=26)
    _bullet_lines(slide, bullets, top, GRAY, compact=True)
    _footer(slide, "Theory")
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def add_demo_slide(prs, title, bullets, notes=""):
    slide = blank_slide(prs, bg=DEMO_BG)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.12), Inches(7.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = DEMO_ACCENT
    bar.line.fill.background()
    _pill_badge(slide, "DEMO", Inches(0.55), Inches(0.32), Inches(0.95), Inches(0.34), DEMO_ACCENT)
    top = _title_card(slide, title, Inches(0.78), color=NAVY, size=26)
    _bullet_lines(slide, bullets, top, GRAY, compact=True)
    _footer(slide, "Demo")
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def add_code_slide(prs, title, code, notes=""):
    slide = blank_slide(prs, bg=OFF_WHITE)
    _top_accent_bar(slide, TEAL)
    top = _title_card(slide, title, Inches(0.55), color=NAVY, size=28)

    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(1.65), Inches(12.2), Inches(5.35))
    box.fill.solid()
    box.fill.fore_color.rgb = CODE_BG
    box.line.color.rgb = NAVY_MID
    box.line.width = Pt(1)

    # Fake window chrome
    chrome = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(1.65), Inches(12.2), Inches(0.32))
    chrome.fill.solid()
    chrome.fill.fore_color.rgb = RGBColor(0x33, 0x41, 0x55)
    chrome.line.fill.background()
    for i, c in enumerate((RGBColor(0xEF, 0x44, 0x44), RGBColor(0xF5, 0x9E, 0x0B), RGBColor(0x22, 0xC5, 0x5E))):
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.75 + i * 0.22), Inches(1.73), Inches(0.12), Inches(0.12))
        dot.fill.solid()
        dot.fill.fore_color.rgb = c
        dot.line.fill.background()

    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.45)
    for i, line in enumerate(code.strip().split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        _set_font(p, size=12, color=CODE_TEXT, name=MONO)
        p.space_after = Pt(2)

    _footer(slide, "Code")
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


# Legacy builders (Italian) — keep exports used elsewhere
HELLO_PLUGIN = '''from iotronic_lightningrod.modules.plugins import Plugin
from oslo_log import log as logging
LOG = logging.getLogger(__name__)

class Worker(Plugin.Plugin):
    def __init__(self, uuid, name, q_result, params=None):
        super(Worker, self).__init__(uuid, name, q_result, params)
    def run(self):
        person_name = self.params.get('name', 'User')
        message = f"Hello {person_name}"
        LOG.info(message)
        self.q_result.put(message)'''

DOCKER_JSON = '''{
  "operation": "run",
  "image": "alpine",
  "container_name": "test_alpine",
  "command": "echo Hello from plugin!",
  "auto_remove": false
}'''


def build_slot1():
    prs = new_prs()
    slides = [
        ("title", "Deploy live dello Stack4Things I/Ocloud", "Capitolo 13 — Part II", "Assembling Smart CPS"),
        ("content", "Dove siamo nel libro", [
            "Part I: fondamenti (Cap. 1–12) — teoria, continuum, middleware",
            "Part II: applicazioni (Cap. 13–21) — deploy, plugin, casi d'uso",
            "Oggi Slot 1: primo passo operativo — I/Ocloud S4T in Docker",
            "Repo: github.com/AssemblingSmartCPS/ch13",
        ], "Durata: 2 min. Collegare al continuum cloud-edge del libro."),
        ("content", "Obiettivi Slot 1", [
            "Clonare e avviare lo stack S4T con Docker Compose",
            "Verificare IoTronic Conductor e Horizon UI",
            "Registrare una virtual board e configurare Lightning-Rod",
            "Consegna: screenshot board in stato Active",
        ]),
        ("hands_on", "Check ambiente corsisti", [
            "$ docker --version && docker compose version",
            "$ groups | grep docker",
            "$ free -h    # >= 4 GB RAM liberi",
            "$ git clone https://github.com/AssemblingSmartCPS/ch13.git",
        ], "5 min — tutti devono completare prima di compose up.", True),
    ]
    for item in slides:
        kind = item[0]
        if kind == "title":
            add_title_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "")
        elif kind == "hands_on":
            add_content_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "", hands_on=True)
        else:
            add_content_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "")
    out = SLIDES_DIR / "Slot1_Longo_Deploy_IOcloud.pptx"
    prs.save(str(out))
    print(f"Saved {out} ({len(prs.slides)} slides)")
    return out


def build_slot2():
    prs = new_prs()
    add_title_slide(prs, "Plugin Stack4Things", "Capitolo 14 — da HelloWorld al Docker lifecycle", "Assembling Smart CPS")
    add_content_slide(prs, "Obiettivi Slot 2", [
        "Creare plugin sincrono HelloName",
        "Inject + Plugin Call da Horizon",
        "Demo Docker lifecycle plugin (opz.)",
    ])
    add_code_slide(prs, "HelloNamePlugin (sync)", HELLO_PLUGIN)
    out = SLIDES_DIR / "Slot2_Longo_Plugin_Services.pptx"
    prs.save(str(out))
    print(f"Saved {out} ({len(prs.slides)} slides)")
    return out


def build_slot3():
    prs = new_prs()
    add_title_slide(prs, "IoT-hosted computation", "Capitolo 15 — Environmental publisher & smart city", "Assembling Smart CPS")
    add_content_slide(prs, "Obiettivi Slot 3", [
        "Deploy InfluxDB time-series store",
        "Plugin async environmental_data → InfluxDB",
        "Query validazione dati",
    ])
    out = SLIDES_DIR / "Slot3_Merlino_IoT_Computation.pptx"
    prs.save(str(out))
    print(f"Saved {out} ({len(prs.slides)} slides)")
    return out


def build_handout_pdf():
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfgen import canvas
    except ImportError:
        print("reportlab not available, skipping handout PDF")
        return None
    out = SLIDES_DIR / "HANDOUT_corso_S4T.pdf"
    c = canvas.Canvas(str(out), pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, h - 2 * cm, "Laboratorio S4T — Handout corsisti")
    c.save()
    print(f"Saved {out}")
    return out
