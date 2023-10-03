import numpy as np
import pandas as pd
from scipy.io import wavfile
import librosa
import seaborn as sns
import matplotlib.pyplot as plt
import glob, os
from pathlib import Path
import statistics

def basic_audio_processor(file,effect,hoplength=512,rate=1):
    data, sr= librosa.load(file)
    if effect=='trim':
        trimmed= librosa.effects.trim(data)
        print('the length of the original audio is ',len(data),' and the length of the trimmed audio is',len(trimmed),' .',(len(data)-len(trimmed)),' values have been removed which contributed to ',(((len(data)-len(trimmed))/len(data))*100),' % of total audio data.')
        return trimmed
    elif effect=='remix':
        _, beat_frames = librosa.beat.beat_track(y=data, sr=sr,hop_length=hoplength)
        beat_samples = librosa.frames_to_samples(beat_frames)
        intervals = librosa.util.frame(beat_samples, frame_length=2,hop_length=1).T
        y_out = librosa.effects.remix(data,intervals[::-1])
        print(' the given audio signal has been time reversed with a hop length of ',hoplength)
        return y_out
    elif effect=='time-strech':
        y_fast = librosa.effects.time_stretch(data, rate=rate)
        print('the given audio signal has been converted to the speed of',rate)
    elif effect=='hpss':
        y_harm, y_perc = librosa.effects.hpss(data)
        return [y_harm,y_perc]
    else:
        return data
    
def statistical_analyser(file):
    data,sr=librosa.load(file)
    d={}
    d['Sampling rate']=sr
    d['Mean Amplitude']=np.mean(data)
    d['Median Amplitude']=np.median(data)
    d['Mode Amplitude']= statistics.mode((data))
    d['Range of Amplitude']= np.max(data)-np.min(data)
    d['Zero crossings']=sum(librosa.zero_crossings(data))
    d['Mean of spectral centroids']=np.mean(librosa.feature.spectral_centroid(y=data,sr=sr))
    d['Median of spectral centroids']=np.median(librosa.feature.spectral_centroid(y=data,sr=sr))
    d['Standard Deviation of spectral centroids']=np.std(librosa.feature.spectral_centroid(y=data,sr=sr))
    d['Mean of spectral bandwidth']= np.mean(librosa.feature.spectral_bandwidth(y=data,sr=sr))
    d['Median of spectral bandwidth']= np.mean(librosa.feature.spectral_bandwidth(y=data,sr=sr))
    d['Standard Deviation of spectral bandwidth']= np.mean(librosa.feature.spectral_bandwidth(y=data,sr=sr))
    d['Mean of spectral contrast']= np.mean(librosa.feature.spectral_contrast(y=data,sr=sr))
    d['Median of spectral contrast']= np.mean(librosa.feature.spectral_contrast(y=data,sr=sr))
    d['Standard Deviation of spectral contrast']= np.mean(librosa.feature.spectral_contrast(y=data,sr=sr))
    d['Mean of RMS']=np.mean(librosa.feature.rms(y=data))
    d['Median of RMS']=np.median(librosa.feature.rms(y=data))
    d['Standard Deviation of RMS']=np.std(librosa.feature.rms(y=data))
    return d

