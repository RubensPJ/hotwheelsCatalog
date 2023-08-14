import os, csv

def to_csv(list_to_write, filename):
  """Writes the contents of a list to a CSV file.
  Args:
    list_to_write: The list of data to write to the CSV file.
    filename: The name of the CSV file to create.
  """
  # Create the CSV file if it doesn't exist.
  if not os.path.exists(filename):
    with open(filename, "w") as f:
      f.write("")

  # Write the contents of the list to the CSV file.
    with open(filename,"w", newline="") as file:
        writer=csv.writer(file)
        for line in list_to_write:
            writer.writerow([line])