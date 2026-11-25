# THE WORLD DESK - NI24 wave 2, account 10 (sindyariana11).
# Carrier only: copies the entry image that sits beside this file into
# /output/entry.png. Pure standard library, no network, deterministic.
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied", src, "->", dst)


if __name__ == "__main__":
    main()
