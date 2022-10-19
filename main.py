"""WORK PACKAGE CONVERTER"""
import tkinter as tk
import tkinter.font as tkfont
from tkinter import Button, filedialog, Frame, Label, messagebox, Scrollbar, Text

def get_title() -> str:
    """Gets the title of the work package."""
    title = split_input()[0]
    title = title.split(" (")
    title = title[0][1:].upper() + '<?Pub _newline?>' + title[1][:-1].upper()
    return title

def get_task() -> str:
    """Gets the task of the work package."""
    task = split_input()[0]
    task = task.split(" (")
    task = task[1][:-1].upper()
    return task

def get_task_title() -> str:
    """Gets the maintenance task title."""
    onenote = txt_input.get("1.0",'end-1c')
    lines = onenote.splitlines()

    for line in lines:
        if line.startswith("Maintenance Task Title:"):
            index = lines.index(line)
            task_title = lines[index+1]
            return task_title

def remove_comments(row) -> str:
    """Removes comments from the output."""
    clean_line = row.split("[")
    row = clean_line[0]
    return row

def split_input() -> list:
    """Splits the input into a list."""
    onenote = txt_input.get("1.0",'end-1c')
    lines = onenote.splitlines()
    return lines

def create_wpidinfo() -> str:
    """Creates the wpidinfo section into XML."""
    wp_title = get_title()
    wpidinfo = '<maintwp chngno="0" wpno="">\n'
    wpidinfo += '\t<wpidinfo>\n'
    wpidinfo += '\t\t<maintlvl level="operator"/>\n'
    wpidinfo += '\t\t<title>' + str(wp_title) + '</title>\n'
    wpidinfo += '\t</wpidinfo>\n'
    return wpidinfo

