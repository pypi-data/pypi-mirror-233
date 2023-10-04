import logging
import os
from multiprocessing import cpu_count
import numba

logger = logging.getLogger(__name__)


def numba_setup() -> None:
    """This function sets defaults for environmental variables and numba
    parameters to achieve a balanced performance for most situations.
    Advanced users may want to customize these parameters.
    """

    try:
        number_of_cpus = len(os.sched_getaffinity(os.getpid()))
    except AttributeError:
        logger.info('Using multiprocessing.cpu_count() to determine the number of availible CPUs.')
        number_of_cpus = cpu_count()
    if number_of_cpus >= 8:
        number_of_threads = 8
    else:
        number_of_threads = number_of_cpus
    os.environ['OMP_NUM_THREADS'] = f'{number_of_threads}'
    os.environ['OPENBLAS_NUM_THREADS'] = f'{number_of_threads}'
    os.environ['MKL_NUM_THREADS'] = f'{number_of_threads}'
    logger.info(f'Setting the number of threads to {number_of_threads}')

    numba.config.NUMBA_DEFAULT_NUM_THREADS = number_of_threads
    numba.config.NUMBA_NUM_THREADS = number_of_threads
    numba.set_num_threads(number_of_threads)

    # numba.cuda has a very high output of `INFO`-level messages.
    numba_logger = logging.getLogger('numba')
    numba_logger.setLevel(logging.WARNING)
    logger.info('Setting numba log level to WARNING.')
