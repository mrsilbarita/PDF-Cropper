# PDF Label Cropper & Watcher

A small Python script that automatically **watches a folder for new PDF shipping labels**, crops them to a fixed region (e.g. 190x100 mm labels), and saves the processed result in a `processed/` subfolder.  

Useful for automatically converting full-page courier labels into smaller ones ready for thermal printers.

---

## ✨ Features
- Monitors a folder for new `.pdf` files.
- Crops each page of the PDF to a configurable region.
- Saves the cropped result in a `processed/` subfolder.
- Deletes the original file once processed.
- Fully self-contained, no external tools required (uses [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) for PDF handling).

Yes, this was written with the help of ChatGPT, I'm sorry.

You need these python libraries installed:
- watchdog
- pymupdf
- pillow

The easiest way to use it is to run it from console with python "PDF-Cropper.py", but you can also use something like pyinstaller to bundle it into a .exe.

This code is published with no guarantees of functionality, safety or reponsability whatsoever. I'm an industrial engineer who learned to code for fun. You use this code at your own risk.
