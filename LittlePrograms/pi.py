import mpmath

def calculate_pi(n):
    mpmath.mp.dps = n
    return str(mpmath.mp.pi)

def calculate_e(n):
    mpmath.mp.dps = n
    return str(mpmath.mp.e)

def calculate_phi(n):
    mpmath.mp.dps = n
    return str(mpmath.mp.phi)

def calculate_euler_mascheroni(n):
    mpmath.mp.dps = n
    return str(mpmath.mp.euler)

def calculate_aperys_constant(n):
    mpmath.mp.dps = n
    return str(mpmath.mp.apery)

def save_constant(n, filename, constant):
    value = constant(n)
    with open(filename, 'w') as f:
        f.write(value)

def main():
    digits = 1000000
    
    save_constant(digits, 'pi_1million.txt', calculate_pi)
    print(f'PI calculated to {digits} digits and saved in pi_1million.txt')
    
    save_constant(digits, 'e_1million.txt', calculate_e)
    print(f'Euler\'s number calculated to {digits} digits and saved in e_1million.txt')
    
    save_constant(digits, 'phi_1million.txt', calculate_phi)
    print(f'The golden ratio calculated to {digits} digits and saved in phi_1million.txt')
    
    save_constant(digits, 'euler_mascheroni_1million.txt', calculate_euler_mascheroni)
    print(f'Euler-Mascheroni constant calculated to {digits} digits and saved in euler_mascheroni_1million.txt')
    
    save_constant(digits, 'aperys_constant_1million.txt', calculate_aperys_constant)
    print(f'Apery\'s constant calculated to {digits} digits and saved in aperys_constant_1million.txt')

if __name__ == '__main__':
    main()
