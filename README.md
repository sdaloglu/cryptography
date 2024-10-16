# Project: Cryptography

**Author**: Sabahattin Mert Daloglu  
**Course**: PHZ 3152: Computational Astrophysics  

## Project Description

This project implements a cryptographic decryption algorithm based on a Markov Chain model of letter transitions. The program processes text data to determine the likelihood of letter sequences in English and uses simulated annealing to optimize a key for decrypting encoded text. The key approach centers on finding an optimal solution to maximize the total probability of the decrypted text matching English language structures.

## Code Architecture

### 1. Input Data Management

The text for *War and Peace* is loaded and analyzed to determine the frequency of letter transitions in the English language. A Markov Chain transition matrix (M) is built to represent the likelihood that one letter follows another. The text data undergoes preprocessing, including conversion to lowercase and filtering out non-alphabet characters.

### 2. Generating a Key

The function `generate_key` creates a random mapping of the alphabet, which serves as the initial decryption key. This key is refined through optimization to maximize the decryption accuracy.

### 3. Calculating Probabilities (`P_calculation`)

The function `P_calculation` computes the total probability, P, of the decrypted phrase matching English letter transition probabilities from the Markov matrix. This serves as the optimization target during simulated annealing.

### 4. Simulated Annealing and Key Optimization (`optimal_swap`)

The `optimal_swap` function uses simulated annealing to iteratively improve the decryption key by randomly swapping two letters in the key and accepting or rejecting swaps based on the Metropolis probability.

### 5. Accuracy Check (`accuracy_check`)

This function compares the decrypted phrase with the correct answer and calculates the accuracy of the decryption based on the percentage of correctly placed letters.

## Parameter Testing and Results

### 1. Simulated Annealing with Varying Time Constants (𝝉)

The performance of the algorithm was evaluated by varying the annealing time constant, 𝝉, which controls the rate of cooling. It was found that slower cooling rates (higher 𝝉 values) resulted in better accuracy, with a maximum accuracy of 25.58%.

### 2. Accepting Only Positive Proposals

When only positive swaps were accepted, the algorithm consistently got stuck in local maxima, yielding an accuracy rate of 9.3%. This result highlights the importance of accepting negative swaps to escape local optima.

### 3. Varying the Probability of Accepting Negative Proposals

By adjusting the probability of accepting negative swaps, it was determined that a balance between rejecting and accepting negative swaps is crucial. Extreme probabilities (either too high or too low) reduced the decryption accuracy.

### 4. Varying Probability Calculation Methods

Different methods of calculating the total probability (addition, multiplication, and logarithmic addition) were tested. The addition method provided the highest accuracy (25.58%), while the multiplication method resulted in 0% accuracy due to the small magnitude of individual probabilities.

## Conclusion

This project demonstrates the use of simulated annealing in cryptography to optimize a decryption key. Through testing various parameters, an optimal solution was found that maximizes the decryption accuracy based on a transition matrix derived from the English language.