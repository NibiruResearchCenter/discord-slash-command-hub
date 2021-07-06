import datetime
import logging

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('function warm up')
