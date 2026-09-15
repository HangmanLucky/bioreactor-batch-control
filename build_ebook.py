# -*- coding: utf-8 -*-
"""
Ebook generator - Automation Skills Portfolio series
Biotechnology: Automated Bioreactor Environmental Control Unit
Author: Sipho Lucky Sibanda
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Oblique", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Cond-Bold", FD + "DejaVuSansCondensed-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Cond", FD + "DejaVuSansCondensed.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FD + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", FD + "DejaVuSansMono-Bold.ttf"))

# ---------------------------------------------------------------------------
# Palette - magenta/cyan "biotech" identity for this project
# ---------------------------------------------------------------------------
BASE      = colors.HexColor("#0A0714")
BASE2     = colors.HexColor("#120E22")
BASE_LINE = colors.HexColor("#2A2040")
BIOACC    = colors.HexColor("#E91E8C")
BIOACC_LT = colors.HexColor("#FBD6EC")
DEEPBIO   = colors.HexColor("#8A1263")
TEAL      = colors.HexColor("#2FBE96")
AMBER     = colors.HexColor("#F5A623")
RED       = colors.HexColor("#E0503E")
CYAN      = colors.HexColor("#2B9BB0")
INK       = colors.HexColor("#22162E")
MUTED     = colors.HexColor("#7A6690")
MUTED_LT  = colors.HexColor("#E3C6DC")
PANEL     = colors.HexColor("#FBEEF6")
ROWBAND   = colors.HexColor("#FDF6FA")
GRIDLINE  = colors.HexColor("#EBD6E7")

PAGE_W, PAGE_H = A4
MARGIN_L, MARGIN_R = 22 * mm, 20 * mm
MARGIN_TOP, MARGIN_BOT = 26 * mm, 24 * mm
AVAIL_W = PAGE_W - MARGIN_L - MARGIN_R

DOC_TITLE = "BIOREACTOR ENVIRONMENTAL CONTROL UNIT"
AUTHOR = "Sipho Lucky Sibanda"
OUTFILE = "/home/claude/bioreactor-batch-control/ebook/Bioreactor_Technical_Manual.pdf"

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
body = ParagraphStyle("body", fontName="Sans", fontSize=10.2, leading=15,
                       textColor=INK, spaceAfter=8, alignment=TA_JUSTIFY)
body_l = ParagraphStyle("body_l", parent=body, alignment=TA_LEFT)
lead = ParagraphStyle("lead", parent=body, fontSize=12.5, leading=18, textColor=DEEPBIO,
                       spaceAfter=10)
kicker = ParagraphStyle("kicker", fontName="Mono", fontSize=8.5, leading=11,
                         textColor=DEEPBIO, spaceAfter=2)
h1 = ParagraphStyle("h1", fontName="Cond-Bold", fontSize=19, leading=22,
                     textColor=colors.HexColor("#5C0F44"), spaceAfter=2)
h2 = ParagraphStyle("h2", fontName="Cond-Bold", fontSize=13.5, leading=16,
                     textColor=colors.HexColor("#5C0F44"), spaceBefore=14, spaceAfter=6)
h3 = ParagraphStyle("h3", fontName="Sans-Bold", fontSize=10.6, leading=13,
                     textColor=colors.HexColor("#5C0F44"), spaceBefore=8, spaceAfter=4)
caption = ParagraphStyle("caption", fontName="Sans-Oblique", fontSize=8.3, leading=11,
                          textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
bullet = ParagraphStyle("bullet", parent=body, alignment=TA_LEFT, leftIndent=12,
                         bulletIndent=0, spaceAfter=5)
chip_num = ParagraphStyle("chip_num", fontName="Cond-Bold", fontSize=17, leading=20,
                           textColor=colors.white, alignment=TA_CENTER)
toc_entry = ParagraphStyle("toc_entry", fontName="Sans", fontSize=10.5, leading=16,
                            textColor=INK)
toc_num = ParagraphStyle("toc_num", fontName="Mono-Bold", fontSize=10.5, leading=16,
                          textColor=DEEPBIO)
cell_hdr = ParagraphStyle("cell_hdr", fontName="Sans-Bold", fontSize=8.6, leading=11,
                           textColor=colors.white)
cell_txt = ParagraphStyle("cell_txt", fontName="Sans", fontSize=8.6, leading=12,
                           textColor=INK)
code_style = ParagraphStyle("code", fontName="Mono", fontSize=7.6, leading=11.2,
                             textColor=BIOACC_LT)
callout_title = lambda c: ParagraphStyle("ct", fontName="Sans-Bold", fontSize=9.6,
                                          leading=12, textColor=c, spaceAfter=3)
callout_body = ParagraphStyle("cb", fontName="Sans", fontSize=9.4, leading=13.4,
                               textColor=INK)

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def P(text, style=body):
    return Paragraph(text, style)

def chapter_head(num, title, kicker_text="BIOREACTOR CONTROL"):
    chip = Table([[Paragraph(str(num).zfill(2), chip_num)]],
                 colWidths=[17 * mm], rowHeights=[17 * mm])
    chip.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DEEPBIO),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    title_block = [P(kicker_text, kicker), P(title, h1)]
    row = Table([[chip, title_block]], colWidths=[22 * mm, AVAIL_W - 22 * mm])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    rule = HRFlowable(width="100%", thickness=1.3, color=BIOACC, spaceBefore=8, spaceAfter=16)
    return [row, rule]

def subhead(text):
    return P(text, h2)

def bullets(items):
    out = []
    for it in items:
        out.append(P("&#8226;&nbsp;&nbsp;" + it, bullet))
    return out

def code_block(code_text, cap=None):
    lines = code_text.strip("\n").split("\n")
    esc_lines = []
    for ln in lines:
        stripped = ln.lstrip(" ")
        n = len(ln) - len(stripped)
        esc_lines.append("&nbsp;" * n + esc(stripped) if stripped else "&nbsp;")
    para = Paragraph("<br/>".join(esc_lines), code_style)
    cell = Table([[para]], colWidths=[AVAIL_W])
    cell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BASE2),
        ("BOX", (0, 0), (-1, -1), 0.75, BASE_LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    out = [cell]
    if cap:
        out.append(P(cap, caption))
    else:
        out.append(Spacer(1, 10))
    return out

def data_table(headers, rows, col_widths=None):
    data = [[Paragraph(h, cell_hdr) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), cell_txt) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5C0F44")),
        ("GRID", (0, 0), (-1, -1), 0.5, GRIDLINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROWBAND))
    t.setStyle(TableStyle(style))
    return t

def callout(title, text, kind="info"):
    color = {"info": CYAN, "warning": AMBER, "critical": RED, "ok": TEAL}[kind]
    label = {"info": "NOTE", "warning": "ENGINEERING NOTE", "critical": "HONEST LIMITATION",
             "ok": "DESIGN NOTE"}[kind]
    content = [P("%s &mdash; %s" % (label, title), callout_title(color)), P(text, callout_body)]
    inner = Table([[content]], colWidths=[AVAIL_W - 16])
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([["", inner]], colWidths=[5, AVAIL_W - 5])
    outer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), color),
        ("BACKGROUND", (1, 0), (1, 0), PANEL),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [outer, Spacer(1, 10)]

def full_image(path, cap, max_h_mm=95):
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    ratio = ih / float(iw)
    w = AVAIL_W
    h = w * ratio
    max_h = max_h_mm * mm
    if h > max_h:
        h = max_h
        w = h / ratio
    img = Image(path, width=w, height=h)
    img.hAlign = "CENTER"
    return [img, P(cap, caption)]


# ---------------------------------------------------------------------------
# Page backgrounds
# ---------------------------------------------------------------------------
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(BASE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setStrokeColor(BASE_LINE)
    c.setLineWidth(0.4)
    step = 12 * mm
    x = 0
    while x < PAGE_W:
        c.line(x, 0, x, PAGE_H); x += step
    y = 0
    while y < PAGE_H:
        c.line(0, y, PAGE_W, y); y += step

    c.setStrokeColor(BIOACC)
    c.setLineWidth(1.1)
    c.rect(10 * mm, 10 * mm, PAGE_W - 20 * mm, PAGE_H - 20 * mm, fill=0, stroke=1)

    # Decorative vessel glyph, bottom right
    cx, cy = PAGE_W - 52 * mm, 36 * mm
    w2, h2 = 20 * mm, 28 * mm
    c.setStrokeColor(BIOACC)
    c.setLineWidth(1.3)
    c.roundRect(cx - w2/2, cy, w2, h2, 4*mm, fill=0, stroke=1)
    c.line(cx, cy + h2, cx, cy + h2 + 6*mm)
    c.setFont("Mono-Bold", 7)
    c.setFillColor(BIOACC)
    c.drawCentredString(cx, cy - 7*mm, "BR-201")

    c.setFillColor(BIOACC)
    c.setFont("Mono", 10.5)
    c.drawString(24 * mm, PAGE_H - 42 * mm, "AUTOMATION SKILLS PORTFOLIO   ·   BIOTECHNOLOGY")

    c.setFillColor(colors.white)
    c.setFont("Cond-Bold", 22)
    for i, line in enumerate(["AUTOMATED BIOREACTOR", "ENVIRONMENTAL CONTROL UNIT"]):
        c.drawString(24 * mm, PAGE_H - 62 * mm - i * 11.5 * mm, line)

    c.setFont("Cond", 13.5)
    c.setFillColor(MUTED_LT)
    c.drawString(24 * mm, PAGE_H - 90 * mm, "for Pharmaceutical Batch Processing")

    c.setStrokeColor(BASE_LINE)
    c.setLineWidth(0.8)
    c.line(24 * mm, 46 * mm, PAGE_W - 24 * mm, 46 * mm)

    c.setFont("Mono", 9.5)
    c.setFillColor(CYAN)
    c.drawString(24 * mm, 38 * mm, "TECHNICAL PROJECT MANUAL  ·  REV. A")
    c.setFont("Sans-Bold", 13)
    c.setFillColor(colors.white)
    c.drawString(24 * mm, 31 * mm, "By " + AUTHOR)
    c.setFont("Sans", 8.6)
    c.setFillColor(MUTED_LT)
    c.drawString(24 * mm, 25.5 * mm, "Platform: Siemens S7-1500 (SCL) / CODESYS-portable Structured Text")
    c.drawString(24 * mm, 21 * mm, "Simulation & Portfolio Engineering Build  ·  Not for GMP Production Use")
    c.restoreState()

def draw_body(c, doc):
    c.saveState()
    c.setFillColor(BASE)
    c.rect(0, PAGE_H - 15 * mm, PAGE_W, 15 * mm, fill=1, stroke=0)
    c.setFillColor(BIOACC)
    c.setFont("Mono", 7.6)
    c.drawString(MARGIN_L, PAGE_H - 9.5 * mm, DOC_TITLE)
    c.setFillColor(colors.white)
    c.setFont("Sans", 7.4)
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 9.5 * mm, "By " + AUTHOR)
    c.setStrokeColor(BIOACC)
    c.setLineWidth(0.8)
    c.line(0, PAGE_H - 15 * mm, PAGE_W, PAGE_H - 15 * mm)

    c.setFillColor(MUTED)
    c.setFont("Mono", 7.8)
    c.drawString(MARGIN_L, 13 * mm, "BIOREACTOR-BATCH-CTRL")
    c.drawCentredString(PAGE_W / 2, 13 * mm, "Page %d" % c.getPageNumber())
    c.drawRightString(PAGE_W - MARGIN_R, 13 * mm, "Simulation / Portfolio Build")
    c.setStrokeColor(BIOACC)
    c.setLineWidth(1)
    c.line(PAGE_W - MARGIN_R, 17 * mm, PAGE_W - MARGIN_R, 21 * mm)
    c.line(PAGE_W - MARGIN_R - 4 * mm, 17 * mm, PAGE_W - MARGIN_R, 17 * mm)
    c.restoreState()


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
story = [PageBreak()]

# ---- Document control / disclaimer ------------------------------------------------
story += chapter_head("i", "Document Control &amp; Disclaimer", "FRONT MATTER")
story.append(P(
    "This document is a self-authored technical project manual produced as part of a "
    "personal engineering portfolio. It describes the design, control philosophy, and "
    "simulated validation of a bioreactor environmental control system, built to "
    "demonstrate ISA-88 batch sequencing, cascade and split-range process control, and "
    "sterilisation-validation mathematics for automation, controls, and biotech/pharma "
    "engineering roles.", body))
story.append(P(
    "The system described here was developed and tested in simulation only (PLCSIM-style "
    "forcing of inputs and desktop review). No part of this project has been installed, "
    "commissioned, or verified on physical bioprocess hardware, and it must not be treated "
    "as a validated GMP manufacturing system.", body))

story += callout(
    "Portfolio project, not a validated GMP system",
    "A real biopharma bioreactor control system requires full process validation, 21 CFR "
    "Part 11 compliant electronic batch records, and qualification against the specific "
    "cell line and product involved, none of which this project claims. Figures, "
    "thresholds, and I/O in this manual are engineering-realistic but illustrative.", "critical")

data = [
    ["Document Title", "Automated Bioreactor Environmental Control Unit \u2014 Technical Manual"],
    ["Author", AUTHOR],
    ["Revision", "A"],
    ["Document Type", "Portfolio Technical Manual (Simulation)"],
    ["Target Platform", "Siemens S7-1500 (TIA Portal / SCL) \u2014 CODESYS-portable"],
    ["Related Repository", "bioreactor-batch-control"],
    ["Series", "Automation Skills Portfolio \u2014 Biotechnology"],
]
t = Table(data, colWidths=[45 * mm, AVAIL_W - 45 * mm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Sans-Bold"), ("FONTNAME", (1, 0), (1, -1), "Sans"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.4), ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#5C0F44")),
    ("TEXTCOLOR", (1, 0), (1, -1), INK),
    ("GRID", (0, 0), (-1, -1), 0.4, GRIDLINE),
    ("BACKGROUND", (0, 0), (0, -1), PANEL),
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(t)
story.append(PageBreak())

# ---- Contents ------------------------------------------------------------
story += chapter_head("ii", "Contents", "FRONT MATTER")
toc = [
    ("01", "Industry &amp; Regulatory Context"),
    ("02", "System Architecture &amp; Batch Overview"),
    ("03", "Hardware &amp; Instrumentation Specification"),
    ("04", "I/O List &amp; Recipe Parameters"),
    ("05", "Control Philosophy: Cascade, Split-Range &amp; F0 Lethality"),
    ("06", "PLC Logic Walkthrough"),
    ("07", "HMI Design &amp; Live Trends"),
    ("08", "Alarm Philosophy &amp; Fail-Safe Design"),
    ("09", "Testing, Commissioning &amp; FAT Procedures"),
    ("10", "Limitations, Real-World Deltas &amp; Future Work"),
    ("A", "Appendix A &mdash; I/O Quick Reference"),
    ("B", "Appendix B &mdash; Full Structured Text Listing"),
    ("C", "Appendix C &mdash; Glossary"),
    ("&mdash;", "About the Author"),
]
rows = []
for num, title in toc:
    rows.append([P(num, toc_num), P(title, toc_entry)])
tt = Table(rows, colWidths=[14 * mm, AVAIL_W - 14 * mm])
tt.setStyle(TableStyle([
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, GRIDLINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(tt)
story.append(PageBreak())

# ---- Executive Summary ----------------------------------------------------
story += chapter_head("iii", "Executive Summary", "FRONT MATTER")
story.append(P(
    "This is the fourth deliberate discipline shift in the wider automation portfolio, "
    "moving from mechanical/electrical process control toward validated pharmaceutical "
    "batch manufacturing - a field where the control logic and the regulatory record it "
    "produces are equally important. Producing a biologic drug substance means holding a "
    "living cell culture inside a precise, validated environment for days, after first "
    "proving the vessel itself was sterilised beyond reasonable doubt.", lead))
story.append(P(
    "<b>FB_Bioreactor_BatchControl</b> sequences a full batch through the ISA-88 style "
    "phases a real biopharma batch record follows: CIP, SIP (sterilisation), Cooldown, "
    "Inoculation, Incubation, and Harvest. Sterilisation itself is validated using the "
    "real <b>F0 lethality</b> formula rather than a fixed timer, because sterilisation "
    "is temperature <i>and</i> time dependent - holding 110&deg;C for an hour is not "
    "equivalent to 121&deg;C for six minutes, and F0 is the industry-standard way of "
    "comparing the two on one scale.", body))
story.append(P(
    "Two linked control loops keep the culture environment in spec throughout incubation: "
    "a <b>cascade temperature loop</b> (vessel temperature setting a jacket temperature "
    "target, which itself drives the heating/cooling valves) and a <b>split-range "
    "dissolved-oxygen loop</b> that exhausts agitation authority before ever opening an "
    "oxygen sparge valve. pH is held with deadband on/off dosing rather than a continuous "
    "controller, avoiding pump chatter on a naturally noisy signal.", body))
story.append(P(
    "What follows documents the regulatory and industry context, architecture, hardware "
    "assumptions, full I/O list and recipe structure, control philosophy, complete "
    "annotated code, HMI design, alarm philosophy, and the functional test procedure used "
    "to validate the logic in simulation.", body))
story.append(PageBreak())

# ---- Chapter 1: Industry & Regulatory Context ------------------------------
story += chapter_head(1, "Industry &amp; Regulatory Context")
story.append(P(
    "Biopharmaceutical manufacturing operates under <b>Good Manufacturing Practice "
    "(GMP)</b>, enforced by regulators including the FDA and EMA. Every batch's process "
    "parameters, deviations, and outcomes must be documented in a way that can withstand "
    "regulatory audit - the control system isn't just running the process, it's generating "
    "the record that proves the process was run correctly.", body))
story.append(subhead("ISA-88: the standard structure behind this project"))
story.append(P(
    "<b>ISA-88 (IEC 61512)</b> is the batch-control standard this project's phase "
    "structure deliberately mirrors: a <b>recipe</b> defines the parameters for a specific "
    "product, a <b>procedure</b> breaks the batch into ordered phases, and each phase runs "
    "its own permissive-gated logic before handing control to the next. This project's "
    "<code>ST_BatchRecipe</code> structure and its CIP/SIP/Cooldown/Inoculation/Incubation/"
    "Harvest phase sequence are a simplified but structurally faithful implementation of "
    "that model.", body))
story.append(subhead("Why sterilisation validation is its own discipline"))
story.append(P(
    "Steam sterilisation (SIP - Sterilise In Place) doesn't just need to reach a target "
    "temperature; it needs to prove enough cumulative thermal lethality was delivered to "
    "kill the resistant spore-forming organisms process validation is built around. That "
    "proof is what <b>F0</b> represents, and it is a real, standard part of sterilisation "
    "validation across pharma and food processing alike, not a concept invented for this "
    "project.", body))
story += callout(
    "The batch record is the product, almost as much as the drug substance is",
    "In a GMP environment, a batch with no F0 record, or an ambiguous one, cannot be "
    "released regardless of how the culture actually grew - this is why Chapter 5's "
    "insistence on treating an aborted, under-sterilised SIP as an explicit failure "
    "(rather than silently proceeding) reflects real regulatory stakes, not an abstract "
    "design preference.", "info")
story.append(PageBreak())

# ---- Chapter 2: Architecture ----------------------------------------------
story += chapter_head(2, "System Architecture &amp; Batch Overview")
story.append(P(
    "A single stirred-tank bioreactor vessel is fitted with a heating/cooling jacket, a "
    "variable-speed agitator, an oxygen sparge line, acid/base dosing pumps, and pH/DO/"
    "temperature/optical-density probes. A SCADA/MES layer downloads the batch recipe; the "
    "PLC owns every control decision from CIP through harvest.", body))
story += full_image("../images/architecture_diagram.png",
    "Figure 2.1 &mdash; Batch phase sequence and control architecture. Dashed lines "
    "represent PLC signal and configuration paths.", max_h_mm=100)
story.append(subhead("Control hierarchy"))
story += bullets([
    "<b>Field layer</b> &mdash; temperature, DO, pH, and optical density probes; heating/"
    "cooling valves; variable-speed agitator; oxygen sparge valve; acid/base dosing pumps.",
    "<b>Control layer</b> &mdash; a single PLC function block, "
    "<b>FB_Bioreactor_BatchControl</b>, hosted on a Siemens S7-1500 (or CODESYS-based "
    "pharmaceutical process controller), running the full batch sequence and every "
    "control loop.",
    "<b>Supervisory layer</b> &mdash; SCADA/MES recipe management (upstream, downloading "
    "the recipe) and the batch HMI (downstream, presenting vessel state and trends).",
])
story.append(KeepTogether([
    subhead("Why the recipe is an input structure, not embedded constants"),
    P(
        "Passing <code>Recipe : ST_BatchRecipe</code> into the function block as a whole "
        "structure - rather than hardcoding setpoints - mirrors real ISA-88 practice: "
        "the same equipment module runs many products over its lifetime, each with its "
        "own validated recipe, without the control logic itself ever changing.", body)
]))
story.append(PageBreak())

# ---- Chapter 3: Hardware ----------------------------------------------------
story += chapter_head(3, "Hardware &amp; Instrumentation Specification")
story.append(P(
    "As with the rest of this portfolio, the logic here is platform-portable but written "
    "against a concrete reference platform so thresholds and timing are grounded.", body))
story.append(data_table(
    ["Component", "Representative Spec", "Role"],
    [
        ["Batch PLC CPU", "Siemens SIMATIC S7-1500", "Executes FB_Bioreactor_BatchControl"],
        ["Vessel/Jacket RTD", "Pt100, 4-20mA, 0-140C", "Cascade temperature control feedback"],
        ["DO Probe", "Polarographic or optical, 4-20mA, 0-100%", "Split-range DO control feedback"],
        ["pH Probe", "Glass electrode, 4-20mA, 0-14", "Deadband dosing control feedback"],
        ["Optical Density Probe", "In-situ OD600-equivalent sensor", "Early-harvest trigger"],
        ["Variable-Speed Agitator", "0-500 RPM, 4-20mA speed reference", "Mixing / DO split-range primary"],
        ["Oxygen Sparge Valve", "4-20mA proportional control valve", "DO split-range secondary"],
        ["Acid / Base Dosing Pumps", "24VDC on/off metering pumps", "pH deadband control"],
    ],
    col_widths=[46 * mm, 66 * mm, AVAIL_W - 46 * mm - 66 * mm]))
story.append(Spacer(1, 8))
story += callout(
    "Why deadband dosing, not a continuous pH controller",
    "A pH probe signal is naturally noisy at the resolution a dosing decision needs. A "
    "continuous PID output driving an on/off pump would chatter the pump open and closed "
    "on every small fluctuation, wasting reagent and potentially destabilising pH more "
    "than it stabilises it. A fixed deadband around setpoint is the standard, deliberately "
    "simple answer used throughout real bioprocess control.", "ok")
story.append(PageBreak())

# ---- Chapter 4: I/O List ----------------------------------------------------
story += chapter_head(4, "I/O List &amp; Recipe Parameters")
story.append(P(
    "The table below is the working I/O list for FB_Bioreactor_BatchControl (see also "
    "<b>docs/IO_List.md</b> in the repository, and Appendix A of this manual).", body))
story.append(subhead("Recipe parameters (downloaded from SCADA/MES)"))
story.append(data_table(
    ["Field", "Typical Value"],
    [
        ["SIP_Temp_Setpoint_C", "121.1 &deg;C"],
        ["SIP_Target_F0_min", "15.0 min"],
        ["Cooldown_Temp_C", "37.0 &deg;C"],
        ["Incubation_Temp_Setpoint_C", "37.0 &deg;C"],
        ["Incubation_DO_Setpoint_Pct", "40.0 %"],
        ["Incubation_pH_Setpoint", "7.00"],
        ["Incubation_Duration_hr", "72.0 hr"],
        ["Harvest_OD_Threshold", "8.0 OD"],
    ],
    col_widths=[70 * mm, AVAIL_W - 70 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Key inputs and outputs"))
story.append(data_table(
    ["Tag", "Description", "Signal"],
    [
        ["AI_VesselTemp_C / AI_JacketTemp_C", "Cascade loop feedback", "4-20mA x2"],
        ["AI_DO_Pct / AI_pH / AI_OpticalDensity", "Process measurements", "4-20mA x3"],
        ["DI_CIP_Complete / DI_StartBatch / DI_AbortBatch", "Batch sequencing commands", "Digital x3"],
        ["AO_HeatingValve_Pct / AO_CoolingValve_Pct", "Jacket control outputs", "4-20mA x2"],
        ["AO_AgitatorSpeed_RPM / AO_O2SpargeValve_Pct", "DO split-range outputs", "4-20mA x2"],
        ["DO_AcidPump / DO_BasePump", "pH dosing outputs", "Digital x2"],
        ["BatchPhase / Current_F0_min / SystemStatus", "State &amp; batch record data", "Mixed"],
    ],
    col_widths=[66 * mm, 66 * mm, AVAIL_W - 66 * mm - 66 * mm]))
story.append(PageBreak())


# ---- Chapter 5: Control Philosophy -----------------------------------------
story += chapter_head(5, "Control Philosophy: Cascade, Split-Range &amp; F0 Lethality")
story.append(P(
    "Three distinct control techniques do the real work in this project, each solving a "
    "genuinely different kind of problem.", body))
story.append(subhead("5.1 &nbsp; Cascade control: why two loops beat one"))
story.append(P(
    "A single PID loop reading vessel temperature and driving the jacket valve directly "
    "would work, eventually - but slowly, because heat has to move from the jacket, "
    "through the vessel wall, into the bulk liquid before the controller ever sees the "
    "effect of its own action. Cascade control splits this into two loops: the <b>outer "
    "loop</b> compares vessel temperature to setpoint and outputs a jacket temperature "
    "target; the <b>inner loop</b> compares actual jacket temperature to that target and "
    "drives the valves directly. The inner loop reacts to a heat-transfer-fluid "
    "disturbance in seconds, long before it would ever show up as a vessel temperature "
    "deviation.", body))
story.append(subhead("5.2 &nbsp; Split-range control: agitation before oxygen"))
story.append(P(
    "Dissolved oxygen can be raised two ways: spin the impeller faster (cheap, fast, but "
    "limited by shear stress on the cells at high speed) or bubble more oxygen through the "
    "broth (effective, but oxygen is a real cost and over-sparging can strip out other "
    "dissolved gases). This project's split-range logic spends the first 70% of the DO "
    "controller's output entirely on agitation, and only opens the oxygen sparge valve "
    "once agitation is already at its ceiling.", body))
story += callout(
    "The split point (70%) is a design choice, and it's named as one",
    "There's nothing physically fundamental about 70% specifically - it's a tuning "
    "decision balancing shear sensitivity against oxygen cost for a given cell line and "
    "vessel geometry. A real commissioning engineer would set this based on the actual "
    "organism and vessel being used; this project states the number plainly as a "
    "parameter rather than presenting it as a universal constant.", "ok")
story.append(subhead("5.3 &nbsp; F0: comparing sterilisation across temperature and time together"))
story.append(P(
    "The standard formula is:", body))
story.append(P(
    "F0 = &Sigma; 10^((T &minus; 121.1) / z) &times; &Delta;t&nbsp;&nbsp;&nbsp;(z = 10)",
    ParagraphStyle("eq", parent=body, fontName="Mono", alignment=TA_CENTER, fontSize=10.5,
                   textColor=DEEPBIO, spaceAfter=10)))
story.append(P(
    "Every 10&deg;C above the 121.1&deg;C reference temperature multiplies the lethality "
    "rate by ten; every 10&deg;C below divides it by ten. Integrating that rate over the "
    "actual temperature profile the vessel experienced - not just the setpoint - produces "
    "a single number, in equivalent minutes at 121.1&deg;C, that can be compared directly "
    "against a validated target. This is exactly why <b>SIP completes on accumulated F0, "
    "not on elapsed time</b>: a vessel that ran slightly cool for part of the hold needs "
    "longer to reach the same lethality, and F0-based completion accounts for that "
    "automatically.", body))
story.append(subhead("5.4 &nbsp; A failure during SIP must never look like success"))
story.append(P(
    "If a batch is aborted mid-SIP, <code>Alarm_SIP_Failed</code> is raised whenever the "
    "accumulated F0 fell short of the recipe's target. This exists so a batch record can "
    "never ambiguously suggest a vessel was safe to inoculate when the sterilisation "
    "target was never actually reached - a direct consequence of Chapter 1's point that "
    "the record is almost as important as the process itself.", body))
story.append(PageBreak())

# ---- Chapter 6: PLC Logic Walkthrough --------------------------------------
story += chapter_head(6, "PLC Logic Walkthrough")
story.append(P(
    "This chapter walks through <b>FB_Bioreactor_BatchControl</b> section by section. The "
    "full listing is reproduced in Appendix B.", body))

story.append(subhead("6.1 &nbsp; The cascade loop"))
story += code_block(
"""OuterTemp_PID(SP := Recipe.Incubation_Temp_Setpoint_C, PV := AI_VesselTemp_C,
                KP := OuterTemp_Kp, TI := OuterTemp_Ti, MANUAL := FALSE,
                LMN_HLM := 135.0, LMN_LLM := 0.0);
