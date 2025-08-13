# Image Encryption Tool - Pixel Manipulation

A Python-based GUI application for encrypting and decrypting images using pixel manipulation (XOR encryption and pixel scrambling). The tool also provides RGB histogram visualization to analyze the color distribution of original, encrypted, and decrypted images.

![Screenshot]d:\Desktop\New folder\screenshot01.png 

## Features
- **Image Upload**: Supports multiple image formats (JPEG, PNG, BMP, TIFF, GIF, WebP).
- **Encryption/Decryption**: Uses XOR encryption with a user-provided key (0–255) and optional pixel scrambling for enhanced security.
- **Image Display**: Shows original, encrypted, and decrypted images side by side with scrollable canvases.
- **Histogram Analysis**: Displays RGB histograms for all images to compare color distributions.
- **Responsive UI**: Full-screen support (toggle with Esc/F11), scrollable image displays, and dynamic layout adjustments.
- **User-Friendly Interface**: Modern design with emoji-enhanced buttons and clear feedback via message boxes.

## Prerequisites
- Python 3.6 or higher
- Required Python packages:
  - `tkinter` (usually included with Python)
  - `Pillow` (PIL) for image handling
  - `opencv-python` for image processing
  - `numpy` for array operations
  - `matplotlib` for histogram visualization

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pabitra3/PRODIGY_CS_02.git
   cd PRODIGY_CS_02
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install pillow opencv-python numpy matplotlib
   ```

4. **Run the Application**:
   ```bash
   python image_encryption_gui.py
   ```

## Usage
1. **Launch the Application**:
   Run the script to open the GUI in full-screen mode.

2. **Upload an Image**:
   - Click the "📁 Upload Image" button.
   - Select an image file (e.g., `.jpg`, `.png`).
   - The original image will appear in the left panel.

3. **Encrypt the Image**:
   - Enter a key (integer between 0 and 255) in the key field.
   - Click the "🔒 Encrypt" button.
   - The encrypted image will appear in the middle panel.

4. **Decrypt the Image**:
   - Enter the same key used for encryption.
   - Click the "🔓 Decrypt" button.
   - The decrypted image will appear in the right panel.
   - If the correct key is used, the decrypted image will match the original.

5. **View Histograms**:
   - Click the "📊 Histograms" button.
   - RGB histograms for all available images (original, encrypted, decrypted) will appear side by side in the bottom panel.

6. **Toggle Full-Screen**:
   - Press `Esc` or `F11` to switch between full-screen and windowed modes.

## Notes
- **Encryption Method**: The tool uses XOR encryption with a single key and pixel scrambling for added complexity. Note that this is a basic encryption method and not suitable for high-security applications.
- **Histogram Analysis**: The encrypted image’s histogram should show a uniform distribution, indicating effective encryption. The decrypted image’s histogram should match the original if the correct key is used.
- **Performance**: Large images may slow down encryption/decryption due to pixel scrambling. Consider resizing images for faster processing.
- **Saving Images**: Currently, the tool does not support saving encrypted/decrypted images. This feature can be added by modifying the code (see [Future Improvements](#future-improvements)).

## Future Improvements
- Add buttons to save encrypted and decrypted images.
- Enhance encryption with stronger algorithms (e.g., AES).
- Optimize pixel scrambling for better performance on large images (e.g., using block-based shuffling or `numba`).
- Improve accessibility with text alternatives for emojis and high-contrast UI elements.
- Add support for batch processing multiple images.

## Troubleshooting
- **"ModuleNotFoundError"**: Ensure all dependencies (`Pillow`, `opencv-python`, `numpy`, `matplotlib`) are installed.
- **Image Loading Errors**: Verify the image file is valid and in a supported format.
- **Large Images**: Very large images may cause performance issues or crashes. Try resizing images before uploading.
- **Full-Screen Issues**: If full-screen toggle fails, check your OS and Tkinter version compatibility.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with [Tkinter](https://docs.python.org/3/library/tkinter.html), [Pillow](https://pillow.readthedocs.io/), [OpenCV](https://opencv.org/), [NumPy](https://numpy.org/), and [Matplotlib](https://matplotlib.org/).
- Inspired by image processing and cryptography tutorials.

---
