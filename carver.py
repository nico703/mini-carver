import argparse, os, csv

# einfache Signaturen (Header, Trailer)
SIGS = {
    "jpg": (b"\xff\xd8\xff", b"\xff\xd9"),
    "png": (b"\x89PNG\r\n\x1a\n", b"IEND"),
    "pdf": (b"%PDF", b"%%EOF"),
}

def carve(data: bytes, outdir: str):
    os.makedirs(outdir, exist_ok=True)
    found = 0
    log_rows = []
    for ext, (head, tail) in SIGS.items():
        start = 0
        while True:
            i = data.find(head, start)
            if i < 0:
                break
            j = data.find(tail, i + len(head))
            if j < 0:
                start = i + 1  # kein Trailer -> weiter suchen
                continue

            # Trailer-Ende grob anpassen
            if ext == "jpg":
                end = j + len(tail)
            elif ext == "png":
                # rudimentär: IEND + 8 Bytes (Länge+CRC)
                end = j + len(tail) + 8
            else:  # pdf
                end = j + len(tail)

            chunk = data[i:end]
            fname = os.path.join(outdir, f"recovered_{found:03d}.{ext}")
            with open(fname, "wb") as f:
                f.write(chunk)
            print(f"[+] {fname} ({len(chunk)} bytes) from {i}..{end}")

            log_rows.append({
                "index": found,
                "ext": ext,
                "start": i,
                "end": end,
                "size": len(chunk),
            })

            found += 1
            start = end

    if found == 0:
        print("Keine bekannten Signaturen gefunden.")

    return log_rows

def main():
    ap = argparse.ArgumentParser(description="Mini File Carver (JPG/PNG/PDF)")
    ap.add_argument("image", help="Pfad zur Binär-/Image-Datei")           # <- fehlte
    ap.add_argument("-o", "--out", default="recovered", help="Ausgabeverzeichnis")
    ap.add_argument("--log-csv", help="Pfad für CSV-Log (optional)")
    args = ap.parse_args()

    with open(args.image, "rb") as f:
        data = f.read()

    rows = carve(data, args.out)

    if args.log_csv and rows:
        with open(args.log_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["index","ext","start","end","size"])
            w.writeheader()
            w.writerows(rows)
        print(f"[+] CSV-Log geschrieben: {args.log_csv}")

if __name__ == "__main__":
    main()
