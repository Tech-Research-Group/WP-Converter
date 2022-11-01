"""XML GENERATORS FOR INITIAL SETUP BOX"""
def testeqp_setup_item(line) -> str:
    """Creates a testeqp setup item in XML format."""
    testeqp = '\t\t\t<testeqp-setup-item>\n'
    testeqp += '\t\t\t\t<name>' + line + '</name>\n'
    testeqp += '\t\t\t\t<itemref>\n'
    testeqp += '\t\t\t\t\t<xref itemid="" wpid="XXXXXX-XX-XXXX-XXX"/>\n'
    testeqp += '\t\t\t\t</itemref>\n'
    testeqp += '\t\t\t</testeqp-setup-item>\n'
    return testeqp

def tools_setup_item(tool) -> str:
    """Creates a tools setup item in XML format."""
    tools = '\t\t\t<tools-setup-item>\n'
    tools += '\t\t\t\t<name>' + tool + '</name>\n'
    tools += '\t\t\t\t<itemref>\n'
    tools += '\t\t\t\t\t<xref itemid="" wpid="XXXXXX-XX-XXXX-XXX"/>\n'
    tools += '\t\t\t\t</itemref>\n'
    tools += '\t\t\t</tools-setup-item>\n'
    return tools

def mtrlpart_setup_item(line) -> str:
    """Creates a mtrlpart setup item in XML format."""
    mtrlpart = '\t\t\t<mtrlpart-setup-item>\n'
    mtrlpart += '\t\t\t\t<name>' + line + '</name>\n'
    mtrlpart += '\t\t\t\t<itemref>\n'
    mtrlpart += '\t\t\t\t\t<xref itemid="" wpid="XXXXXX-XX-XXXX-XXX"/>\n'
    mtrlpart += '\t\t\t\t</itemref>\n'
    mtrlpart += '\t\t\t</mtrlpart-setup-item>\n'
    return mtrlpart

def mrp_setup_item(line) -> str:
    """Creates an mrp setup item in XML format."""
    mrp = '\t\t\t<mrp-setup-item>\n'
    mrp += '\t\t\t\t<name>' + line + '</name>\n'
    mrp += '\t\t\t\t<qty></qty>\n'
    mrp += '\t\t\t\t<itemref>\n'
    mrp += '\t\t\t\t\t<xref itemid="MRPL_" wpid="XXXXXX-XX-XXXX-XXX"/>\n'
    mrp += '\t\t\t\t</itemref>\n'
    mrp += '\t\t\t</mrp-setup-item>\n'
    return mrp


    