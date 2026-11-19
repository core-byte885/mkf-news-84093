# core-byte885 :: seed mkf-news-84093
# news-image-20261119 : 1024x768 newspaper front page, pure zlib/struct PNG.

import zlib, struct, os

# ---------------------------------------------------------------- 5x7 font
_F = {
'A':["01110","10001","10001","11111","10001","10001","10001"],
'B':["11110","10001","10001","11110","10001","10001","11110"],
'C':["01110","10001","10000","10000","10000","10001","01110"],
'D':["11100","10010","10001","10001","10001","10010","11100"],
'E':["11111","10000","10000","11110","10000","10000","11111"],
'F':["11111","10000","10000","11110","10000","10000","10000"],
'G':["01110","10001","10000","10111","10001","10001","01111"],
'H':["10001","10001","10001","11111","10001","10001","10001"],
'I':["01110","00100","00100","00100","00100","00100","01110"],
'J':["00111","00010","00010","00010","00010","10010","01100"],
'K':["10001","10010","10100","11000","10100","10010","10001"],
'L':["10000","10000","10000","10000","10000","10000","11111"],
'M':["10001","11011","10101","10101","10001","10001","10001"],
'N':["10001","10001","11001","10101","10011","10001","10001"],
'O':["01110","10001","10001","10001","10001","10001","01110"],
'P':["11110","10001","10001","11110","10000","10000","10000"],
'Q':["01110","10001","10001","10001","10101","10010","01101"],
'R':["11110","10001","10001","11110","10100","10010","10001"],
'S':["01111","10000","10000","01110","00001","00001","11110"],
'T':["11111","00100","00100","00100","00100","00100","00100"],
'U':["10001","10001","10001","10001","10001","10001","01110"],
'V':["10001","10001","10001","10001","10001","01010","00100"],
'W':["10001","10001","10001","10101","10101","11011","10001"],
'X':["10001","10001","01010","00100","01010","10001","10001"],
'Y':["10001","10001","01010","00100","00100","00100","00100"],
'Z':["11111","00001","00010","00100","01000","10000","11111"],
'0':["01110","10001","10011","10101","11001","10001","01110"],
'1':["00100","01100","00100","00100","00100","00100","01110"],
'2':["01110","10001","00001","00110","01000","10000","11111"],
'3':["11110","00001","00001","01110","00001","00001","11110"],
'4':["00010","00110","01010","10010","11111","00010","00010"],
'5':["11111","10000","11110","00001","00001","10001","01110"],
'6':["00110","01000","10000","11110","10001","10001","01110"],
'7':["11111","00001","00010","00100","01000","01000","01000"],
'8':["01110","10001","10001","01110","10001","10001","01110"],
'9':["01110","10001","10001","01111","00001","00010","01100"],
' ':["00000","00000","00000","00000","00000","00000","00000"],
'.':["00000","00000","00000","00000","00000","00100","00100"],
',':["00000","00000","00000","00000","00100","00100",  "01000"],
':':["00000","00100","00100","00000","00100","00100","00000"],
';':["00000","00100","00100","00000","00100","00100","01000"],
'!':["00100","00100","00100","00100","00100","00000","00100"],
'?':["01110","10001","00001","00110","00100","00000","00100"],
'-':["00000","00000","00000","11111","00000","00000","00000"],
'/':["00001","00010","00010","00100","01000","01000","10000"],
'(':["00010","00100","01000","01000","01000","00100","00010"],
')':["01000","00100","00010","00010","00010","00100","01000"],
"'":["00100","00100","01000","00000","00000","00000","00000"],
'"':["01010","01010","00000","00000","00000","00000","00000"],
'+':["00000","00100","00100","11111","00100","00100","00000"],
'=':["00000","00000","11111","00000","11111","00000","00000"],
'%':["10001","00010","00100","00100","01000","10001","00000"],
'$':["00100","01111","10100","01110","00101","11110","00100"],
'&':["01100","10010","10100","01000","10101","10010","01101"],
'*':["00000","10101","01110","11111","01110","10101","00000"],
'#':["01010","11111","01010","01010","01010","11111","01010"],
'@':["01110","10001","10111","10101","10111","10000","01110"],
'<':["00010","00100","01000","10000","01000","00100","00010"],
'>':["01000","00100","00010","00001","00010","00100","01000"],
'|':["00100","00100","00100","00100","00100","00100","00100"],
'_':["00000","00000","00000","00000","00000","00000","11111"],
'^':["00100","01010","00000","00000","00000","00000","00000"],
'~':["00000","00000","01000","10101","00010","00000","00000"],
'[':["01110","00100","00100","00100","00100","00100","01110"],
']':["01110","00100","00100","00100","00100","00100","01110"],
}
FONT = {c: [int(row, 2) for row in rows] for c, rows in _F.items()}
GLYPH_W, GLYPH_H = 5, 7

