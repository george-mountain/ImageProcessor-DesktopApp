import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


mouse_down = False
rect_roi = None


class ImageMaskingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        self.root.configure(background="#f0f0f0")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create a grid to organize the layout
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.preview_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.preview_frame.grid(
            row=0, column=0, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew"
        )
        self.preview_frame.configure(background="white")
        self.preview_label = tk.Label(
            self.preview_frame, bg="white", bd=2, relief=tk.GROOVE
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
        self.button_frame.columnconfigure(0, weight=1)


        # create side buttons
        self.upload_button = tk.Button(
            self.button_frame,
            text="Upload Image",
            command=self.upload_image,
            bg="#4caf50",
            fg="white",
            font=("Arial", 14),
            padx=10,
            pady=5,
        )
        self.upload_button.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)

        self.crop_button = tk.Button(
            self.button_frame,
            text="Crop Image",
            command=self.crop_image,
            bg="#008CBA",
            fg="white",
            font=("Arial", 14),
            padx=10,
            pady=5,
        )
        self.crop_button.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)

        self.blur_button = tk.Button(
            self.button_frame,
            text="Apply Blur",
            command=self.apply_blur,
            bg="#ff5722",
            fg="white",
            font=("Arial", 14),
            padx=10,
            pady=5,
        )
        self.blur_button.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)

        self.save_cropped_button = tk.Button(
            self.button_frame,
            text="Save Cropped Image",
            command=self.save_cropped_image,
            bg="#2196F3",
            fg="white",
            font=("Arial", 14),
            padx=10,
            pady=5,
        )
        self.save_cropped_button.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)

        self.image = None
        self.cropped_image = None


        self.resize_button = tk.Button(
            self.button_frame,
            text="Resize Image",
            command=self.resize_image,
            bg="#FFC107",
            fg="white",
            font=("Arial", 12),
            padx=10,
            pady=5,
        )
        self.resize_button.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)


        # define form inputs
        self.width_label = tk.Label(
            self.button_frame,
            text="Width:",
            font=("Arial", 12),
            padx=10,
            pady=5,
        )
        self.width_label.pack(side=tk.TOP, anchor="w")

        self.width_entry = tk.Entry(self.button_frame, font=("Arial", 12))
        self.width_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.height_label = tk.Label(
            self.button_frame,
            text="Height:",
            font=("Arial", 12),
            padx=10,
            pady=5,
        )
        self.height_label.pack(side=tk.TOP, anchor="w")

        self.height_entry = tk.Entry(self.button_frame, font=("Arial", 12))
        self.height_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    # helper functions
    def upload_image(self):
        global file_path
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is not None:
                self.display_image()

    def display_image(self):
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image=image_pil)
        self.preview_label.config(image=image_tk)
        self.preview_label.image = image_tk

    def crop_image(self):
        if self.image is None:
            self.show_error_message("Please upload an image first.")
            return

        x, y, w, h = cv2.selectROI(
            "Select Region to Crop", self.image, fromCenter=False
        )
        if w > 0 and h > 0:
            self.cropped_image = self.image[y : y + h, x : x + w]
            self.display_image()

    def apply_blur(self):
        if self.image is None:
            self.show_error_message("Please upload an image first.")
            return

        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", self.mouse_callback, param=self.image)

        while True:
            cv2.imshow("Image", self.image)
            key = cv2.waitKey(1) & 0xFF

            if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
                break

            if key == 27:  # Press ESC to exit
                break

        cv2.destroyAllWindows()

        self.display_image()

    def save_cropped_image(self):
        if self.cropped_image is None:
            self.show_error_message("No cropped image to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")]
        )
        if file_path:
            cv2.imwrite(file_path, self.cropped_image)
            print("Cropped image saved successfully!")

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def on_close(self):
        if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow("Image")
        self.root.destroy()

    def mouse_callback(self, event, x, y, flags, param):
        global rect_roi, mouse_down

        if event == cv2.EVENT_LBUTTONDOWN:
            rect_roi = (x, y, 0, 0)
            mouse_down = True
        elif event == cv2.EVENT_LBUTTONDBLCLK:
            mouse_down = False
            if rect_roi[2] > 0 and rect_roi[3] > 0:
                self.cropped_image = param[
                    rect_roi[1] : rect_roi[1] + rect_roi[3],
                    rect_roi[0] : rect_roi[0] + rect_roi[2],
                ]
                self.save_cropped_image()

        elif event == cv2.EVENT_MOUSEMOVE and mouse_down:
            if rect_roi is not None:
                rect_roi = (rect_roi[0], rect_roi[1], x - rect_roi[0], y - rect_roi[1])
                self.display_image_with_rect()

        elif event == cv2.EVENT_LBUTTONUP:
            mouse_down = False
            if rect_roi[2] > 0 and rect_roi[3] > 0:
                self.blur_and_mask_area(param, rect_roi)
            rect_roi = None

    def display_image_with_rect(self):
        image_with_rect = self.image.copy()
        if rect_roi is not None:
            x, y, w, h = rect_roi
            cv2.rectangle(image_with_rect, (x, y), (x + w, y + h), (0, 255, 0), 2)
        image_rgb = cv2.cvtColor(image_with_rect, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image=image_pil)
        self.preview_label.config(image=image_tk)
        self.preview_label.image = image_tk

    def blur_and_mask_area(self, image, points, blur_factor=65):
        x, y, w, h = points
        roi = image[y : y + h, x : x + w]
        blurred_roi = cv2.GaussianBlur(roi, (blur_factor, blur_factor), 0)
        image[y : y + h, x : x + w] = blurred_roi
        cv2.imwrite(file_path, image)
        self.display_image_with_rect()
    

    def resize_image(self):
        if self.image is None:
            self.show_error_message("Please upload an image first.")
            return

        try:
            target_width = int(self.width_entry.get())
            target_height = int(self.height_entry.get())
        except ValueError:
            self.show_error_message("Invalid width or height. Please enter integers.")
            return

        if target_width <= 0 or target_height <= 0:
            self.show_error_message("Width and height must be positive integers.")
            return

        self.image = cv2.resize(self.image, (target_width, target_height))
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")]
        )
        if file_path:
            cv2.imwrite(file_path, self.image)
            print("resize image saved successfully!")
        self.display_image()



if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")
    root.iconbitmap("C:/Users/georg/Desktop/SRimage_data/icon_dir/icon_file.ico")
    app = ImageMaskingApp(root)
    root.mainloop()
