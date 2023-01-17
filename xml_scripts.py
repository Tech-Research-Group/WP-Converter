"""XML GENERATORS FOR INITIAL SETUP BOX"""
def testeqp_setup_item(line, tm_no) -> str:
    """Creates a testeqp setup item in XML format."""
    testeqp = '\t\t\t<testeqp-setup-item>\n'
    testeqp += '\t\t\t\t<name>' + line + '</name>\n'
    testeqp += '\t\t\t\t<itemref>\n'
    testeqp += f'\t\t\t\t\t<xref itemid="" wpid="XXXXXX-{tm_no}"/>\n'
    testeqp += '\t\t\t\t</itemref>\n'
    testeqp += '\t\t\t</testeqp-setup-item>\n'
    return testeqp

def tools_setup_item(tool, tm_no) -> str:
    """Creates a tools setup item in XML format."""
    tools = '\t\t\t<tools-setup-item>\n'
    tools += '\t\t\t\t<name>' + tool + '</name>\n'
    tools += '\t\t\t\t<itemref>\n'
    tools += f'\t\t\t\t\t<xref itemid="" wpid="XXXXXX-{tm_no}"/>\n'
    tools += '\t\t\t\t</itemref>\n'
    tools += '\t\t\t</tools-setup-item>\n'
    return tools

def mtrlpart_setup_item(line, tm_no) -> str:
    """Creates a mtrlpart setup item in XML format."""
    mtrlpart = '\t\t\t<mtrlpart-setup-item>\n'
    mtrlpart += '\t\t\t\t<name>' + line + '</name>\n'
    mtrlpart += '\t\t\t\t<itemref>\n'
    mtrlpart += f'\t\t\t\t\t<xref itemid="" wpid="XXXXXX-{tm_no}"/>\n'
    mtrlpart += '\t\t\t\t</itemref>\n'
    mtrlpart += '\t\t\t</mtrlpart-setup-item>\n'
    return mtrlpart

def mrp_setup_item(line) -> str:
    """Creates an mrp setup item in XML format."""
    mrp = '\t\t\t<mrp-setup-item>\n'
    mrp += '\t\t\t\t<name>' + line + '</name>\n'
    mrp += '\t\t\t\t<qty></qty>\n'
    mrp += '\t\t\t\t<itemref>\n'
    mrp += f'\t\t\t\t\t<xref itemid="MRPL_" wpid="{get_mrp_wpid()}"/>\n'
    mrp += '\t\t\t\t</itemref>\n'
    mrp += '\t\t\t</mrp-setup-item>\n'
    return mrp

def get_mrp_wpid() -> str:
    """Finds item in MRP list and returns its name"""
    with open("templates/B0080-S00008-MRP.txt", "r", encoding="utf-8") as _f:
        for _l in _f:
            if 'wpno="' in _l:
                wpid = _l.split('wpno="')
                wpid = wpid[1].split('">')
                wpid = wpid[0]
                print(wpid)

        _f.close()
        return wpid


# def get_mrpl(line) -> str:
#     """Gets Mandatory Replacement Part MRPL_ id"""
#     with open("templates/B0080-S00008-MRP.txt", "r", encoding="utf-8") as _f:
#         for _l in _f:
#             line = _l
#             # print(line)
#             if "id=" in line:
#                 print(line[17:-2])

#         return line