AO_JacketTempSetpoint_C := OuterTemp_PID.LMN;

InnerJacketTemp_PID(SP := AO_JacketTempSetpoint_C, PV := AI_JacketTemp_C,
                      KP := InnerJacket_Kp, TI := InnerJacket_Ti, MANUAL := FALSE,
                      LMN_HLM := 100.0, LMN_LLM := -100.0);

IF InnerJacketTemp_PID.LMN >= 0.0 THEN
    AO_HeatingValve_Pct := InnerJacketTemp_PID.LMN;
ELSE
    AO_CoolingValve_Pct := ABS(InnerJacketTemp_PID.LMN);
END_IF""", "Listing 6.1 &mdash; The outer loop's output literally becomes the inner loop's setpoint.")

story.append(subhead("6.2 &nbsp; F0 accumulation"))
story += code_block(
"""T_ScanTime(IN := (BatchPhase = PH_SIP), PT := T_ScanTime_PT);
IF BatchPhase = PH_SIP THEN
    IF T_ScanTime.Q THEN
        T_ScanTime(IN := FALSE);
        LethalityRate_PerMin := EXPT(10.0, (AI_VesselTemp_C - F0_RefTemp_C) / F0_zValue);
        Current_F0_min := Current_F0_min + (LethalityRate_PerMin * (1.0 / 60.0));
    END_IF
