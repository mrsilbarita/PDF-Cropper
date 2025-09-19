import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import fitz  # PyMuPDF
from PIL import Image
import sys

if getattr(sys, 'frozen', False):  
    # Running as a bundled EXE
    BASE_FOLDER = os.path.dirname(sys.executable)
else:  
    # Running as a script
    BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

WATCH_FOLDER = BASE_FOLDER
OUTPUT_FOLDER = os.path.join(BASE_FOLDER, "processed")


# Crop box in pixels: (left, top, right, bottom)
# You can tweak these values to match the label section you need
CROP_BOX = (160, 160, 1320, 2260)
# ------------------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def wait_for_file(file_path, timeout=10):
    """Wait until the file is accessible or timeout expires"""
    start_time = time.time()
    while True:
        try:
            if os.path.exists(file_path):
                with open(file_path, "rb"):
                    return True
        except (OSError, PermissionError):
            pass
        if time.time() - start_time > timeout:
            return False
        time.sleep(0.5)


def process_pdf(pdf_path):
    print(f"Processing {pdf_path}...")
    try:
        with fitz.open(pdf_path) as doc:
            cropped_images = []
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                cropped = img.crop(CROP_BOX)
                cropped_images.append(cropped)

        if cropped_images:
            pdf_out_path = os.path.join(OUTPUT_FOLDER, os.path.basename(pdf_path))
            try:
                cropped_images[0].save(pdf_out_path, save_all=True, append_images=cropped_images[1:])
                print(f"Saved cropped PDF to {pdf_out_path}")
            except Exception as e:
                print(f"Failed to save cropped PDF {pdf_out_path}: {e}")
        else:
            print(f"No pages found in {pdf_path}")

        # Now safe to delete original PDF
        try:
            os.remove(pdf_path)
            print(f"Deleted original PDF: {pdf_path}")
        except Exception as e:
            print(f"Could not delete {pdf_path}: {e}")

    except Exception as e:
        print(f"Failed to open PDF {pdf_path}: {e}")


class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.lower().endswith(".pdf"):
            return

        print(f"Detected new PDF: {event.src_path}")

        if wait_for_file(event.src_path, timeout=15):
            process_pdf(event.src_path)
        else:
            print(f"File {event.src_path} not accessible after timeout.")


if __name__ == "__main__":
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"Watching folder: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
