#Shiny
[English Version]
Interpreter of an small language call shiny that is inserted into a html file.
The program interpret the file and generate an graphic and console output recognizing the expressions in the file.
Grammar parser and lexer of the language define as shiny.

[Spanish Version]
Intérprete de un pequeño lenguaje llamado "Shiny" que viene insertado en un archivo html.
El programa interpreta el archivo y genera una salida gráfica y consola al reconocer las expresiones en el archivo.
Gramática y analizador léxico de la lengua define como brillante.

#Python Version
Python 2.7

#First Run / Primera Ejecucion
```
sudo yum install python-matplotlib
pip install pydot2
pip install networkx 
```

#Execute /  Ejecucion
python shiny.py file.html

#Output  / Salida
resultado.sel

#Example of Shiny / Ejemplo de Shiny
```html
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>Shiny Test</title>
</head>
<body>
<h2> Hello Word! </h2>
{% variable : int := 2 + 2 %}
{% iamstring : string := "cadena de caracteres" %}
{% new : int := variable + 1 %}
</body>
</html>
```
