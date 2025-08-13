import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
import os

class ImageEncryptionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool - Pixel Manipulation")
        
        # Get screen dimensions for full-screen layout
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Set window to full screen
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.configure(bg='#f8f9fa')
        
        # Force full screen state
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                self.root.attributes('-fullscreen', True)  # Alternative
        
        # Allow exit from fullscreen with Escape
        self.root.bind('<Escape>', lambda e: self.toggle_fullscreen())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        
        # Initialize variables
        self.original_image = None
        self.encrypted_image = None
        self.decrypted_image = None
        self.current_key = None
        self.fullscreen = True
        
        # Initialize button references
        self.encrypt_btn = None
        self.decrypt_btn = None
        self.histogram_btn = None
        
        self.setup_ui()
        
        # Bind resize event for responsiveness
        self.root.bind('<Configure>', self.on_window_resize)
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            try:
                self.root.state('zoomed')
            except:
                try:
                    self.root.attributes('-zoomed', True)
                except:
                    self.root.attributes('-fullscreen', True)
        else:
            self.root.state('normal')
            self.root.attributes('-fullscreen', False)
            self.root.geometry("1400x900+100+50")
    
    def on_window_resize(self, event):
        """Handle window resize events for better responsiveness"""
        if event.widget == self.root:
            # Update scrollregion when window is resized
            self.root.after_idle(lambda: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
    
    def setup_ui(self):
        # Create main container without scrollbars for full-screen experience
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure main frame grid
        main_frame.grid_rowconfigure(2, weight=1)  # Images section
        main_frame.grid_rowconfigure(3, weight=2)  # Histogram section (larger)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title with compact design
        title_frame = tk.Frame(main_frame, bg='#f8f9fa', height=60)
        title_frame.grid(row=0, column=0, sticky='ew', pady=(0, 5))
        title_frame.grid_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="🔐 Image Encryption Tool - Pixel Manipulation", 
                              font=('Arial', 18, 'bold'), 
                              bg='#f8f9fa', 
                              fg='#2c3e50')
        title_label.pack(side=tk.LEFT, pady=5)
        
        # Full screen hint
        hint_label = tk.Label(title_frame, 
                             text="Press ESC or F11 to toggle fullscreen", 
                             font=('Arial', 9), 
                             bg='#f8f9fa', 
                             fg='#6c757d')
        hint_label.pack(side=tk.RIGHT, pady=5)
        
        # Setup components with optimized spacing
        self.setup_control_panel(main_frame)
        self.setup_images_frame(main_frame)
        self.setup_histogram_frame(main_frame)
    
    def setup_control_panel(self, parent):
        # Compact control panel
        control_frame = ttk.LabelFrame(parent, text="🎛️ Control Panel", padding=10)
        control_frame.grid(row=1, column=0, sticky='ew', pady=(0, 5))
        
        # Configure grid for responsiveness
        control_frame.grid_columnconfigure(1, weight=1)
        
        # Single row layout for compact design
        self.upload_btn = tk.Button(control_frame, 
                                   text="📁 Upload Image", 
                                   command=self.upload_image,
                                   font=('Arial', 11, 'bold'),
                                   bg='#28a745', 
                                   fg='white',
                                   padx=20, 
                                   pady=8,
                                   relief=tk.RAISED, 
                                   bd=2,
                                   cursor='hand2')
        self.upload_btn.grid(row=0, column=0, padx=(0, 10), sticky='w')
        
        # Key input
        key_label = tk.Label(control_frame, 
                           text="🔑 Key:", 
                           font=('Arial', 10, 'bold'),
                           bg='#f8f9fa')
        key_label.grid(row=0, column=1, padx=(10, 5), sticky='w')
        
        self.key_var = tk.StringVar()
        self.key_entry = tk.Entry(control_frame, 
                                 textvariable=self.key_var,
                                 font=('Arial', 11), 
                                 width=8,
                                 justify='center')
        self.key_entry.grid(row=0, column=2, padx=(0, 10))
        
        # Action buttons
        self.encrypt_btn = tk.Button(control_frame, 
                                   text="🔒 Encrypt",
                                   command=self.encrypt_image,
                                   font=('Arial', 10, 'bold'),
                                   bg="#007bff",
                                   fg='white',
                                   padx=15,
                                   pady=8,
                                   cursor='hand2',
                                   state=tk.DISABLED)
        self.encrypt_btn.grid(row=0, column=3, padx=5)
        
        self.decrypt_btn = tk.Button(control_frame, 
                                   text="🔓 Decrypt",
                                   command=self.decrypt_image,
                                   font=('Arial', 10, 'bold'),
                                   bg="#fd7e14",
                                   fg='white',
                                   padx=15,
                                   pady=8,
                                   cursor='hand2',
                                   state=tk.DISABLED)
        self.decrypt_btn.grid(row=0, column=4, padx=5)
        
        self.histogram_btn = tk.Button(control_frame, 
                                     text="📊 Histograms",
                                     command=self.visualize_histograms,
                                     font=('Arial', 10, 'bold'),
                                     bg="#6f42c1",
                                     fg='white',
                                     padx=15,
                                     pady=8,
                                     cursor='hand2',
                                     state=tk.DISABLED)
        self.histogram_btn.grid(row=0, column=5, padx=5)
    
    def setup_images_frame(self, parent):
        # Images section with larger display
        images_section = ttk.LabelFrame(parent, text="🖼️ Images Display", padding=10)
        images_section.grid(row=2, column=0, sticky='nsew', pady=(0, 5))
        
        # Configure for responsive layout
        for i in range(3):
            images_section.grid_columnconfigure(i, weight=1)
        images_section.grid_rowconfigure(0, weight=1)
        
        # Create image display areas with larger dimensions
        self.image_frames = {}
        titles = ['Original Image', 'Encrypted Image', 'Decrypted Image']
        colors = ['#28a745', '#dc3545', '#007bff']
        
        for i, (title, color) in enumerate(zip(titles, colors)):
            # Column frame
            col_frame = tk.Frame(images_section, 
                               bg='#ffffff', 
                               relief=tk.RIDGE, 
                               bd=2)
            col_frame.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            col_frame.grid_rowconfigure(1, weight=1)
            col_frame.grid_columnconfigure(0, weight=1)
            
            # Title header
            title_header = tk.Label(col_frame,
                                  text=title,
                                  font=('Arial', 12, 'bold'),
                                  bg=color,
                                  fg='white',
                                  pady=5)
            title_header.grid(row=0, column=0, sticky='ew')
            
            # Image display area with larger dimensions and scrollbars
            img_frame = tk.Frame(col_frame)
            img_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
            img_frame.grid_rowconfigure(0, weight=1)
            img_frame.grid_columnconfigure(0, weight=1)
            
            # Canvas for image with scrollbars
            img_canvas = tk.Canvas(img_frame, bg='#f8f9fa', highlightthickness=1, 
                                 highlightbackground='#dee2e6')
            img_canvas.grid(row=0, column=0, sticky='nsew')
            
            v_scroll = ttk.Scrollbar(img_frame, orient="vertical", command=img_canvas.yview)
            v_scroll.grid(row=0, column=1, sticky='ns')
            
            h_scroll = ttk.Scrollbar(img_frame, orient="horizontal", command=img_canvas.xview)
            h_scroll.grid(row=1, column=0, sticky='ew')
            
            img_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            
            # Initial placeholder
            placeholder_text = f"No {title.lower()}\nloaded yet\n\n📷"
            img_label = tk.Label(img_canvas, text=placeholder_text, bg='#f8f9fa', 
                               fg='#6c757d', font=('Arial', 10))
            img_canvas.create_window(0, 0, window=img_label, anchor='nw')
            
            # Store references
            self.image_frames[title.lower().replace(' ', '_')] = {
                'canvas': img_canvas,
                'label': img_label,
                'frame': img_frame
            }
            
            # Mouse wheel scrolling for images
            def make_scroll_handler(canvas):
                def _on_img_scroll(event):
                    if event.state & 0x1:  # Shift pressed
                        canvas.xview_scroll(int(-1*(event.delta/120)), "units")
                    else:
                        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                return _on_img_scroll
            
            img_canvas.bind("<MouseWheel>", make_scroll_handler(img_canvas))
    
    def setup_histogram_frame(self, parent):
        # Histogram section with larger space
        histogram_section = ttk.LabelFrame(parent, text="📈 RGB Histogram Analysis", padding=10)
        histogram_section.grid(row=3, column=0, sticky='nsew')
        
        # Configure for full histogram display
        histogram_section.grid_rowconfigure(0, weight=1)
        histogram_section.grid_columnconfigure(0, weight=1)
        
        # Main histogram container
        self.histogram_container = tk.Frame(histogram_section, bg='#ffffff')
        self.histogram_container.grid(row=0, column=0, sticky='nsew')
        
        # Configure for three equal columns
        for i in range(3):
            self.histogram_container.grid_columnconfigure(i, weight=1)
        self.histogram_container.grid_rowconfigure(0, weight=1)
        
        # Initial message
        self.show_initial_histogram_message()
    
    def show_initial_histogram_message(self):
        initial_frame = tk.Frame(self.histogram_container, bg='#ffffff')
        initial_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')
        
        message = tk.Label(initial_frame,
                          text="📊 RGB Histogram Analysis Center\n\n" +
                               "• Upload an image and click 'Histograms'\n" +
                               "• View color distribution patterns side by side\n" +
                               "• Compare original vs encrypted vs decrypted\n" +
                               "• All three histograms will be displayed simultaneously\n\n" +
                               "Ready to analyze your images!",
                          font=('Arial', 12),
                          bg='#ffffff',
                          fg='#495057',
                          justify=tk.CENTER)
        message.pack(expand=True)
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=[
                ("All Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif *.webp"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("BMP files", "*.bmp"),
                ("TIFF files", "*.tiff *.tif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Load image using cv2
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    raise ValueError("Could not load image. Please check the file format.")
                
                # Convert BGR to RGB
                self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                
                # Display the image
                self.display_image(self.original_image, 'original_image')
                
                # Enable buttons
                self.encrypt_btn.config(state=tk.NORMAL)
                self.histogram_btn.config(state=tk.NORMAL)
                
                # Reset other images
                self.encrypted_image = None
                self.decrypted_image = None
                self.reset_image_display('encrypted_image', "No encrypted\nimage yet\n\n🔒")
                self.reset_image_display('decrypted_image', "No decrypted\nimage yet\n\n🔓")
                self.decrypt_btn.config(state=tk.DISABLED)
                
                # Show success message
                img_shape = self.original_image.shape
                messagebox.showinfo("Image Loaded Successfully!", 
                                  f"✅ Image loaded successfully!\n\n" +
                                  f"Size: {img_shape[1]} x {img_shape[0]} pixels\n" +
                                  f"Channels: {img_shape[2]}\n\n" +
                                  f"Ready for encryption!")
                
            except Exception as e:
                messagebox.showerror("Error Loading Image", f"❌ Failed to load image:\n\n{str(e)}")
    
    def display_image(self, img_array, frame_key):
        try:
            # Get canvas reference
            canvas = self.image_frames[frame_key]['canvas']
            
            # Convert to PIL Image
            img_pil = Image.fromarray(img_array.astype(np.uint8))
            
            # Get canvas size for scaling
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            
            # If canvas is too small, use minimum size
            if canvas_width < 100:
                canvas_width = 300
            if canvas_height < 100:
                canvas_height = 250
            
            # Calculate scaling to fit in canvas while preserving aspect ratio
            img_width, img_height = img_pil.size
            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
            scale = min(scale_x, scale_y, 1.0)  # Don't scale up
            
            # Calculate new dimensions
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize image
            img_resized = img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            img_tk = ImageTk.PhotoImage(img_resized)
            
            # Clear canvas and add image
            canvas.delete("all")
            canvas.create_image(canvas_width//2, canvas_height//2, image=img_tk, anchor='center')
            
            # Update scroll region
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            # Keep reference to prevent garbage collection
            canvas.image = img_tk
            
        except Exception as e:
            # Show error in canvas
            canvas = self.image_frames[frame_key]['canvas']
            canvas.delete("all")
            error_msg = f"Error displaying image:\n{str(e)[:50]}..."
            canvas.create_text(150, 100, text=error_msg, fill='red', font=('Arial', 10))
    
    def reset_image_display(self, frame_key, message):
        """Reset image display to show placeholder message"""
        canvas = self.image_frames[frame_key]['canvas']
        canvas.delete("all")
        canvas.create_text(150, 100, text=message, fill='#6c757d', font=('Arial', 10), justify='center')
        canvas.image = None
    
    def validate_key(self):
        try:
            key = int(self.key_var.get().strip())
            if 0 <= key <= 255:
                return key
            else:
                messagebox.showerror("Invalid Key", "❌ Key must be between 0 and 255")
                return None
        except ValueError:
            messagebox.showerror("Invalid Key", "❌ Please enter a valid integer key (0-255)")
            return None
    
    def encrypt_image(self):
        if self.original_image is None:
            messagebox.showerror("No Image", "❌ Please upload an image first")
            return
        
        key = self.validate_key()
        if key is None:
            return
        
        try:
            # Create a copy for encryption
            self.encrypted_image = self.original_image.copy().astype(np.uint16)
            
            # XOR encryption
            self.encrypted_image = np.bitwise_xor(self.encrypted_image, key)
            
            # Additional scrambling for enhanced security
            if key > 0:
                height, width = self.encrypted_image.shape[:2]
                np.random.seed(key)  # Reproducible scrambling
                
                # Generate scrambling indices
                total_pixels = height * width
                indices = np.arange(total_pixels)
                np.random.shuffle(indices)
                
                # Apply scrambling
                flat_img = self.encrypted_image.reshape(-1, self.encrypted_image.shape[2])
                scrambled_img = flat_img[indices]
                self.encrypted_image = scrambled_img.reshape(self.encrypted_image.shape)
            
            # Convert back to uint8
            self.encrypted_image = np.clip(self.encrypted_image, 0, 255).astype(np.uint8)
            
            # Display encrypted image
            self.display_image(self.encrypted_image, 'encrypted_image')
            
            # Enable decrypt button
            self.current_key = key
            self.decrypt_btn.config(state=tk.NORMAL)
            
            messagebox.showinfo("Encryption Complete", 
                              f"🔒 Image encrypted successfully!\n\n" +
                              f"Key: {key}\n" +
                              f"Method: XOR + Pixel Scrambling")
            
        except Exception as e:
            messagebox.showerror("Encryption Error", f"❌ Encryption failed:\n\n{str(e)}")
    
    def decrypt_image(self):
        if self.encrypted_image is None:
            messagebox.showerror("No Encrypted Image", "❌ No encrypted image available to decrypt")
            return
        
        key = self.validate_key()
        if key is None:
            return
        
        try:
            # Create copy for decryption
            self.decrypted_image = self.encrypted_image.copy().astype(np.uint16)
            
            # Reverse scrambling first
            if key > 0:
                height, width = self.decrypted_image.shape[:2]
                np.random.seed(key)  # Same seed as encryption
                
                # Generate same indices as encryption
                total_pixels = height * width
                indices = np.arange(total_pixels)
                np.random.shuffle(indices)
                
                # Create reverse mapping
                reverse_indices = np.argsort(indices)
                
                # Apply reverse scrambling
                flat_img = self.decrypted_image.reshape(-1, self.decrypted_image.shape[2])
                unscrambled_img = flat_img[reverse_indices]
                self.decrypted_image = unscrambled_img.reshape(self.decrypted_image.shape)
            
            # Reverse XOR encryption
            self.decrypted_image = np.bitwise_xor(self.decrypted_image, key)
            
            # Convert back to uint8
            self.decrypted_image = np.clip(self.decrypted_image, 0, 255).astype(np.uint8)
            
            # Display decrypted image
            self.display_image(self.decrypted_image, 'decrypted_image')
            
            # Status check
            if key == self.current_key:
                status = "Perfect decryption! ✅"
            else:
                status = f"Warning: Different key used (encrypted with {self.current_key}) ⚠️"
            
            messagebox.showinfo("Decryption Complete",
                              f"🔓 Image decrypted!\n\n" +
                              f"Key: {key}\n" +
                              f"Status: {status}")
            
        except Exception as e:
            messagebox.showerror("Decryption Error", f"❌ Decryption failed:\n\n{str(e)}")
    
    def visualize_histograms(self):
        # Clear previous histograms
        for widget in self.histogram_container.winfo_children():
            widget.destroy()
        
        # Collect available images
        images_data = []
        
        if self.original_image is not None:
            images_data.append(('Original Image', self.original_image, '#28a745'))
        
        if self.encrypted_image is not None:
            images_data.append(('Encrypted Image', self.encrypted_image, '#dc3545'))
        
        if self.decrypted_image is not None:
            images_data.append(('Decrypted Image', self.decrypted_image, '#007bff'))
        
        if not images_data:
            messagebox.showwarning("No Images", "❌ No images available for histogram analysis.\nPlease upload an image first.")
            return
        
        try:
            # Create histogram for each image - side by side layout
            for i, (title, img_array, color_theme) in enumerate(images_data):
                # Frame for this histogram
                hist_frame = tk.Frame(self.histogram_container,
                                    bg='#ffffff',
                                    relief=tk.RIDGE,
                                    bd=2)
                hist_frame.grid(row=0, column=i, padx=3, pady=5, sticky='nsew')
                
                # Calculate figure size based on available space
                fig_width = 5
                fig_height = 4
                
                # Create matplotlib figure
                fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height), dpi=80)
                fig.patch.set_facecolor('white')
                
                # Plot title
                ax.set_title(f'{title}\nRGB Distribution', 
                           fontsize=11, fontweight='bold', pad=10, color='#2c3e50')
                
                # Calculate histograms
                colors = ['#e74c3c', '#27ae60', '#3498db']
                labels = ['Red', 'Green', 'Blue']
                
                max_freq = 0
                for j, (color, label) in enumerate(zip(colors, labels)):
                    hist = cv2.calcHist([img_array], [j], None, [256], [0, 256])
                    hist = hist.flatten()
                    max_freq = max(max_freq, np.max(hist))
                    
                    # Plot with styling
                    ax.plot(range(256), hist, color=color, linewidth=2, label=label, alpha=0.9)
                    ax.fill_between(range(256), hist, alpha=0.2, color=color)
                
                # Styling
                ax.set_xlim(0, 255)
                ax.set_ylim(0, max_freq * 1.1)
                ax.set_xlabel('Pixel Intensity', fontsize=9)
                ax.set_ylabel('Frequency', fontsize=9)
                ax.legend(fontsize=8, loc='upper right')
                ax.grid(True, alpha=0.3, linestyle='--')
                
                # Clean up plot
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.tick_params(axis='both', labelsize=8)
                
                plt.tight_layout()
                
                # Embed plot
                canvas = FigureCanvasTkAgg(fig, hist_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # Close figure to free memory
                plt.close(fig)
            
            # Fill empty columns if less than 3 images
            for i in range(len(images_data), 3):
                empty_frame = tk.Frame(self.histogram_container, bg='#f8f9fa', relief=tk.SUNKEN, bd=1)
                empty_frame.grid(row=0, column=i, padx=3, pady=5, sticky='nsew')
                
                empty_label = tk.Label(empty_frame,
                                     text="No histogram\navailable",
                                     bg='#f8f9fa',
                                     fg='#6c757d',
                                     font=('Arial', 10))
                empty_label.pack(expand=True)
            
            messagebox.showinfo("Histograms Generated",
                              f"📊 Generated {len(images_data)} histogram(s) successfully!\n\n" +
                              "All histograms are displayed side by side for easy comparison.")
            
        except Exception as e:
            messagebox.showerror("Histogram Error", f"❌ Failed to generate histograms:\n\n{str(e)}")

def main():
    root = tk.Tk()
    app = ImageEncryptionTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()