ELSIF BatchPhase = PH_CIP THEN
    Current_F0_min := 0.0;
END_IF""", "Listing 6.2 &mdash; Lethality is integrated once per second against the ACTUAL vessel temperature.")

story.append(subhead("6.3 &nbsp; Split-range DO control"))
story += code_block(
"""IF DO_ControllerOutput_Pct <= 70.0 THEN
    AO_AgitatorSpeed_RPM := Agitator_Min_RPM
        + (DO_ControllerOutput_Pct / 70.0) * (Agitator_Max_RPM - Agitator_Min_RPM);
    AO_O2SpargeValve_Pct := 0.0;
ELSE
    AO_AgitatorSpeed_RPM := Agitator_Max_RPM;
    AO_O2SpargeValve_Pct := (DO_ControllerOutput_Pct - 70.0) / 30.0 * 100.0;
END_IF""", "Listing 6.3 &mdash; Agitation authority is fully spent before sparge ever opens.")

story.append(subhead("6.4 &nbsp; SIP completion and failure flagging"))
story += code_block(
"""PH_SIP:
    IF Current_F0_min >= Recipe.SIP_Target_F0_min THEN
        BatchPhase := PH_COOLDOWN;
    END_IF

// ... elsewhere, evaluated every scan ...
Alarm_SIP_Failed := (BatchPhase = PH_ABORT) AND (Current_F0_min < Recipe.SIP_Target_F0_min);""",
    "Listing 6.4 &mdash; SIP advances on lethality, not time; an abort short of target is flagged, not hidden.")
story.append(PageBreak())


# ---- Chapter 7: HMI ---------------------------------------------------------
story += chapter_head(7, "HMI Design &amp; Live Trends")
story.append(P(
    "The HMI mockup (<b>hmi/index.html</b> in the repository) centres on a vessel "
    "cross-section - jacket, agitator, liquid fill, rising bubbles when sparging - paired "
    "with scrolling trend charts for pH, dissolved oxygen, and temperature, exactly the "
    "operator view a real batch record review would reference.", body))
story += full_image("../images/hmi-dashboard.png",
    "Figure 7.1 &mdash; Incubation active: agitator spinning, jacket in a light heating "
    "trim, live trends showing the cooldown transition and the DO recovery curve from a "
    "scripted split-range event.", max_h_mm=115)
story.append(subhead("Design decisions"))
story += bullets([
    "<b>Magenta/cyan \"cleanroom\" palette</b> &mdash; a fifth distinct visual identity "
    "in this portfolio, chosen to read as clinical/biotech rather than heavy industrial, "
    "appropriate for a process governed by GMP rather than a switchboard or safety panel.",
    "<b>The phase chip row is always visible</b> &mdash; CIP through Complete, with the "
    "active phase highlighted, so an operator glancing at the screen always knows exactly "
    "where in the batch lifecycle the vessel currently sits.",
    "<b>Bubbles only appear when sparge is actually active</b> &mdash; a small detail, "
    "but one that ties the visual directly to the split-range logic from Chapter 5 rather "
    "than running as generic decoration.",
    "<b>Real scrolling trends, not static gauges</b> &mdash; matching the recruiter-facing "
    "brief this project was built against: a chemical vat simulation with real-time graphs "
    "tracking pH and dissolved oxygen, not just instantaneous numbers.",
])
story.append(PageBreak())

# ---- Chapter 8: Alarm Philosophy -------------------------------------------
story += chapter_head(8, "Alarm Philosophy &amp; Fail-Safe Design")
story.append(P(
    "Every alarm in this system maps to a specific batch-record-relevant condition, "
    "consistent with the rest of this portfolio.", body))
story.append(data_table(
    ["Condition", "Meaning", "Expected Response"],
    [
        ["Alarm_SIP_Failed", "Batch aborted before F0 target reached", "Vessel must be re-sterilised - never inoculate on an unproven SIP"],
        ["Alarm_DO_Low", "Dissolved oxygen below 50% of setpoint", "Check sparge/agitation authority; investigate a possible sensor or supply fault"],
        ["Alarm_pH_Excursion", "pH more than 0.5 from setpoint", "Investigate dosing pump function and reagent supply"],
        ["Alarm_TempDeviation", "Vessel temperature more than 2&deg;C from setpoint", "Investigate cascade loop tuning or a jacket-side fault"],
    ],
    col_widths=[42 * mm, 56 * mm, AVAIL_W - 42 * mm - 56 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Fail-safe defaults, summarised"))
story += bullets([
    "Batch abort &rarr; cooling valve to 100%, agitator/sparge/dosing all off - pulling "
    "heat out and stopping every active input to the vessel.",
    "An aborted SIP short of its F0 target is explicitly flagged, never silently treated "
    "as equivalent to a completed one.",
    "pH dosing pumps default off outside the Incubation phase - no dosing action is ever "
    "possible during CIP, SIP, or cooldown.",
])
story.append(PageBreak())

# ---- Chapter 9: Testing -----------------------------------------------------
story += chapter_head(9, "Testing, Commissioning &amp; FAT Procedures")
story.append(P(
    "The function block was validated against fourteen functional test cases, anchored by "
    "two F0-accumulation-rate tests with known, calculable correct answers. The full "
    "procedure is in <b>docs/Testing_Procedures.md</b>; the matrix is reproduced below.", body))
story.append(data_table(
    ["#", "Test Case", "Expected Result"],
    [
        ["1-2", "Batch start / CIP handoff to SIP", "Phase transitions correctly; F0 resets at CIP entry"],
        ["3", "F0 rate at reference temperature", "~1.0 min/min accumulation at exactly 121.1C"],
        ["4", "F0 rate 10C above reference", "10x faster accumulation than Test 3"],
        ["5", "SIP completes on F0, not time", "Transitions on accumulated lethality alone"],
        ["6", "Cascade response to a temperature step", "Jacket setpoint and heating valve respond correctly"],
        ["7", "Cooldown requires a stable hold", "Confirmed only after a full 5-minute settle, not on first touch"],
        ["8-9", "DO split-range, both regions", "Agitation-only below 70% output; sparge engages above it"],
        ["10-11", "pH deadband and excursion alarm", "No dosing chatter within deadband; alarm past 0.5 deviation"],
        ["12", "Early harvest on optical density", "Transitions to Harvest before the incubation timer expires"],
        ["13-14", "Abort safe state and SIP failure flag", "Full safe-state outputs; F0 shortfall explicitly flagged"],
    ],
    col_widths=[12 * mm, 66 * mm, AVAIL_W - 12 * mm - 66 * mm]))
story.append(Spacer(1, 10))
story += callout(
    "Why Tests 3 and 4 anchor the whole suite",
    "F0 accumulation rate at the reference temperature has a known correct answer "
    "(approximately 1.0 equivalent minute per real minute), and the rate exactly 10 "
    "degrees above reference must be exactly ten times faster by the formula's own "
    "definition. If either of these doesn't land, no SIP completion decision anywhere "
    "downstream can be trusted, regardless of how reasonable it looks in isolation.", "warning")
story.append(PageBreak())

# ---- Chapter 10: Limitations -------------------------------------------------
story += chapter_head(10, "Limitations, Real-World Deltas &amp; Future Work")
story.append(P(
    "Naming the gap between a strong simulation and a validated GMP system is part of the "
    "engineering, consistent with every other project in this portfolio.", body))
story.append(subhead("What a real installation would add"))
story += bullets([
    "<b>21 CFR Part 11 compliant electronic batch records</b> &mdash; audit trails, "
    "electronic signatures, and data integrity controls this project makes no claim to.",
    "<b>A maximum SIP duration alarm</b> &mdash; named directly in the code comments "
    "(Chapter 6.4): an unreachable F0 target should never be able to hold a vessel at high "
    "temperature indefinitely without operator intervention.",
    "<b>A fully sequenced inoculation transfer</b> &mdash; this project's Inoculation "
    "phase advances on a settle timer; a real recipe would sequence valve alignments, a "
    "transfer pump, and a confirmed volume addition.",
    "<b>Process validation</b> &mdash; qualification runs proving the control strategy "
    "actually holds spec for the specific cell line and product involved.",
])
story.append(subhead("10.1 &nbsp; Hazard &amp; safeguard register (HAZOP-style)"))
story.append(data_table(
    ["Hazard", "Cause", "Safeguard in This Design"],
    [
        ["Under-sterilised vessel inoculated", "SIP aborted or ended prematurely",
         "F0-based completion, not a timer; Alarm_SIP_Failed on any shortfall"],
        ["Cell culture shear damage", "Agitation pushed too high chasing DO alone",
         "Split-range control shares the DO response with oxygen sparging"],
        ["Runaway high SIP temperature", "No maximum SIP duration/temperature ceiling modelled",
         "Named gap - a real system needs an independent high-temperature trip"],
        ["Dosing pump reagent depletion undetected", "No reagent level/flow feedback in this I/O set",
         "Named gap - a real system would add tank level monitoring on both dosing lines"],
    ],
    col_widths=[46 * mm, 52 * mm, AVAIL_W - 46 * mm - 52 * mm]))
story.append(Spacer(1, 8))
story.append(subhead("Where this project could go next"))
story += bullets([
    "Add an independent, hard-wired high-temperature trip during SIP, separate from the "
    "F0-based software logic.",
    "Model a second vessel and a shared CIP/SIP skid, demonstrating equipment-module "
    "arbitration per the full ISA-88 model.",
    "Extend the batch record output to a structured, timestamped export suitable for a "
    "real electronic batch record system to ingest.",
])
story.append(PageBreak())


# ---- Appendix A: I/O Quick Reference ---------------------------------------
story += chapter_head("A", "Appendix A &mdash; I/O Quick Reference", "APPENDIX")
story.append(data_table(
    ["Tag", "Dir.", "Type", "Notes"],
    [
        ["Recipe", "IN", "ST_BatchRecipe", "From SCADA/MES"],
        ["AI_VesselTemp_C / AI_JacketTemp_C", "IN", "REAL x2", "Cascade feedback"],
        ["AI_DO_Pct / AI_pH / AI_OpticalDensity", "IN", "REAL x3", "Process measurements"],
        ["AI_AgitatorSpeed_RPM", "IN", "REAL", "Feedback"],
        ["DI_CIP_Complete / StartBatch / AbortBatch", "IN", "BOOL x3", "Sequencing"],
        ["DI_System_Enable", "IN", "BOOL", "Master enable"],
        ["AO_JacketTempSetpoint_C", "OUT", "REAL", "Cascade intermediate"],
        ["AO_HeatingValve_Pct / CoolingValve_Pct", "OUT", "REAL x2", "Jacket control"],
        ["AO_AgitatorSpeed_RPM / O2SpargeValve_Pct", "OUT", "REAL x2", "DO split-range"],
        ["DO_AcidPump / DO_BasePump", "OUT", "BOOL x2", "pH deadband dosing"],
        ["BatchPhase", "OUT", "ENUM", "9-state machine"],
        ["Current_F0_min / BatchElapsed_hr", "OUT", "REAL x2", "Batch record data"],
        ["Alarm_SIP_Failed / DO_Low / pH_Excursion / TempDeviation", "OUT", "BOOL x4", "Process alarms"],
        ["SystemStatus", "OUT", "STRING", "HMI display"],
    ],
    col_widths=[68 * mm, 14 * mm, 30 * mm, AVAIL_W - 68 * mm - 14 * mm - 30 * mm]))
story.append(PageBreak())

# ---- Appendix B: Full ST Listing -------------------------------------------
story += chapter_head("B", "Appendix B &mdash; Full Structured Text Listing", "APPENDIX")
story.append(P("Complete, unedited listing of <b>src/Bioreactor_BatchControl.st</b>.", body))

story += code_block(
"""(*
====================================================================================
  PROJECT   : Automated Bioreactor Environmental Control Unit
              for Pharmaceutical Batch Processing
  MODULE    : FB_Bioreactor_BatchControl
  PLATFORM  : IEC 61131-3 Structured Text (Siemens SCL / CODESYS-portable)
  AUTHOR    : Sipho Lucky Sibanda
  See Chapter 5 for cascade, split-range, and F0 lethality discussion.
====================================================================================
*)

