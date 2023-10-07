# The following code will search 'MM/DD/YYYY' (e.g. 11/30/2016 or NOV/30/2016, etc ),
# and replace with 'MM-DD-YYYY' in multi-line mode.
import re
output_file = open("output.txt", "w")
with open ('file.txt', 'r' ) as f:
    content = f.read()
    content_new = re.sub(r'.* "location": "(http://.*)"\}, .*\n', r'\1\n', content)
    output_file.write(content_new)
