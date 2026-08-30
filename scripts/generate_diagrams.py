#!/usr/bin/env python3
"""Generate architecture PNG diagrams for modular S4T training decks."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "assets" / "diagrams"
W, H = 1400, 800
BG = (0xF8, 0xFA, 0xFC)
NAVY = (0x0D, 0x2B, 0x45)
NAVY_MID = (0x1A, 0x4A, 0x6E)
TEAL = (0x00, 0x8B, 0x9A)
GREEN = (0x1B, 0x5E, 0x20)
ORANGE = (0xF5, 0x7C, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)
GRAY = (0x37, 0x47, 0x4F)
ACCENT = (0xB2, 0xEB, 0xF2)


def _font(size: int):
    for name in ("DejaVuSans.ttf", "LiberationSans-Regular.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def new_canvas(title: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, W, 72), radius=0, fill=NAVY)
    draw.rounded_rectangle((0, 68, W, 76), radius=0, fill=TEAL)
    draw.text((40, 20), title, fill=WHITE, font=_font(26))
    draw.text((40, 52), "Assembling Smart CPS · Stack4Things", fill=ACCENT, font=_font(13))
    return img, draw


def box(draw, x, y, w, h, label, fill=TEAL, text=WHITE, sub=""):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=14, fill=fill, outline=NAVY_MID, width=2)
    f = _font(18)
    tw = draw.textlength(label, font=f)
    draw.text((x + (w - tw) / 2, y + h / 2 - (24 if sub else 12)), label, fill=text, font=f)
    if sub:
        fs = _font(13)
        sw = draw.textlength(sub, font=fs)
        draw.text((x + (w - sw) / 2, y + h / 2 + 10), sub, fill=text, font=fs)


def arrow(draw, x1, y1, x2, y2):
    draw.line((x1, y1, x2, y2), fill=NAVY, width=3)
    if x2 > x1:
        draw.polygon([(x2, y2), (x2 - 12, y2 - 6), (x2 - 12, y2 + 6)], fill=NAVY)
    elif x2 < x1:
        draw.polygon([(x2, y2), (x2 + 12, y2 - 6), (x2 + 12, y2 + 6)], fill=NAVY)
    elif y2 > y1:
        draw.polygon([(x2, y2), (x2 - 6, y2 - 12), (x2 + 6, y2 - 12)], fill=NAVY)
    else:
        draw.polygon([(x2, y2), (x2 - 6, y2 + 12), (x2 + 6, y2 + 12)], fill=NAVY)


def save(img: Image.Image, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.save(path)
    print(f"OK {path.relative_to(OUT.parent.parent)}")


def diagram_s4t_stack():
    img, d = new_canvas("S4T I/Ocloud Stack (Ch.13)")
    box(d, 80, 120, 200, 70, "Horizon UI", fill=NAVY, sub=":80")
    box(d, 320, 120, 220, 70, "IoTronic Conductor", fill=TEAL, sub="REST :8812")
    box(d, 580, 120, 180, 70, "MariaDB", fill=GRAY)
    box(d, 800, 120, 180, 70, "Keystone", fill=GRAY)
    box(d, 1020, 120, 180, 70, "RabbitMQ", fill=GRAY)
    box(d, 320, 280, 220, 70, "Crossbar WAMP", fill=TEAL, sub=":8181")
    box(d, 580, 280, 180, 70, "WSTUN", fill=ORANGE, sub=":8080")
    box(d, 800, 280, 180, 70, "WAgent", fill=ORANGE)
    box(d, 320, 480, 220, 90, "Lightning-Rod", fill=GREEN, sub="edge :1474")
    box(d, 620, 480, 220, 90, "InfluxDB", fill=GREEN, sub=":8086 (lab)")
    for x1, y1, x2, y2 in [(280, 155, 320, 155), (540, 155, 580, 155), (420, 190, 420, 280), (430, 350, 430, 480)]:
        arrow(d, x1, y1, x2, y2)
    arrow(d, 540, 515, 620, 515)
    d.text((80, 680), "Docker network: s4t — LR connects wss://crossbar:8181", fill=GRAY, font=_font(16))
    save(img, "s4t-stack.png")


def diagram_plugin_pipelines():
    img, d = new_canvas("Plugin Pipelines — Sync vs Async (Ch.14)")
    box(d, 60, 140, 160, 60, "Horizon", fill=NAVY)
    box(d, 280, 140, 180, 60, "IoTronic", fill=TEAL)
    box(d, 520, 140, 180, 60, "Crossbar", fill=TEAL)
    box(d, 760, 140, 200, 60, "Lightning-Rod", fill=GREEN)
    arrow(d, 220, 170, 280, 170)
    arrow(d, 460, 170, 520, 170)
    arrow(d, 700, 170, 760, 170)
    d.text((60, 240), "Sync (Hello): Plugin Call → Worker.run() once → result to Horizon", fill=NAVY, font=_font(17))
    d.text((60, 280), "Async (Ch.15): Start plugin → while _is_running loop → InfluxDB", fill=NAVY, font=_font(17))
    box(d, 760, 320, 200, 70, "Worker plugin", fill=GREEN, sub="class Worker")
    box(d, 520, 420, 180, 60, "InfluxDB", fill=ORANGE)
    arrow(d, 860, 390, 860, 320)
    arrow(d, 760, 455, 700, 455)
    save(img, "plugin-sync-async.png")


def diagram_environmental():
    img, d = new_canvas("Environmental Dataflow (Ch.15)")
    box(d, 80, 200, 180, 70, "CSV file", fill=GRAY)
    box(d, 320, 200, 220, 70, "async Worker", fill=GREEN)
    box(d, 600, 200, 200, 70, "InfluxDB", fill=TEAL, sub="secco DB")
    box(d, 860, 200, 200, 70, "Grafana", fill=NAVY, sub="optional")
    arrow(d, 260, 235, 320, 235)
    arrow(d, 540, 235, 600, 235)
    arrow(d, 800, 235, 860, 235)
    d.text((80, 340), "host=influxdb (NOT localhost) · sleep 30s · measurement environmental_data", fill=GRAY, font=_font(16))
    save(img, "environmental-dataflow.png")


def diagram_vn_attach():
    img, d = new_canvas("Virtual Networking — Attach Port (Ch.5)")
    box(d, 80, 180, 200, 70, "Horizon / API", fill=NAVY)
    box(d, 340, 180, 220, 70, "IoTronic", fill=TEAL)
    box(d, 620, 180, 200, 70, "WAgent", fill=ORANGE)
    box(d, 880, 180, 200, 70, "Board VIF", fill=GREEN, sub="ip, MAC, VIF_name")
    arrow(d, 280, 215, 340, 215)
    arrow(d, 560, 215, 620, 215)
    arrow(d, 820, 215, 880, 215)
    d.text((80, 320), "POST /v1/boards/{uuid}/ports/  →  verify JSON with VIF_name, ip, MAC_add", fill=GRAY, font=_font(16))
    d.text((80, 360), "Lab: attach-port.sh list | attach BOARD_UUID NETWORK_UUID", fill=GRAY, font=_font(16))
    save(img, "vn-attach-workflow.png")


def diagram_fl():
    img, d = new_canvas("Federated Learning — Flower (Ch.19)")
    box(d, 520, 120, 260, 80, "Flower Server", fill=NAVY, sub="server.py")
    for i, (label, x) in enumerate([("board-alpha", 80), ("board-beta", 380), ("board-gamma", 680)]):
        box(d, x, 380, 200, 80, f"LR :{1474+i}", fill=GREEN, sub=label)
        box(d, x, 520, 200, 60, "FL client.py", fill=TEAL, sub=f"heart_{i+1}.csv")
        arrow(d, x + 100, 460, x + 100, 520)
        arrow(d, x + 100, 380, 650, 200)
    d.text((80, 640), "3 Active boards required · demo: FL_ROUNDS=2", fill=GRAY, font=_font(16))
    save(img, "fl-architecture.png")


def diagram_blueprint():
    img, d = new_canvas("SLICES Blueprint — 3 Layers (Ch.11)")
    box(d, 120, 180, 320, 90, "Infrastructure", fill=GRAY, sub="Crossplane + K3s")
    box(d, 120, 320, 320, 90, "Service", fill=TEAL, sub="S4T provider CRDs")
    box(d, 120, 460, 320, 90, "Workflow", fill=GREEN, sub="Experiment composition")
    box(d, 560, 250, 360, 200, "S4T on K3s", fill=NAVY, sub="ch11_s4t-k3s-deploy")
    arrow(d, 440, 225, 560, 300)
    arrow(d, 440, 365, 560, 350)
    arrow(d, 440, 505, 560, 400)
    d.text((560, 500), "Same VM: Docker S4T + K3s (≥8 GB RAM)", fill=GRAY, font=_font(16))
    save(img, "blueprint-layers.png")


def diagram_faas():
    img, d = new_canvas("FaaS / Deviceless Contrast (Ch.7)")
    box(d, 80, 200, 280, 100, "Sync Hello plugin", fill=GREEN, sub="atomic · serverless-like")
    box(d, 480, 200, 280, 100, "Async env plugin", fill=TEAL, sub="long-running service")
    box(d, 880, 200, 280, 100, "Qinling / OpenWhisk", fill=GRAY, sub="theory · external")
    d.text((80, 380), "Lab demo: contrast Plugin Call (once) vs Start (loop) on same LR", fill=GRAY, font=_font(16))
    save(img, "faas-contrast.png")


def diagram_wstun():
    img, d = new_canvas("WSTUN Port Forwarding — Board → Cloud (Ch.14)")
    box(d, 80, 200, 200, 70, "Board LR", fill=GREEN, sub="local :50000")
    box(d, 380, 200, 220, 70, "iotronic-wstun", fill=ORANGE, sub=":8080 control")
    box(d, 680, 200, 240, 70, "Cloud endpoint", fill=NAVY, sub=":50001–50100")
    box(d, 980, 200, 200, 70, "curl client", fill=TEAL)
    arrow(d, 280, 235, 380, 235)
    arrow(d, 600, 235, 680, 235)
    arrow(d, 920, 235, 980, 235)
    d.text((80, 340), "ServiceEnable API → public_port on wstun → HTTP to edge nginx", fill=GRAY, font=_font(16))
    save(img, "wstun-port-forwarding.png")


def diagram_multiboard():
    img, d = new_canvas("Multi-board Fleet Topology (Module D)")
    for i, (name, port) in enumerate([("board-alpha", 1474), ("board-beta", 1475), ("board-gamma", 1476)]):
        x = 80 + i * 420
        box(d, x, 200, 300, 70, name, fill=GREEN)
        box(d, x, 320, 300, 70, f"Lightning-Rod :{port}", fill=TEAL)
        arrow(d, x + 150, 270, x + 150, 320)
    box(d, 480, 480, 360, 80, "Fleet + Hello inject", fill=NAVY)
    for x in (230, 650, 1070):
        arrow(d, x, 390, 660, 480)
    save(img, "multiboard-fleet.png")


# ---------------------------------------------------------------------------
# UML-style sequence diagrams (training workflows)
# ---------------------------------------------------------------------------

def _seq_canvas(title: str, participants: list[str], height: int = 900) -> tuple:
    """Return (image, draw, lifeline_x_coords, y_messages_start)."""
    w = max(W, 160 + len(participants) * 220)
    img = Image.new("RGB", (w, height), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 20), title, fill=NAVY, font=_font(26))
    d.text((40, 52), "UML sequence diagram — training lab workflow", fill=GRAY, font=_font(14))
    xs = []
    pw = min(180, (w - 80) // max(len(participants), 1) - 20)
    gap = (w - 80 - pw * len(participants)) // max(len(participants) - 1, 1)
    x0 = 60
    y_head = 90
    y_end = height - 40
    for i, name in enumerate(participants):
        x = x0 + i * (pw + gap)
        xs.append(x + pw // 2)
        box(d, x, y_head, pw, 50, name, fill=TEAL if i % 2 else NAVY, sub="")
        d.line((xs[-1], y_head + 50, xs[-1], y_end), fill=GRAY, width=2)
    return img, d, xs, y_head + 80, w


def _seq_msg(d, xs, y, src, dst, label, num: str = ""):
    x1, x2 = xs[src], xs[dst]
    col = NAVY
    d.line((x1, y, x2, y), fill=col, width=2)
    if x2 >= x1:
        d.polygon([(x2, y), (x2 - 10, y - 5), (x2 - 10, y + 5)], fill=col)
    else:
        d.polygon([(x2, y), (x2 + 10, y - 5), (x2 + 10, y + 5)], fill=col)
    if num:
        d.text((min(x1, x2) + 8, y - 22), num, fill=ORANGE, font=_font(13))
    tw = min(abs(x2 - x1) - 20, 200)
    lx = min(x1, x2) + 12
    d.text((lx, y - 18), label[:48], fill=NAVY, font=_font(13))


def _seq_return(d, xs, y, src, dst, label=""):
    x1, x2 = xs[src], xs[dst]
    d.line((x1, y, x2, y), fill=GRAY, width=1)
    d.polygon([(x2, y), (x2 + 8, y - 4), (x2 + 8, y + 4)], fill=GRAY)
    if label:
        d.text((min(x1, x2) + 12, y - 16), label, fill=GRAY, font=_font(12))


def seq_training_workflow():
    parts = ["Instructor", "Git/repos", "Docker", "validate-all", "Slides"]
    img, d, xs, y, w = _seq_canvas("Training Lab — End-to-end workflow", parts, 820)
    y0 = y
    steps = [
        (0, 1, "git clone ch13–ch19 repos", "1"),
        (1, 2, "compose up + lab overlay", "2"),
        (2, 3, "stack healthy (18+ checks)", "3"),
        (3, 4, "generate_diagrams + slides", "4"),
        (4, 0, "Module A–I hands-on", "5"),
    ]
    for i, (s, t, lbl, n) in enumerate(steps):
        _seq_msg(d, xs, y0 + i * 70, s, t, lbl, n)
    d.text((40, y0 + 5 * 70 + 20), "Regenerate: scripts/generate_diagrams.py · generate_slides_modular_en.py", fill=GRAY, font=_font(14))
    save(img, "seq-training-workflow.png")


def seq_board_onboarding():
    parts = ["Horizon", "Conductor", "Crossbar", "Lightning-Rod"]
    img, d, xs, y, _ = _seq_canvas("Module A — Board onboarding sequence (Ch.13)", parts, 880)
    msgs = [
        (0, 1, "POST /v1/boards/ (create)", "1"),
        (1, 2, "WAMP board registration", "2"),
        (2, 3, "wss connect + auth", "3"),
        (3, 2, "registration ACK", ""),
        (1, 0, "board state: Active", "4"),
    ]
    for i, (s, t, lbl, n) in enumerate(msgs):
        yy = y + i * 65
        if i == 3:
            _seq_return(d, xs, yy, s, t, lbl)
        else:
            _seq_msg(d, xs, yy, s, t, lbl, n)
    d.text((40, y + 5 * 65 + 10), "LR config: http://{{VM_IP}}:1474/config · credentials {{LR_CRED}}", fill=GRAY, font=_font(13))
    save(img, "seq-board-onboarding.png")


def seq_plugin_sync():
    parts = ["Horizon", "Conductor", "Crossbar", "LR Worker"]
    img, d, xs, y, _ = _seq_canvas("Module B — Sync plugin call (HelloName)", parts, 820)
    for i, (s, t, lbl, n) in enumerate([
        (0, 1, "Inject plugin → board", "1"),
        (0, 1, 'Plugin Call {"name":"..."}', "2"),
        (1, 2, "WAMP rpc invoke", "3"),
        (2, 3, "Worker.run(params)", "4"),
        (3, 2, "Hello <name>", ""),
        (2, 1, "result", ""),
        (1, 0, "display in Horizon", "5"),
    ]):
        yy = y + i * 55
        if lbl in ("Hello <name>", "result"):
            _seq_return(d, xs, yy, s, t, lbl)
        else:
            _seq_msg(d, xs, yy, s, t, lbl, n)
    save(img, "seq-plugin-sync.png")


def seq_environmental_async():
    parts = ["Horizon", "LR Worker", "InfluxDB"]
    img, d, xs, y, _ = _seq_canvas("Module C — Async environmental publisher (Ch.15)", parts, 780)
    for i, (s, t, lbl, n) in enumerate([
        (0, 1, "Inject + Start async plugin", "1"),
        (1, 1, "loop: read CSV row", "2"),
        (1, 2, "POST point → secco DB", "3"),
        (2, 1, "ACK", ""),
        (1, 1, "sleep 30s · repeat", "4"),
    ]):
        yy = y + i * 60
        if lbl == "ACK":
            _seq_return(d, xs, yy, s, t, lbl)
        elif s == t:
            d.line((xs[s] - 30, yy, xs[s] + 30, yy), fill=GREEN, width=2)
            d.polygon([(xs[s] + 30, yy), (xs[s] + 22, yy - 5), (xs[s] + 22, yy + 5)], fill=GREEN)
            d.text((xs[s] + 40, yy - 10), lbl, fill=GREEN, font=_font(13))
            if n:
                d.text((xs[s] - 50, yy - 22), n, fill=ORANGE, font=_font(13))
        else:
            _seq_msg(d, xs, yy, s, t, lbl, n)
    d.text((40, y + 5 * 60 + 10), "host=influxdb (Docker DNS) · measurement environmental_data", fill=GRAY, font=_font(13))
    save(img, "seq-environmental-async.png")


def seq_wstun_enable():
    parts = ["Horizon/API", "Conductor", "WSTUN", "Board HTTP"]
    img, d, xs, y, _ = _seq_canvas("Module F — ServiceEnable / WSTUN sequence (Ch.14)", parts, 860)
    for i, (s, t, lbl, n) in enumerate([
        (0, 1, "POST catalog service (port)", "1"),
        (0, 1, "ServiceEnable on board", "2"),
        (1, 2, "allocate public_port", "3"),
        (2, 3, "open reverse tunnel", "4"),
        (3, 2, "local :8088 or :50000", ""),
        (2, 0, "public_port in response", "5"),
    ]):
        yy = y + i * 58
        if lbl.startswith("local"):
            _seq_return(d, xs, yy, s, t, lbl)
        else:
            _seq_msg(d, xs, yy, s, t, lbl, n)
    d.text((40, y + 6 * 58 + 10), "curl http://{{VM_IP}}:public_port/sensors → JSON (weather demo)", fill=GRAY, font=_font(13))
    save(img, "seq-wstun-enable.png")


def seq_fleet_inject():
    parts = ["Horizon", "Conductor", "board-α", "board-β", "board-γ"]
    img, d, xs, y, _ = _seq_canvas("Module D — Fleet plugin inject sequence", parts, 780)
    _seq_msg(d, xs, y, 0, 1, "Create fleet + add boards", "1")
    _seq_msg(d, xs, y + 55, 0, 1, "Fleet Inject HelloName", "2")
    for i, b in enumerate([2, 3, 4]):
        _seq_msg(d, xs, y + 110 + i * 50, 1, b, "inject plugin", str(3 + i))
    _seq_msg(d, xs, y + 110 + 3 * 50, 0, 1, "fleet status: injected", "6")
    save(img, "seq-fleet-inject.png")


def seq_fl_round():
    parts = ["Flower Server", "client α", "client β", "client γ"]
    img, d, xs, y, _ = _seq_canvas("Module G — Federated Learning round (Ch.19)", parts, 820)
    _seq_msg(d, xs, y, 0, 1, "broadcast global weights", "1")
    _seq_msg(d, xs, y, 0, 2, "broadcast global weights", "1")
    _seq_msg(d, xs, y, 0, 3, "broadcast global weights", "1")
    _seq_msg(d, xs, y + 55, 1, 1, "local train heart_1.csv", "2")
    _seq_msg(d, xs, y + 110, 2, 2, "local train heart_2.csv", "2")
    _seq_msg(d, xs, y + 165, 3, 3, "local train heart_3.csv", "2")
    _seq_msg(d, xs, y + 220, 1, 0, "upload gradients", "3")
    _seq_msg(d, xs, y + 275, 2, 0, "upload gradients", "3")
    _seq_msg(d, xs, y + 330, 3, 0, "upload gradients", "3")
    _seq_msg(d, xs, y + 385, 0, 0, "FedAvg → next round", "4")
    save(img, "seq-fl-round.png")


def main():
    diagram_s4t_stack()
    diagram_plugin_pipelines()
    diagram_environmental()
    diagram_vn_attach()
    diagram_fl()
    diagram_blueprint()
    diagram_faas()
    diagram_wstun()
    diagram_multiboard()
    seq_training_workflow()
    seq_board_onboarding()
    seq_plugin_sync()
    seq_environmental_async()
    seq_wstun_enable()
    seq_fleet_inject()
    seq_fl_round()
    print(f"Generated {len(list(OUT.glob('*.png')))} diagrams in {OUT}")


if __name__ == "__main__":
    main()