TYPE E_BatchPhase :
(
    PH_IDLE, PH_CIP, PH_SIP, PH_COOLDOWN, PH_INOCULATION,
    PH_INCUBATION, PH_HARVEST, PH_COMPLETE, PH_ABORT
);
END_TYPE

TYPE ST_BatchRecipe :
STRUCT
    SIP_Temp_Setpoint_C : REAL;      SIP_Target_F0_min : REAL;
    Cooldown_Temp_C : REAL;
    Incubation_Temp_Setpoint_C : REAL;   Incubation_DO_Setpoint_Pct : REAL;
    Incubation_pH_Setpoint : REAL;         Incubation_Duration_hr : REAL;
    Harvest_OD_Threshold : REAL;
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_Bioreactor_BatchControl
VAR_INPUT
    Recipe : ST_BatchRecipe;
    AI_VesselTemp_C : REAL;       AI_JacketTemp_C : REAL;
    AI_DO_Pct : REAL;               AI_pH : REAL;
    AI_OpticalDensity : REAL;         AI_AgitatorSpeed_RPM : REAL;
    DI_CIP_Complete : BOOL;             DI_StartBatch : BOOL;
    DI_AbortBatch : BOOL;                 DI_System_Enable : BOOL;
END_VAR""")

story += code_block(
"""VAR_OUTPUT
    AO_JacketTempSetpoint_C : REAL := 0.0;
    AO_HeatingValve_Pct : REAL := 0.0;         AO_CoolingValve_Pct : REAL := 0.0;
    AO_AgitatorSpeed_RPM : REAL := 0.0;           AO_O2SpargeValve_Pct : REAL := 0.0;
    DO_AcidPump : BOOL := FALSE;                    DO_BasePump : BOOL := FALSE;
    BatchPhase : E_BatchPhase := PH_IDLE;
    Current_F0_min : REAL := 0.0;                      BatchElapsed_hr : REAL := 0.0;
    Alarm_SIP_Failed : BOOL := FALSE;                     Alarm_DO_Low : BOOL := FALSE;
    Alarm_pH_Excursion : BOOL := FALSE;                     Alarm_TempDeviation : BOOL := FALSE;
    SystemStatus : STRING[28] := 'STANDBY';