# ---------------------------------------------------------------- palette
PAPER  = bytes((0xF7, 0xF2, 0xE6))
INK    = bytes((0x18, 0x22, 0x33))
RED    = bytes((0x8C, 0x2F, 0x2F))
BLUE   = bytes((0x2C, 0x4A, 0x6E))
GREY   = bytes((0x8A, 0x8A, 0x80))
LGREY  = bytes((0xD9, 0xD3, 0xC4))
WHITE  = bytes((0xFF, 0xFF, 0xFF))
GOLD   = bytes((0xB8, 0x8A, 0x2E))
TEAL   = bytes((0x2E, 0x6B, 0x66))

# ---------------------------------------------------------------- canvas
W, H = 1024, 768
_buf = bytearray(PAPER * (W * H))

def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        _buf[i:i+3] = c

def rect(x0, y0, w, h, c):
    x0 = max(0, x0); y0 = max(0, y0)
    w = min(w, W - x0); h = min(h, H - y0)
    if w <= 0 or h <= 0:
        return
    row = bytes(c) * w
    off = (y0 * W + x0) * 3
    step = W * 3
    for _ in range(h):
        _buf[off:off+len(row)] = row
        off += step

def hline(x0, x1, y, c, t=1):
    rect(x0, y, x1 - x0, t, c)

def vline(x, y0, y1, c, t=1):
    rect(x, y0, t, y1 - y0, c)

def invert_rect(x0, y0, w, h):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            i = (y * W + x) * 3
            _buf[i]   ^= 255
            _buf[i+1] ^= 255
            _buf[i+2] ^= 255

# ---------------------------------------------------------------- text
def text(s, x, y, c=INK, scale=1, spacing=1):
    cx = x
    adv = (GLYPH_W + spacing) * scale
    for ch in s.upper():
        g = FONT.get(ch, FONT['?'])
        for r in range(GLYPH_H):
            bi= g[r]
            for b in range(GLYPH_W):
                if bi>> (GLYPH_W - 1 - b) & 1:
                    if scale == 1:
                        px(cx + b, y + r, c)
                    else:
                        rect(cx + b*scale, y + r*scale, scale, scale, c)
        cx += adv
    return cx

def text_w(s, scale=1, spacing=1):
    return len(s) * (GLYPH_W + spacing) * scale - spacing * scale

