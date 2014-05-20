# This file is part of QuTiP: Quantum Toolbox in Python.
#
#    Copyright (c) 2011 and later, Paul D. Nation and Robert J. Johansson.
#    All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without 
#    modification, are permitted provided that the following conditions are 
#    met:
#
#    1. Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the QuTiP: Quantum Toolbox in Python nor the names
#       of its contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
#    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
#    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
#    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
#    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
import numpy as np
import scipy.sparse as sp
from qutip.qobj import *
from qutip.quantum_info.gates import snot, cphase

def qft(N=1):
    """
    Quantum Fourier Transform operator on N qubits.
    
    Parameters
    ----------
    N : int
        Number of qubits.
    
    Returns
    -------
    QFT: qobj
        Quantum Fourier transform operator.
    
    """
    if N < 1:
        raise ValueError("Minimum value of N can be 1")    

    N2 = 2**N
    phase = 2.0j * np.pi/N2
    arr = np.arange(N2)
    L, M = np.meshgrid(arr, arr)
    L = phase * (L * M)
    L = np.exp(L)
    dims = [[2] * N, [2] * N]
    return Qobj(1.0/np.sqrt(N2) * L, dims=dims)


def qft_steps(N=1):
    """
    Quantum Fourier Transform operator on N qubits returning the individual
    steps as unitary matrices.
    
    Parameters
    ----------
    N: int
        Number of qubits.
    
    Returns
    -------
    U_step_list: list of qobj
        List of Hadamard and controlled rotation gates implementing QFT.
    
    """
    if N < 1:
        raise ValueError("Minimum value of N can be 1")
    
    U_step_list = []
    if N == 1:
        U_step_list.append(snot())
    else:
        for i in range(N):
            for j in range(i):
                U_step_list.append(cphase(np.pi/(2**(i-j)), N,
                                   control=i, target=j))
            U_step_list.append(snot(N, i))
        
    return U_step_list