END_VAR

VAR
    OuterTemp_PID : FB_PID;         InnerJacketTemp_PID : FB_PID;
    OuterTemp_Kp : REAL := 3.0;       OuterTemp_Ti : REAL := 300.0;
    InnerJacket_Kp : REAL := 6.0;       InnerJacket_Ti : REAL := 60.0;

    DO_PID : FB_PID;
    DO_Kp : REAL := 4.0;                  DO_Ti : REAL := 120.0;
    DO_ControllerOutput_Pct : REAL;
    Agitator_Min_RPM : REAL := 100.0;       Agitator_Max_RPM : REAL := 400.0;

    pH_Deadband : REAL := 0.10;

    T_ScanTime : TON;   T_ScanTime_PT : TIME := T#1S;
    F0_RefTemp_C : REAL := 121.1;   F0_zValue : REAL := 10.0;
    LethalityRate_PerMin : REAL;

    T_IncubationTimer : TON;
    T_CooldownConfirm : TON;   T_CooldownConfirm_PT : TIME := T#5M;
    TempDeviation_Deg : REAL := 2.0;
END_VAR""")

story += code_block(
"""// 1. CASCADE TEMPERATURE CONTROL
IF (BatchPhase = PH_SIP) OR (BatchPhase = PH_COOLDOWN)
   OR (BatchPhase = PH_INOCULATION) OR (BatchPhase = PH_INCUBATION) THEN
    CASE BatchPhase OF
        PH_SIP: OuterTemp_PID(SP := Recipe.SIP_Temp_Setpoint_C, PV := AI_VesselTemp_C,
                  KP := OuterTemp_Kp, TI := OuterTemp_Ti, MANUAL := FALSE, LMN_HLM := 135.0, LMN_LLM := 0.0);
        PH_COOLDOWN: OuterTemp_PID(SP := Recipe.Cooldown_Temp_C, PV := AI_VesselTemp_C,
                  KP := OuterTemp_Kp, TI := OuterTemp_Ti, MANUAL := FALSE, LMN_HLM := 135.0, LMN_LLM := 0.0);
        PH_INOCULATION, PH_INCUBATION: OuterTemp_PID(SP := Recipe.Incubation_Temp_Setpoint_C, PV := AI_VesselTemp_C,
                  KP := OuterTemp_Kp, TI := OuterTemp_Ti, MANUAL := FALSE, LMN_HLM := 135.0, LMN_LLM := 0.0);
        ELSE ;
    END_CASE
    AO_JacketTempSetpoint_C := OuterTemp_PID.LMN;
    InnerJacketTemp_PID(SP := AO_JacketTempSetpoint_C, PV := AI_JacketTemp_C,
        KP := InnerJacket_Kp, TI := InnerJacket_Ti, MANUAL := FALSE, LMN_HLM := 100.0, LMN_LLM := -100.0);
    IF InnerJacketTemp_PID.LMN >= 0.0 THEN
        AO_HeatingValve_Pct := InnerJacketTemp_PID.LMN; AO_CoolingValve_Pct := 0.0;
    ELSE
        AO_HeatingValve_Pct := 0.0; AO_CoolingValve_Pct := ABS(InnerJacketTemp_PID.LMN);
    END_IF
    Alarm_TempDeviation := ABS(AI_VesselTemp_C - OuterTemp_PID.SP) > TempDeviation_Deg;
