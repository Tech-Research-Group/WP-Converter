"""WORK PACKAGE CONVERTER"""
import tkinter as tk
import tkinter.font as tkfont
from tkinter.constants import END, WORD
from tkinter import Button, filedialog, Frame, Label, messagebox, Scrollbar, Text
import re
import mos_codes
import xml_scripts as xs


def get_title() -> str:
    """Gets the title of the work package."""
    title = split_input()[0].split(" (")
    return f'{title[0].upper()}<?Pub _newline?>{title[1][:-1].upper()}'

def get_task() -> str:
    """Gets the task of the work package."""
    task = split_input()[0].split(" (")
    return task[1][:-1].upper()

def get_wpid() -> str:
    """Gets the WPID from the input."""
    lines = txt_input.get("1.0", END).splitlines()
    for line in lines:
        if line.startswith("WPID:"):
            wpid = line.split("WPID: ")[1]
    return wpid

def get_tmno() -> str:
    """Gets the TM number from the input."""
    return get_wpid()[7:]

def add_period(step1) -> str:
    """Adds a period to step1's with incorrect closing punctuation."""
    return '' if str(step1).endswith(".") else f"{str(step1)}."

def remove_comments(row) -> str:
    """Removes comments from the output."""
    return row.split("[")[0]

def split_input() -> list:
    """Splits the input into a list."""
    return txt_input.get("1.0", END).splitlines()

def create_wpidinfo() -> str:
    """Creates the wpidinfo section into XML."""
    wpidinfo = f'<maintwp chngno="0" wpno="{get_wpid()}">\n\t<wpidinfo>\n\t\t<maintlvl level="operator"/>\n'
    wpidinfo += f'\t\t<title>{get_title()}</title>\n\t</wpidinfo>\n'
    return wpidinfo

def get_mos(mos_code) -> str:
    """Gets the name of the MOS based on code."""
    for key in mos_codes.CODES:
        if mos_code == key:
            MOS_NAME = mos_codes.CODES.get(key)
            print(f'{key} - {MOS_NAME}')
            break
    if mos_code not in mos_codes.CODES:
        MOS_NAME = ""
        messagebox.showerror("Error!", "No MOS code found. If you are going to define a MOS, you need to supply a valid code. Please try again.")
    return MOS_NAME


def get_fig_title(line) -> str:
    """Grabs the title of the current figure."""
    title = line.split(":")
    return title[1][:-1].capitalize()


