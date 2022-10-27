# WP Converter

### Introduction
To use this application copy your OneNote data starting with the title of the note all the way through
your follow-on maintenance instructions. Paste the data in the textarea on the left and click the 
"Convert" button. The converted output should come up in the textarea on the right. From here you can
copy the newly generated XML into an existing txt file or choose to save it as a new file. 

### Template Syntax
Use the following syntax in your OneNote work packages to ensure the proper conversion to XML:
- The title of the WP should be Procedure Title (Procedure). 
    - For example: Shower Head (Replace)
- Add a new line after the last item in each section in the initial setup box (ISB).
- Place a "*.*" infront of each step1, figure, note, etc. in **first** level of indentation from *maintsk* tags.
- Try to end each step1, note, caution, and warning with a "*.*". If you do not, the program will add one.
- Use "*.NOTE*" for notes, "*.CAUTION*" for cautions, and "*.WARNING*" for warnings.
- To add a figure placeholder, use "*.figure*"
- Public comments that should remain in the XML are surrounded by opening/closing "*()*"
- Private comments that should be removed from the XML are surrounded by opening/closing "*[]*"

![WP Converter](https://github.com/Tech-Research-Group/WP-Converter/blob/main/screenshot.png "WP Converter")

If you find any bugs or have some ideas to improve the program please reach out to [Nick Ricci](https://github.com/trg-nickr) so he can address them properly. Thanks!
