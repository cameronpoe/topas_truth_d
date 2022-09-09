import numpy as np
import matplotlib.pyplot as plt
from zernike import RZern
from scipy import optimize

def fix_npy_ending(file_loc):
    # file_loc: str - path of the file in question

    # adds '.npy' if the string does not end in '.npy'
    if not file_loc[-4:] == '.npy':
        file_loc += '.npy'
    return file_loc

def keplerslicer(volume, sliceplane, slicevalue) :
    # first step is to define a new 2d plane that can be graphed
    # if the slice plane is "x" then the x values are held
    # constant and a new array of y ans z is created
    # Symmetric for all axis. x->yz, y->xz, z->xy
    if sliceplane == "x" or sliceplane == "X":
        useslice = volume[slicevalue]
    elif sliceplane == "y" or sliceplane == "Y":
        useslice = volume[:, slicevalue]
    elif sliceplane == "z" or sliceplane == "Z":
        useslice = volume[:,:, slicevalue]
    else:
        print('only \'x\', \'y\', \'z\' allowed for `sliceplace`. Try again.')
        exit()
    return useslice

# shows what the zernike error from the image is
def zernikeerror(p, image, rows, cols, order):
    
    cart = RZern(order); #something from the Zernike polynoial library

    #defines an object? Polynomial up to order?
    x = p[0]
    y = p[1]
    r = p[2]

    # makes a set of positions from left to right and top to bottom to check
    # same thing done for y
    ddx = np.linspace(-x/r, (rows-x)/r, rows)
    # makes a range of numbers of size rows from left to right
    ddy = np.linspace(-y/r, (cols-y)/r, cols)
    xv, yv = np.meshgrid(ddx, ddy) # makes an x and y matrix of values
    cart.make_cart_grid(xv, yv, unit_circle=False)
    eval = cart.eval_grid(cart.fit_cart_grid(image)[0], matrix=True);
    # evaluation of Zernike Polynomials somehow
    # print(np.size(eval))
    return np.reshape(image-eval, rows*cols);

# takes an np array or location of np array and fits a zernike up to `order` then subtracts to create a filtered image
def plot_zernike_fitted(file, order, sliceplane, slicevalue, display=True):
    # file: str - location of .npy file, np.array - np array object
    # order: int - highest order of Zernike function to fit
    # sliceplane: 
    # slicevalue:
    # display: bool - displays all images as default
    
    # uses `file` data type to either load as np array or to treat as np array
    if isinstance(file, (str,)):
        currentimage = np.load(fix_npy_ending(file))
    elif isinstance(file, (np.ndarray,)):
        currentimage = file
    else:
        print('File type " %s " not supported'%type(file))
        exit()    

    # checks to see if needs to call keplerslicer to render 3d image into 2d array
    if (len(np.shape(file)) == 3):
        img = keplerslicer(currentimage, sliceplane, slicevalue)
    elif (len(np.shape(file)) == 2):
        img = currentimage
    else:
        print('Dimensions of %s not allowed. Try again with 2D or 3D numpy array.'%file)
        exit()

    # assigns rows, cols the lengths in x, y of img
    rows, cols = img.shape

    #defines the radius to create unitcircle
    r0 = cols/2. if rows>cols else rows/2.

    x0 = rows/2.; # x0 = half width
    y0 = cols/2.; # y0 = half height

    # initial vector
    p0 = [x0, y0, r0]

    # finds zernikes up to `order` that best fit img
    p1, success = optimize.leastsq(zernikeerror, p0, args=(img, rows, cols, order))
    cart = RZern(order);

    # assigns final vector components to x, y, r
    x, y, r = p1[0], p1[1], p1[2]
    print('Best estimate coordinate origin: (x,y,r)=(%s, %s, %s)'%(x,y,r))

    ddx = np.linspace(-x/r, (rows-x)/r, rows)
    ddy = np.linspace(-y/r, (cols-y)/r, cols)

    xv, yv = np.meshgrid(ddx, ddy)
    cart.make_cart_grid(xv, yv, unit_circle=False)

    # creates numpy arrays of all images
    eval = cart.eval_grid(cart.fit_cart_grid(img)[0], matrix=True);
    fitted_image = currentimage - eval
    original_image = currentimage

    if display:
        # plot zernike
        plt.figure(1)
        aplot = plt.imshow(eval, cmap='gray')
        plt.colorbar(aplot, orientation='vertical')

        # plot fitted graph
        plt.figure(2)
        bplot = plt.imshow(fitted_image, cmap='gray')
        plt.colorbar(bplot, orientation='vertical')

        # plot original graph
        # print(original_image[81][125])
        # print(original_image[109][109])
        plt.figure(3)
        cplot = plt.imshow(original_image, cmap='gray')
        plt.colorbar(cplot, orientation='vertical')
        # plt.grid(color='w')
        plt.show()

