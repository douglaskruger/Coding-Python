def dec_to_bases(n, num_digits):
  """Converts a decimal integer to binary, octal, and hexadecimal strings.

  Args:
      n: The decimal integer to convert.
      num_digits: The desired number of digits for each representation.

  Returns:
      A tuple containing the binary, octal, and hexadecimal representations.
  """
  binary = format(n, '0' + str(num_digits) + 'b')
  octal = format(n, '0' + str(num_digits) + 'o')
  hexadecimal = format(n, '0' + str(num_digits) + 'x')
  return binary, octal, hexadecimal

while True:
  try:
    number = int(input("Enter a decimal integer to convert: "))
    num_digits = int(input("Enter the desired number of digits: "))
    break
  except ValueError:
    print("Invalid input. Please enter whole numbers.")

binary, octal, hexadecimal = dec_to_bases(number, num_digits)

print(f"Binary:    {binary}")
print(f"Octal:     {octal}")
print(f"Hexadecimal: {hexadecimal}")
