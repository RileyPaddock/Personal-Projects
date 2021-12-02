def is_prime(n):
  #check all numbers up to our numbers square root for factors
  for i in range(2,round(n**(0.5))):
    if n%i == 0:
      return False
  else:
    return True

def prime_factorization(n):
  prime_fact = []
  #if our number is prime, it is its own prime factorization
  if is_prime(n):
    
    return [n]
  else:
    #if our number is not prime, find the first factor, add it to the factorization, and factor it out of our number and continue.
    for i in range(2,round(n**(0.5))):
      if n%i == 0:
        for elem in prime_factorization(i):
          prime_fact.append(elem)
        for elem in prime_factorization(int(n/i)):
          prime_fact.append(elem)
        break
  return prime_fact


print([prime_factorization(675),prime_factorization(330)])