"""Render lightweight, self-hosted motion graphics for a GitHub README.

These are editable typography/UI assets. Requires Pillow; uses DejaVu fonts.
Run from any directory: python3 scripts/build_readme_motion.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
BG = '#0d1117'
RED = '#ff5058'
FG = '#e6edf3'
MUTED = '#8b949e'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

def save_gif(frames, durations, name):
    # One palette for all frames avoids color flicker.
    sampler = Image.new('RGB', (frames[0].width, frames[0].height * 3), BG)
    for i, frame in enumerate((frames[0], frames[len(frames)//2], frames[-1])):
        sampler.paste(frame, (0, i * frame.height))
    palette = sampler.quantize(colors=64)
    indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(OUT/name, save_all=True, append_images=indexed[1:],
                    duration=durations, loop=0, disposal=1, optimize=True)

def focus_line():
    w, h, scale = 1000, 76, 2
    font = ImageFont.truetype(MONO, 28*scale)
    prefix_font = ImageFont.truetype(MONO, 24*scale)
    phrases = ['Applied AI & generative models',
               'Computer vision & multi-agent systems',
               'AI Accelerator Architecture']
    frames, durations = [], []
    def frame(phrase, cursor=True):
        im = Image.new('RGB', (w*scale, h*scale), BG)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((2, 2, w*scale-3, h*scale-3), radius=14*scale,
                            fill=BG, outline='#30363d', width=2)
        d.text((24*scale, 20*scale), '>_', font=prefix_font, fill=RED)
        d.text((82*scale, 18*scale), phrase, font=font, fill=FG)
        x = 82*scale+d.textlength(phrase, font=font)+7*scale
        if cursor:
            d.rectangle((x, 23*scale, x+2*scale, 51*scale), fill=RED)
        return im.resize((w,h), Image.Resampling.LANCZOS)
    for phrase in phrases:
        for i in range(len(phrase)+1):
            frames.append(frame(phrase[:i])); durations.append(80)
        for _ in range(2):
            frames.extend([frame(phrase,False),frame(phrase,True)])
            durations.extend([450,450])
        for i in range(len(phrase)-1,-1,-1):
            frames.append(frame(phrase[:i])); durations.append(40)
        frames.append(frame('')); durations.append(300)
    save_gif(frames,durations,'focus-line.gif')

def inline_chip():
    w=h=72; s=3
    frames=[]
    for frame in range(36):
        im=Image.new('RGB',(w*s,h*s),BG)
        d=ImageDraw.Draw(im)
        def line(points,color,width=1.5):
            d.line([(round(x*s),round(y*s)) for x,y in points],fill=color,width=round(width*s))
        for p in (25,36,47):
            line([(p,7),(p,18)],'#81404b')
            line([(p,54),(p,65)],'#81404b')
            line([(7,p),(18,p)],'#81404b')
            line([(54,p),(65,p)],'#81404b')
        d.rounded_rectangle((18*s,18*s,54*s,54*s),radius=7*s,
                            fill='#161b22',outline=RED,width=2*s)
        for row in range(3):
            for col in range(3):
                phase=(frame/4-row-col)%9
                active=phase<2
                x=(25+col*11)*s; y=(25+row*11)*s
                color=RED if active else '#44303c'
                d.rounded_rectangle((x-3*s,y-3*s,x+3*s,y+3*s),radius=s,fill=color)
        frames.append(im.resize((w,h),Image.Resampling.LANCZOS))
    save_gif(frames,[100]*len(frames),'inline-chip.gif')

if __name__=='__main__':
    focus_line()
    inline_chip()
    for p in sorted(OUT.glob('*.gif')):
        im=Image.open(p)
        print(f'{p.name}: {im.width}x{im.height}, {im.n_frames} frames, {p.stat().st_size:,} bytes')
