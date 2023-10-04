import numpy as np

from ecallisto_ng.combine_antennas.utils import (
    align_spectrograms_middle,
    align_to_reference,
    find_best_reference,
    make_frequencies_match_spectograms,
    make_times_match_spectograms,
    shift_spectrograms,
)
from ecallisto_ng.data_processing.utils import (
    apply_median_filter,
    elimwrongchannels,
    mean_filter,
    subtract_constant_background,
)
from ecallisto_ng.plotting.plotting import fill_missing_timesteps_with_nan


def process_data(datas, min_n_frequencies=30, freq_range=[20, 80], max_freq=150, filter_type=None):
    """
    Process a list of DataFrames based on a series of filtering and transformation steps.

    Parameters
    ----------
    datas : list of pd.DataFrame
        List of DataFrames to be processed.
    min_n_frequencies : int, optional
        Minimum number of frequencies required for processing. Default is 100.
    freq_range : list of float, optional
        Frequency range to keep. Default is [20, 80].
    max_freq : float, optional.
        Maximum frequency an instrument should measure. Default is 150.
    filter_type : str, optional
        Type of filter to apply ('median' or 'mean'). Default is None.

    Returns
    -------
    list of pd.DataFrame
        List of processed DataFrames.
    """
    data_processed = []
    for data in datas:
        try:
            if max([float(col) for col in data.columns]) > max_freq:
                continue

            # Cut away columns based on frequency limits
            columns = np.array([float(col) for col in data.columns])
            data = data.loc[:, (columns > freq_range[0]) & (columns < freq_range[1])]

            # Check column conditions
            if len(data.columns) < min_n_frequencies:
                continue

            # Data transformations
            data = fill_missing_timesteps_with_nan(data)
            data = elimwrongchannels(data)
            data = subtract_constant_background(data, 100)

            # Apply filter if specified
            if filter_type == 'median':
                data = apply_median_filter(data)
            if filter_type == 'mean':
                data = mean_filter(data)

            # Cap min value to 0 and scale to [0, 1]
            data[data < 0] = 0
            data = (data - data.min()) / (data.max() - data.min())
            data.fillna(0, inplace=True)

            # Append processed data
            data_processed.append(data)
        except Exception as e:
            print("Error processing data")
            print(e)
    return data_processed
