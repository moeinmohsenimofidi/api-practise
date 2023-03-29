import ijson


input_file = "Custom_location_46_4423_11_2525_63fc88e098a8260007094a1e.json"
output_file = 'transformed_file.json'

def json_transform(item):

     pass
# Open the input and output files
with open(input_file, 'r') as input_f, open(output_file, 'w') as output_f:
 # Create an ijson parser for the input file
 parser = ijson.parse(input_f)

 # Iterate over each item in the JSON file and write the transformed data to the output file
 output_f.write('[')  # start the JSON array
for prefix, event, value in parser:
   if prefix == 'item':
    # Apply the transformation function to the item
    new_item = json_transform(value)

    # Write the transformed item to the output file
    if parser.get_total_bytes_read() > 2:
     # Add a comma to separate items if this is not the first item in the array
     output_f.write(',')
    json.dump(new_item, output_f)
output_f.write(']')  # end the JSON array



