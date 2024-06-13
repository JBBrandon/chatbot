import csv
import typer
from rich import print
from rich.table import Table

# Función para leer datos desde un archivo CSV
def read_csv_data(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            cleaned_row = {key.strip(): value.strip() for key, value in row.items() if key}
            data.append(cleaned_row)
    return data

# Función principal del chatbot
def main():
    # Cargar datos desde los archivos CSV
    asignaturas_data = read_csv_data('descripcion_asignaturas.csv')
    horarios_data = read_csv_data('horarios_clases.csv')

    print("💬 ChatGPT API en Python")

    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la aplicación")
    table.add_row("new", "Crear una nueva conversación")
    print(table)

    # Contexto del asistente
    context = {"role": "system", "content": "Eres un asistente muy útil."}
    messages = [context]

    while True:
        content = __prompt()

        if content == "new":
            print("🆕 Nueva conversación creada")
            messages = [context]
            content = __prompt()

        messages.append({"role": "user", "content": content})

        # Manejar consultas sobre asignaturas
        if "asignaturas" in content.lower():
            asignaturas = ", ".join([asignatura['Asignatura'] for asignatura in asignaturas_data])
            respuesta = f"Las asignaturas disponibles son: {asignaturas}. ¿Sobre cuál específicamente quieres información?"
            messages.append({"role": "assistant", "content": respuesta})
            print(f"[bold green]> [/bold green] [green]{respuesta}[/green]")
        
        # Manejar consultas sobre horarios de asignaturas específicas
        elif any(asignatura['Asignatura'].lower() == content.lower() for asignatura in asignaturas_data):
            asignatura_encontrada = next(asignatura for asignatura in asignaturas_data if asignatura['Asignatura'].lower() == content.lower())
            descripcion = asignatura_encontrada['Introducción']
            horarios = [horario for horario in horarios_data if horario['Asignatura'].lower() == content.lower()]
            if horarios:
                horarios_texto = "\n".join([f"{horario['Día']} de {horario['Horario Inicio']} a {horario['Horario Fin']} en {horario['Aula']}, {horario['Pabellón']}" for horario in horarios])
                respuesta = f"{descripcion}\n\nHorarios:\n{horarios_texto}"
            else:
                respuesta = descripcion
            messages.append({"role": "assistant", "content": respuesta})
            print(f"[bold green]> [/bold green] [green]{respuesta}[/green]")

        elif content == "exit":
            exit = typer.confirm("✋ ¿Estás seguro?")
            if exit:
                print("👋 ¡Hasta luego!")
                raise typer.Abort()

        else:
            messages.append({"role": "assistant", "content": "Lo siento, no tengo información sobre eso."})
            print("[bold green]> [/bold green] [green]Lo siento, no tengo información sobre eso.[/green]")

# Función para solicitar la entrada del usuario
def __prompt() -> str:
    prompt = typer.prompt("\n¿Hola, Sobre qué quieres hablar? ")
    return prompt

if __name__ == "__main__":
    typer.run(main)