def create_initial_setup() -> str:
    """Creates the initial_setup section into XML."""
    lines = txt_input.get("1.0", END).split("\n")
    initial_setup = '\t<initial_setup>\n'

    for line in lines:
        index = lines.index(line)
        if line.startswith("Test Equipment:") and lines[index + 1] != '':
            initial_setup += '\t\t<testeqp>\n'
            index += 1

            while lines[index] != '':
                initial_setup += xs.testeqp_setup_item(lines[index], get_tmno())
                index += 1
            initial_setup += '\t\t</testeqp>\n'

        if line.startswith("Tools:") and lines[index + 1] != '':
            initial_setup += '\t\t<tools>\n'
            index += 1

            while lines[index] != '':
                initial_setup += xs.tools_setup_item(lines[index], get_tmno())
                index += 1
            initial_setup += '\t\t</tools>\n'

        if line.startswith("Materials:") and lines[index + 1] != '':
            initial_setup += '\t\t<mtrlpart>\n'
            index += 1

            while lines[index] != '':
                initial_setup += xs.mtrlpart_setup_item(remove_comments(lines[index]), get_tmno())
                index += 1
            initial_setup += '\t\t</mtrlpart>\n'

        if line.startswith("Mandatory Replacement Parts:") and lines[index + 1] != '':
            initial_setup += '\t\t<mrp>\n'
            index += 1

            while lines[index] != '':
                initial_setup += xs.mrp_setup_item(remove_comments(lines[index]))
                print(lines[index])
                index += 1
            initial_setup += '\t\t</mrp>\n'

        if line.startswith("Personnel:") and lines[index + 1] != '':
            initial_setup += '\t\t<persnreq>\n'
            index += 1

            while lines[index] != '':
                line = lines[index].split("[")[0] # Remove comments

                initial_setup += '\t\t\t<persnreq-setup-item>\n'
                if line.startswith("MOS: "):
                    mos_code = line[5:8]
                    initial_setup += f'\t\t\t\t<name>{get_mos(mos_code)}</name>\n'
                    initial_setup += f'\t\t\t\t<mos>{mos_code}</mos>\n'
                    initial_setup += '\t\t\t</persnreq-setup-item>\n'
                    index += 1
                    
                    if lines[index] != '' and lines[index].startswith("1"):
                        initial_setup += '\t\t\t<persnreq-setup-item>\n'
                        initial_setup += '\t\t\t\t<name>Additional Person</name>\n'
                        initial_setup += '\t\t\t\t<mos></mos>\n'
                    elif lines[index] != '':
                        initial_setup += '\t\t\t<persnreq-setup-item>\n'
                        personnel = re.findall('[0-9]+', lines[index])
                        initial_setup += '\t\t\t\t<name>Additional Personnel</name>\n'
                        initial_setup += f'\t\t\t\t<qty>{personnel[0]}</qty>\n'
                    else:
                        break

                else:
                    initial_setup += f'\t\t\t\t<name>{lines[index]}</name>\n'

                index += 1
                initial_setup += '\t\t\t</persnreq-setup-item>\n'
            initial_setup += '\t\t</persnreq>\n'

        if line.startswith("References:") and lines[index + 1] != '':
            initial_setup += '\t\t<ref>\n'
            index += 1

            while lines[index] != '':
                initial_setup += '\t\t\t<ref-setup-item>\n'
                if lines[index].startswith("TM"):
                    initial_setup += f'\t\t\t\t<extref docno="{remove_comments(lines[index])}"/>\n'
                else:
                    initial_setup += f'\t\t\t\t<xref wpid="XXXXXX-{get_tmno()}"/>\n'
                initial_setup += '\t\t\t</ref-setup-item>\n'
                index += 1
            initial_setup += '\t\t</ref>\n'

        if line.startswith("Equipment Condition:") and lines[index + 1] != '':
            initial_setup += '\t\t<eqpconds>\n'
            index += 1

            while lines[index] != '':
                initial_setup += '\t\t\t<eqpconds-setup-item>\n'
                if lines[index].startswith("TM"):
                    initial_setup += '\t\t\t\t<condition>PLACEHOLDER</condition>\n'
                    initial_setup += '\t\t\t\t<itemref>\n'
                    initial_setup += f'\t\t\t\t<extref docno="{lines[index]}"/>\n'
                else:
                    initial_setup += f'\t\t\t\t<condition>{lines[index]}</condition>\n'
                    initial_setup += '\t\t\t\t<itemref>\n'
                    initial_setup += f'\t\t\t\t\t<xref wpid="XXXXXX-{get_tmno()}"/>\n'
                initial_setup += '\t\t\t\t</itemref>\n'
                initial_setup += '\t\t\t</eqpconds-setup-item>\n'
                index += 1
            initial_setup += '\t\t</eqpconds>\n'
    initial_setup += '\t</initial_setup>\n'
    return initial_setup

