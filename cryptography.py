##### Project 1: Cryptography
#Code author: Sabahattin Mert Daloglu
#PHZ3152

import numpy as np
import pandas as pd
import random
import string
from math import exp, factorial
import math 
import matplotlib.pyplot as plt 



data = np.load("war_peace.npz")    #Loading "War and Peace" data
text = data['text']    #Choosing the value of key 'text' key
text = str(text.item())    #Selecting the scalar element of the text array and converting to string
text = text.lower()    #Convert all letters to lower case
char_list = list(text)    #Convert each character to an element of an array
transitions = char_list    #Renaming this list to transitions which corresponds to the sequence of states for the transition matrix


def rank(letter):
    
    """
    Defining a rank system in uncode code relative to letterr "a"
    Inputs:
     - letter: a single letter
     
    Outputs:
     - (Unicode code of the input letter) - (Unicode code of "a")
    
    """

    return ord(letter) - ord('a')


T = [rank(element) for element in transitions]    #Filling the array with the relative uncicode code of each letter in transitions

T_new = []    #New list of characters with special characters or numbers removed (only alphabet letters)
for i in T:
    if i<26 and i>=0:    #Relative unicode of alphabet letters are between 0-25
        T_new.append(i)

        
M = [[0]*26 for _ in range(26)]    #create zero matrix of size 26x26

for (i,j) in zip(T_new,T_new[1:]):
    M[i][j] += 1    #Filling this matrix with the liklihood that one letter is followed by another sequentially
    
#Normalize each row to find the probabilities
for row in M:
    n = sum(row)
    row[:] = [element/sum(row) for element in row]
    #The case which n = 0 is ignored 
        
        
df = pd.DataFrame(M)    #Converting to pandas data frame, easier to visualize




listoflet = list(string.ascii_lowercase)    #List of alphabet letters in lower case
phrase = list("zywdynfzmbboanxjrxiaimbbxpgaxwiyrymbpgoyxal")

def generate_key(list_of_letters):
    """
    This function generates a dictionary which maps the letters in the alphabet to a sequence of randomly shuffled letters.
    
    Input:
     - list_of_letters: list of alphabet letters
    Output:
     - key: the dictionary representing the mapping
    """
    x = list_of_letters
    random.seed(1)
    random.shuffle(x)
    key = dict(zip(string.ascii_lowercase,x))
    #reverse_key = dict(zip(string.ascii_lowercase,x))
    return key


key = generate_key(listoflet)    #Generating the key

    
def P_calculation(key):
    
    """
    This function calculates the value P from for the letters of the jumbled phrase from the probability matrix M
    
    Input:
     - key: python dictionary to generate solution phrase
    Output:
     - P: total probability of the liklihood that one letter is followed by another sequentially
    """
    
    mapped_into = []
    for letter in phrase:
        mapped_into.append(key[letter])    #Decrypted phrase by using the 'key' dictionary
    P = 0
    for i in range(len(mapped_into)-1):
        P += (M[rank(mapped_into[i])][rank(mapped_into[i+1])])

    return P


def optimal_swap(key,tau):
    
    """
    This function swaps the indices of the input key for some number of times determined by the cooling time of the simulated annealing
    
    Input:
     - key: python dictionary to generate solution phrase
     - tau: time constant of the simulated annealing
    Output:
     - new_key: new solution mapping of type dictionary
     - P_new: new total probability of the liklihood that one letter is followed by another sequentially
     - N: Number of successfull swaps
    """
    
    #Using simulated annealing with the temperature variable to find the global minimum instead of local minimum.
    successful_itiration = []
    N = 0
    t = 0
    T_max = 10.0
    T_min = 1e-4
    T = T_max
    while T > T_min:
        t += 1
        T = T_max*exp(-t/tau)
        P = P_calculation(key)
        key1,key2 = random.sample(list(key),2)    #Randomly selecting two indices to swap
        key[key1], key[key2] = key[key2], key[key1]    #Swapping the indices
        P_new = P_calculation(key)
        N += 1
        deltaP = -(P_new - P)    #negative sign is because we are interested in global maximum instead of minium. Energy states are reversed
        
        if deltaP<0:
            #If the new calculated P is higher than the previous P accept the swap
            continue
            
        elif random.random() >= exp(-deltaP/T):
            #If the new calculated P is lower than the previous P reject the swap with the Metropolis probability
            key[key2], key[key1] = key[key1], key[key2]
            N -= 1
    new_key = key
    return new_key,P_new, N

