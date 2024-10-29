from flask import Flask, render_template, request

app = Flask(__name__)

# Definisi konversi untuk setiap jenis pengukuran
conversions = {
    "length": {
        "millimeter": 1,
        "centimeter": 10,
        "meter": 1000,
        "kilometer": 1000000,
        "inch": 25.4,
        "foot": 304.8,
        "yard": 914.4,
        "mile": 1609344
    },
    "weight": {
        "milligram": 1,
        "gram": 1000,
        "kilogram": 1000000,
        "ounce": 28349.5,
        "pound": 453592
    },
    "temperature": {
        "celsius": "celsius",
        "fahrenheit": "fahrenheit",
        "kelvin": "kelvin"
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        value = float(request.form['value'])
        from_unit = request.form['from_unit']
        to_unit = request.form['to_unit']
        measurement_type = request.form['measurement_type']
        
        result = convert(value, from_unit, to_unit, measurement_type)
        return render_template('index.html', result=result, conversions=conversions)
    
    return render_template('index.html', conversions=conversions)

def convert(value, from_unit, to_unit, measurement_type):
    if measurement_type == "temperature":
        return round(convert_temperature(value, from_unit, to_unit), 2)
    
    from_value = conversions[measurement_type][from_unit]
    to_value = conversions[measurement_type][to_unit]
    
    return round((value * from_value) / to_value, 2)

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return round(value, 2)
    
    if from_unit == "celsius":
        if to_unit == "fahrenheit":
            return round((value * 9/5) + 32, 2)
        elif to_unit == "kelvin":
            return round(value + 273.15, 2)
    elif from_unit == "fahrenheit":
        if to_unit == "celsius":
            return round((value - 32) * 5/9, 2)
        elif to_unit == "kelvin":
            return round((value - 32) * 5/9 + 273.15, 2)
    elif from_unit == "kelvin":
        if to_unit == "celsius":
            return round(value - 273.15, 2)
        elif to_unit == "fahrenheit":
            return round((value - 273.15) * 9/5 + 32, 2)
    return round(value, 2)

if __name__ == '__main__':
    app.run(debug=True)