from tkinter import filedialog
import tkinter as tk
import numpy as np
import pandas as pd
import csv


class CSV_pandas:
    """Class to load and extract signals from CSV into Pandas DataFrame and numpy arrays"""

    step = 8

    def __init__(self):
        """Constructor
        Once class instance is created, a window will be opened to
        search for CSV file.
        """
        self.csv_load()

    def csv_load(self):
        """Method to open a file exporer
        window to load CSV file from system"""
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.lift()

        self.path = filedialog.askopenfilename(
            multiple=False,
            title="cargue CSV",
            filetypes=(("archivos CSV", "*.csv"),),
        )
        print(self.path)

        self.nombre = self.path[self.path.rfind("/") + 1 :]
        self.nombre = self.nombre.replace(".csv", "")
        print(f"Se seleccionó {self.nombre}")
        root.destroy()
        self.extraer_csv()

    # métodos privados
    def extraer_csv(self):
        """Method to create pandas dataframe from CSV file"""

        # para encontrar el tipo de delimitador del archivo .csv
        with open(self.path, "r") as f:
            header = next(f)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(header).delimiter

        df = pd.read_csv(self.path, delimiter=delimiter)
        # Obtener un número par de muestras
        if len(df) % 2 != 0:
            df.drop(df.tail(1).index, inplace=True)

        self.df = self.__rename_columns(df)

    def __rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Private method, renames columns from Dataframe into more
        readable names. i.e. it creates a new name for each column by
        merging the three original named columns returned on CSV from
        ATP

        Parameters
        ----------
        df : pd.DataFrame
            Signals dataframe

        Returns
        -------
        pd.DataFrame
            Signals dataframe with renamed columns
        """
        # Extraer los labels de las filas 1 y 2
        pattern = r"^b'([\w ]*)'"
        node_from = df.iloc[0].str.replace(pattern, r"\1", regex=True).str.strip()
        node_to = df.iloc[1].str.replace(pattern, r"\1", regex=True).str.strip()
        df = df.drop(index=0)
        df = df.drop(index=1)

        df = self.__columns_replace(df)

        # Extraer si la medición es V, I o models; borrar si es Model
        labels_list = df.columns.values.tolist()

        # convertir los labels de cada nodo a una lista
        node_from_list = node_from.values.tolist()
        node_to_list = node_to.values.tolist()

        self.labels_list = self.__new_labels(node_from_list, node_to_list, labels_list)

        df.columns = self.labels_list
        self.labels_list = self.labels_list[1:]
        df.set_index("time")
        df = df.reset_index(drop=True)
        return df

    def __columns_replace(self, df: pd.DataFrame) -> pd.DataFrame:
        """Private method, standarizes columns names, making it easier to rename them
        according to signal type they represent.

        eg. for different CSV with time column named as: "Time", "TIME" or "time", all will
        be returned as "time"


        Parameters
        ----------
        df : pd.DataFrame
            Signals dataframe

        Returns
        -------
        pd.DataFrame
            Signals dataframe with standarized columns names
        """
        patterns = [
            (" ", ""),
            (r"^(V|I)[.\w-]*", r"\1"),
            (r"^(C)[.\w-]*", r"I"),
            (r"^(?![\s\S])", r"Model"),
            (r"^\d*\.*\d+", r"Model"),
            (r"MODELS\.*[\d]*", r"Model"),
            (r"Time", r"time"),
            (r"b'", r""),
        ]
        # INFORMACIÓN DE Regex en patterns
        # Quitar los espacios blancos
        # Columnas que comienzan con V-xxx, I-xxx [SEM] o Voltage [Manual]
        # Columnas que comienzan con Current [manual]
        # Columnas que estén vacías [Manual]
        # Columnas cuyos nombres sean números [SEM]
        # Columnas que tengan MODELS en mayúscula [Manual]
        # Hacer la T de time minúscula

        # Crear un diccionario e iterar sobre este para reemplazar el str.replace(x,y)
        for pattern in patterns:
            df.columns = df.columns.str.replace(pattern[0], pattern[1], regex=True)
        return df

    # función para devolver la lista de labels correcta
    def __new_labels(self, list1: list, list2: list, labels: list) -> list:
        """Private method, merges three labels rows from each column into one row

        Parameters
        ----------
        list1 : list
            FROM node list. ROW 2 in CSV
        list2 : list
            TO node list. ROW 3 in CSV
        labels : list
            Signal type list (current, voltage or MODEL). ROW 1 in CSV

        Returns
        -------
        list
            List with correct column labels
        """

        final_list = []
        for x, y, z in zip(list1, list2, labels):
            if z == "time":
                final_list.append(z)
            elif y == "":
                final_list.append(f"{z}: {x}")
            elif z == "Model":
                final_list.append(f"{x}: {y}")
            else:
                final_list.append(f"{z}: {x}-{y}")
        return final_list

    # Método públicos
    def load_data(self, relay_name: str) -> tuple[np.ndarray, np.ndarray, dict]:
        """Loads a signal from CSV given a relay_name (signal name) as input

        Parameters
        ----------
        relay_name : str
            Name of signal to load. Use .relay_list method to list all available signals

        Returns
        -------
        tuple[np.ndarray, np.ndarray, dict]
            signal array, time array, dictionary with signal parameters
        """
        try:
            params = {}
            signals = self.df[["time", relay_name]]
            signals = signals.to_numpy().astype(float)
            if len(signals[1]) % 2 == 0:
                n_samples = len(signals)
            else:
                n_samples = len(signals) - 1

            signals = signals[: n_samples : self.step]
            t = signals[:, 0]
            x = signals[:, 1]
            tf = max(t)
            ti = t[0]
            fs = int((len(t) - 1) / (tf - 0))
            dt = 1 / fs
            params["tf"] = tf
            params["ti"] = ti
            params["fs"] = fs
            params["dt"] = dt
            params["n_samples"] = n_samples
            return x, t, params

        except KeyError:
            print(
                f"There is no signal '{relay_name}\n please use .relay_list() method.'"
            )
            exit()

    def relay_list(
        self, currents: bool = True, voltages: bool = False, MODELS: bool = False
    ):
        """Method, prints a list of available signals. Only lists currents by default.
        To list voltages use voltages = True.
        To list MODELS use Models = True.

        Parameters
        ----------
        currents : bool, optional
            Whether or not to print available current signals,
            by default True
        voltages : bool, optional
            Wheter or not to print available voltage signals,
            by default False
        Models : bool, optional
            Wheter or not to print available MODELS signals,
            by default False
        """
        for i in self.labels_list:
            if ("V:" in i) and voltages:
                print(i)
            elif ("I:" in i) and currents:
                print(i)
            elif MODELS:
                print(i)


# Clase para hacer pruebas, luego borrar
# no muestra ventana de selección
class CSV_pandas_path(CSV_pandas):
    """Class to load CSV with path and not by opening
    a file explorer window

    Parameters
    ----------
    CSV_pandas : parent class
        Parent class from which CSV_pandas_path inherits from
    """

    def __init__(self, filename: str):
        """Constructor

        Parameters
        ----------
        filename : str
            Path of CSV
        """

        self.csv_load(filename)

    def csv_load(self, filename: str):
        """Function to load CSV

        Parameters
        ----------
        filename : str
            Path of CSV
        """
        self.path = filename
        # self.path = "C:\\Users\\aherrada\\OneDrive - Universidad del Norte\\Uninorte\\DetectionDataBase\\septDataBaseCSV\\Caps\\NoFault02_B112.csv"
        self.extraer_csv()


def synthetic_signal(t, harmonics=[60], fundamental=60):
    """
    Function for the creation of a synthetic signal



    Returns
    -------
    numpy.array
        (3, n) three phase matrix
    """
    wt = 2 * np.pi * fundamental * t
    ang_A = float(0) * np.pi / 180
    ang_B = float(240) * np.pi / 180
    ang_C = float(120) * np.pi / 180

    A, B, C = 0, 0, 0

    for s in harmonics:
        n = s / fundamental
        A += 100 * np.sin(n * (wt + ang_A))
        B += 100 * np.sin(n * (wt + ang_B))
        C += 100 * np.sin(n * (wt + ang_C))

    return np.array((A, B, C))


class SyntheticSignal:
    """Creates a synthetic signal"""

    def __init__(
        self, samples_cycle=64, cycles=4, frequency_components=[60, 120]
    ) -> None:
        """Constructor of the signal

        Parameters
        ----------

        samples_cycle: int
            Number of samples in a period of the signal.

        cycles: int
            Number of cycles of the signal.

        frequency_components: list
            List containing frequencies (int) in the signal.
        """
        self.dt = 1 / (60 * samples_cycle)
        self.t = np.arange(0, cycles / 60, self.dt)
        self.tf = self.t[-1]
        self.fs = int(1 / self.dt)
        wt = 2 * np.pi * 60 * self.t
