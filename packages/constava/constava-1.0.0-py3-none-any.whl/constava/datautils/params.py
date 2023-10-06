from dataclasses import dataclass, field
from typing import List


@dataclass
class ConstavaParameters:
    """The parameters that govern the function of Constava
    
    Parameters:
    -----------
        input_files : List[str]
            Input file(s) that contain the dihedral angles
        input_format : str
            Format of the input file: {"auto", "csv", "json"}
        input_degrees : bool
            Set `True` if input files are in degrees
        output_file : str
            The file to write the output to
        output_format : str
            Format of output file: {"csv", "json"}

        load_model : str
        train_model : str
        dump_model : str
        kde_bandwidth : float
        grid_points : int

        window : List[int]
        bootstrap : List[int]
        bootstrap_samples : int
        seed : int
        quick : bool
        precision : int
    """

    # Input/Output Options
    input_files : List[str] = None
    input_format : str = "auto"
    input_degrees : bool = False
    output_file : str = None
    output_format : str = "auto"

    # Conformational State Model Options
    load_model : str = None
    fit_model : str = None
    fit_degrees : bool = False
    dump_model : str = None
    kde_bandwidth : float = .13
    grid_points : int = 10_000

    # Miscellaneous Options
    window : List[int] = field(default_factory=lambda: [1].copy())
    bootstrap : List[int] = field(default_factory=lambda: [3,5].copy())
    bootstrap_samples : int = 500
    seed : int = None
    quick : bool = False
    precision : int = 4