# simply displays a 3d or 2d .npy file as a 2d image
def show_image(source_file, pixels, slice=10, super_slice=0, display=True):
    # source_file: str - location of .npy file
    # pixels: int - number of pixels of one side of square np array
    # slice: int - 
    # super_slice: int
    # display: bool - True runs plt.show() to display image

    source = np.load(fix_npy_ending(source_file))

    print("Dimensions of source: %s"%str(np.shape(source)))

    # tests if source is a 2d or 3d image
    if (len(np.shape(source)) == 3):
        image = source[:,:,slice]
        if (super_slice > 0):
            for i in range(super_slice):
                image += source[:,:,slice + i - int(super_slice / 2)]
    elif (len(np.shape(source)) == 2):
        image = source.reshape((pixels,pixels))
    else:
        print('Dimensions of %s not allowed. Try again with 2D or 3D numpy array.'%source_file)
        exit()

    # displays source
    if display:
        fig, pre = plt.subplots()
        pre_ = pre.imshow(image, cmap='gray')
        pre_bar = plt.colorbar(pre_)
        plt.show()

    return image

def fft(image, filterloc, display=True):
    # image: np.array - np array of the image to be filtered
    # filterloc: str - path to the np array of the filter
    # display: bool - displays image as default

    image_F = np.fft.fftn(image)

    filter = np.load(fix_npy_ending(filterloc))

    symmetry = 2

    filter = 1 * filter

    cutoff_low = symmetry
    cutoff_high = pixels - symmetry
    # filter[cutoff_low:cutoff_high,cutoff_low:cutoff_high] = 1
    # filter[cutoff_high:,:] = 1
    # filter[:,cutoff_high:] = 1
    # filter[:cutoff_low, :] = 1
    # filter[:, :cutoff_low] = 1

    filter[cutoff_low:cutoff_high, :] = 1
    filter[:, cutoff_low:cutoff_high] = 1

    # now filter out the edge behavior

    fig, ax = plt.subplots()
    # fig, ay = plt.subplots()
    ax.imshow(np.real(filter))
    # ay.imshow(np.real(image_F))
    # plt.show()
    print('Dimensions of filter: %s'%str(filter.shape))
    cleaned_F = np.multiply(image_F, filter)

    symmetry = 30

    cutoff_low = symmetry
    cutoff_high = pixels - symmetry

    cleaned_F[cutoff_low:cutoff_high, :] = 1
    cleaned_F[:, cutoff_low:cutoff_high] = 1

    cleaned = np.fft.ifftn(cleaned_F)

    fig, az = plt.subplots()

    cleaned = np.real(cleaned)
    # cleaned = np.where(cleaned > 0,cleaned, 0.0)

    # conditionally displays image
    if display:
        az_ = az.imshow(cleaned, cmap='gray')
        az_bar = plt.colorbar(az_)
        plt.show()

    #np.save(source_file + "_clean", cleaned)
    return cleaned

source_file = ''
# source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T1mm_timerand\400px_2sig_thin_noatten_nola"

# source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T500um_timerand\400px_2sig_thin_noatten_nola"

#source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T100um_timerand\400px_2sig_thin_noatten_nola"

# source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T1mm_timerand\400px_2sig_bin_noatten_nola"

# source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T500um_timerand\800px_2sig_thin_noatten_nola"

# source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T500um_timerand\1200px_2sig_thin_noatten_nola"

# source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T1mm_timerand\400px_2sig_log_noatten_nola"





# source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T100um_timerand\400px_2sig_thin_noatten_nola_ta10"

# source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T100um_timerand\400px_2sig_bin_noatten_nola_ta10.npy"

# source_file = r'C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L100cm_100um_notimerand\400px_2sig_bin_noatten_nola_ta10'


source_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\8e7_sidearms\L130ps_T100um_timerand\400px_2sig_bin_noatten_nola_ta10_z83.55.npy"

pixels = 400
filter_file = r"C:\Users\camer\topaspet-github\topas_truth_d\phantoms\xcat_topas_pet_examples\brain_images\filters\4_pi_filter.npy"
source_file_image = show_image(source_file, pixels)
source_file_image_fft = fft(source_file_image, filter_file, display=False)
plot_zernike_fitted(source_file_image_fft, 3, 'z', 1)