def create_initial_setup() -> str:
    """Creates the initial_setup section into XML."""
    onenote = txt_input.get("1.0",'end-1c')
    lines = onenote.split("\n")
    initial_setup = '\t<initial_setup>\n'

    for line in lines:
        if line.startswith("Test Equipment:"):
            index = lines.index(line)

            if lines[index + 1] != '':
                initial_setup += '\t\t<testeqp>\n'
                index += 1

                while lines[index] != '':
                    initial_setup += '\t\t\t<testeqp-setup-item>\n'
                    initial_setup += '\t\t\t\t<name>' + remove_comments(lines[index]) + '</name>\n'
                    initial_setup += '\t\t\t\t<itemref>\n'
                    initial_setup += '\t\t\t\t\t<xref itemid="" wpid=""/>\n'
                    initial_setup += '\t\t\t\t</itemref>\n'
                    initial_setup += '\t\t\t</testeqp-setup-item>\n'
                    index += 1
                initial_setup += '\t\t</testeqp>\n'

        if line.startswith("Tools:"):
            index = lines.index(line)
            if lines[index + 1] != '':
                initial_setup += '\t\t<tools>\n'
                index += 1
                while lines[index] != '':
                    initial_setup += '\t\t\t<tools-setup-item>\n'
                    initial_setup += '\t\t\t\t<name>' + remove_comments(lines[index]) + '</name>\n'
                    initial_setup += '\t\t\t\t<itemref>\n'
                    initial_setup += '\t\t\t\t\t<xref itemid="" wpid=""/>\n'
                    initial_setup += '\t\t\t\t</itemref>\n'
                    initial_setup += '\t\t\t</tools-setup-item>\n'
                    index += 1
                initial_setup += '\t\t</tools>\n'

        if line.startswith("Materials:"):
            index = lines.index(line)
            if lines[index + 1] != '':
                initial_setup += '\t\t<mtrlpart>\n'
                index += 1

                while lines[index] != '':
                    initial_setup += '\t\t\t<mtrlpart-setup-item>\n'
                    initial_setup += '\t\t\t\t<name>' + remove_comments(lines[index]) + '</name>\n'
                    initial_setup += '\t\t\t\t<itemref>\n'
                    initial_setup += '\t\t\t\t\t<xref itemid="" wpid=""/>\n'
                    initial_setup += '\t\t\t\t</itemref>\n'
                    initial_setup += '\t\t\t</mtrlpart-setup-item>\n'
                    index += 1
                initial_setup += '\t\t</mtrlpart>\n'

        if line.startswith("Mandatory Replacement Parts:"):
            index = lines.index(line)
            if lines[index + 1] != '':
                initial_setup += '\t\t<mrp>\n'
                index += 1

                while lines[index] != '':
                    initial_setup += '\t\t\t<mrp-setup-item>\n'
                    initial_setup += '\t\t\t\t<name>' + remove_comments(lines[index]) + '</name>\n'
                    initial_setup += '\t\t\t\t<qty></qty>\n'
                    initial_setup += '\t\t\t\t<itemref>\n'
                    initial_setup += '\t\t\t\t\t<xref itemid="MRPL_" wpid=""/>\n'
                    initial_setup += '\t\t\t\t</itemref>\n'
                    initial_setup += '\t\t\t</mrp-setup-item>\n'
                    index += 1
                initial_setup += '\t\t</mrp>\n'

        if line.startswith("Personnel:"):
            index = lines.index(line)
            if lines[index + 1] != '':
                initial_setup += '\t\t<persnreq>\n'
                index += 1

                while lines[index] != '':
                    # Remove comments
                    clean_line = lines[index].split("[")
                    line = clean_line[0]
                    initial_setup += '\t\t\t<persnreq-setup-item>\n'
                    initial_setup += '\t\t\t\t<name>' + line[5:] + '</name>\n'
                    initial_setup += '\t\t\t\t<mos></mos>\n'
                    initial_setup += '\t\t\t</persnreq-setup-item>\n'
                    index += 1
                initial_setup += '\t\t</persnreq>\n'

        if line.startswith("References:"):
            index = lines.index(line)
            if lines[index + 1] != '':
                initial_setup += '\t\t<ref>\n'
                index += 1

                while lines[index] != '':
                    initial_setup += '\t\t\t<ref-setup-item>\n'
                    if lines[index].startswith("TM"):
                        initial_setup += '\t\t\t\t<extref docno="' + remove_comments(lines[index]) + '"/>\n'
                    else:
                        initial_setup += '\t\t\t\t<xref wpid=""/>\n'
                    initial_setup += '\t\t\t</ref-setup-item>\n'
                    index += 1
                initial_setup += '\t\t</ref>\n'

        if line.startswith("Equipment Condition:"):
            index = lines.index(line)
            if lines[index + 1] != '':
                initial_setup += '\t\t<eqpconds>\n'
                index += 1

                while lines[index] != '':
                    initial_setup += '\t\t\t<eqpconds-setup-item>\n'
                    initial_setup += '\t\t\t\t<condition>' + remove_comments(lines[index]) + '</condition\n'
                    initial_setup += '\t\t\t\t<itemref>\n'
                    initial_setup += '\t\t\t\t\t<xref wpid=""/>\n'
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
            index = lines.index(line)
            # Get the task name and wrap it in xml tags
            task = get_task()
            maintsk += '\t\t<' + task.lower() + '>\n'
            maintsk += '\t\t\t<proc>\n'
            maintsk += '\t\t\t\t<title/>\n'

            for line in lines:
                if line.startswith("."):
                    index = lines.index(line)

                    if line.startswith(".Note:"):
                        # print("Line: " + str(index) + " " + lines[index][1:])
                        maintsk += '\t\t\t\t<step1>\n'
                        maintsk += '\t\t\t\t\t<specpara>\n'
                        maintsk += '\t\t\t\t\t\t<note>\n'

                        # Remove possible spaces between the colon and the text
                        if lines[index].startswith(".Note: "):
                            maintsk += '\t\t\t\t\t\t\t<trim.para>' + remove_comments(lines[index][7:]) + '</trim.para>\n'
                        else:
                            maintsk += '\t\t\t\t\t\t\t<trim.para>' + remove_comments(lines[index][6:]) + '</trim.para>\n'

                        maintsk += '\t\t\t\t\t\t\t<para>' + remove_comments(lines[index + 1][1:]) + '</para>\n'
                        maintsk += '\t\t\t\t\t\t</note>\n'
                        maintsk += '\t\t\t\t\t</specpara>\n'
                        maintsk += '\t\t\t\t</step1>\n'
                        lines[index + 1] = ''

                    elif line.startswith(".Caution:"):
                        # print("Line: " + str(index) + " " + lines[index][1:])
                        maintsk += '\t\t\t\t<step1>\n'
                        maintsk += '\t\t\t\t\t<specpara>\n'
                        maintsk += '\t\t\t\t\t\t<caution>\n'
                        maintsk += '\t\t\t\t\t\t\t<icon-set boardno="PLACEHOLDER"/>\n'

                        # Remove possible spaces between the colon and the text
                        if lines[index].startswith(".Caution: "):
                            maintsk += '\t\t\t\t\t\t\t<trim.para>' + remove_comments(lines[index][10:]) + '</trim.para>\n'
                        else:
                            maintsk += '\t\t\t\t\t\t\t<trim.para>' + remove_comments(lines[index][9:]) + '</trim.para>\n'

                        maintsk += '\t\t\t\t\t\t\t<para>' + remove_comments(lines[index + 1][1:]) + '</para>\n'
                        maintsk += '\t\t\t\t\t\t</caution>\n'
                        maintsk += '\t\t\t\t\t</specpara>\n'
                        maintsk += '\t\t\t\t</step1>\n'
                        lines[index + 1] = ''

                    elif line.startswith(".Warning:"):
                        # print("Line: " + str(index) + " " + lines[index][1:])
                        maintsk += '\t\t\t\t<step1>\n'
                        maintsk += '\t\t\t\t\t<specpara>\n'
                        maintsk += '\t\t\t\t\t\t<warning>\n'
                        maintsk += '\t\t\t\t\t\t\t<icon-set boardno="PLACEHOLDER"/>\n'

                        # Remove possible spaces between the colon and the text
                        if lines[index].startswith(".Warning: "):
                            maintsk += '\t\t\t\t\t\t\t<trim.para>' + remove_comments(lines[index][10:]) + '</trim.para>\n'
                        else:
                            maintsk += '\t\t\t\t\t\t\t<trim.para>' + remove_comments(lines[index][9:]) + '</trim.para>\n'

                        maintsk += '\t\t\t\t\t\t\t<para>' + remove_comments(lines[index + 1][1:]) + '</para>\n'
                        maintsk += '\t\t\t\t\t\t</warning>\n'
                        maintsk += '\t\t\t\t\t</specpara>\n'
                        maintsk += '\t\t\t\t</step1>\n'
                        lines[index + 1] = ''

                    elif line.startswith(".figure") or line.startswith(".Figure") or line.startswith(".FIGURE"):
                        maintsk += '\t\t\t\t<figure assocfig="">\n'
                        maintsk += '\t\t\t\t\t<title></title>\n'
                        maintsk += '\t\t\t\t\t<graphic boardno="PLACEHOLDER"/>\n'
                        maintsk += '\t\t\t\t</figure>\n'

                    else:
                        maintsk += '\t\t\t\t<step1>\n'
                        maintsk += '\t\t\t\t\t<para>' + remove_comments(lines[index][1:]) + '</para>\n'
                        maintsk += '\t\t\t\t</step1>\n'

            maintsk += '\t\t\t</proc>\n'
            maintsk += '\t\t</' + task.lower() + '>\n'
    maintsk += '\t</maintsk>\n'

    for line in lines:
        if line.startswith("Follow on ") or line.startswith("Follow-on "):
            # Get index of line for Follow On Task Name
            index = lines.index(line)

            # Check to make sure there is a follow-on task first
            try:
                if lines[index + 1]:
                    # Jump to next line to get the task data
                    followon_maintsk = lines[index + 1]
                    maintsk += '\t<followon.maintsk>\n'
                    maintsk += '\t\t<proc>\n'
                    # Remove comments from the follow-on maintenance task
                    followon_maintsk = remove_comments(followon_maintsk)
                    # Display the follow-on maintenance task w/o comments
                    maintsk += '\t\t\t<para>' + followon_maintsk + '</para>\n'
                    maintsk += '\t\t</proc>\n'
                    maintsk += '\t</followon.maintsk>\n'

            except IndexError:
                # Display empty follow-on maintenance task tags
                # maintsk += '\t<followon.maintsk>\n'
                # maintsk += '\t\t<proc>\n'
                # maintsk += '\t\t\t<para></para>\n'
                # maintsk += '\t\t</proc>\n'
                # maintsk += '\t</followon.maintsk>\n'
                print("No follow-on maintenance task found")
    maintsk += '</maintwp>\n'
    return maintsk