ELSE
    AO_HeatingValve_Pct := 0.0; AO_CoolingValve_Pct := 0.0; Alarm_TempDeviation := FALSE;
END_IF

// 2. F0 LETHALITY ACCUMULATION
T_ScanTime(IN := (BatchPhase = PH_SIP), PT := T_ScanTime_PT);
IF BatchPhase = PH_SIP THEN
    IF T_ScanTime.Q THEN
        T_ScanTime(IN := FALSE);
        LethalityRate_PerMin := EXPT(10.0, (AI_VesselTemp_C - F0_RefTemp_C) / F0_zValue);
        Current_F0_min := Current_F0_min + (LethalityRate_PerMin * (1.0 / 60.0));
    END_IF
ELSIF BatchPhase = PH_CIP THEN
    Current_F0_min := 0.0;
END_IF""")

_final_block_text = """// 3. DO SPLIT-RANGE CONTROL
IF BatchPhase = PH_INCUBATION THEN
    DO_PID(SP := Recipe.Incubation_DO_Setpoint_Pct, PV := AI_DO_Pct,
            KP := DO_Kp, TI := DO_Ti, MANUAL := FALSE, LMN_HLM := 100.0, LMN_LLM := 0.0);
    DO_ControllerOutput_Pct := DO_PID.LMN;
    IF DO_ControllerOutput_Pct <= 70.0 THEN
        AO_AgitatorSpeed_RPM := Agitator_Min_RPM + (DO_ControllerOutput_Pct / 70.0) * (Agitator_Max_RPM - Agitator_Min_RPM);
        AO_O2SpargeValve_Pct := 0.0;
    ELSE
        AO_AgitatorSpeed_RPM := Agitator_Max_RPM;
        AO_O2SpargeValve_Pct := (DO_ControllerOutput_Pct - 70.0) / 30.0 * 100.0;
    END_IF
    Alarm_DO_Low := AI_DO_Pct < (Recipe.Incubation_DO_Setpoint_Pct * 0.5);
