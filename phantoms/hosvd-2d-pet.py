import numpy as np
from PIL import Image, ImageOps
from scipy import optimize as opt
import matplotlib.pyplot as plt

def to_np_gray(file):
    image = ImageOps.grayscale(Image.open(file))
    data = np.array(image).astype(float)
    return data

def asvt(data):
    return None


def get_std_dev(data):
    hist, bin_edges = np.histogram(data, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2

    # Define model function to be used to fit to the data above:
    def gauss(x, *p):
        A, mu, sigma = p
        return A*np.exp(-(x-mu)**2/(2.*sigma**2))

    # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
    p0 = [1.0, 75.0, 25.0]

    # computes the fitted coefficients
    coeff, var_matrix = opt.curve_fit(gauss, bin_centers, hist, p0=p0)

    # extracts standard deviation
    std_dev = coeff[2]

    # plots histogram data against the fitted gaussian at the same points (bin_centers)
    hist_fit = gauss(bin_centers, *coeff)
    plt.plot(bin_centers, hist, label='Test data')
    plt.plot(bin_centers, hist_fit, label='Fitted data')
    plt.show()

    return std_dev

def plot_histograms():
    #data1 = to_np_gray(r"C:\Users\camer\Downloads\Source_e10.png")[99:126, 306:339]
    #data2 = to_np_gray(r"C:\Users\camer\Downloads\Generated_e10.png")[99:126, 306:339]
    #data3 = to_np_gray(r"C:\Users\camer\Downloads\Truth_e10.png")[99:126, 306:339]


    data1 = to_np_gray(r"C:\Users\camer\Downloads\Source_e10.png")
    data2 = to_np_gray(r"C:\Users\camer\Downloads\Generated_e10.png")
    data3 = to_np_gray(r"C:\Users\camer\Downloads\Truth_e10.png")
    
    #plt.plot(data3)

    #plt.imshow(data2, interpolation='none', origin='lower')
    #plt.imshow(data3)

    hist1, bin_edges1 = np.histogram(data1, density=True)
    bin_centers1 = (bin_edges1[:-1] + bin_edges1[1:])/2

    hist2, bin_edges2 = np.histogram(data2, density=True)
    bin_centers2 = (bin_edges2[:-1] + bin_edges2[1:])/2

    hist3, bin_edges3 = np.histogram(data3, density=True)
    bin_centers3 = (bin_edges3[:-1] + bin_edges3[1:])/2

    plt.plot(bin_centers1, hist1, label='Source')
    plt.plot(bin_centers2, hist2, label='ML Denoised')
    plt.plot(bin_centers3, hist3, label='Truth')
    plt.legend()
    plt.yscale('log')

    plt.show()
    
    return None

def get_patches(data, s):
    
    # iterates through the left-top corner of each s_patch-by-s_patch region of data
    patches = []
    x_size, y_size = data.shape[0], data.shape[1]
    i = 0
    while (i+s) <= x_size:
        j = 0
        while (j+s) <= y_size:
            patch = data[i:i+s, j:j+s]
            patches.append(patch)
            j += 1
        i += 1

    return patches

def get_sim_patches(patch, patches, s, std_dev, max_k=8):
    
    # defines the distance threshold
    tau_d = 6*(std_dev**2)*(s**2)
    
    # loops through all patches and checks if a candidate patch is similar enough to the input patch
    sim_patches = []
    for candidate in patches:
        if np.linalg.norm(np.subtract(patch, candidate))**2 < tau_d and len(sim_patches) <= max_k and not np.array_equal(candidate, patch):
            sim_patches.append(candidate)

    return sim_patches


def extra():
    patch_list, tau_d, max_k = [], 0, 0
    for patch in patch_list:
        similar_patches = []
        for candidate in patch_list:
            if np.linalg.norm(np.subtract(patch, candidate))**2 < tau_d and len(similar_patches) <= max_k and np.array_equal(candidate, patch):
                similar_patches.append(candidate)
        print(similar_patches)


if __name__ == '__main__':
    #data = to_np_gray(r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\noisyderenzo25.png")
    #std_dev = get_std_dev(data)
    #s = 9     # side length of square patch
    #patches = get_patches(data, s)
    #for patch in patches:
    #    sim_patches = get_sim_patches(patch, patches, s, std_dev)

    plot_histograms()
    

    
