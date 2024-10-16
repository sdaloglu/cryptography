# Project: Cryptography

**Author**: Sabahattin Mert Daloglu  
**Course**: PHZ 3152: Computational Astrophysics  

## Project Description

This project focuses on decrypting encoded text using a statistical approach, specifically a Markov Chain model to simulate letter transitions in English. The goal is to optimize a decryption key through simulated annealing to maximize the likelihood that the decrypted text matches common English letter sequences.

## Code Architecture

### 1. **Rank Function (`rank`)**

The `rank` function calculates the Unicode value of characters relative to the Unicode value of lowercase 'a'. This is used to map letters of the alphabet to numeric indices for building the transition matrix.

### 2. **Generating a Key (`generate_key`)**

The `generate_key` function maps the alphabet to another randomly shuffled sequence of letters. This randomized key serves as the initial guess for decrypting the encoded text. The function returns a dictionary containing this mapping.

### 3. **Calculating Probabilities (`P_calculation`)**

The `P_calculation` function evaluates how well a given decrypted phrase matches the English language structure by calculating the total probability based on the Markov transition matrix. It sums the transition probabilities for each pair of consecutive letters in the decrypted phrase.

### 4. **Simulated Annealing and Key Optimization (`optimal_swap`)**

The `optimal_swap` function implements a simulated annealing algorithm to optimize the decryption key. Two random letters in the key are swapped, and the new key is accepted or rejected based on the calculated probability of improvement. The function uses a temperature variable to control the acceptance of less optimal swaps (Metropolis criterion).

### 5. **Accuracy Check (`accuracy_check`)**

The `accuracy_check` function compares the decrypted phrase to the original encoded phrase and calculates the fraction of letters that have been correctly mapped. This is used to evaluate the performance of the decryption algorithm.

### 6. **Analysis Functions**

Several functions such as `optimal_swap_analysis`, `accuracy_check_analysis`, and `test_tau` are used to test the effect of different parameters on the accuracy of the decryption:
- **`test_tau`**: Tests the effect of varying the time constant (𝝉) on the cooling schedule in the simulated annealing process.
- **`test_positive_proposal`**: Analyzes the effect of only accepting positive swaps during optimization.
- **`test_negative_proposal`**: Examines the probability of accepting negative proposals and its effect on optimization.

## Dependencies

- Python 3.x
- NumPy
- Pandas
- Matplotlib
- SciPy

These libraries are essential for matrix operations, statistical analysis, and visualization.

## How to Run the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cryptography.git
   ```

2. **Navigate to the project folder:**
    ```bash
    cd cryptography
   ```

3. **Install required dependencies:**
    ```bash
   pip install -r requirements.txt
   ```

4. **Run the cryptography code:**
    ```bash
   python cryptography.py
   ```