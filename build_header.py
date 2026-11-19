"""Extend the original editable profile banner with an illustrative MAC array.

The artwork is a conceptual illustration, not a measured hardware simulation.
Requires Pillow. Fonts use the system DejaVu family.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
S = 2
BG = '#090d14'
FG = '#f3f4f6'
MUTED = '#a2adbf'
RED = '#ff5058'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(size, bold=False, mono=False):
    return ImageFont.truetype(MONO if mono else BOLD if bold else SANS, round(size*S))

def text(d, xy, value, size, color=FG, bold=False, mono=False):
    d.text(tuple(round(n*S) for n in xy), value, font=font(size,bold,mono), fill=color)

def line(d, points, color, width=1):
    d.line([(round(x*S),round(y*S)) for x,y in points], fill=color, width=max(1,round(width*S)))

def rect(d, box, fill=None, outline=None, width=1, radius=0):
    box=tuple(round(n*S) for n in box)
    if radius:
        d.rounded_rectangle(box, radius=round(radius*S), fill=fill, outline=outline, width=max(1,round(width*S)))
    else:
        d.rectangle(box, fill=fill, outline=outline, width=max(1,round(width*S)))

def canvas(w,h):
    im=Image.new('RGB',(w*S,h*S),BG)
    d=ImageDraw.Draw(im)
    # Subtle architectural grid and a warm glow behind the compute region.
    for x in range(0,w,32):
        line(d,[(x,0),(x,h)],'#111721',.5)
    for y in range(0,h,32):
        line(d,[(0,y),(w,y)],'#111721',.5)
    for x in range(w-440,w,24):
        for y in range(24,h,24):
            d.ellipse((x*S,y*S,x*S+2,y*S+2),fill='#31303a')
    rect(d,(0,0,5,h),RED)
    return im

def mac_array(d, x, y, cell=39, gap=12, phase=3, labels=True):
    step=cell+gap
    n=6
    extent=n*step-gap
    # Orthogonal links; pulses move into and across the compute fabric.
    for r in range(n):
        yy=y+r*step+cell/2
        line(d,[(x-34,yy),(x+extent+32,yy)],'#60313e',1)
        px=x-32+((phase-r)%14)/14*(extent+64)
        rect(d,(px-3,yy-1.3,px+3,yy+1.3),RED)
    for c in range(n):
        xx=x+c*step+cell/2
        line(d,[(xx,y-30),(xx,y+extent+27)],'#452d3d',1)
    for r in range(n):
        for c in range(n):
            xx=x+c*step; yy=y+r*step
            distance=abs(((r+c-phase+7)%14)-7)
            active=distance<1.3
            trail=distance<2.7
            fill='#79303e' if active else '#301d2b' if trail else '#111722'
            edge=RED if active else '#6b3548' if trail else '#354052'
            rect(d,(xx,yy,xx+cell,yy+cell),fill,edge,1,radius=4)
            if labels and cell>=33:
                text(d,(xx+7,yy+cell/2-7),'MAC',10,'#ffe0df' if active else '#a3aabb',mono=True)
            else:
                line(d,[(xx+cell*.34,yy+cell*.34),(xx+cell*.66,yy+cell*.66)],'#ffc5c4' if active else '#6d7084',1)
                line(d,[(xx+cell*.34,yy+cell*.66),(xx+cell*.66,yy+cell*.34)],'#ffc5c4' if active else '#6d7084',1)
    return extent

def github(phase):
    w,h=1600,560
    im=canvas(w,h); d=ImageDraw.Draw(im)
    text(d,(62,39),'JÔNATAS EDUARDO',24,FG,bold=True)
    text(d,(62,81),'ELECTRONIC ENGINEERING STUDENT',12,MUTED,mono=True)
    line(d,[(62,130),(910,130)],'#303441')
    text(d,(58,168),'AI ACCELERATOR',68,FG,bold=True)
    text(d,(58,246),'ARCHITECTURE',68,RED,bold=True)
    text(d,(63,348),'Building foundations for intelligent computing.',23,MUTED)
    text(d,(1068,47),'COMPUTE / DATAFLOW',13,MUTED,mono=True)
    rect(d,(1068,83,1362,111),'#171b27','#43303d',radius=4)
    text(d,(1154,89),'WEIGHTS',12,MUTED,mono=True)
    mac_array(d,1068,146,39,12,phase)
    text(d,(1410,274),'Σ',24,RED)
    line(d,[(1394,300),(1468,300),(1468,321)],'#854052',2)
    text(d,(1068,465),'MAC ARRAY / ILLUSTRATIVE',11,MUTED,mono=True)
    line(d,[(63,449),(908,449)],'#303441')
    text(d,(63,480),'VHDL / RTL',15,FG,mono=True)
    text(d,(255,480),'COMPUTER ARCHITECTURE',15,FG,mono=True)
    text(d,(623,480),'AI HARDWARE',15,FG,mono=True)
    return im.resize((w,h),Image.Resampling.LANCZOS)

def linkedin():
    w,h=1584,396
    im=canvas(w,h); d=ImageDraw.Draw(im)
    # Main copy is outside the lower-left profile-photo overlap area.
    mac_array(d,100,67,30,8,3,False)
    text(d,(482,39),'JÔNATAS EDUARDO',23,FG,bold=True)
    text(d,(482,80),'ELECTRONIC ENGINEERING STUDENT',12,MUTED,mono=True)
    text(d,(478,126),'AI ACCELERATOR',53,FG,bold=True)
    text(d,(478,188),'ARCHITECTURE',53,RED,bold=True)
    line(d,[(483,270),(1497,270)],'#3c303d')
    text(d,(484,293),'VHDL / RTL  ·  COMPUTER ARCHITECTURE  ·  AI HARDWARE',17,MUTED,mono=True)
    text(d,(484,340),'Building foundations for intelligent computing.',15,MUTED)
    return im.resize((w,h),Image.Resampling.LANCZOS)

if __name__=='__main__':
    static=github(3)
    static.save(OUT/'header-static.png',optimize=True)
    linkedin().save(OUT/'linkedin-banner.png',optimize=True)
    frames=[github(14*i/56) for i in range(56)]
    palette=Image.new('RGB',(256,1))
    palette.putdata([(i,i,i) for i in range(256)])
    # Shared palette includes all reds and active tiles to avoid frame flicker.
    sampler=Image.new('RGB',(1600,560*4))
    for j,k in enumerate([0,8,16,24]): sampler.paste(frames[k],(0,j*560))
    palette=sampler.quantize(colors=160)
    indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(OUT/'header.gif',save_all=True,append_images=indexed[1:],duration=90,loop=0,optimize=True,disposal=1)
    print('Created 1600x560 animated GitHub banner and 1584x396 LinkedIn cover.')