def text_c(s, cx, y, c=INK, scale=1, spacing=1):
    return text(s, cx - text_w(s, scale, spacing)//2, y, c, scale, spacing)

def text_r(s, rx, y, c=INK, scale=1, spacing=1):
    return text(s, rx - text_w(s, scale, spacing), y, c, scale, spacing)

# ---------------------------------------------------------------- layout
M = 28            # page margin
CW = W - 2 * M    # content width

def rule(y, t=2, c=INK):
    hline(M, W - M, y, c, t)

def box(x, y, w, h, border=INK, t=1):
    hline(x, x + w, y, border, t)
    hline(x, x + w, y + h - t, border, t)
    vline(x, y, y + h, border, t)
    vline(x + w - t, y, y + h, border, t)

def kicker(s, x, y, c=RED, scale=1):
    return text(s, x, y, c, scale)

def byline(s, x, y, c=GREY):
    return text(s, x, y, c, 1)

# ---------------------------------------------------------------- masthead
def masthead():
    # top folio line
    text_l = "LATE EDITION"
    text_r_ = "No. 84093"
    text_l2 = "CITY FINAL"
    text(text_l, M, 10, RED, 1)
    text(text_l2, M + text_w(text_l) + 10, 10, GREY, 1)
    text_r("No. 84093  |  ONE DOLLAR", W - M, 10, GREY, 1)
    # masthead title
    ty = 26
    text_c("WORLD NEWS", W // 2, ty, INK, 7)
    # thin double rules under title
    rule(ty + 42, 2, INK)
    rule(ty + 45, 1, GREY)
    # dateline band
    dy = ty + 52
    text_c("THURSDAY 19 NOVEMBER 2026", W // 2, dy, INK, 2)
    # flanking ornaments
    hline(M, W//2 - 118, dy + 6, GOLD, 2)
    hline(W//2 + 118, W - M, dy + 6, GOLD, 2)
    text("*", W//2 - 110, dy - 1, GOLD, 1)
    text("*", W//2 + 105, dy - 1, GOLD, 1)
    rule(dy + 18, 1, GREY)
    return dy + 26   # y where content starts

# ---------------------------------------------------------------- headline boxes
def headline_box(x, y, w, h, kick, head_lines, body, accent, fill=None,
                 kicker_dark=False):
    """One framed story box with kicker, headline, body filler text."""
    if fill is not None:
        rect(x + 1, y + 1, w - 2, h - 2, fill)
    box(x, y, w, h, accent, 2)
    pad = 8
    cy = y + pad
    # kicker tag
    if kicker_dark:
        kw = text_w(kick, 1) + 8
        rect(x + pad, cy - 2, kw, 11, accent)
        text(kick, x + pad + 4, cy, PAPER, 1)
        cy += 16
    else:
        text(kick, x + pad, cy, accent, 1)
        cy += 12
    hline(x + pad, x + w - pad, cy, accent, 1)
    cy += 5
    # headline lines (scale 2, up to 3 lines)
    for line in head_lines:
        text(line, x + pad, cy, INK, 2)
        cy += 18
    cy += 3
    rule_gap = h - (cy - y) - 10
    # body: wrapped filler text at scale 1
    if body:
        maxw = w - 2 * pad
        words = body.split()
        line = ""
        lines = []
        for wd in words:
            t = (line + " " + wd).strip()
            if text_w(t, 1) <= maxw:
                line = t
            else:
                lines.append(line)
                line = wd
        if line:
            lines.append(line)
        for ln in lines:
            if cy > y + h - 12:
                break
            text(ln, x + pad, cy, INK, 1)
            cy += 10
    return cy

# ---------------------------------------------------------------- art blocks
def art_coins(x, y, w, h):
    """Markets: simple candlestick chart."""
    rect(x, y, w, h, INK)
    base = y + h - 14
    prices = [30, 38, 34, 46, 42, 55, 50, 62, 58, 72, 66, 80, 76, 90]
    n = len(prices)
    cw_ = (w - 20) // n
    for i, p in enumerate(prices):
        cx = x + 10 + i * cw_
        bh = int(p * (h - 30) / 100)
        col = GOLD if i % 3 else TEAL
        vline(cx, base - bh, base, col, max(2, cw_ - 4))
        hline(cx - 3, cx + 3, base - bh, WHITE, 1)
    text("GLOBAL MARKETS", x + 6, y + 5, PAPER, 1)
    text("+2.4%", x + w - text_w("+2.4%", 1) - 6, y + 5, GOLD, 1)

def art_globe(x, y, w, h):
    """Climate: globe with meridians."""
    rect(x, y, w, h, TEAL)
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 12
    # filled disc via midpoint scanlines
    for dy in range(-r, r + 1):
        half = int((r*r - dy*dy) ** 0.5)
        hline(cx - half, cx + half, cy + dy, PAPER, 1)
    # latitude lines
    for k in (-2, -1, 0, 1, 2):
        dy = k * r // 3
        half = int((r*r - dy*dy) ** 0.5)
        hline(cx - half, cx + half, cy + dy, TEAL, 1)
    # meridians: ellipses via per-row width
    for m in (1, 2):
        mw = r * m // 3
        for dy in range(-r, r + 1):
            half = int((mw*mw * (1 - (dy*dy)/(r*r))) ** 0.5) if r else 0
            if half:
                px(cx - half, cy + dy, TEAL)
                px(cx + half, cy + dy, TEAL)
    vline(cx, cy - r, cy + r, TEAL, 1)
    text("COP31 BELEM", x + 6, y + 5, PAPER, 1)
    text("DAY 9", x + w - text_w("DAY 9") - 6, y + 5, GOLD, 1)

def art_chip(x, y, w, h):
    """Tech: chip die on motherboard traces."""
    rect(x, y, w, h, INK)
    # traces
    for i in range(6):
        ty = y + 12 + i * (h - 24) // 5
        hline(x, x + w, ty, BLUE, 1)
        px(x + 14 + i * 9, ty, GOLD)
    # chip body
    cw_, ch_ = w // 3, h // 2
    x0, y0 = x + (w - cw_)//2, y + (h - ch_)//2
    rect(x0, y0, cw_, ch_, GREY)
    box(x0, y0, cw_, ch_, PAPER, 1)
    rect(x0 + cw_//4, y0 + ch_//4, cw_//2, ch_//2, INK)
    text("AI", x0 + cw_//2 - 7, y0 + ch_//2 - 3, GOLD, 1)
    # pins
    for i in range(5):
        px(x0 - 3 + i * (cw_ + 6) // 4, y0 - 2, GOLD)
        px(x0 - 3 + i * (cw_ + 6) // 4, y0 + ch_ + 1, GOLD)
    text("SILICON WATCH", x + 6, y + 5, PAPER, 1)

def art_ball(x, y, w, h):
    """Sport: football pitch top-down with ball."""
    rect(x, y, w, h, TEAL)
    # pitch stripes
    for i in range(0, w, 24):
        if (i // 24) % 2 == 0:
            rect(x + i, y, min(24, w - i), h, bytes((0x2E, 0x7B, 0x6B)))
    box(x + 6, y + 6, w - 12, h - 12, PAPER, 1)
    hline(x + 6, x + w - 6, y + h // 2, PAPER, 1)
    # centre circle
    cx, cy = x + w // 2, y + h // 2
    r = 12
    for dy in range(-r, r + 1):
        half = int((r*r - dy*dy) ** 0.5)
        px(cx - half, cy + dy, PAPER)
        px(cx + half, cy + dy, PAPER)
    # ball
    rect(cx - 3, cy - 3, 6, 6, WHITE)
    px(cx - 1, cy - 1, INK)
    text("FULL TIME", x + 8, y + 8, PAPER, 1)

# ---------------------------------------------------------------- page
def draw_page():
    top = masthead()
    col = (W - 2 * M - 3 * 12) // 3   # 3 columns with 12px gutters
    g = 12
    x0 = M
    x1 = M + col + g
    x2 = M + 2 * (col + g)
    bot = H - M

    # ---------------- lead story (full width, top)
    lead_h = 118
    headline_box(
        x0, top, W - 2 * M, lead_h,
        "GAMING / CONSOLE LAUNCH",
        ["GTA VI HITS SHELVES TODAY",
         "AS NEXT-GEN CONSOLES",
         "SELL OUT WORLDWIDE"],
        "Retailers report midnight queues as the long-awaited "
        "title lands on store shelves; console bundles sell out "
        "within hours across three continents.",
        RED, None, True)
    y = top + lead_h + 12

    # ---------------- three columns of boxes
    # column 1: markewith chart
    c1h = 172
    headline_box(
        x0, y, col, c1h,
        "MARKETS",
        ["STOCKS RALLY",
         "TO RECORD",
         "HIGHS"],
        None, BLUE, None, False)
    art_coins(x0 + 8, y + c1h - 66, col - 16, 58)

    # column 2: climate with globe art
    c2h = 172
    headline_box(
        x1, y, col, c2h,
        "CLIMATE",
        ["COP31 DEAL",
         "NEAR ON",
         "COAL PHASE"],
        None, TEAL, None, False)
    art_globe(x1 + 8, y + c2h - 66, col - 16, 58)

    # column 3: tech with chip art
    c3h = 172
    headline_box(
        x2, y, col, c3h,
        "TECH / AI",
        ["AI CHIPS",
         "POWER NEW",
         "DATA WAVE"],
        None, GOLD, None, False)
    art_chip(x2 + 8, y + c3h - 66, col - 16, 58)

    y2 = y + c1h + 12

    # ---------------- sport strip (left 2 cols) + weather box (right)
    s_h = 108
    headline_box(
        x0, y2, 2 * col + g, s_h,
        "SPORT",
        ["HOSTS LIFT THE FINAL",
         "IN ADDED TIME THRILLER"],
        "A stoppage-time goal settles a breathless final in front "
        "of a full house; fans spill onto the streets the "
        "tournament closes in style.",
        BLUE, None, True)

    # weather box (right col)
    wx, wy, ww, wh = x2, y2, col, s_h
    rect(wx + 1, wy + 1, ww - 2, wh - 2, INK)
    box(wx, wy, ww, wh, GOLD, 2)
    text("TOMORROW", wx + 8, wy + 8, GOLD, 1)
    text_c("13C", wx + ww // 2, wy + 24, PAPER, 3)
    text_c("MILD | WINDY", wx + ww // 2, wy + 52, LGREY, 1)
    # little sun/cloud icon
    icx, icy = wx + ww // 2, wy + 72
    for dy in range(-6, 7):
        half = int((36 - dy*dy) ** 0.5)
        hline(icx - 6 - half, icx - 6 + half, icy + dy, GOLD, 1)
    rect(icx - 10, icy - 2, 16, 9, PAPER)
    rect(icx - 7, icy - 6, 12, 5, PAPER)

    y3 = y2 + s_h + 12

    # ---------------- bottom: briefs column + quote box
    q_h = bot - y3
    # left: world in brief
    rect(x0 + 1, y3 + 1, 2 * col + g - 2, q_h - 2, PAPER)
    box(x0, y3, 2 * col + g, q_h, RED, 2)
    text("WORLD IN BRIEF", x0 + 8, y3 + 8, RED, 1)
    hline(x0 + 8, x0 + 2 * col + g - 8, y3 + 20, RED, 1)
    briefs = [
        "SUMMIT: LEADERS AGREE EMISSIONS CHECK 2031",
        "MARKETS: OIL STEADIES BELOW 71 DOLLARS",
        "TECH: CHIP EXPORT RULES EASED FOR PLANTS",
        "CITY: TRANSIT STRIKE ENDS ON NIGHT SERVICE",
        "SPACE: CREW DOCKS AFTER SIX HOUR FLIGHT",
    ]
    by = y3 + 26
    for b in briefs:
        text("*", x0 + 8, by, GOLD, 1)
        text(b, x0 + 18, by, INK, 1)
        by += 11
    # mini "market closing" ticker line
    hline(x0 + 8, x0 + 2 * col + g - 8, by + 2, LGREY, 1)
    text("CLOSING: FT 8410 +1.2  DAX 24110 +0.8  NIKKEI 52904 +1.5",
         x0 + 8, by + 7, BLUE, 1)

    # right: quote of the day
    qx, qw = x2, col
    rect(qx + 1, y3 + 1, qw - 2, q_h - 2, PAPER)
    box(qx, y3, qw, q_h, TEAL, 2)
    text("\"", qx + 6, y3 + 6, TEAL, 3)
    text_c("THE WORLD", qx + qw // 2, y3 + 30, INK, 1)
    text_c("IS ONE MARKET", qx + qw // 2, y3 + 41, INK, 1)
    text_c("NOW.", qx + qw // 2, y3 + 52, INK, 1)
    text_c("- MARKET NOTE", qx + qw // 2, y3 + 68, GREY, 1)

    # footer
    rule(bot - 2, 1, GREY)
    text("WORLD NEWS DESK", M, bot - 8, GREY, 1)
    text_r("PAGE 1 OF 1", W - M, bot - 8, GREY, 1)

# ---------------------------------------------------------------- png out
def make_png(path):
    draw_page()
    raw = b"\x00" + bytes(_buf[0:W*3])  # placeholder replaced below
    stride = W * 3
    rows = b""
    for y_ in range(H):
        rows += b"\x00" + bytes(_buf[y_*stride:(y_+1)*stride])
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(rows, 9))
    png += chunk(b"IEND", b"")
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)
    return png

if __name__ == "__main__":
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    p = os.path.join(out, "entry.png")
    data = make_png(p)
    print(f"wrote {p} {len(data)} bytes")