def create_maintsk() -> str:
    """Creates the maintsk section into XML."""
    lines = split_input()
    maintsk = '\t<maintsk>\n'
    for line in lines:
        if line.startswith("Maintenance Task Here:"):
            # Get the task name and wrap it in xml tags
            task = get_task()
            maintsk += '\t\t<' + task.lower() + '>\n'
            maintsk += '\t\t\t<proc>\n' + '\t\t\t\t<title/>\n'

            for line in lines:
                index = lines.index(line)
                if line.startswith("."):

                    if line.startswith(".Note: ") or line.startswith(".NOTE: "): # and lines[index + 1].startswith(".NOTE:"):
                        maintsk += '\t\t\t\t<step1>\n' + '\t\t\t\t\t<specpara>\n' + '\t\t\t\t\t\t<note>\n'

                        while lines[index].startswith(".NOTE: "):
                            maintsk += f'\t\t\t\t\t\t\t<trim.para>{insert_callouts(remove_comments(lines[index][7:]))}.</trim.para>\n'
                            lines[index] = ""
                            index += 1
                            
                        maintsk += f'\t\t\t\t\t\t\t<para>{insert_callouts(remove_comments(lines[index + 1][1:]))}.\n'
                        index += 1
                        lines[index] = ""
                        # TODO Fix adding step2s here
                        # index += 1
                        # while lines[index].startswith(".."):
                        #     maintsk += '\t\t\t\t\t\t\t\t<step2>\n'
                        #     maintsk += f'\t\t\t\t\t\t\t\t\t<para>{insert_callouts(lines[index][2:])}.</para>\n'
                        #     maintsk += '\t\t\t\t\t\t\t\t</step2>\n'
                        #     index += 1

                        maintsk += '\t\t\t\t\t\t\t</para>\n'
                        maintsk += '\t\t\t\t\t\t</note>\n' + '\t\t\t\t\t</specpara>\n' + '\t\t\t\t</step1>\n'
                        lines[index + 1] = ''

                    elif line.startswith(".Caution: ") or line.startswith(".CAUTION: "):
                        maintsk += '\t\t\t\t<step1>\n' + '\t\t\t\t\t<specpara>\n' + '\t\t\t\t\t\t<caution>\n'
                        maintsk += '\t\t\t\t\t\t\t<icon-set boardno="PLACEHOLDER"/>\n'

                        while lines[index].startswith(".Caution: ") or lines[index].startswith(".CAUTION: "):
                            maintsk += f'\t\t\t\t\t\t\t<trim.para>{insert_callouts(remove_comments(lines[index][10:]))}.</trim.para>\n'
                            lines[index] = ""
                            index += 1

                        maintsk += f'\t\t\t\t\t\t\t<para>{insert_callouts(remove_comments(lines[index + 1][1:]))}.\n'
                        index += 1
                        lines[index] = ""

                        maintsk += '\t\t\t\t\t\t\t</para>\n'
                        maintsk += '\t\t\t\t\t\t</caution>\n' + '\t\t\t\t\t</specpara>\n' + '\t\t\t\t</step1>\n'
                        lines[index + 1] = ''

                    elif line.startswith(".Warning: ") or line.startswith(".WARNING: "):
                        maintsk += '\t\t\t\t<step1>\n' + '\t\t\t\t\t<specpara>\n' + '\t\t\t\t\t\t<warning>\n'
                        maintsk += '\t\t\t\t\t\t\t<icon-set boardno="PLACEHOLDER"/>\n'

                        while lines[index].startswith(".Warning: ") or lines[index].startswith(".WARNING: "):
                            maintsk += f'\t\t\t\t\t\t\t<trim.para>{insert_callouts(remove_comments(lines[index][10:]))}.</trim.para>\n'
                            lines[index] = ""
                            index += 1

                        maintsk += f'\t\t\t\t\t\t\t<para>{insert_callouts(remove_comments(lines[index + 1][1:]))}.</para>\n'
                        index += 1
                        lines[index] = ""

                        maintsk += '\t\t\t\t\t\t\t</para>\n'
                        maintsk += '\t\t\t\t\t\t</warning>\n' + '\t\t\t\t\t</specpara>\n' + '\t\t\t\t</step1>\n'
                        lines[index + 1] = ''

                    elif line.startswith(".figure") or line.startswith(".Figure") or line.startswith(".FIGURE"):
                        maintsk += f'\t\t\t\t<figure id="{get_wpid()}-F00{insert_figid(line)}">\n'
                        if lines[index].split(": ")[-1] == '.figure':
                            maintsk += '\t\t\t\t\t<title></title>\n'
                        else:
                            maintsk += f'\t\t\t\t\t<title>{lines[index].split(": ")[-1]}</title>\n'
                        maintsk += '\t\t\t\t\t<graphic boardno="PLACEHOLDER"/>\n'
                        maintsk += '\t\t\t\t</figure>\n'

                    else:
                        maintsk += '\t\t\t\t<step1>\n'
                        # maintsk += f'\t\t\t\t\t<para>{insert_callouts(remove_comments(lines[index][1:]))}.</para>\n'
                        maintsk += f'\t\t\t\t\t<para>{insert_callouts(lines[index][1:])}.\n'
                        
                        while lines[index + 1].startswith("..") and not lines[index + 1].startswith("..."):
                            maintsk += '\t\t\t\t\t\t<step2>\n'
                            maintsk += f'\t\t\t\t\t\t\t<para>{insert_callouts(lines[index + 1][2:])}.\n'
                            
                            # TODO Fix loop creating step2/3s interfering w/ one another
                            # while lines[index + 1].startswith("..."):
                            #     maintsk += '\t\t\t\t\t\t\t\t<step3>\n'
                            #     maintsk += f'\t\t\t\t\t\t\t\t<para>{insert_callouts(lines[index + 1][3:])}.</para>\n'
                            #     maintsk += '\t\t\t\t\t\t\t\t</step3>\n'
                            #     lines[index + 1] = ''
                            #     index += 1
                            maintsk += '\t\t\t\t\t\t\t</para>\n'
                            maintsk += '\t\t\t\t\t\t</step2>\n'
                            lines[index + 1] = ''
                            index += 1
                        maintsk += '\t\t\t\t\t</para>\n'
                        maintsk += '\t\t\t\t</step1>\n'
                elif line == "":
                    index += 1
            maintsk += '\t\t\t</proc>\n'
            maintsk += f'\t\t</{task.lower()}>\n'
    maintsk += '\t</maintsk>\n'

    for line in lines:
        if line.startswith("Follow on ") or line.startswith("Follow-on "):
            # Get index of line for Follow On Task Name
            index = lines.index(line)

            # Check to make sure there is a follow-on task first
            try:
                if lines[index + 1] == "":
                    break

                # Jump to next line to get the task data
                followon_maintsk = lines[index + 1]
                maintsk += '\t<followon.maintsk>\n' + '\t\t<proc>\n'
                # Remove comments from the follow-on maintenance task
                followon_maintsk = insert_iaw(remove_comments(followon_maintsk))
                # Display the follow-on maintenance task w/o comments
                maintsk += '\t\t\t<para>' + followon_maintsk + '.</para>\n'
                maintsk += '\t\t</proc>\n' + '\t</followon.maintsk>\n' + '</maintwp>\n'
            except IndexError:
                # Display empty follow-on maintenance task tags
                maintsk += '</maintwp>\n'
    return maintsk

