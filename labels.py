from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas as pd
import json
from io import BytesIO
import base64
import qrcode


def genQr(rowdata):
    # The data in the QR code is specified here
    qrdata = {
        'name': rowdata['Firstname'].title() + ' ' + rowdata['Surname'].title(),
        'memb': rowdata['Mem No.'],
        'emerg': {
            'name': rowdata['Emergency contact name'],
            'numb': rowdata['Emergency contact phone']
        },
        'email': rowdata['Email']
    }
    img = qrcode.make(json.dumps(qrdata))
    buf = BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()


jinjaEnv = Environment(
    loader=FileSystemLoader(['.']),
    autoescape=select_autoescape(['html'])
)


def addressFilter(addr):
    return addr.replace("\n", "<br/>")


jinjaEnv.filters['addr'] = addressFilter

EVENTS = [
    '23-977',
    '23-984'
]

alldata = []

for event in EVENTS:
    evFile = "Ev %s.xls" % event

    with open(evFile, 'rb') as fp:
        data = pd.read_excel(fp, keep_default_na=False, dtype=str).to_dict(orient='records')

    for row in data:
        first = row['Firstname'].title()
        last = row['Surname'].title()
        if row['Time'] == 'DNS':
            print("Rider %s %s - DNS." % (first, last))
            continue
        email = row['Email']
        if not isinstance(email, str) or  (isinstance(email, str) and '@' not in email):
            print("Invalid email!")
            row['email'] = 'None'
        addr = ''
        for afield in ['Address', 'A1', 'A2', 'Town', 'Code']:
            if row[afield] != '' and not addr.endswith(row[afield] + "\n"):
                addr += row[afield] + "\n"
        row['Postal'] = addr
        row['Event'] = event
        row['qr'] = str(genQr(row))
        alldata.append(row)

while len(alldata) % 18 != 0:
    alldata.append({
        'blank': True
    })

template = jinjaEnv.get_template('label_base.html')

with open("labels.html", 'w') as fp:
    fp.write(template.render({
        'event': event,
        'topmargin': 9,         # Label top margin (mm)
        'labelheight': 46.6,    # Label height (mm)
        'labelygap': 0,         # Vertical gap between labels (mm)
        'leftmargin': 8,        # Label left margin (mm)
        'labelwidth': 63.5,     # Label width (mm)
        'labelxgap': 2.5,       # Horizontal gap between labels (mm)
        'riders': alldata
    }))
