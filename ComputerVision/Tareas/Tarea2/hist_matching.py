import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

########## Histogram Processing Functions ##########
def calculate_cdf(histogram):
    # Helper function to calculate the Cumulative Distribution Function (CDF) of
    # a histogram
    cdf = histogram.cumsum()
    normalized_cdf = cdf / float(cdf.max())
    return normalized_cdf

def match_channel_histogram(source_channel, reference_channel):
    # Matches the histogram of a single channel from the source to the
    # reference.

    # Calculate histograms
    s_hist, _ = np.histogram(source_channel.flatten(), 256, [0, 256])
    r_hist, _ = np.histogram(reference_channel.flatten(), 256, [0, 256])

    # Calculate CDFs
    s_cdf = calculate_cdf(s_hist)
    r_cdf = calculate_cdf(r_hist)

    # Create Lookup Table
    # We are looking for the pixel value in Reference (j) such that:
    # CDF_source(i) approx= CDF_reference(j)
    
    lut = np.zeros(256, dtype=np.uint8)
    g_j = 0
    
    for g_i in range(256):
        while g_j < 255 and r_cdf[g_j] < s_cdf[g_i]:
            g_j += 1
        lut[g_i] = g_j

    # Apply mapping using the LUT
    matched_channel = cv2.LUT(source_channel, lut)
    return matched_channel

def exchange_image_histograms(image_a, image_b):
    """
    Performs a bidirectional histogram match.
    Returns:
        new_a: Image A with the color palette of Image B
        new_b: Image B with the color palette of Image A
    """
    # Split images into B, G, R channels
    a_channels = cv2.split(image_a)
    b_channels = cv2.split(image_b)
    
    new_a_channels = []
    new_b_channels = []

    # Process each channel (Blue, Green, Red) independently
    for i in range(3):
        # Apply B's histogram to A
        matched_a = match_channel_histogram(a_channels[i], b_channels[i])
        new_a_channels.append(matched_a)
        
        # Apply A's histogram to B
        matched_b = match_channel_histogram(b_channels[i], a_channels[i])
        new_b_channels.append(matched_b)

    # Merge channels back
    new_image_a = cv2.merge(new_a_channels)
    new_image_b = cv2.merge(new_b_channels)
    
    return new_image_a, new_image_b

########## Visualization Modules ##########
def create_histogram_plot(image_bgr, title="Histogram", size=(400, 300)):
    # Generates a histogram plot using Matplotlib and converts it to an OpenCV
    # image
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    dpi = 80
    fig_w, fig_h = size[0] / dpi, size[1] / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    
    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        hist = cv2.calcHist([image_rgb], [i], None, [256], [0, 256])
        ax.plot(hist, color=color, linewidth=1.5)
        
    ax.set_title(title, fontsize=10)
    ax.set_xlim([0, 256])
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    
    # Render to Numpy Array
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    plot_img = np.asarray(buf)
    
    plot_img = cv2.cvtColor(plot_img, cv2.COLOR_RGBA2BGR)
    plot_img = cv2.resize(plot_img, size)
    
    plt.close(fig) 
    return plot_img

def display_results(original_a, original_b, new_a, new_b):
    # Displays the Original vs Transformed images side-by-side.
    
    # Resize for display consistency if needed
    h, w = 300, 400
    
    # Prepare data for Image 1 (A)
    orig_a_rs = cv2.resize(original_a, (w, h))
    new_a_rs = cv2.resize(new_a, (w, h))
    hist_orig_a = create_histogram_plot(original_a, "Original A Hist", (w, h))
    hist_new_a  = create_histogram_plot(new_a, "A with B's Colors", (w, h))
    
    # Prepare data for Image 2 (B)
    orig_b_rs = cv2.resize(original_b, (w, h))
    new_b_rs = cv2.resize(new_b, (w, h))
    hist_orig_b = create_histogram_plot(original_b, "Original B Hist", (w, h))
    hist_new_b  = create_histogram_plot(new_b, "B with A's Colors", (w, h))

    show_img1 = True
    print("Controls:\n 't': Toggle between Image 1 and Image 2\n 'q': Quit")

    while True:
        if show_img1:
            # Quadrant 1: Original A, Quadrant 2: Result A
            top_row = np.hstack((orig_a_rs, new_a_rs))
            # Quadrant 3: Hist Original A, Quadrant 4: Hist Result A
            bot_row = np.hstack((hist_orig_a, hist_new_a))
        else:
            # Quadrant 1: Original B, Quadrant 2: Result B
            top_row = np.hstack((orig_b_rs, new_b_rs))
            # Quadrant 3: Hist Original B, Quadrant 4: Hist Result B
            bot_row = np.hstack((hist_orig_b, hist_new_b))
        
        # Combine all
        final_grid = np.vstack((top_row, bot_row))
        
        cv2.imshow("Histogram Color Exchange", final_grid)
        
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('t'):
            show_img1 = not show_img1
            
    cv2.destroyAllWindows()

########## Main Execution ##########
def main():
    # Load Images
    image_path_1 = "./imgs/forest_h.jpg"
    image_path_2 = "./imgs/winter.jpg" 

    img1 = cv2.imread(image_path_1)
    img2 = cv2.imread(image_path_2)
    print("Processing images...")

    # Histogram Matching
    result_a, result_b = exchange_image_histograms(img1, img2)

    # Display Results
    print("Displaying results. Press any key to close window.")
    display_results(img1, img2, result_a, result_b)

if __name__ == "__main__":
    main()