new_key,P_new,N = optimal_swap(key,1e4)

#print(N)


def accuracy_check(new_key,phrase):
    
    """
    This function calculates the fraction of correct letters at the right position for the decrypted phrase
    
    Input:
     - new_key: new solution mapping of type dictionary
     - phrase: list of jumbled letters given
    """
    
    answer = []
    for letter in phrase:
        answer.append(new_key[letter])
    print("The decrypted answer is: " + ''.join(answer))
    
    real_answer = "JACKANDJILLWENTUPTHEHILLTOFETCHAPAILOFWATER"
    real_answer = real_answer.lower()
    real_answer_list = list(real_answer)


    true_count = 0
    for i in range(len(real_answer_list)):
        if real_answer_list[i] == answer[i]:
            true_count += 1

    print("Fraction of correct letters at the right position is: " + str(true_count/len(real_answer_list)*100) + "%")
    print("Although this result is not very impresive, comparing this to the probability of randomly picking a letter for each position: ")
    
    distinct_letters = np.unique(real_answer_list)
    print(str((factorial(26-len(distinct_letters))/factorial(26))*100)+"%")
    print("Hence, the calculated percentage of the correct letters in the solution phrase is much higher than random draw.")
    print("The rate at which this fraction converges is around 25.58% with the use of following:")
    print("-> Time constant (tau) for the annealing is 1e4, higher values yield the same rate. ")
    print("-> Accepting negative proposals with the Metropolis probability that is random.random()<exp(-deltaP/T).")
    print("-> Total P calculation by taking the sum of the probabilities since these indidivual probabilities are too small, multiplying them yields zero whereas adding the log yields negative infinity.")


accuracy_check(new_key,phrase)



#The following sections are for the analysis of the project, same functions are used to generate diagnostic plots

########################### Testing the effect of different annealing rates on the accuracy rate ###########################

def optimal_swap_analysis(key,tau):
    
    #Using simulated annealing with the temperature variable to find the global minimum instead of local minimum.
    N = 0
    t = 0
    T_max = 100.0
    T_min = 1e-3
    T = T_max
    while T > T_min:
        t += 1
        T = T_max*exp(-t/tau)
        P = P_calculation(key)
        random.seed(t)
        key1,key2 = random.sample(list(key),2)
        key[key1], key[key2] = key[key2], key[key1]
        P_new = P_calculation(key)
        N += 1
        deltaP = -(P_new - P)    #negative sign is because we are interested in global maximum instead of minium. Energy states are reversed
        
        if deltaP<0:
            #If the new calculated P is higher than the previous P accept the swap
            continue
        
        elif random.random() >= exp(-deltaP/T):
            #If the new calculated P is lower than the previous P reject the swap with the Metropolis probability
            key[key2], key[key1] = key[key1], key[key2]
            N -= 1
        
    new_key = key
    return new_key,N

def accuracy_check_analysis(new_key,phrase):
    answer = []
    for letter in phrase:
        answer.append(new_key[letter])
        
    real_answer = "JACKANDJILLWENTUPTHEHILLTOFETCHAPAILOFWATER"
    real_answer = real_answer.lower()
    real_answer_list = list(real_answer)
    
    true_count = 0
    
    for i in range(len(real_answer_list)):
        if real_answer_list[i] == answer[i]:
            true_count += 1
            
    rate  = true_count/len(real_answer_list)*100
    
    return rate

def test_tau():
    
    """
    This function plots the accuracy rate as a function of tau(time constant of the cooling)
    
    """
    
    x_axis = []
    y_axis = []

    for i in np.arange(1,4.4,0.2):    #Itirating over the power of tau values
        random.seed(2)
        x = list(string.ascii_lowercase)
        random.shuffle(x)
        key = dict(zip(string.ascii_lowercase,x))
        new_key,N = optimal_swap_analysis(key,10**i)    #Inputing different tau values 
        rate = accuracy_check_analysis(new_key,phrase)
        print(i,rate,N)
        x_axis.append(i)
        y_axis.append(rate)
    plt.plot(x_axis,y_axis)
    plt.xlabel("log(tau)")
    plt.ylabel("Fraction of correct letters[%]")
    plt.title("Time constant vs Accuracy Rate")
    plt.savefig("annealing.png")
    plt.show()
    
