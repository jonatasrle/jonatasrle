"""Render an original, illustrative digital timing diagram for the profile."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
S = 2
W,H = 1280,430
BG = '#0d1117'
FG = '#f0f3f6'
MUTED = '#a5b0be'
RED = '#ff514e'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size, bold=False, mono=False):
    return ImageFont.truetype(MONO if mono else BOLD if bold else SANS, size*S)
def text(d, xy, value, size, color=FG, bold=False, mono=False):
    d.text(tuple(int(n*S) for n in xy),value,font=font(size,bold,mono),fill=color)
def line(d, pts, color, width=1):
    d.line([(int(x*S),int(y*S)) for x,y in pts],fill=color,width=width*S)
def rect(d, box, fill=None, outline=None, width=1, radius=0):
    box = tuple(int(n*S) for n in box)
    if radius:d.rounded_rectangle(box,radius=radius*S,fill=fill,outline=outline,width=width*S)
    else:d.rectangle(box,fill=fill,outline=outline,width=width*S)

base = Image.new('RGB',(W*S,H*S),BG)
d = ImageDraw.Draw(base)
for x in range(704,1280,24):
    for y in range(28,430,24):
        d.ellipse((x*S,y*S,x*S+2,y*S+2),fill='#242c36')
rect(d,(0,0,7,H),RED)
text(d,(44,34),'JRE  /  ENGINEERING NOTEBOOK',14,RED,mono=True)
text(d,(44,78),'Jônatas',65,bold=True)
text(d,(44,152),'Eduardo.',65,bold=True)
text(d,(47,244),'Electronics. Code. Curiosity.',24,MUTED)
line(d,[(47,300),(1200,300)],'#2d333d')
text(d,(47,331),'INSTRUMENTATION',15,MUTED,mono=True)
text(d,(327,331),'PYTHON AUTOMATION',15,MUTED,mono=True)
text(d,(644,331),'DIGITAL HARDWARE',15,MUTED,mono=True)
text(d,(47,382),'RIO DE JANEIRO / BR',12,'#7d8998',mono=True)
text(d,(1058,382),'@ZAGALU',12,RED,mono=True)

# Precise rectangular clock trace and illustrative data-bus timing.
rect(d,(737,42,1234,276),'#111820','#303945',radius=14)
text(d,(763,62),'TIMING / DIGITAL DESIGN',13,MUTED,mono=True)
line(d,[(762,95),(1209,95)],'#303945')
text(d,(763,120),'CLK',14,MUTED,mono=True)
text(d,(763,187),'DATA',14,MUTED,mono=True)
start,end,step=839,1206,40
clock=[(start,153)]
for i,x in enumerate(range(start,end,step)):
    y=124 if i%2==0 else 153
    clock.extend([(x,y),(min(x+step,end),y)])
line(d,clock,RED,2)
for x in range(start,end,80):
    line(d,[(x,111),(x,232)],'#24313d')
for j,val in enumerate(['01','10','11','00']):
    x=start+j*92
    points=[(x,202),(x+8,186),(x+84,186),(x+92,202),(x+84,218),(x+8,218),(x,202)]
    line(d,points,'#8c9dad',1)
    text(d,(x+34,191),val,13,FG,mono=True)
text(d,(763,246),'SIGNALS → LOGIC → SYSTEMS',12,'#82909e',mono=True)
frames=[]
for i in range(56):
    im=base.copy(); a=ImageDraw.Draw(im)
    x=start+(end-start)*i/56
    rect(a,(x-12,109,x+12,230),'#192b37')
    # Redraw traces over the translucent-style cursor strip.
    line(a,clock,RED,2)
    for j in range(4):
        bx=start+j*92
        line(a,[(bx,202),(bx+8,186),(bx+84,186),(bx+92,202),(bx+84,218),(bx+8,218),(bx,202)],'#8c9dad')
        text(a,(bx+34,191),['01','10','11','00'][j],13,FG,mono=True)
    line(a,[(x,109),(x,230)],'#fd8c73',1)
    a.ellipse(((x-3)*S,102*S,(x+3)*S,108*S),fill=RED)
    frames.append(im.resize((W,H),Image.Resampling.LANCZOS))
frames[0].save(OUT/'header-static.png')
palette=base.resize((W,H),Image.Resampling.LANCZOS).quantize(colors=128)
indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
indexed[0].save(OUT/'header.gif',save_all=True,append_images=indexed[1:],duration=80,loop=0,optimize=True,disposal=1)
print(f'GIF: {(OUT/"header.gif").stat().st_size:,} bytes; {len(frames)} frames')
