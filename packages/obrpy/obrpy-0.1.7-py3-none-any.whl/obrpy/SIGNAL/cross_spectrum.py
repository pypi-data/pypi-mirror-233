import numpy as np
import nitime.algorithms as tsa

def dB(x, out=None):
    if out is None:
        return 10 * np.log10(x)
    else:
        np.log10(x, out)
        np.multiply(out, 10, out)

def mtem(i, j, dt):
    """
    multitaper estimation method
    Input:
    i      first time series
    j      second time series

    Output:
    fki    power spectral density i
    fkj    power spectral density j
    cij    cross-spectral density ij
    coh    coherence
    ph     phase spectrum between ij at input freq

    """
    #print('i size', i.shape)
    #print('j size', j.shape)

    # apply multi taper cross spectral density from nitime module
    f, pcsd_est = tsa.multi_taper_csd(np.vstack([i,j]), Fs=1/dt, low_bias=True, adaptive=True, sides='onesided')

    # output is MxMxN matrix, extract the psd and csd
    fki = pcsd_est.diagonal().T[0]
    fkj = pcsd_est.diagonal().T[1]
    cij = pcsd_est.diagonal(+1).T.ravel()

    # using complex argument of cxy extract phase component
    ph = np.angle(cij)

    # calculate coherence using csd and psd
    coh = np.abs(cij)**2 / (fki * fkj)

    return f, fki, fkj, cij, ph, coh

def mtem_unct(i_, j_, dt_, cf, mc_no=20):
    """
    Uncertainty function using Monte Carlo analysis
    Input:
    i_     timeseries i
    j_     timeseries j
    cf     coherence function between i and j
    mc_no  number of iterations default is 20, minimum is 3

    Output:
    phif   phase uncertainty bounded between 0 and pi
    """
    #print('iteration no is', mc_no)

    data = np.vstack([i_,j_])
    # number of iterations
    # flip coherence and horizontal stack
    cg = np.hstack((cf[:-1], np.flipud(cf[:-1])))

    # random time series fi
    mc_fi = np.random.standard_normal(size=(mc_no,len(data[0])))
    mc_fi = mc_fi / np.sum(abs(mc_fi),axis=1)[None].T

    # random time series fj
    mc_fj = np.random.standard_normal(size=(mc_no,len(data[0])))
    mc_fj = mc_fj / np.sum(abs(mc_fj),axis=1)[None].T

    # create semi random timeseries based on magnitude squared coherence
    # and inverse fourier transform for js
    js = np.real(np.fft.ifft(mc_fj * np.sqrt(1 - cg ** 2)))
    js_ = js + np.real(np.fft.ifft(mc_fi *cg))

    # inverse fourier transform for xs
    is_ = np.real(np.fft.ifft(mc_fi))

    # spectral analysis
    f_s, pcsd_est = tsa.multi_taper_csd(np.vstack([is_,js_]), Fs=1/dt_, low_bias=True, adaptive=True, sides='onesided')
    cijx = pcsd_est.diagonal(+int(is_.shape[0])).T
    phi = np.angle(cijx)

    # sort and average the highest uncertianties
    pl = int(round(0.95*mc_no)+1)
    phi = np.sort(phi,axis=0)
    phi = phi[((mc_no+1)-pl):pl]
    phi = np.array([phi[pl-2,:],-phi[pl-mc_no,:]])
    phi = phi.mean(axis=0)#
    phi = np.convolve(phi, np.array([1,1,1])/3)
    phif = phi[1:-1]
    return phif

def PSSS(y0:np.ndarray,y1:np.ndarray,z:np.ndarray,f:np.ndarray,display=False) -> float:

    """ Function to compute the relative phase spectrum spectral shift in a region.

        The cross spectrum phase spectrum is computed using the multitapper method defined 
        in other functions of this module and using the TSA nitime algorithm.
        Then signal.correlate is used to determine the cross correlation, and the
        maximum position is located and related with the spectral shift trought the scan ratio

        :param  y0 (np.array)   : First signal to compare, used as reference
        :param  y1 (np.array)   : Second signal to compare
        :param  f  (np.array)   : Frequency domain x axis [GHz]

        :optional display=False (bool) : If True, a plot with the cross correlation will be displayed 
                                        (add  "plt.show()" or "plt.savefig()" after this funtion)

        :retruns -1*out/np.mean(f) (float)   : relative phase spectrum spectral shift
    """


    # Unpack the signals 

    p1 = y0[0,:]
    p2 = y1[0,:]
    s1 = y0[1,:]
    s2 = y1[1,:]

    # Check length of signal to discard a value if necessary

    if len(p1)%2 == 0:
        p1 = p1[:-1]
        p2 = p2[:-1]
        s1 = s1[:-1]
        s2 = s2[:-1]

    # Frequency sampling
    DF = f[-1]-f[0]     # Total frequency increment [GHz]
    n = len(p1)         # Sample lenght
    dt = 1/(f[1]-f[0])  # Time increment

    # Phase spectrum
    f, fki, fkj, cij, ph, coh = mtem(p1,s1,dt)
    Y1 = ph
    f, fki, fkj, cij, ph, coh = mtem(p2,s2,dt)
    Y2 = ph

    # Normalization
    Y1 = (Y1 - np.mean(Y1)) / (np.std(Y1)* len(Y1))
    Y2 = (Y2 - np.mean(Y2)) / (np.std(Y2))

    # Cross correlation
    corr = np.correlate(Y1, Y2, mode='same')

    # Frequency lags
    freq_lags = np.linspace(-0.5*DF, 0.5*DF, n)
    out = freq_lags[np.argmax(corr)]

    return -1*out/np.mean(f)
