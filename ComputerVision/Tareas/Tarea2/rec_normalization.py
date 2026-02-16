import cv2
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import mediapipe as mp

########## Image Normalization Modules ##########
def retrieve_histogram(image):
    # Calculates the histogram of a grayscale image
    histogram = np.zeros(256, dtype=int)
    # Iterate over pixels to count frequencies
    for pixel in image.flat:
        histogram[pixel] += 1
    return histogram

def equalization(image):
    # Performs histogram equalization on an image
    hist = retrieve_histogram(image)
    
    # Calculate CDF
    cdf = np.zeros(256, dtype=float)
    cum_sum = 0
    total_pixels = image.size
    
    for i in range(256):
        cum_sum += hist[i]
        cdf[i] = cum_sum / total_pixels
        
    # Calculate mapping: s = floor((L-1) * cdf)
    mapping = np.floor(255 * cdf).astype(np.uint8)
    
    # Apply mapping
    return mapping[image]

# Toggle statement to test out histogram equalization without using cv2 methods
if 0:
    equalization = cv2.equalizeHist

def normalize_histogram_luminance(image_bgr):
    # Normalizes the histogram of the Luminance (Y) channel only

    # Convert to YCrCb (Y=Luma, Cr/Cb=Chroma)
    ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    
    # Split channels
    channels = list(cv2.split(ycrcb))
    
    # Equalize only the Y channel (index 0)
    channels[0] = equalization(channels[0])
    
    # Merge and convert back to BGR
    ycrcb_merged = cv2.merge(channels)
    return cv2.cvtColor(ycrcb_merged, cv2.COLOR_YCrCb2BGR)

def normalize_histogram_rgb(image_bgr):
    # Normalizes the histogram of the R, G, and B channels individually
    # Split into Blue, Green, Red channels (OpenCV uses BGR)
    b, g, r = cv2.split(image_bgr)
    
    # Equalize each channel independently
    b_eq = equalization(b)
    g_eq = equalization(g)
    r_eq = equalization(r)
    
    # Merge back together
    return cv2.merge((b_eq, g_eq, r_eq))

########## Visualization & Plotting Modules ##########
def create_histogram_plot(image_bgr, title="Histogram", size=(320, 240)):
    # Generates a histogram plot using Matplotlib and converts it to an OpenCV
    # image, Optimized for speed using FigureCanvasAgg
    
    # Convert BGR to RGB so the plot colors match the channel names
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    # Setup Figure
    dpi = 80
    fig_w, fig_h = size[0] / dpi, size[1] / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    
    # Plot histograms for R, G, B
    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        hist = cv2.calcHist([image_rgb], [i], None, [256], [0, 256])
        ax.plot(hist, color=color, linewidth=1.5)
        
    # Styling
    ax.set_title(title, fontsize=10)
    ax.set_xlim([0, 256])
    # Hide ticks
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    
    # Render to Numpy Array (Optimized)
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    plot_img = np.asarray(buf)
    
    # Convert RGBA to BGR and resize strictly to target
    plot_img = cv2.cvtColor(plot_img, cv2.COLOR_RGBA2BGR)
    plot_img = cv2.resize(plot_img, size)
    
    plt.close(fig) # vital to free memory
    return plot_img

########## Display Modules ##########
def compose_quadrant_view(original, normalized, hist_orig, hist_norm):
    # Combines 4 images into a 2x2 grid and returns the result

    # Ensure all images are same size (using original as reference)
    h, w = original.shape[:2]
    
    # Resize histograms to match video frame size if they differ
    if hist_orig.shape[:2] != (h, w):
        hist_orig = cv2.resize(hist_orig, (w, h))
    if hist_norm.shape[:2] != (h, w):
        hist_norm = cv2.resize(hist_norm, (w, h))
        
    # Stack Top Row
    top_row = np.hstack((original, normalized))
    # Stack Bottom Row
    bot_row = np.hstack((hist_orig, hist_norm))
    # Stack Vertically
    grid = np.vstack((top_row, bot_row))
    
    return grid

def display_individual_windows(original, normalized):
    # Displays the original and normalized videos in separate windows
    cv2.imshow("Individual View - Original", original)
    cv2.imshow("Individual View - Normalized", normalized)

########## Main Execution ##########

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Webcam not found.")
        return

    # State variables
    use_quadrant_view = True  # Toggle between Quadrant and Individual views
    use_luminance_norm = True # Toggle between Luminance and RGB normalization
    
    print("--- Controls ---")
    print(" 'v' : Toggle View (Quadrant vs Individual Windows)")
    print(" 'n' : Toggle Normalization (Luminance vs RGB Split)")
    print(" 'q' : Quit")

    # Setup Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 10.0, (1280, 960))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Resize for performance
        frame = cv2.resize(frame, (640, 480))
        
        # 1. Apply Normalization based on current mode
        if use_luminance_norm:
            norm_frame = normalize_histogram_luminance(frame)
            norm_type_text = "Method: Luminance (YCrCb)"
        else:
            norm_frame = normalize_histogram_rgb(frame)
            norm_type_text = "Method: RGB Channels"

        # 2. Add text overlay to indicate method
        cv2.putText(norm_frame, norm_type_text, (10, 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Generate histograms and composite view for recording
        hist_orig = create_histogram_plot(frame, "Original Hist")
        hist_norm = create_histogram_plot(norm_frame, "Normalized Hist")
        
        grid = compose_quadrant_view(frame, norm_frame, hist_orig, hist_norm)
        out.write(grid)

        # 3. Display Logic
        if use_quadrant_view:
            # If switching from individual to quadrant, close individual windows
            try:
                if cv2.getWindowProperty("Individual View - Original", cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow("Individual View - Original")
                    cv2.destroyWindow("Individual View - Normalized")
            except cv2.error:
                pass
            
            cv2.imshow("Quadrant View", grid)
            
        else:
            # If switching from quadrant to individual, close quadrant window
            try:
                if cv2.getWindowProperty("Quadrant View", cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow("Quadrant View")
            except cv2.error:
                pass
                
            display_individual_windows(frame, norm_frame)

        # 4. Handle User Input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('v'):
            use_quadrant_view = not use_quadrant_view
            print(f"Switched View. Quadrant Mode: {use_quadrant_view}")
        elif key == ord('n'):
            use_luminance_norm = not use_luminance_norm
            print(f"Switched Normalization. Luminance Mode: {use_luminance_norm}")

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()