#test_tau()    Uncomment this line to generate the diagnostic plot


####################### Testing the effect of accepting only positive proposals on the accuracy rate ########################

def optimal_swap_analysis1(key,tau):
    
    #Using simulated annealing with the temperature variable to find the global minimum instead of local minimum.
    N = 0
    t = 0
    T_max = 100.0
    T_min = 1e-3
    T = T_max
    while T > T_min:
        t += 1
        T = T_max*exp(-t/tau)
        P = P_calculation(key)
        random.seed(t)
        key1,key2 = random.sample(list(key),2)
        key[key1], key[key2] = key[key2], key[key1]
        P_new = P_calculation(key)
        N += 1
        deltaP = -(P_new - P)    #negative sign is because we are interested in global maximum instead of minium. Energy states are reversed
        
        if deltaP<0:
            #If the new calculated P is higher than the previous P accept the swap
            continue
        
        else:
            #If the new calculated P is lower than the previous P reject the swap
            key[key2], key[key1] = key[key1], key[key2]
            N -= 1
        
    new_key = key
    return new_key,N

def accuracy_check_analysis1(new_key,phrase):
    answer = []
    for letter in phrase:
        answer.append(new_key[letter])
        
    real_answer = "JACKANDJILLWENTUPTHEHILLTOFETCHAPAILOFWATER"
    real_answer = real_answer.lower()
    real_answer_list = list(real_answer)
    
    true_count = 0
    
    for i in range(len(real_answer_list)):
        if real_answer_list[i] == answer[i]:
            true_count += 1
            
    rate  = true_count/len(real_answer_list)*100
    
    return rate

def test_positive_proposal():
    
    """
    This function plots the accuracy rate as a function of tau(time constant of the cooling) for only positive proposals
    
    """
    
    x_axis = []
    y_axis = []

    for i in np.arange(1,4.1,0.2):
        random.seed(0)
        x = list(string.ascii_lowercase)
        random.shuffle(x)
        key = dict(zip(string.ascii_lowercase,x))
        new_key,N = optimal_swap_analysis1(key,10**i)
        rate = accuracy_check_analysis1(new_key,phrase)
        print(i,rate,N)
        x_axis.append(i)
        y_axis.append(rate)
    plt.plot(x_axis,y_axis)
    plt.xlabel("log(tau)")
    plt.ylabel("Fraction of correct letters[%]")
    plt.title("Time constant vs Accuracy Rate for only positive proposals")
    plt.savefig("positive_proposals_only.png")
    plt.show()
#test_positive_proposal()    Uncomment this line to generate the diagnostic plot

 
########### Testing the effect of the probability by which negative proposals are accepted on the accuracy rate  ############

def optimal_swap_analysis(key,tau,i):
    
    #Using simulated annealing with the temperature variable to find the global minimum instead of local minimum.
    N = 0
    t = 0
    T_max = 100.0
    T_min = 1e-3
    T = T_max
    while T > T_min:
        t += 1
        T = T_max*exp(-t/tau)
        P = P_calculation(key)
        random.seed(t)
        key1,key2 = random.sample(list(key),2)
        key[key1], key[key2] = key[key2], key[key1]
        P_new = P_calculation(key)
        N += 1
        deltaP = -(P_new - P)    #negative sign is because we are interested in global maximum instead of minium. Energy states are reversed
        
        if deltaP<0:
            #If the new calculated P is higher than the previous P accept the swap
            continue
        

        elif random.random() >= exp(-(10**i)*deltaP/T):

            #If the new calculated P is lower than the previous P reject the swap with the Metropolis probability
            key[key2], key[key1] = key[key1], key[key2]
            N -= 1
        
    new_key = key
    return new_key

def accuracy_check_analysis(new_key,phrase):
    answer = []
    for letter in phrase:
        answer.append(new_key[letter])
        
    real_answer = "JACKANDJILLWENTUPTHEHILLTOFETCHAPAILOFWATER"
    real_answer = real_answer.lower()
    real_answer_list = list(real_answer)
    
    true_count = 0
    
    for i in range(len(real_answer_list)):
        if real_answer_list[i] == answer[i]:
            true_count += 1
            
    rate  = true_count/len(real_answer_list)*100
    
    return rate