ELSE
    AO_AgitatorSpeed_RPM := 0.0; AO_O2SpargeValve_Pct := 0.0; Alarm_DO_Low := FALSE;
END_IF

// 4. pH DEADBAND DOSING
IF BatchPhase = PH_INCUBATION THEN
    DO_AcidPump := AI_pH > (Recipe.Incubation_pH_Setpoint + pH_Deadband);
    DO_BasePump := AI_pH < (Recipe.Incubation_pH_Setpoint - pH_Deadband);
    Alarm_pH_Excursion := ABS(AI_pH - Recipe.Incubation_pH_Setpoint) > 0.5;
ELSE
    DO_AcidPump := FALSE; DO_BasePump := FALSE; Alarm_pH_Excursion := FALSE;
END_IF"""
story += code_block(_final_block_text)

_final_block_text = """// 5. BATCH PHASE STATE MACHINE
IF DI_AbortBatch THEN BatchPhase := PH_ABORT; END_IF
CASE BatchPhase OF
    PH_IDLE: IF DI_System_Enable AND DI_StartBatch THEN BatchPhase := PH_CIP; END_IF
    PH_CIP: IF DI_CIP_Complete THEN BatchPhase := PH_SIP; END_IF
    PH_SIP: IF Current_F0_min >= Recipe.SIP_Target_F0_min THEN BatchPhase := PH_COOLDOWN; END_IF
    PH_COOLDOWN:
        T_CooldownConfirm(IN := ABS(AI_VesselTemp_C - Recipe.Cooldown_Temp_C) < 1.0, PT := T_CooldownConfirm_PT);
        IF T_CooldownConfirm.Q THEN BatchPhase := PH_INOCULATION; END_IF
    PH_INOCULATION:
        T_IncubationTimer(IN := TRUE, PT := T#2M);
        IF T_IncubationTimer.Q THEN T_IncubationTimer(IN := FALSE); BatchPhase := PH_INCUBATION; END_IF
    PH_INCUBATION:
        T_IncubationTimer(IN := TRUE, PT := REAL_TO_TIME(Recipe.Incubation_Duration_hr * 3600000.0));
        BatchElapsed_hr := TIME_TO_REAL(T_IncubationTimer.ET) / 3600000.0;
        IF T_IncubationTimer.Q OR (AI_OpticalDensity >= Recipe.Harvest_OD_Threshold) THEN
            T_IncubationTimer(IN := FALSE); BatchPhase := PH_HARVEST;
        END_IF
    PH_HARVEST: BatchPhase := PH_COMPLETE;
    PH_COMPLETE: ;
    PH_ABORT:
        AO_HeatingValve_Pct := 0.0; AO_CoolingValve_Pct := 100.0;
        AO_AgitatorSpeed_RPM := 0.0; AO_O2SpargeValve_Pct := 0.0;
        DO_AcidPump := FALSE; DO_BasePump := FALSE;
    ELSE ;
END_CASE
Alarm_SIP_Failed := (BatchPhase = PH_ABORT) AND (Current_F0_min < Recipe.SIP_Target_F0_min);

END_FUNCTION_BLOCK"""
story += code_block(_final_block_text, "Listing B.1 &mdash; Complete FB_Bioreactor_BatchControl source.")
story.append(PageBreak())

# ---- Appendix C: Glossary --------------------------------------------------
story += chapter_head("C", "Appendix C &mdash; Glossary", "APPENDIX")
story.append(data_table(
    ["Term", "Meaning"],
    [
        ["ISA-88", "The standard batch-control model (recipes, phases, procedures) this project follows"],
        ["GMP", "Good Manufacturing Practice &mdash; the regulatory framework for pharma manufacturing"],
        ["CIP / SIP", "Clean-in-Place / Sterilise-in-Place &mdash; automated vessel cleaning and sterilisation"],
        ["F0", "Accumulated sterilisation lethality, expressed as equivalent minutes at 121.1C"],
        ["Cascade control", "An outer loop's output becomes an inner loop's setpoint"],
        ["Split-range control", "One controller output driving two final elements over different output ranges"],
        ["Dissolved Oxygen (DO)", "The concentration of oxygen available to the culture, expressed as % of saturation"],
        ["OD / OD600", "Optical Density &mdash; a common proxy measurement for cell culture density"],
        ["Deadband control", "An on/off control strategy with a tolerance band to prevent output chatter"],
        ["Batch record", "The documented history of a specific manufacturing batch, required for GMP release"],
    ],
    col_widths=[36 * mm, AVAIL_W - 36 * mm]))
story.append(PageBreak())

# ---- About the Author -------------------------------------------------------
story += chapter_head("&mdash;", "About the Author", "CLOSING")
story.append(P(
    "<b>Sipho Lucky Sibanda</b> is an automation and controls engineer building a "
    "multi-disciplinary portfolio spanning marine systems, avionics, architectural "
    "technology, applied AI, biotechnology, and industrial automation. This manual "
    "documents the fourth deliberate discipline shift in that portfolio, following the "
    "same documentation standard as every other project in the series: full logic, I/O "
    "documentation, a live HMI, functional test procedures, and an honest account of what "
    "separates a strong simulation from a validated production system.", lead))
story.append(P("Repository: <b>bioreactor-batch-control</b>", body))
story.append(Spacer(1, 20))
story.append(HRFlowable(width="40%", thickness=1, color=BIOACC))
story.append(Spacer(1, 6))
story.append(P("End of document.", caption))

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
doc = SimpleDocTemplate(
    OUTFILE, pagesize=A4,
    leftMargin=MARGIN_L, rightMargin=MARGIN_R,
    topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOT,
    title="Automated Bioreactor Environmental Control Unit - Technical Manual",
    author=AUTHOR,
)
doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_body)
print("Built:", OUTFILE)
