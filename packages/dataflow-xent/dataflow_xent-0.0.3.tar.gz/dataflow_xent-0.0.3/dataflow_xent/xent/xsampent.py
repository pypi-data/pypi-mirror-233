"""Base Cross Sample Entropy function."""
import numpy as np 

def XSampEn(Sig, m=2, tau=1, r=None, Logx=np.exp(1)):

    """This code was copied from EntropyHub to avoid dill.py version conflict with apache-beam
    XSampEn  Estimates the cross-sample entropy between two univariate data sequences.
    
    .. code-block:: python
    
        XSamp, A, B = XSampEn(Sig) 
        
    Returns the cross-sample entropy estimates (``XSamp``) and the number of 
    matched vectors (``m: B``, ``m+1: A``) for ``m`` = [0,1,2] estimated for the two 
    univariate data sequences contained in ``Sig`` using the default parameters:
    embedding dimension = 2, time delay = 1, radius = 0.2*SD(``Sig``), logarithm = natural
 
    .. code-block:: python 
 
         XSamp, A, B = XSampEn(Sig, keyword = value, ...)
                  
    Returns the cross-sample entropy estimates (``XSamp``) for dimensions [0,1,..., ``m``]
    estimated between the data sequences in ``Sig`` using the specified 'keyword' arguments:
        :m:    - Embedding Dimension, a positive integer  [default: 2]
        :tau:   - Time Delay, a positive integer         [default: 1]
        :r:     - Radius, a positive scalar              [default: 0.2*SD(``Sig``)]
        :Logx:  - Logarithm base, a positive scalar      [default: natural]
 
    :See also:
        ``XFuzzEn``, ``XApEn``, ``SampEn``, ``SampEn2D``, ``XMSEn``, ``ApEn``
    
    :References:
        [1] Joshua S Richman and J. Randall Moorman. 
            "Physiological time-series analysis using approximate entropy
            and sample entropy." 
            American Journal of Physiology-Heart and Circulatory Physiology
            (2000)
    
    """
      
    Sig = np.squeeze(Sig)
    if r is None:
        r = 0.2*np.std(Sig)    
    if Sig.shape[0] == 2:
        Sig = Sig.transpose()        
    N = Sig.shape[0]
    assert N>10 and min(Sig.shape)==2,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and r>=0, "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    
    S1 = Sig[:,0]; S2 = Sig[:,1]     
    M = np.hstack((m*np.ones(N-m*tau), np.repeat(np.arange(m-1,0,-1),tau)))
    Counter = 1*(abs(np.expand_dims(S2,axis=0) -np.expand_dims(S1,axis=1))<= r)  
    A = np.zeros(m+1)
    B = np.zeros(m+1)
    A[0] = np.sum(Counter)
    B[0] = N*N
    
    for n in range(M.shape[0]):
        ix = np.where(Counter[n, :] == 1)[0]        
        for k in range(1,int(M[n]+1)):              
            ix = ix[ix + (k*tau) < N]
            if not len(ix):
                break  
            p1 = np.tile(S1[n: n+1+(tau*k):tau], (ix.shape[0], 1))                       
            p2 = S2[np.expand_dims(ix,axis=1) + np.arange(0,(k*tau)+1,tau)]
            ix = ix[np.amax(abs(p1 - p2), axis=1) <= r] 
            Counter[n, ix] += 1
    
    for k in range(1, m+1):
        A[k] = np.sum(Counter > k)
        B[k] = np.sum(Counter >= k)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        XSamp = -np.log(A/B)/np.log(Logx)
 
    return XSamp, A, B