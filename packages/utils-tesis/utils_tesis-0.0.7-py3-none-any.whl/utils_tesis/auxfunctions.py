import numpy as np

# Para realizar la transformada de Fourier
from scipy.fft import rfft, rfftfreq
from scipy.signal.windows import get_window as wndw

# Para crear la ventana móvil (ventanas)
from numpy.lib.stride_tricks import sliding_window_view as swv

# Para graficar

def xf_calc(N, dt) -> int:
    return rfftfreq(N, dt)[: N // 2]


def superimposed(signal, fs):
    """
    Superimposed components of a signal

    Parameters
    ----------

    signal: numpy array
        Array of shape (1, n).

    fs: int
        Signal's sampling frequency.
    """
    n_first_cycle = int(fs / 60)
    N = len(signal)

    si_signal1 = [0 for i in range(n_first_cycle)]
    si_signal2 = [round(signal[i] - signal[i - 64], 9) for i in range(n_first_cycle, N)]

    return np.array(si_signal1 + si_signal2)


def fourier(window, N, dt):
    """
    Returns fft of input signal

    parameters
    ----------

    window: np.array
        Window with signal

    N: int
        Number of samples inside window

    returns
    -------

    numpy.array
        fft coefficients
    """
    xf = xf_calc(N, dt)
    yf = rfft(window)
    try:
        yf.shape[1]
        return xf, (2.0 / N) * np.abs(yf[:, 0 : N // 2])
    except IndexError:
        return xf, (2.0 / N) * np.abs(yf[0 : N // 2])


# def fourier_windows(windows, N):

#     for window in windows:
#         yf = rfft(window)
#         return (2.0 / N) * np.abs(yf[0 : N // 2])


def moving_window(data, N, step, window_name="boxcar"):
    """
    Creación de las ventanas móviles para todas las señales

    parameters
    ----------

    data: np.array
        señal en el tiempo

    N: int
        Tamaño de la ventana (muestras)

    step: int
        Tamaño de paso de las ventanas


    returns
    -------

    np.array
        Array con ventanas de tamaño N
    """
    window_func = wndw(window_name, N, fftbins=True)
    ventanas_punto_a_punto = swv(data, (N))
    return ventanas_punto_a_punto[0::step]


def iterador_max_val(windows, window_function, N, dt, signal_name):
    xf = rfftfreq(N, dt)[: N // 2]
    window_max = np.empty(len(xf))

    for window in windows:

        window = window * window_function
        fft_window = fourier(window, N)

        for freq, (value, prev_max) in enumerate(zip(fft_window, window_max)):
            if value > prev_max:
                window_max[freq] = value

        print(f"Frequency Max {signal_name}")
        for i, max_val in enumerate(window_max):
            print(f"Frequency {60*i:4}: {max_val:7.3f}")



