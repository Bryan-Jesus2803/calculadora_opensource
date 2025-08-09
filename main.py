"""
Archivo "main.py"
En el archivo principal se genera la interfaz gráfica de una calculadora.

Para esto me apoyé con la libreria Tkinter.
Incluye: botones 0-9, operadores +, -, *, /, y =, y un espacio (Entry) para mostrar la expresión.

Ejecución en terminal:
    python main.py

Nota: en este proyecto restringí la escritura por teclado, es decir que el usuario
solo puede ingresar los valores desde la UI usando los botones.
"""
import tkinter as tk
from suma import sumar as sum
from resta import restar as res
from multiplicacion import multiplicar as mul
from division import dividir as div
from suma_avanzada import suma_avanzada as sum_avanzada

class CalculadoraUI:

    #Generó el metodo constructor donde se instancia el objeto y guardamos los detalles principales del mismo
    #Por convencion usaré "master" para referirme al contenedor principal o widget principal de otros widgets
    def __init__(self, master):
        self.master = master
        master.title("Calculadora")
        master.resizable(False, False) #Evito que el usuario redimensione la ventana

        #En esta variable se concatenan los digitos que el usuario ingresa
        self.expresion = ""
        
        #Esta variable en resumen sirve para actualizar los widgets cuando su valor cambia
        #-----self.display_var = tk.StringVar(value="")

        #Genero el display o pantalla y los argumentos necesarios para que funcione correctamente
        #como la tipografia y el tamaño de fuente, alineacion, tamaño de ancho (esta en el número aproximado de caracteres que puede haber en pantalla)
        self.display = tk.Entry(
            master,
            #--- textvariable=self.display_var,  #Con esto el entry muestra el contenido de "display_var"
            font=("Helvetica", 24),         #Detalles de la tipografia
            borde=5,                        #Ancho del borde
            relief=tk.RIDGE,                #Estilo del borde
            justify="right",                #Alineacion del tecto a la derecha
            #state="readonly",               #Mantengo el estado de solo lectura, para que el usuario no ingrese valores mediante teclado
            width=15,                       #Pongo un aproximado de 15 caracteres de ancho en la pantalla
        )

        #Especificamos que todo se ordena mediante columnas y el display ocupa las 4 columnas
        #Ademas usé "padx" y "pady" para agregar una pequeña separacion entre los bordes de la venta y el display
        self.display.grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="we")

        #Definí la posición de cada boton, para mi caso la disposicion se maneja con grid
        #Emplee una lista de tuplas con el orden de texto, fila y columna 
        distribucion_botones = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("⌫", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("+", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), ("x", 4, 1), ("÷", 4, 2), ("=", 4, 3),
        ]

        #Creé un buclue que recorre la lista de distribucion para crear los botones
        for (text, row, col) in distribucion_botones: 
            action = lambda ch=text: self.backspace() if ch == "⌫" else self.add_char(ch)
            boton = tk.Button(
                master,
                text=text,
                width=4,
                height=2,
                font=("Helvetica", 18),
                command=action, 
            )

            #Con esto se crea el widget con el texto apropiado y el comando asociado al mismo
            boton.grid(row=row, column=col, padx=4, pady=4, sticky="we")

    #Este metodo añade un número u operador a la expresión y actualiza el display.
    def add_char(self, char):
        if char == "=":
            self._resolver_operacion() #Evaluo que si el boton presionado es igual, en ese caso se hace la operacion
        else:
            self.expresion += str(char) #Concateno el carécter a la expresión
            self._update_display()      #Llamo al metodo que actualiza el display  

    #Creo un metodo propio para el boton de retroceso o backspace
    def backspace(self):
        # Borra el último carácter de la expresión actual
        self.expresion = self.expresion[:-1]
        self._update_display() 

    #Este metodo actualiza el display para mostrar el contenido
    def _update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expresion)

    def _resolver_operacion(self):
        try:
            #Si la operacion es suma primero se evalua cuantos elementos a sumar hay
            if "+" in self.expresion:
                partes_a_sumar = self.expresion.split("+")

                #Si hay más de 2 se utiliza la suma avanzada
                if len(partes_a_sumar) > 2:
                    numeros = list(map(float, partes_a_sumar))
                    resultado = sum_avanzada(*numeros)
                else:
                    #En cambio si es solo uno se utiliza la suma de 2 numeros
                    num1, num2 = map(float, partes_a_sumar)
                    resultado = sum(num1, num2)
            
            #Con esta evaluacion verifique si es una resta
            elif "-" in self.expresion:
                num1, num2 = map(float, self.expresion.split("-"))
                resultado = res(num1, num2)

            #Utilice la letra x por apariencia para representar la multiplicación
            elif "x" in self.expresion:
                num1, num2 = map(float, self.expresion.split("x"))
                resultado = mul(num1, num2)

            #En este caso igual por apariencia elegi utilizar el simbolo común de la división en lugar de la diagonal
            elif "÷" in self.expresion:
                num1, num2 = map(float, self.expresion.split("÷"))
                resultado = div(num1, num2)

            #Y aqui agregue un else devuelva la misma expresión si no se ha presionado ninguna de las operaciones al dar igual
            else:
                resultado = self.expresion

            #Y actualizo la pantalla mostrando el resultado
            self.expresion = str(resultado)
            self._update_display()          

        except Exception:
            self.expresion = "Error"
            self._update_display()

#Leyendo un poco vi que en algunos lados se usa "root" por convencion para llamar a la ventana principal
def main():
    root = tk.Tk()
    CalculadoraUI(root)
    root.mainloop()     #mainloop() dirve para mantener la ventana activa e iniciar el bucle de la aplicacion gráfica

#Esta linea se encarga de verificar que el archivo se ejecute directamente
#Es decir que no se puede importar y ejecutar desde otro archivo
if __name__ == "__main__":
    main()