def convert() -> None:
    """Converts the input from OneNote to XML."""
    txt_output.delete("1.0",'end-1c')
    try:
        # Call functions that convert input into XML
        xml = create_wpidinfo()
        xml += create_initial_setup()
        xml += create_maintsk()

        # Insert XML into the output box
        txt_output.insert(tk.END, xml)

        # Show the Save button once conversion is complete
        btn_save = Button(root, text ="Save", font=("Arial",14), fg = "white",bg="#F05454",
                             activebackground="#007ACC", relief="flat", borderwidth="0", command=lambda:[save(),
                             btn_save.place_forget()])
        btn_save.place(relx = 0.5, rely = 0.9, relwidth="0.5", height=100, anchor='nw')
    except IndexError:
        messagebox.showerror("Error!", "No input found. Paste your OneNote input into the input box on the left before converting. Please try again.")

def save() -> None:
    """Saves the output as an XML file."""
    xml = txt_output.get("1.0",'end-1c')
    filename = filedialog.asksaveasfilename(initialdir = "/",
        title="Select file",filetypes = (("xml files","*.xml"), ("txt files", "*.txt"),
        ("all files","*.*")))
    with open(filename, 'w', encoding='utf-8') as _f:
        _f.write(xml)

root = tk.Tk()

#root.resizable(False, False)
root.title("Maintenance Work Package Converter")
root.configure(background='#222831')

