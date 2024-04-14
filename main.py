#!/bin/env python
import io
import os.path
import utils
import utils.read_file as rf

import streamlit as sl
import numpy as np
import pandas as pd

if __name__ == '__main__':
    sl.title("Caso 1: New York City Taxi")
    sl.markdown(rf.read(os.path.abspath(utils.INTRO_PATH)))
