"""D.B. Cooper belgeselini uçtan uca üretir.

Kullanım:
    .venv/bin/python scripts/crime_documentary/render.py [--out storage/dbcooper]

Adımlar: Edge TTS ile seslendirme (kelime zamanlamalı) -> PIL ile sahne
görselleri -> ffmpeg ile Ken Burns + film greni -> sentezlenmiş gerilim
müziği -> ASS altyazı -> son MP4 + küçük resim + YouTube metinleri.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import subprocess
import sys
import wave
from pathlib import Path

import edge_tts
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import story  # noqa: E402
import visuals  # noqa: E402

FPS = 30
VOICE = "tr-TR-AhmetNeural"
RATE = "+25%"
SR = 44100


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


# ------------------------------------------------------------------ TTS
async def tts_one(text: str, mp3: Path, meta: Path):
    if mp3.exists() and meta.exists() and mp3.stat().st_size > 0:
        return
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    for attempt in range(5):
        try:
            comm = edge_tts.Communicate(text, VOICE, rate=RATE, proxy=proxy, boundary="WordBoundary")
            words, audio = [], bytearray()
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    audio.extend(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    words.append({
                        "start": chunk["offset"] / 1e7,
                        "end": (chunk["offset"] + chunk["duration"]) / 1e7,
                        "text": chunk["text"],
                    })
            mp3.write_bytes(bytes(audio))
            meta.write_text(json.dumps(words, ensure_ascii=False))
            return
        except Exception as e:  # ağ hatalarında tekrar dene
            print(f"  TTS tekrar ({attempt + 1}): {e}")
            await asyncio.sleep(2 * (attempt + 1))
    raise RuntimeError("TTS başarısız")


def probe_duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)
    ])
    return float(out.strip())


# ------------------------------------------------------------- altyazı
def attach_punctuation(words, text):
    """TTS kelime sınırları noktalamasızdır; orijinal metinden geri ekle."""
    pos = 0
    for w in words:
        j = text.find(w["text"], pos)
        if j < 0:
            continue
        k = j + len(w["text"])
        while k < len(text) and not text[k].isspace() and not text[k].isalnum():
            k += 1
        w["text"] = text[j:k]
        pos = k


def tr_title(text):
    low = text.replace("I", "ı").replace("İ", "i").lower()
    return " ".join(x[:1].replace("i", "İ").replace("ı", "I").upper() + x[1:] for x in low.split(" "))


def ass_time(t: float) -> str:
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def build_subs(all_words, path: Path):
    lines = []
    cur = []
    for w in all_words:
        cur.append(w)
        text = " ".join(x["text"] for x in cur)
        ends_sentence = w["text"][-1:] in ".?!:"
        if len(text) > 38 or ends_sentence or len(cur) >= 7:
            lines.append(cur)
            cur = []
    if cur:
        lines.append(cur)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter Display,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,120,120,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for i, ln in enumerate(lines):
        start = ln[0]["start"]
        end = ln[-1]["end"] + 0.15
        if i + 1 < len(lines):
            end = min(end + 0.3, lines[i + 1][0]["start"])
        text = " ".join(x["text"] for x in ln)
        events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Sub,,0,0,0,,{text}")
    path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- müzik
def synth_music(total: float, hits: list[float], path: Path):
    n = int(total * SR)
    t = np.arange(n) / SR
    # karanlık drone: Re minör tonlar, yavaş nefes alan genlik
    sig = np.zeros(n)
    for f, a, lfo in [(36.71, 0.30, 0.031), (55.0, 0.22, 0.047), (73.42, 0.14, 0.023), (87.31, 0.08, 0.057), (110.0, 0.05, 0.019)]:
        env = 0.6 + 0.4 * np.sin(2 * np.pi * lfo * t + f)
        sig += a * env * np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.1 * t))
    # kalp atışı nabzı (dakikada ~52)
    beat = 60 / 52
    ph = np.mod(t, beat)
    thump = np.exp(-ph * 18) * np.sin(2 * np.pi * 48 * ph) + 0.6 * np.exp(-np.clip(ph - 0.22, 0, None) * 18) * np.sin(2 * np.pi * 44 * np.clip(ph - 0.22, 0, None)) * (ph > 0.22)
    sig += 0.18 * thump
    # rüzgâr/hışırtı: filtrelenmiş gürültü
    rng = np.random.default_rng(1)
    noise = rng.standard_normal(n)
    k = 400
    noise = np.convolve(noise, np.ones(k) / k, mode="same") * 6
    sig += 0.05 * noise * (0.5 + 0.5 * np.sin(2 * np.pi * 0.013 * t))
    # bölüm geçişlerinde derin vuruş
    for h in hits:
        i0 = int(h * SR)
        L = int(3.5 * SR)
        if i0 >= n:
            continue
        L = min(L, n - i0)
        tt = np.arange(L) / SR
        boom = np.sin(2 * np.pi * (60 * np.exp(-tt * 1.2) + 28) * tt) * np.exp(-tt * 1.6)
        sig[i0:i0 + L] += 0.9 * boom
    # giriş/çıkış fade
    fade = int(4 * SR)
    sig[:fade] *= np.linspace(0, 1, fade)
    sig[-fade:] *= np.linspace(1, 0, fade)
    sig = sig / np.max(np.abs(sig)) * 0.9
    pcm = (sig * 32767).astype(np.int16)
    stereo = np.column_stack([pcm, pcm]).ravel()
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(stereo.tobytes())


# ----------------------------------------------------------------- klip
MOTIONS = [
    ("min(1+0.00035*on,1.15)", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
    ("max(1.15-0.00035*on,1.0)", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
    ("1.12", "(iw-iw/zoom)*on/{N}", "ih/2-(ih/zoom/2)"),
    ("1.12", "(iw-iw/zoom)*(1-on/{N})", "ih/2-(ih/zoom/2)"),
    ("min(1+0.00030*on,1.13)", "(iw-iw/zoom)*0.3", "(ih-ih/zoom)*0.6"),
]


def make_clip(img: Path, frames: int, idx: int, kind: str, out: Path):
    if out.exists():
        return
    z, x, y = MOTIONS[idx % len(MOTIONS)]
    x = x.replace("{N}", str(frames))
    y = y.replace("{N}", str(frames))
    dur = frames / FPS
    fd = 0.6 if kind == "chapter" else 0.25
    vf = (
        f"scale=2880:1620,zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s=1920x1080:fps={FPS},"
        f"noise=alls=14:allf=t+u,"
        f"eq=brightness='0.015*sin(2*PI*t*7)':eval=frame,"
        f"vignette=PI/4.5,"
        f"fade=t=in:st=0:d={fd},fade=t=out:st={dur - fd:.3f}:d={fd},format=yuv420p"
    )
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(img), "-vf", vf, "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", str(FPS), str(out),
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="storage/dbcooper")
    args = ap.parse_args()
    out = Path(args.out)
    (out / "work").mkdir(parents=True, exist_ok=True)
    work = out / "work"

    scenes = story.SCENES
    print(f"{len(scenes)} sahne")

    # 1) seslendirme
    async def all_tts():
        sem = asyncio.Semaphore(4)

        async def one(i, s):
            async with sem:
                await tts_one(s["text"], work / f"v{i:02d}.mp3", work / f"v{i:02d}.json")

        await asyncio.gather(*(one(i, s) for i, s in enumerate(scenes)))

    asyncio.run(all_tts())
    print("seslendirme tamam")

    # 2) zamanlama
    lead = 0.35
    timeline = []
    t = 0.0
    all_words = []
    for i, s in enumerate(scenes):
        vd = probe_duration(work / f"v{i:02d}.mp3")
        tail = 1.4 if s["type"] == "chapter" else 0.5
        frames = int(math.ceil((lead + vd + tail) * FPS))
        dur = frames / FPS
        words = json.loads((work / f"v{i:02d}.json").read_text())
        attach_punctuation(words, s["text"])
        for w in words:
            all_words.append({"start": t + lead + w["start"], "end": t + lead + w["end"], "text": w["text"]})
        timeline.append({"i": i, "start": t, "dur": dur, "frames": frames, "voice": vd})
        t += dur
    total = t
    print(f"toplam süre: {total / 60:.2f} dk")

    # 3) ses izi: her anlatım kendi sahnesinin başına + lead
    voice_wav = work / "voice.wav"
    inputs, filt = [], []
    for k, tl in enumerate(timeline):
        inputs += ["-i", str(work / f"v{tl['i']:02d}.mp3")]
        ms = int(round((tl["start"] + lead) * 1000))
        filt.append(f"[{k}:a]aresample={SR},adelay={ms}|{ms}[a{k}]")
    mix = "".join(f"[a{k}]" for k in range(len(timeline)))
    filt.append(f"{mix}amix=inputs={len(timeline)}:normalize=0,apad,atrim=0:{total:.3f}[v]")
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[v]", "-ac", "2", str(voice_wav)])

    music_wav = work / "music.wav"
    hits = [tl["start"] for tl, s in zip(timeline, scenes) if s["type"] in ("chapter", "title")]
    synth_music(total, hits, music_wav)

    mixed = work / "mix.m4a"
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(voice_wav), "-i", str(music_wav), "-filter_complex",
        "[1:a]volume=0.16[m];[m][0:a]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];"
        "[0:a]volume=1.0,highpass=f=70,acompressor=threshold=0.2:ratio=3[vo];"
        "[vo][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]",
        "-map", "[o]", "-c:a", "aac", "-b:a", "192k", str(mixed),
    ])
    print("ses miksi tamam")

    # 4) görseller + klipler
    from concurrent.futures import ThreadPoolExecutor

    def do_scene(tl):
        i = tl["i"]
        png = work / f"s{i:02d}.png"
        if not png.exists():
            visuals.render_scene(scenes[i], seed=100 + i).save(png)
        make_clip(png, tl["frames"], i, scenes[i]["type"], work / f"c{i:02d}.mp4")
        return i

    with ThreadPoolExecutor(max_workers=4) as ex:
        for i in ex.map(do_scene, timeline):
            print(f"  klip {i + 1}/{len(scenes)}")

    concat = work / "concat.txt"
    concat.write_text("".join(f"file 'c{tl['i']:02d}.mp4'\n" for tl in timeline))
    joined = work / "joined.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(joined)])

    # 5) altyazı + birleştirme
    subs = out / "altyazi.ass"
    build_subs(all_words, subs)
    final = out / "DB_Cooper_Gokyuzunde_Kaybolan_Adam.mp4"
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(joined), "-i", str(mixed),
        "-vf", f"ass={subs}", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-maxrate", "6M", "-bufsize", "12M",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-shortest", str(final),
    ])
    # altyazının SRT kopyası (YouTube'a ayrıca yüklenebilir)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(subs), str(out / "altyazi.srt")])

    visuals.thumbnail().save(out / "kucuk_resim.jpg", quality=92)

    # bölüm zaman damgaları
    chapters = ["00:00 Giriş"]
    for tl, s in zip(timeline, scenes):
        if s["type"] == "chapter":
            m, sec = divmod(int(tl["start"]), 60)
            chapters.append(f"{m:02d}:{sec:02d} {tr_title(s['num'])} – {tr_title(s['title'])}")
    (out / "chapters.txt").write_text("\n".join(chapters) + "\n", encoding="utf-8")
    print("BİTTİ:", final, f"{total / 60:.2f} dk")


if __name__ == "__main__":
    main()
