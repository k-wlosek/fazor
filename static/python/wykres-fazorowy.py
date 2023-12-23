import js
from phasors.symbol import Symbol
from phasors.diagram import Diagram
from data import inp, angles
import io, base64

def convert_to_phasors(inp):
    data = []
    for i in inp:
        # symbols
        symbol = []
        for j in range(len(i)-1):
            temp = []
            datapoint = i[j]
            temp.append(float(datapoint[0]))
            temp.append(float(datapoint[1]))
            temp.append(datapoint[2])
            temp.append(datapoint[3])
            symbol.append(tuple(temp))
        symbol.append(i[-1])
        data.append(symbol)
    return Symbol.from_list(data)

def convert_to_angles(angles):
    data = []
    for i in angles:
        # angle
        temp = []
        for j in range(len(i)-1):
            temp.append(float(i[j]))
        temp.append(i[-1])
        data.append(tuple(temp))
    return data

if __name__ == "__main__":
    phasors = convert_to_phasors(inp)
    title = js.document.getElementById("ph-title").value
    angles = convert_to_angles(angles)
    diagram = Diagram(phasors, title, angles)
    diagram.create()
    byte = d.save_as_bytes("png")
    byte.seek(0)
    global ph_img
    ph_img = 'data:image/png;base64,' + base64.b64encode(byte.read()).decode('UTF-8')
