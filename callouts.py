# CALLOUTS VERSION 1
def insert_callouts(row) -> str:
    """Scans through the xml output and inserts callouts where they belong."""
    if "(F" in row:
        row1 = row.split("(F")
        row1 = row1[0]
        assocfig = row.split("(F")
        assocfig = assocfig[1].split(", I")
        assocfig = int(assocfig[0])
        if assocfig < 10:
            assocfig = f"0{assocfig}"
        if ", I" in row:
            label = row.split(", I")
            label= label[1].split(")")
            label = int(label[0])
        if ")" in row:
            row2 = row.split(")")
            row2 = row2[1]

            return f'{row1}<callout assocfig="{get_wpid()}-F00{assocfig}" label="{label}"/>{row2}'
    else:
        return row
    

# CALLOUTS VERSION 2
def insert_callouts(row) -> str:
    """Scans through the xml output and inserts callouts where they belong."""
    if "(F" not in row:
        return row
    row1 = row.split("(F")
    row1 = row1[0]
    assocfig = _extracted_from_insert_callouts_12(row, "(F", ", I")
    if assocfig < 10:
        assocfig = f"0{assocfig}"
    if ", I" in row:
        label = _extracted_from_insert_callouts_12(row, ", I", ")")
    if ")" in row:
        row2 = row.split(")")
        row2 = row2[1]

        return f'{row1}<callout assocfig="{get_wpid()}-F00{assocfig}" label="{label}"/>{row2}'

# TODO Rename this here and in `insert_callouts`
def _extracted_from_insert_callouts_12(row, arg1, arg2):
    result = row.split(arg1)
    result = result[1].split(arg2)
    result = int(result[0])
    return result


# CALLOUTS VERSION 3
def insert_callouts(row) -> str:
    """Scans through the xml output and inserts callouts where they belong."""
    r1 = []
    afig = []
    lbl = []
    r2 = []
    x = 0
    newLine = ""
    if "(F" in row:
        row1 = row.split("(F")
        row1 = row1[0]
        r1.append(row1)
        assocfig = row.split("(F")
        assocfig = assocfig[1].split(", I")
        assocfig = int(assocfig[0])
        # afig.append(assocfig)
        if assocfig < 10:
            assocfig = f"0{assocfig}"
            # afig.remove(assocfig)
            afig.append(assocfig)
        if ", I" in row:
            label = row.split(", I")
            label= label[1].split(")")
            label = int(label[0])
            lbl.append(label)
        if ")" in row:
            row2 = row.split(")")
            row2 = row2[1]
            r2.append(row2)
        for r1[x] in row:
            newLine += f'{r1[x]}<callout assocfig="{get_wpid()}-F00{afig[x]}" label="{lbl[x]}"/>{r2[x]}'
            x += 1
        print(newLine)
        return newLine
            # return f'{row1}<callout assocfig="{get_wpid()}-F00{assocfig}" label="{label}"/>{row2}'
    else:
        return row


# CALLOUTS VERSION 4: RegEx
def insert_callouts(row) -> str:
    """Scans through the xml output and inserts callouts where they belong."""
    callout = []
    x = 0
    fig_start = "(F"
    if fig_start not in row:
        return row
    
    print(row)

    cdata = re.findall('(F[1-9]+, I[1-9]+)', row)
    print(cdata)
    
    for cdata[x] in cdata:
        new_cdata = re.findall('[0-9]+', cdata[x])
        print(new_cdata)
        callout.append(f'<callout assocfig="{get_wpid()}-F00{new_cdata[0]}" label="{new_cdata[1]}"/>')
        print(callout)


# CALLOUTS VERSION 5: RegEx
def insert_callout(row) -> str:
    """Scans through the xml output and inserts callouts where they belong."""
    callout = []
    x = 0
    fig_start = "(F"
    if fig_start not in row:
        return row

    cdata = re.findall('(F[1-9]+, I[1-9]+)', row)
    print(cdata)
    
    for cdata[x] in cdata:
        new_cdata = re.findall('[0-9]+', cdata[x])
        print(new_cdata)
        callout.append(f'<callout assocfig="{get_wpid()}-F00{new_cdata[0]}" label="{new_cdata[1]}"/>')
        print(callout)
        data = row.split(cdata[x])
        print(data)
        
        print(data[0] + callout[0] + data[1])