#root.geometry("1008x769") # MacOS
root.geometry("1450x900") # Windows

#canvas = tk.Canvas(root, height = 900,width = 1450, background='#222831')
#canvas.pack( expand = True)

frame1 = Frame(root, bg='#c6cbcf', bd=10)
frame1.place(relx = 0, rely=0.05, relwidth=0.5, relheight=0.85, anchor='nw')

text_scroll1 = Scrollbar(frame1)
text_scroll1.pack(side="left",fill="y")

#input text
txt_input = Text(frame1,font =("Arial",13), insertbackground="black", bg = "#c6cbcf",
                    fg ="black", selectbackground="#30475E", selectforeground="white", undo=True,
                    yscrollcommand=text_scroll1.set, wrap=tk.WORD)
txt_input.pack(side = "left",fill="y")

text_scroll1.config(command=txt_input.yview)

#Convert Button
button1 = Button(root, text ="Convert", font=("Arial",14), fg = "white", bg="#F05454",
                    activebackground="#007ACC", relief="flat", borderwidth="0", command=convert)
button1.place(relx = 0, rely = .9, relwidth="0.5", height=100, anchor='nw')

label1 = Label(root,text="Copy your work package data from OneNote and paste it in the box below.",
                  font=("Arial",12), bg='#DDDDDD')
label1.place(relx=0,rely=0,relwidth=0.5,relheight=0.05)

frame2 = Frame(root, bg='#c6cbcf', bd=10)
frame2.place(relx = 0.5, rely=0.05,relwidth=0.5, relheight=0.85, anchor='nw')

text_scroll2 = Scrollbar(frame2)
text_scroll2.pack(side="left", fill="y")

#output text
txt_output = Text(frame2,font =("Menlo",13),insertbackground="black", bg = "#c6cbcf",
                     fg ="black", selectbackground="#30475E", selectforeground="white",
                     undo=True, yscrollcommand=text_scroll2.set, wrap=tk.WORD)
txt_output.pack(side="left",fill="y")

font = tkfont.Font(font=txt_output['font'])
tab=font.measure("    ")
txt_output.configure(tabs = tab)

text_scroll2.config(command=txt_output.yview)

label2 = Label(root, text="Results:", font=("Arial",12), bg='#DDDDDD')
label2.place(relx = 0.5, rely=0, relwidth=0.5, relheight=0.05)

root.mainloop()
