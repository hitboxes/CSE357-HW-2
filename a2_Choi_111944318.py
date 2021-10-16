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
    null_school_name = school_data[0]
    null_case_counts = school_data[1]
    null_population = school_data[2]
    null_probability = null_case_counts/null_population
    test_school_name = school_data[3]
    test_case_counts = school_data[4]
    test_population = school_data[5]
    test_probability = test_case_counts/test_population
    null_dist = ss.binom(null_population, null_probability)
    test_sample = test_probability * null_population
    print(null_probability)
    print(test_probability)
    print(test_sample)
    p = 1 - null_dist.cdf(test_sample)
    decision = test_school_name
    if(p < alpha):
        decision = decision + ", Decision: reject; p: " + str(p)
    else:
        decision = decision + ", Decision: Failed to reject; p: " + str(p)
    return p, decision

def schoolNormalHypTest(null_school, test_school, alpha, school_data):
    # null_state: the school representing the null hypothesis distribution
    # test_state: the school representing the observed count
    # alpha: significance level
    # school_data: the school name, case counts, and population
    school_name = school_data[0]
    case_counts = school_data[1]
    population = school_data[2]
    return p, decision

    
if __name__ == "__main__":
    # College Covid Case Counts
    sampleSchoolData = ["Stony Brook University", 1126, 29607.0, "New York University", 2389, 51123.0]
    p, decision = schoolBinonmialHypTest("Stony Brook University", "New York University", .05, sampleSchoolData)
    print(p)
    print(decision)
    # Comparing SBU to Many New York Schools

    # Modeling with the normal

    # Standard Error based CI

    # Bootstrapped CI