def test_negative_proposal():
    
    """
    This function plots the accuracy rate as a function of the constant that will be used to change the the probability by which negative proposals are accepted
    
    """
    
    x_axis = []
    y_axis = []

    for i in np.arange(-3,3, dtype=float):    #Itirating over the power of constant that will be used to change the the probability by which negative proposals are accepted
        random.seed(2)
        x = list(string.ascii_lowercase)
        random.shuffle(x)
        key = dict(zip(string.ascii_lowercase,x))
        new_key = optimal_swap_analysis(key,1e4,i)
        rate = accuracy_check_analysis(new_key,phrase)
        print(i,rate)
        x_axis.append(i)
        y_axis.append(rate)
    plt.plot(x_axis,y_axis)
    plt.xlabel("log(i)")
    plt.ylabel("Fraction of correct letters[%]")
    plt.title("Time constant vs Accuracy Rate")
    plt.savefig("negative_proposals_rate.png")
    plt.show()
#test_negative_proposal()    Uncomment this line to generate the diagnostic plot


###### Testing the effect of different ways of calculating probability for the solution key on the accuracy rate ####

def P_calculation_analysis(key,method):
    
    mapped_into = []
    for letter in phrase:
        mapped_into.append(key[letter])
    
    if method == "adding":
        P = 0    #Initial value
        for i in range(len(mapped_into)-1):
            P += (M[rank(mapped_into[i])][rank(mapped_into[i+1])])
    
    elif method == "multiplying":
        P = 1    #Initial value
        for i in range(len(mapped_into)-1):
            P *= (M[rank(mapped_into[i])][rank(mapped_into[i+1])])
        
    elif method == "adding log":
        P = 0    #Initial value
        for i in range(len(mapped_into)-1):
            P += np.log(M[rank(mapped_into[i])][rank(mapped_into[i+1])])
    else:
        print("invalid method")
        
    return P

def optimal_swap_analysis(key,tau,method):
    
    #Using simulated annealing with the temperature variable to find the global minimum instead of local minimum.
    N = 0
    t = 0
    T_max = 10.0
    T_min = 1e-3
    T = T_max
    while T > T_min:
        t += 1
        T = T_max*exp(-t/tau)
        P = P_calculation_analysis(key,method)
        random.seed(t)
        key1,key2 = random.sample(list(key),2)
        key[key1], key[key2] = key[key2], key[key1]
        P_new = P_calculation_analysis(key,method)
        N += 1
        deltaP = -(P_new - P)    #negative sign is because we are interested in global maximum instead of minium. Energy states are reversed
        
        if deltaP<0:
            #If the new calculated P is higher than the previous P accept the swap
            continue
        
        elif random.random() >= exp(-deltaP/T):

            #If the new calculated P is lower than the previous P reject the swap with the Metropolis probability
            key[key2], key[key1] = key[key1], key[key2]
            N -= 1
        
    new_key = key
    return new_key

def accuracy_check_analysis(new_key,phrase):
    answer = []
    for letter in phrase:
        answer.append(new_key[letter])
        
    real_answer = "JACKANDJILLWENTUPTHEHILLTOFETCHAPAILOFWATER"
    real_answer = real_answer.lower()
    real_answer_list = list(real_answer)
    
    true_count = 0
    
    for i in range(len(real_answer_list)):
        if real_answer_list[i] == answer[i]:
            true_count += 1
            
    rate  = true_count/len(real_answer_list)*100
    
    return rate

def test_method():
    
    """
    This function plots the accuracy rate as a function of the method used to calculate the total probability for the solution key
    
    """
   
    x_axis = []
    y_axis = []
    methods = ["multiplying","adding log","adding"]
    for i in methods:
        random.seed(2)
        x = list(string.ascii_lowercase)
        random.shuffle(x)
        key = dict(zip(string.ascii_lowercase,x))
        new_key = optimal_swap_analysis(key,1e4,i)
        rate = accuracy_check_analysis(new_key,phrase)
        print(i,rate)
        x_axis.append(i)
        y_axis.append(rate)
    plt.plot(x_axis,y_axis)
    plt.xlabel("Method of calculating the total probability for the solution key")
    plt.ylabel("Fraction of correct letters[%]")
    plt.title("P calculation method vs Accuracy Rate")
    plt.savefig("P_calculation.png")
    plt.show()
#test_method()     Uncomment this line to generate the diagnostic plot

