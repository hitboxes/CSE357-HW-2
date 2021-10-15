from typing import no_type_check

import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
import csv

def schoolBinonmialHypTest(null_school, test_school, alpha, school_data):
    # null_state: the school representing the null hypothesis distribution
    # test_state: the school representing the observed count
    # alpha: significance level
    # school_data: the school name, case counts, and population

    return p, decision

def schoolNormalHypTest(null_school, test_school, alpha, school_data):
    # null_state: the school representing the null hypothesis distribution
    # test_state: the school representing the observed count
    # alpha: significance level
    # school_data: the school name, case counts, and population

    return p, decision

    
if __name__ == "__main__":
    # College Covid Case Counts
    schoolBinonmialHypTest("Stony Brook University", "New York University", .05, "ny_colleges.csv")
    # Comparing SBU to Many New York Schools

    # Modeling with the normal

    # Standard Error based CI
    
    # Bootstrapped CI
