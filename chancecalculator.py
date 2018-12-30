#!/usr/bin/env python3.7
from scipy.stats import binom
from seaborn import heatmap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Calculate the probability to achieve a given number of successes for dice rolls.

# Calculate the chance of a success
# Number of dice is influenced by the first event.
# Reroll of dice changes probability of success.o

def calculate_chance(
        to_hit_value, 
        to_wound_value, 
        max_number_of_dice=20,
        reroll_to_hit=False, 
        reroll_to_wound=False):

    ''' Calculates the chance of a success for two consecutive w6 rolls including
        rerolls. Suitable for warhammer age of sigmar.'''

    #TODO: Include Save and Damage Dice Rolls

    choices = ['ones', 'all']

    # Roll of 2+ means a value of 2 and higher, therefore a 5/6 chance
    p0 = (7.-to_hit_value)/float(6.) 

    if reroll_to_hit is False:
        p = p0
    elif reroll_to_hit is 'ones':
        p = p0 + (1/6 * p0) # p(1+1/6) 
    elif reroll_to_hit is 'all':
        p = p0 + (3/6 * p0)


    q0 = (7.-to_wound_value)/float(6.)

    if reroll_to_wound is False:
        q = q0
    if reroll_to_wound is 'ones':
        q = q0 + (1/6 * q0) # p(1+1/6) 
    if reroll_to_wound is 'all':
        q = q0 + (3/6 * q0)

    probability_of_success = p * q
    k = np.arange(0,21) # Number of successes


    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    matrix = []
    for n in np.arange(1, max_number_of_dice+1):
        # f(k) = n over k * p**k * (1-p)**(n-k)
        binomial = binom.pmf(k, n, probability_of_success)
        matrix.append(binomial)


    df = pd.DataFrame(data=matrix)

    colnames = {0:'No successes'}
    df.rename(columns=colnames, inplace=True)
    df.index.name = 'Dice'

    heatmap(df.iloc[1:,1:], vmin=0, vmax=1, square=True, cmap='Blues')
    


    if reroll_to_hit is False: 
        rrth = 'no_reroll' 
    else:
        rrth = reroll_to_hit

    if reroll_to_wound is False: 
        rrtw = 'no_reroll' 
    else:
        rrtw = reroll_to_wound

    plt.savefig('{}-{}-{}-{}.png'.format(int(to_hit_value), int(to_wound_value), rrth, rrtw))
    #plt.show()
    plt.clf()

    return(df.round(3)*100)

#if __name__ == '__main__()':
calculate_chance(to_hit_value=3, to_wound_value=3)
calculate_chance(to_hit_value=3, to_wound_value=3, reroll_to_hit='ones')
calculate_chance(to_hit_value=3, to_wound_value=3, reroll_to_hit='ones', reroll_to_wound='ones')
calculate_chance(to_hit_value=3, to_wound_value=4)
calculate_chance(to_hit_value=3, to_wound_value=4, reroll_to_hit='ones')
calculate_chance(to_hit_value=4, to_wound_value=4)
calculate_chance(to_hit_value=4, to_wound_value=4, reroll_to_hit='ones')
