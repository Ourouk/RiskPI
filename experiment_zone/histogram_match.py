import argparse
import os
import sys

from skimage.exposure import match_histograms, histogram, cumulative_distribution
import matplotlib.pyplot as plt
import cv2

# Example of usage:
# python histogram_match.py -r ../data/gsm/amerique_latine.jpg -i ../data/gsm/amerique_latine_dark.jpg -o ../data/gsm/outputs -n newName.jpg

def main(reference_path, input_path, output_dir, save_histogram, use_HSV, output_name=None):
    if output_name is None:
        output_name = input_path
    
    print(f"Reference file: {reference_path}")
    print(f"Input file: {input_path}")
    print(f"Output directory: {output_dir}")
    
    # Read the input and reference files
    input_file = cv2.imread(input_path)
    reference_file = cv2.imread(reference_path)
    
    # Convert the images to HSV if required
    if use_HSV:
        input_file = cv2.cvtColor(input_file, cv2.COLOR_BGR2HSV)
        reference_file = cv2.cvtColor(reference_file, cv2.COLOR_BGR2HSV)

    # Match the histograms    
    matchedImage = match_histograms(input_file, reference_file, channel_axis=-1) 
    
    # Save the histogram of the output if required
    if save_histogram:
        fig, axes = plt.subplots(3, 1, figsize=(10, 8))
        if use_HSV:
            colors_plot = ['purple', 'green', 'orange']
            labels_axis = ['Hue', 'Saturation', 'Value']
        else:
            colors_plot = ['blue', 'green', 'red']
            labels_axis = ['Blue', 'Green', 'Red']
        for c, color in enumerate(colors_plot):
            channel_data = matchedImage[..., c]
            img_hist, bins = histogram(channel_data, source_range='dtype')
            axes[c].plot(bins, img_hist / img_hist.max(), color=color)
            img_cdf, bins = cumulative_distribution(channel_data)
            axes[c].plot(bins, img_cdf, color=color, linestyle='dashed')
            axes[c].set_ylabel(labels_axis[c])  # Explicitly set the ylabel
        axes[0].set_title('Histogram and CDF')
        output_histogram_file = os.path.join(output_dir, f"{os.path.basename(output_name)}_histogram_plot.png")
        print(f"Saving histogram plot of the output to {output_histogram_file}")
        plt.savefig(output_histogram_file)
        plt.close(fig)
    
    # Convert the image back to BGR if required
    if use_HSV:
        matchedImage = cv2.cvtColor(matchedImage, cv2.COLOR_HSV2BGR)
    
    # Save the matched image
    output_file = os.path.join(output_dir, os.path.basename(output_name))
    print(f"Saving matched image to {output_file}")
    cv2.imwrite(output_file, matchedImage)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script applies a histogram matching algorithm to an input file using a reference file.\nExample: python histogram_match.py -r reference.png -i input.png -o output_dir",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    parser.add_argument("-r", "--reference", type=str, help="Path to the reference file", required=True)
    parser.add_argument("-i", "--input", type=str, help="Path to the input file", required=True)
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", required=True)
    parser.add_argument("-n", "--name", type=str, help="Name of the output file")
    parser.add_argument("-h", "--histogram", action="store_true", help="Also saves the histogram of the output")
    parser.add_argument("-f", "--HSV", action="store_false", help="Formats the image in HSV")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.reference):
        raise FileNotFoundError(f"The reference file {args.reference} does not exist.")
    
    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"The input file {args.input} does not exist.")
    
    if not os.path.isdir(args.output):
        raise NotADirectoryError(f"The output directory {args.output} does not exist.")
    
    main(args.reference, args.input, args.output, args.histogram, args.HSV, args.name)
