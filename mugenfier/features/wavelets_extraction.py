import librosa
import numpy as np
from collections import Counter
import scipy
import dtcwt
import pywt

wavelets_names = ['db4', 'db12', 'db20']

wavelet_name = 'db12' 

dtcwt_levels = [15, 17]

trans = dtcwt.Transform1d(biort='antonini', qshift='qshift_d')

def calculate_entropy(list_values):
	counter_values = Counter(list_values).most_common()
	probabilities = [elem[1]/len(list_values) for elem in counter_values]
	entropy=scipy.stats.entropy(probabilities)
	return entropy

def calculate_statistics(list_values):
	n5 = np.nanpercentile(list_values, 5)
	n25 = np.nanpercentile(list_values, 25)
	n75 = np.nanpercentile(list_values, 75)
	n95 = np.nanpercentile(list_values, 95)
	median = np.nanpercentile(list_values, 50)
	mean = np.nanmean(list_values)
	std = np.nanstd(list_values)
	var = np.nanvar(list_values)
	rms = np.nanmean(np.sqrt(list_values**2))
	return [n5, n25, n75, n95, median, mean, std, var, rms]

def calculate_crossings(list_values):
	zero_crossing_indices = np.nonzero(np.diff(np.array(list_values) > 0))[0]
	no_zero_crossings = len(zero_crossing_indices)
	mean_crossing_indices = np.nonzero(np.diff(np.array(list_values) > np.nanmean(list_values)))[0]
	no_mean_crossings = len(mean_crossing_indices)
	return [no_zero_crossings, no_mean_crossings]

def get_features(list_values):
	entropy = calculate_entropy(list_values)
	crossings = calculate_crossings(list_values)
	statistics = calculate_statistics(list_values)
	return [entropy] + crossings + statistics

def extract_dwt(file_path:str, dwt:str='db12'):
    """ Given a music file path returns the Descrete Wavelet Transform (dwt) 
    feature for that music."""
    if dwt not in wavelets_names:
        dwt = wavelet_name

    d, fs = librosa.load(file_path)
    list_coeff = pywt.wavedec(d, dwt)
    features = []
    for coeff in list_coeff:
        features += get_features(coeff)
    return features

def extract_dtcwt(file_path:str,nlevels:int=17):    
    """ Given a music file path returns the Dual-Tree Complex Wavelet Transform (dtcwt) 
    feature for that music."""
    if nlevels not in dtcwt_levels:
        nlevels = 17
        
    d, fs = librosa.load(file_path)
    forw = trans.forward(d, nlevels=nlevels)
    features = []
    for coeff in forw.highpasses:
        temp = (np.abs(coeff.squeeze()))
        features += get_features(temp)
        
    features += get_features(forw.lowpass.squeeze())    
    return features

