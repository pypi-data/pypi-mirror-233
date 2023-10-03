from utils_tesis.auxfunctions import superimposed, moving_window, fourier
from utils_tesis.detection import detection_iter
import numpy as np
from itertools import repeat


def signal_t(
    signal_info: dict, no_return: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    """Returns time and signal vectors

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain 'signals' and 'signal_name'
    no_return : bool, optional
        Internal variable to use when accessing from other functions from module,
        by default False

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        time vector, signal vector
    """
    # Extraer la información del diccionario
    signal_name = signal_info["signal_name"]
    signals = signal_info["signals"]
    # Cargar la señal
    signal, t, params = signals.load_data(signal_name)
    # Guardar los valores en el diccionario
    signal_info["signal"] = signal
    signal_info["t"] = t
    signal_info["params"] = params

    if no_return:
        return

    return t, signal


def si_signal_t(
    signal_info: dict, no_return: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    """Returns time and superimposed signal vectors

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain 'signal',
        'signals' and 'signal_name'
    no_return : bool, optional
        Internal variable to use when accessing from other functions from module,
        by default False

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        time vector, superimposed signal vector
    """
    signal = signal_info.get("signal", "")

    if len(signal) == 0:
        signal_t(signal_info, no_return=True)

    signal = signal_info["signal"]
    fs = signal_info["params"]["fs"]
    t = signal_info["t"]

    si_signal = superimposed(signal, fs)

    signal_info["si_signal"] = si_signal
    if no_return:
        return

    return t, si_signal


def windows_creator(
    signal_info: dict, no_return: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    """Returns time and signal windows

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain 'signal', 'window_length',
        'step', 'signals' and 'signal_name'
    no_return : bool, optional
        Internal variable to use when accessing from other functions from module,
        by default False

    Returns
    -------
    tuple[np.ndarray, np.ndarray]

        time windows, signal windows
        shape -> (m, N)
            with:

            m = ((M - N)/step) + 1

            where
            m = amount of windows
            N = windows length
            M = signal length

    """
    signal = signal_info.get("signal", "")

    if len(signal) == 0:
        signal_t(signal_info, no_return=True)

    signal = signal_info["signal"]
    t = signal_info["t"]
    window_length = signal_info["window_length"]
    step = signal_info["step"]
    signal_windows, t_windows = list(
        map(moving_window, [signal, t], repeat(window_length), repeat(step))
    )

    signal_info["signal_windows"] = signal_windows
    signal_info["t_windows"] = t_windows

    if no_return:
        return

    return t_windows, signal_windows


def si_windows_creator(
    signal_info: dict, no_return: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    """Returns time and superimposed signal windows

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain 'si_signal', 'window_length',
        'step', 'signals' and 'signal_name'
    no_return : bool, optional
        Internal variable to use when accessing from other functions from module,
        by default False

    Returns
    -------
    tuple[np.ndarray, np.ndarray]

        time windows, superimposed signal windows
        shape -> (m, N)
            with:

            m = ((M - N)/step) + 1

            where
            m = amount of windows
            N = windows length
            M = signal length

    """

    si_signal = signal_info.get("si_signal", "")
    if len(si_signal) == 0:
        si_signal_t(signal_info, no_return=True)

    si_signal = signal_info["si_signal"]
    t = signal_info["t"]
    window_length = signal_info["window_length"]
    step = signal_info["step"]

    si_signal_windows, t_windows = list(
        map(moving_window, [si_signal, t], repeat(window_length), repeat(step))
    )

    signal_info["si_signal_windows"] = si_signal_windows
    signal_info["t_windows"] = t_windows

    if no_return:
        return

    return t_windows, si_signal_windows


def STFT(signal_info: dict, no_return: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Returns short time Fourier transform of signal.

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain 'signal_windows', 'window_length',
        'step', 'dt', 'signals' and 'signal_name'
    no_return : bool, optional
        Internal variable to use when accessing from other functions from module,
        by default False

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Frecuency bins array, Fast Fourier Transform vector
    """

    signal_windows = signal_info.get("signal_windows", "")
    if len(signal_windows) == 0:
        windows_creator(signal_info, no_return=True)

    signal_windows = signal_info["signal_windows"]
    dt = signal_info["params"]["dt"]
    window_length = signal_info["window_length"]

    xf, fft_windows = fourier(signal_windows, window_length, dt)

    signal_info["xf"] = xf
    signal_info["fft_windows"] = fft_windows
    signal_info["fft_windows_fundamental"] = fft_windows[:, 1]

    if no_return:
        return

    number_of_windows = len(fft_windows)

    return np.tile(xf, (number_of_windows, 1)), fft_windows


def si_STFT(
    signal_info: dict, no_return: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    """Returns short time Fourier transform of signal's superimposed components.

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain 'si_signal_windows', 'window_length',
        'step', 'dt', 'signals' and 'signal_name'
    no_return : bool, optional
        Internal variable to use when accessing from other functions from module,
        by default False

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Frecuency bins array, si signal Fast Fourier Transform vector
    """

    si_signal_windows = signal_info.get("si_signal_windows", "")
    if len(si_signal_windows) == 0:
        si_windows_creator(signal_info, no_return=True)

    si_signal_windows = signal_info["si_signal_windows"]
    dt = signal_info["params"]["dt"]
    window_length = signal_info["window_length"]

    xf, si_fft_windows = fourier(si_signal_windows, window_length, dt)

    signal_info["xf"] = xf
    signal_info["si_fft_windows"] = si_fft_windows
    signal_info["si_fft_windows_fundamental"] = si_fft_windows[:, 1]

    if no_return:
        return

    number_of_windows = len(si_fft_windows)

    return np.tile(xf, (number_of_windows, 1)), si_fft_windows


def trip(signal_info: dict, no_return: bool = False) -> list:
    """Returns trip signal for signal

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain:
        - 'signal_windows'
        - 'window_length',
        - 'step'
        - 'dt'
        - 'signals'
        - 'signal_name'
    no_return : bool, optional
        Internal variable to use when accessing from other functions from module,
        by default False

    Returns
    -------
    list
        List containing trip values
    """

    fft_windows = signal_info.get("fft_windows", "")
    if len(fft_windows) == 0:
        STFT(signal_info, no_return=True)

    fft_windows = signal_info["fft_windows"]
    fundamental = signal_info["fft_windows_fundamental"]
    trip_windows = detection_iter(fft_windows, fundamental)

    signal_info["trip_windows"] = trip_windows

    if no_return:
        return

    return trip_windows


def si_trip(signal_info: dict, no_return: bool = False) -> list:
    """Returns trip signal for signal

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain:
        - 'si_signal_windows'
        - 'fft_windows_fundamental'
        - 'window_length'
        - 'step'
        - 'dt'
        - 'signals'
        - 'signal_name'
    no_return : bool, optional
        Internal variable to use when accessing from other functions from module,
        by default False

    Returns
    -------
    list
        List containing trip values of superimposed signal
    """
    si_fft_windows = signal_info.get("si_fft_windows", "")
    fundamental = signal_info.get("fft_windows_fundamental", "")
    if len(si_fft_windows) == 0:
        si_STFT(signal_info, no_return=True)
    if len(fundamental) == 0:
        STFT(signal_info, no_return=True)

    si_fft_windows = signal_info["si_fft_windows"]
    fundamental = signal_info["fft_windows_fundamental"]
    si_trip_windows = detection_iter(si_fft_windows, fundamental)

    signal_info["si_trip_windows"] = si_trip_windows

    if no_return:
        return

    return si_trip_windows


def img_trip(signal_info: dict) -> tuple[np.ndarray, np.ndarray]:
    """Returns time vector with trip signal

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain:
        - 'signal_windows'
        - 'trip windows
        - 'fft_windows_fundamental'
        - 'window_length'
        - 'step'
        - 'dt'
        - 'signals'
        - 'signal_name'

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        time vector, trip signal
    """
    trip_windows = signal_info.get("trip_windows", "")
    if len(trip_windows) == 0:
        trip(signal_info, no_return=True)

    trip_windows = signal_info["trip_windows"]
    t_windows = signal_info["t_windows"]
    t_window = np.insert(t_windows[:, -1], 0, 0)
    trip_windows = np.insert(trip_windows, 0, 0)
    return t_window, trip_windows


def img_si_trip(signal_info: dict) -> tuple[np.ndarray, np.ndarray]:
    """Returns time vector with trip signal

    Parameters
    ----------
    signal_info : dict
        Dictionary with signal parameters. Must contain:
        - 'si_signal_windows'
        - 'trip windows'
        - 't_windows'
        - 'fft_windows_fundamental'
        - 'window_length'
        - 'step'
        - 'dt'
        - 'signals'
        - 'signal_name'

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        time vector, trip signal for superimposed components
    """
    trip_windows = signal_info.get("si_trip_windows", "")
    if len(trip_windows) == 0:
        si_trip(signal_info, no_return=True)

    trip_windows = signal_info["si_trip_windows"]
    t_windows = signal_info["t_windows"]
    t_window = np.insert(t_windows[:, -1], 0, 0)
    trip_windows = np.insert(trip_windows, 0, 0)
    return t_window, trip_windows