def insert_iaw(line):
    """Parse a line for IAW's and inputs correct XML syntax."""
    if "IAW" not in line:
        return line
    start = line.split(" IAW")[0]
    ref = line.split("IAW")[1][1:]

    if "TM" in line:
        new_line = f"{start} IAW (<extref docno='{ref}'/>)"
    else:
        new_line = f"{start} IAW {ref} (<xref wpid=''/>)"
    print(new_line)
    return new_line

def convert() -> None:
    """Converts the input from OneNote to XML."""
    # Clear the output box
    txt_output.delete("1.0", END)

    try:
        create_xml()
    except IndexError:
        messagebox.showerror("Error!", "No input found. Paste your OneNote data into the input box on the left before converting. Please try again.")

def create_xml() -> None:
    """Creates/displays the XML output and calls the Save button."""
    # Call functions that convert input into XML
    xml = create_wpidinfo()
    xml += create_initial_setup()
    xml += create_maintsk()

    # Insert XML into the output box
    txt_output.insert(END, xml)

    # Show the Save button
    show_save_button()

# CALLOUTS VERSION 1
def insert_callouts(row) -> str:
    """Scans through the xml output and inserts callouts where they belong."""
    if "(F" not in row:
        return row

    row1 = row.split("(F")
    end = row.rpartition(")")[2]
    row1 = row1[0]

    assocfig = get_callout_data(row, "(F", ", I")
    if assocfig < 10:
        assocfig = f"0{assocfig}"
    if ", I" in row:
        label = get_callout_data(row, ", I", ")")
    if ")" in row:
        row2 = row.split(")")
        row2 = row2[1]
        new_row = f'{row1}<callout assocfig="{get_wpid()}-F00{assocfig}" label="{label}"/>{row2}'
    if "(F" not in new_row:
        return new_row
    row2 = f'{row2})'
    new_row = new_row.split("(F")
    new_row = new_row[0]
    assocfig2 = get_callout_data(row2, "(F", ", I")
    if assocfig2 < 10:
        assocfig2 = f"0{assocfig2}"
    if ", I" in row2:
        label2 = get_callout_data(row2, ", I", ")")
    if ")" in end:
        end = end.split(")")
        end = end[1]

    return f'{new_row}<callout assocfig="{get_wpid()}-F00{assocfig2}" label="{label2}"/>{end}'


