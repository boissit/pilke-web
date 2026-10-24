"""The smallest .pptx Google Slides will convert, at a print page size.

    .venv/bin/python skeleton.py a4-portrait out/slides/a4-pysty.pptx

Google Slides sets a file's page size only when the file is made: neither the Slides
API nor the Drive connector can change it afterwards. So each print file starts as
this one-slide .pptx, uploaded to Drive converted, and everything on its pages is then
drawn through the Slides API. It is kept small (about 4 KB) because the Drive connector
carries an upload's bytes inside the tool call.

The theme it carries is the site's: Fredoka for headings and Figtree for body text,
and the palette in the theme colours, so they are one click away in the Slides editor.
"""
import sys
import zipfile

EMU_PER_MM = 36000
SIZES = {
    'a4-portrait': (210, 297),
    'a4-landscape': (297, 210),
    'a5-portrait': (148, 210),
}

CT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/></Types>"""

R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'

RELS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/officeDocument" Target="ppt/presentation.xml"/></Relationships>"""

PRES_RELS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/slideMaster" Target="slideMasters/slideMaster1.xml"/><Relationship Id="rId2" Type="{R}/slide" Target="slides/slide1.xml"/><Relationship Id="rId3" Type="{R}/theme" Target="theme/theme1.xml"/></Relationships>"""

MASTER_RELS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="{R}/theme" Target="../theme/theme1.xml"/></Relationships>"""

LAYOUT_RELS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>"""

SLIDE_RELS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>"""

TREE = '<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>'
NS = f'xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}"'

MASTER = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster {NS}>{TREE}<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>"""

LAYOUT = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout {NS} type="blank"><p:cSld name="Tyhjä"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>"""

SLIDE = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld {NS}><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"""


def colour(tag, hx):
    return f'<a:{tag}><a:srgbClr val="{hx}"/></a:{tag}>'


def fill():
    return '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'


THEME = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="{A}" name="Pilke"><a:themeElements><a:clrScheme name="Pilke">{colour('dk1', '3A2E2B')}{colour('lt1', 'FFFFFF')}{colour('dk2', '6E5F5A')}{colour('lt2', 'FFF8F4')}{colour('accent1', 'FFA98C')}{colour('accent2', 'F4504F')}{colour('accent3', 'FFE3DA')}{colour('accent4', 'A8DACB')}{colour('accent5', 'FCD1C3')}{colour('accent6', '3C3C3C')}{colour('hlink', '8F3A26')}{colour('folHlink', '8F3A26')}</a:clrScheme><a:fontScheme name="Pilke"><a:majorFont><a:latin typeface="Fredoka"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Figtree"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="Pilke"><a:fillStyleLst>{fill() * 3}</a:fillStyleLst><a:lnStyleLst>{('<a:ln w="9525">' + fill() + '</a:ln>') * 3}</a:lnStyleLst><a:effectStyleLst>{'<a:effectStyle><a:effectLst/></a:effectStyle>' * 3}</a:effectStyleLst><a:bgFillStyleLst>{fill() * 3}</a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>"""


def presentation(w_mm, h_mm):
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:presentation {NS}>'
            '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
            '<p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst>'
            f'<p:sldSz cx="{w_mm * EMU_PER_MM}" cy="{h_mm * EMU_PER_MM}"/>'
            f'<p:notesSz cx="{h_mm * EMU_PER_MM}" cy="{w_mm * EMU_PER_MM}"/></p:presentation>')


def build(size, path):
    w, h = SIZES[size]
    parts = [
        ('[Content_Types].xml', CT), ('_rels/.rels', RELS),
        ('ppt/presentation.xml', presentation(w, h)), ('ppt/_rels/presentation.xml.rels', PRES_RELS),
        ('ppt/slideMasters/slideMaster1.xml', MASTER), ('ppt/slideMasters/_rels/slideMaster1.xml.rels', MASTER_RELS),
        ('ppt/slideLayouts/slideLayout1.xml', LAYOUT), ('ppt/slideLayouts/_rels/slideLayout1.xml.rels', LAYOUT_RELS),
        ('ppt/slides/slide1.xml', SLIDE), ('ppt/slides/_rels/slide1.xml.rels', SLIDE_RELS),
        ('ppt/theme/theme1.xml', THEME),
    ]
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, text in parts:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, text)


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] not in SIZES:
        sys.exit(f'usage: skeleton.py {{{",".join(SIZES)}}} out.pptx')
    build(sys.argv[1], sys.argv[2])
