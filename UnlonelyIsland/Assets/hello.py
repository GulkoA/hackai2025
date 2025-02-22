
file_name = "output.txt"
text_to_write = "Hello, this is a sample text written to the file."


with open(file_name, 'w') as file:
  file.write(text_to_write)

print(f"Text has been written to {file_name}")

def my_method():
  return "helo"