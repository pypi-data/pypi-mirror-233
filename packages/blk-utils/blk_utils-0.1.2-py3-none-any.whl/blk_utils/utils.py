import pandas as pd
from decimal import Decimal, ROUND_HALF_DOWN
from pathlib import Path
from timeutils import Stopwatch


# =============================================================================
# general utils


def quantize_number(number, precision=2, rounding=ROUND_HALF_DOWN):
    """Quantizes a number to a given precision and returns a float.

    Args:
      number: The number to quantize.
      precision: The precision to quantize to.

    Returns:
      A float.
    """
    # Convert the input number to a Decimal object
    try:
        number_decimal = Decimal(str(number))
    except Exception as e:
        print(e)
    # Set the precision to the desired number of decimal places
    precision_decimal = Decimal("0." + "0" * precision)

    # Quantize the number using ROUND_HALF_DOWN rounding mode
    quantized_decimal = number_decimal.quantize(precision_decimal, rounding=rounding)

    # Convert the quantized Decimal back to a float
    quantized_float = float(quantized_decimal)

    return quantized_float


def timer(func):
    """
    this is a decorator that shows the execution time of the
    function passed in human readable format

    :param func: function
    :return: function output
    """

    def wrap_func(*args, **kwargs):
        sw = Stopwatch(start=True)
        result = func(*args, **kwargs)
        sw.stop()
        print(f"Function {func.__name__!r} executed in {sw.elapsed.human_str()}")
        return result

    return wrap_func


def create_output_path(filepath):
    """
    create output path

    :param filepath: str or path object
    :return: path
    """
    p = Path(filepath)
    if p.is_dir():
        print("directory exists...")
    else:
        p.mkdir(parents=True, exist_ok=False)
        print("creating directory...")
        print("directory created [complete]")
    return p


def get_relative_project_dir(project_repo_name=None, partial=True):
    """
    helper function to get top level project directory path using exact or
    partial name matching.

    :param project_repo_name: str
    :param partial: bool, default=True
    :return: path obj
    """
    current_working_directory = Path.cwd()
    cwd_parts = current_working_directory.parts
    if partial:
        while project_repo_name not in cwd_parts[-1]:
            current_working_directory = current_working_directory.parent
            cwd_parts = current_working_directory.parts
            if len(cwd_parts) == 1:
                if project_repo_name not in cwd_parts[0]:
                    raise ValueError(
                        f"{project_repo_name} not found in directory tree!"
                    )
    else:
        while cwd_parts[-1] != project_repo_name:
            current_working_directory = current_working_directory.parent
            cwd_parts = current_working_directory.parts
            if len(cwd_parts) == 1:
                if project_repo_name not in cwd_parts[0]:
                    raise ValueError(
                        f"{project_repo_name} not found in directory tree!"
                    )
    return current_working_directory


def cprint(df, nrows=None):
    """
    custom print function to output series or dataframe information

    :param df: pandas series or dataframe
    :param nrows: int
    :return: None
    """
    if not isinstance(df, (pd.DataFrame,)):
        try:
            df = df.to_frame()
        except:
            raise ValueError("object cannot be coerced to df")

    if not nrows:
        nrows = 5
    print("-" * 79)
    print("dataframe information")
    print("-" * 79)
    print(f"HEAD num rows: {nrows}")
    print(df.head(nrows))
    print("-" * 25)
    print(f"TAIL num rows: {nrows}")
    print(df.tail(nrows))
    print("-" * 50)
    print(df.info(verbose=True))
    print("-" * 79)
    print()
    return