def AutomatedExtractor_single(file):
    def mfcc_extractor(file):
        data, sr = librosa.load(file) 
        mfccs_features = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=128)
        mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
        return mfccs_scaled_features
    def zero_extractor(file):
        data, sr = librosa.load(file)
        zeros=librosa.feature.zero_crossing_rate(data,frame_length=2048, hop_length=512, center=True)
        zeros_scaled_features= np.mean(zeros.T,axis=0)
        return zeros_scaled_features
    def rms_extractor(file):
        data, sr = librosa.load(file)    
        rms=librosa.feature.rms(y=data)
        rms_scaled_features= np.mean(rms.T,axis=0)
        return rms_scaled_features
    def spectral_centroid_extractor(file):
        data, sr = librosa.load(file)
        sc=librosa.feature.spectral_centroid(y=data,sr=sr)
        sc_scaled_features= np.mean(sc.T,axis=0)
        return sc_scaled_features
    def spectral_bandwidth_extractor(file):
        data, sr = librosa.load(file)
        sb=librosa.feature.spectral_bandwidth(y=data,sr=sr)
        sb_scaled_features= np.mean(sb.T,axis=0)
        return sb_scaled_features
    def spectral_contrast_extractor(file):
        data, sr = librosa.load(file)
        sco=librosa.feature.spectral_contrast(y=data,sr=sr)
        sco_scaled_features= np.mean(sco.T,axis=0)
        return sco_scaled_features
    def polynomial_extractor(file):
        data, sr = librosa.load(file)
        poly=librosa.feature.poly_features(y=data,sr=sr,order=2)
        poly_scaled_features= np.mean(poly.T,axis=0)
        return poly_scaled_features
    mfcc_features=[]
    zero_features=[]
    rms_features=[]
    sc_features=[]
    sb_features=[]
    sco_features=[]
    poly_features=[]
    mfcc=mfcc_extractor(file)
    mfcc_features.append(mfcc.tolist())

    zero=zero_extractor(file)
    zero_features.append(zero.tolist())

    rms=rms_extractor(file)
    rms_features.append(rms.tolist())

    spectral_centroid=spectral_centroid_extractor(file)
    sc_features.append(spectral_centroid.tolist())

    spectral_bandwidth=spectral_bandwidth_extractor(file)
    sb_features.append(spectral_bandwidth.tolist())

    spectral_contrast=spectral_contrast_extractor(file)
    sco_features.append(spectral_contrast.tolist())

    poly=polynomial_extractor(file)
    poly_features.append(poly.tolist())
    extracted_features_df=pd.DataFrame([mfcc_features,zero_features,rms_features,sc_features,sb_features,sco_features,poly_features])
    extracted_df=extracted_features_df.T
    extracted_df.columns=['mfcc','zero crossing rate','root mean square','spectral centroid','spectral bandwidth','spectral contrast','polynomial']
    return extracted_df

def AutomatedExtractor_multiple(file):
    def mfcc_extractor(file):
        data, sr = librosa.load(file) 
        mfccs_features = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=128)
        mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
        return mfccs_scaled_features
    def zero_extractor(file):
        data, sr = librosa.load(file)
        zeros=librosa.feature.zero_crossing_rate(data,frame_length=2048, hop_length=512, center=True)
        zeros_scaled_features= np.mean(zeros.T,axis=0)
        return zeros_scaled_features
    def rms_extractor(file):
        data, sr = librosa.load(file)    
        rms=librosa.feature.rms(y=data)
        rms_scaled_features= np.mean(rms.T,axis=0)
        return rms_scaled_features
    def spectral_centroid_extractor(file):
        data, sr = librosa.load(file)
        sc=librosa.feature.spectral_centroid(y=data,sr=sr)
        sc_scaled_features= np.mean(sc.T,axis=0)
        return sc_scaled_features
    def spectral_bandwidth_extractor(file):
        data, sr = librosa.load(file)
        sb=librosa.feature.spectral_bandwidth(y=data,sr=sr)
        sb_scaled_features= np.mean(sb.T,axis=0)
        return sb_scaled_features
    def spectral_contrast_extractor(file):
        data, sr = librosa.load(file)
        sco=librosa.feature.spectral_contrast(y=data,sr=sr)
        sco_scaled_features= np.mean(sco.T,axis=0)
        return sco_scaled_features
    def polynomial_extractor(file):
        data, sr = librosa.load(file)
        poly=librosa.feature.poly_features(y=data,sr=sr,order=2)
        poly_scaled_features= np.mean(poly.T,axis=0)
        return poly_scaled_features
    mfcc_features=[]
    zero_features=[]
    rms_features=[]
    sc_features=[]
    sb_features=[]
    sco_features=[]
    poly_features=[]
    for i in file:
            mfcc=mfcc_extractor(i)
            mfcc_features.append(mfcc)

            zero=zero_extractor(i)
            zero_features.append(zero)

            rms=rms_extractor(i)
            rms_features.append(rms)

            spectral_centroid=spectral_centroid_extractor(i)
            sc_features.append(spectral_centroid)

            spectral_bandwidth=spectral_bandwidth_extractor(i)
            sb_features.append(spectral_bandwidth)

            spectral_contrast=spectral_contrast_extractor(i)
            sco_features.append(spectral_contrast)

            poly=polynomial_extractor(i)
            poly_features.append(poly)
    extracted_features_df=pd.DataFrame([mfcc_features,zero_features,rms_features,sc_features,sb_features,sco_features,poly_features])
    extracted_features_df=extracted_features_df.T
    extracted_features_df.columns=['mfcc','zero crossing rate','root mean square','spectral centroid','spectral bandwidth','spectral contrast','polynomial']
    return extracted_features_df