def get_callout_data(arg0, arg1, arg2):
    """Function to extract assocfig's and label's from a line for callouts"""
    result = arg0.split(arg1)
    result = result[1].split(arg2)
    result = int(result[0])
    return result

def insert_figid(line) -> str:
    """Scans through the xml output and inserts figure id's where they belong."""
    if ".FIGURE" in line or ".figure" in line:
        figid = re.findall('[0-9]+', line)
        figid = int(figid[0])
        if figid < 10:
            figid = f"0{figid}"
        return figid

def show_save_button() -> None:
    """Shows the Save button."""
    # Show the Save button once conversion is complete
    btn_save = Button(root, text="Save", font=("Arial",14), fg="white",bg="#F05454",
                         activebackground="#007ACC", relief="flat", borderwidth="0",
                         command=lambda:[save(), btn_save.place_forget()])
    btn_save.place(relx=0.5, rely=0.9, relwidth="0.5", height=100, anchor='nw')

def save() -> None:
    """Saves the output as an XML file."""
    output = txt_output.get("1.0", END)
    filename = filedialog.asksaveasfilename(initialdir = "/",
        title="Select file",filetypes = (("xml files","*.xml"), ("txt files", "*.txt"),
        ("all files","*.*")))
    with open(filename, 'w', encoding='utf-8') as _f:
        _f.write(output)
        _f.close()

root = tk.Tk()

root.resizable(False, False)
root.title("Maintenance Work Package Converter")
root.configure(background='#222831')

# root.geometry("1008x769") # MacOS
root.geometry("1450x1000") # Windows

frame1 = Frame(root, bg='#c6cbcf', bd=10)
frame1.place(relx=0, rely=0.05, relwidth=0.5, relheight=0.85, anchor='nw')

text_scroll1 = Scrollbar(frame1)
text_scroll1.pack(side="right", fill="y")

#input text
txt_input = Text(frame1,font =("Arial", 13), insertbackground="black", bg="#ffffff",
                    fg ="black", selectbackground="#30475E", selectforeground="white", undo=True,
                    yscrollcommand=text_scroll1.set, wrap=WORD)
txt_input.pack(side = "left", fill="y")

text_scroll1.config(command=txt_input.yview)

#Convert Button
button1 = Button(root, text ="Convert", font=("Arial",14), fg="white", bg="#F05454",
                    activebackground="#007ACC", relief="flat", borderwidth="0", command=convert)
button1.place(relx = 0, rely = .9, relwidth="0.5", height=100, anchor='nw')

# btn_mrp = Button(root, text="Select MRP", font=("Arial",14), fg="white",bg="#F05454",
#                          activebackground="#007ACC", relief="flat", borderwidth="0",
#                          command=search_mrp)
# btn_mrp.place(relx=0.5, rely=0.9, relwidth="0.5", height=100, anchor='nw')

label1 = Label(root,text="Copy your work package data from OneNote and paste it in the box below.",
                  font=("Arial", 12), bg='#DDDDDD')
label1.place(relx=0, rely=0, relwidth=0.5, relheight=0.05)

frame2 = Frame(root, bg='#c6cbcf', bd=10)
frame2.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.85, anchor='nw')

text_scroll2 = Scrollbar(frame2)
text_scroll2.pack(side="right", fill="y")

#output text
txt_output = Text(frame2,font =("Menlo", 13),insertbackground="black", bg="#ffffff",
                     fg ="black", selectbackground="#30475E", selectforeground="white",
                     undo=True, yscrollcommand=text_scroll2.set, wrap=WORD)
txt_output.pack(side="left", fill="y")

font = tkfont.Font(font=txt_output['font'])
tab=font.measure("    ")
txt_output.configure(tabs=tab)

text_scroll2.config(command=txt_output.yview)

label2 = Label(root, text="Results:", font=("Arial", 12), bg='#DDDDDD')
label2.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.05)

root.mainloop()
