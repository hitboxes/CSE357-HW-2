import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
import csv
import sys

def schoolBinonmialHypTest(null_school, test_school, alpha, school_data):
    # null_state: the school representing the null hypothesis distribution
    # test_state: the school representing the observed count
    # alpha: significance level
    # school_data: the school name, case counts, and population
    null_school_name = school_data[0]
    null_case_counts = float(school_data[1])
    null_population = float(school_data[2])
    null_probability = null_case_counts/null_population
    test_school_name = school_data[3]
    test_case_counts = float(school_data[4])
    test_population = float(school_data[5])
    test_probability = test_case_counts/test_population
    null_dist = ss.binom(null_population, null_probability)
    test_sample = test_probability * null_population
    p = 1 - null_dist.cdf(test_sample)
    decision = test_school_name
    if(p < alpha):
        decision = decision + ", Decision: reject; p: " + str(p)
    else:
        decision = decision + ", Decision: Failed to reject; p: " + str(p)
    return p, decision

def comparingSBUtoNYSchool(null_school, null_school_Data, alpha, school_File):
    decision = ""
    with open(school_File, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if(row[5] != null_school):
                if(row[0] == "date"):
                    continue
                else:
                    combinedCollege = [null_school_Data[0], null_school_Data[1], null_school_Data[2], row[5], row[7], row[6]]
                    p, temp = schoolBinonmialHypTest(null_school_Data[0], row[5], alpha, combinedCollege)
                    newAlpha = alpha/float(combinedCollege[2])
                    familyWiseErrorRate = 1 - (1 - newAlpha)** float(combinedCollege[2])
                    difference = p - familyWiseErrorRate
                    temp1 = row[5] + ", diff: " + str(difference) + ", orig p: " + str(p) + ", corrected p: " + str(familyWiseErrorRate) + " \n"
                    decision += temp1
    return decision

def schoolNormalHypTest(null_school, test_school, alpha, school_data):
    # null_state: the school representing the null hypothesis distribution
    # test_state: the school representing the observed count
    # alpha: significance level
    # school_data: the school name, case counts, and population
    null_school_name = school_data[0]
    null_case_counts = float(school_data[1])
    null_population = int(float(school_data[2]))
    null_proportion = null_case_counts/null_population
    test_school_name = school_data[3]
    test_case_counts = float(school_data[4])
    test_population = int(float(school_data[5]))
    test_proportion = test_case_counts/test_population
    null_sample = ss.norm(null_proportion, 1).rvs(null_population)
    test_sample = ss.norm(test_proportion, 1).rvs(test_population)
    null_mean = null_sample.mean()
    test_mean = test_sample.mean()
    t = (null_mean - test_mean) / np.sqrt(np.concatenate([null_sample, test_sample]).var() * (1/len(null_sample)+1/len(test_sample)) )
    df = (len(null_sample)-1) + (len(test_sample)-1)
    p = ss.t(df).cdf(t)
    decision = test_school_name
    if(p < alpha):
        decision = decision + ", Decision: reject; p: " + str(p)
    else:
        decision = decision + ", Decision: Failed to reject; p: " + str(p)
    return p, decision

def schoolStandardErrorBootstrapped(school_File):
    decision = ""
    with open(school_File, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if(row[0] == "date"):
                continue
            else:
                school_name = row[5]
                case_counts = float(row[7])
                population = int(float(row[6]))
                proportion = case_counts/population
                sample = ss.norm(proportion, 1).rvs(population)
                n = len(sample)
                mean = sample.mean()
                std = sample.std(ddof = 1)
                stderr = std/np.sqrt(n)
                iters = 1000
                all_means = []
                for i in range(iters):
                    resample = np.random.choice(sample, size=n, replace=True)
                    resample_mean = resample.mean()
                    all_means.append(resample_mean)
                sorted_means = sorted(all_means)
                lower = sorted_means[int(0.025*iters)]
                upper = sorted_means[-int(0.025*iters)]
                decision += school_name + ", " + str(mean) + ", stderr CI: [" + str(mean - 1.96*stderr) + ", " + str(mean + 1.96*stderr) + ", bootstrapped CI: [" + str(lower) + ", " + str(upper) + "]\n" 
    return decision

if __name__ == "__main__":
    sys.stdout = open('a2_Choi_111944318_OUTPUT.txt', 'w')
    # College Covid Case Counts
    print("Part 1:")
    nullCollegeRow = []
    testCollegeRow = []
    with open('ny_colleges.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if(row[5] == "Stony Brook University"):
                nullCollegeRow = row
            if(row[5] == "New York University"):
                testCollegeRow = row
    combinedCollege = [nullCollegeRow[5], nullCollegeRow[7], nullCollegeRow[6], testCollegeRow[5], testCollegeRow[7], testCollegeRow[6]]
    p, decision = schoolBinonmialHypTest("Stony Brook University", "New York University", .05, combinedCollege)
    print(decision + "\n")
    # Comparing SBU to Many New York Schools
    print("Part 2:")
    result = comparingSBUtoNYSchool("Stony Brook University", ["Stony Brook University", "1126", "29607"], .05, 'ny_colleges.csv')
    print(result + "\n")
    # Modeling with the normal
    print("Part 3:")
    p, decision = schoolNormalHypTest("Stony Brook University", "New York University", .05, combinedCollege)
    print(decision + "\n")
    # Standard Error based CI and Bootstrapped CI
    print("Part 4 5:")
    decision = schoolStandardErrorBootstrapped('ny_colleges.csv')
    print(decision)
    
