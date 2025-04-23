from flask import Flask, render_template, request,jsonify
import os

# -*- coding: utf-8 -*-
# --- function that imitates a disease prediction model ---

def predecir_estado_enfermedad(
    # --- Parámetros Demográficos (Opcionales) ---
    age: int = None,
    sex: str = None, # Esperado: 'F' o 'M'
    temperature: float = None, # Temperatura corporal en grados Celsius

    # --- Síntomas (Booleanos, Opcionales, default=False) ---
    # Lista reducida según la solicitud
    itching: bool = False,
    skin_rash: bool = False,
    continuous_sneezing: bool = False,
    shivering: bool = False,
    joint_pain: bool = False,
    stomach_pain: bool = False,
    # Se puede añadir **kwargs si se esperan más síntomas no listados explícitamente
    # **other_symptoms
) -> str:
    """
    Predice un estado de enfermedad básico basado en un conjunto reducido de
    síntomas y datos demográficos.

    Args:
        age (int, optional): Edad del paciente. Defaults to None.
        sex (str, optional): Sexo del paciente ('F' o 'M'). Defaults to None.
        temperature (float, optional): Temperatura corporal. Defaults to None.
        itching (bool, optional): Presencia de picazón. Defaults to False.
        skin_rash (bool, optional): Presencia de erupción cutánea. Defaults to False.
        continuous_sneezing (bool, optional): Presencia de estornudos continuos. Defaults to False.
        shivering (bool, optional): Presencia de escalofríos leves/intensos. Defaults to False.
        joint_pain (bool, optional): Presencia de dolor articular. Defaults to False.
        stomach_pain (bool, optional): Presencia de dolor estomacal. Defaults to False.

    Returns:
        str: Uno de los siguientes estados: "NO ENFERMO", "ENFERMEDAD LEVE",
             "ENFERMEDAD AGUDA", "ENFERMEDAD CRÓNICA", o un mensaje de error
             si no se proporcionan suficientes datos.
    """

    # Recopilar todos los síntomas proporcionados como True
    symptoms_dict = {
        'itching': itching, 'skin_rash': skin_rash,
        'continuous_sneezing': continuous_sneezing, 'shivering': shivering,
        'joint_pain': joint_pain, 'stomach_pain': stomach_pain
    }
    symptoms_present = [symptom for symptom, present in symptoms_dict.items() if present]
    num_symptoms_present = len(symptoms_present)

    # Contar cuántos datos demográficos se proporcionaron
    num_demographics_provided = sum(1 for val in [age, sex, temperature] if val is not None)

    # Contar el total de datos relevantes proporcionados
    total_relevant_inputs = num_demographics_provided + num_symptoms_present

    # Verificar si se proporcionaron al menos 3 datos relevantes
    if total_relevant_inputs < 3:
        return "ERROR: Se requieren al menos 3 datos relevantes (demográficos o síntomas presentes)."

    # --- Lógica de Decisión (Ajustada para nuevos síntomas) ---
    # Esta lógica es arbitraria y solo busca poder retornar todos los estados.

    # 1. Condiciones para ENFERMEDAD CRÓNICA
    # (Ej: Dolor articular persistente + edad avanzada)
    if joint_pain and (age is not None and age >= 60):
        return "ENFERMEDAD CRÓNICA"

    # 2. Condiciones para ENFERMEDAD AGUDA
    # (Ej: Fiebre alta O escalofríos intensos O combinación de síntomas agudos)
    is_high_fever = temperature is not None and temperature >= 38.5
    acute_symptoms_present = shivering or continuous_sneezing or stomach_pain

    # Fiebre alta O escalofríos con fiebre moderada/alta O >2 síntomas agudos
    if is_high_fever or \
       (shivering and temperature is not None and temperature >= 37.8) or \
       (sum(1 for s in [continuous_sneezing, shivering, stomach_pain] if s) >= 2):
        # Asegurarse que no sea solo dolor articular crónico
        if not (num_symptoms_present == 1 and joint_pain):
             return "ENFERMEDAD AGUDA"

    # 3. Condiciones para ENFERMEDAD LEVE
    # (Ej: Fiebre moderada O síntomas cutáneos O estornudos/dolor leve)
    is_moderate_fever = temperature is not None and 37.5 <= temperature < 38.5
    mild_symptoms_present = itching or skin_rash

    # Se considera leve si hay fiebre moderada o algún síntoma presente (y no cumple criterios de Aguda/Crónica)
    if is_moderate_fever or num_symptoms_present >= 1:
        # Esta condición se alcanza si no se cumplieron las de Crónica o Aguda
        # y hay al menos fiebre moderada o algún síntoma.
        # Se refina para evitar que solo joint_pain en joven sea leve (podría ser crónico no detectado aquí)
        if not (num_symptoms_present == 1 and joint_pain and (age is None or age < 60)):
            return "ENFERMEDAD LEVE"
        # Si es solo joint_pain en joven, podría ser no enfermo o requerir más datos
        # Para este ejemplo, lo dejamos pasar a "NO ENFERMO" si no hay otros indicadores.

    # 4. Condición por defecto: NO ENFERMO
    # Si no se cumple ninguna de las condiciones anteriores
    return "NO ENFERMO"


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_word():
    return render_template('/index.html')

@app.route('/predict', methods=['POST'])
def predict_disease_state():
    """
    Receives patient data via POST request, performs a simple prediction,
    and returns the predicted disease state.
    """
    try:
        data = request.get_json() # Get the JSON data sent from the frontend

        if not data:
            # Return a Bad Request error if no JSON data is received
            return jsonify({'prediction': 'ERROR: No se recibieron datos válidos.'}), 400

        # --- Extract data safely, providing default values or handling None ---
        age = data.get('age') # Can be None if input was empty
        sex = data.get('sex') # Can be 'F', 'M', or None if 'NA' or not selected
        temperature = data.get('temperature') # Can be None if input was empty

        # Checkbox values default to False if not explicitly True in the JSON
        itching = data.get('itching', False)
        skin_rash = data.get('skin_rash', False)
        continuous_sneezing = data.get('continuous_sneezing', False)
        shivering = data.get('shivering', False)
        joint_pain = data.get('joint_pain', False)
        stomach_pain = data.get('stomach_pain', False)


        prediction = "NO ENFERMO" # Default prediction

        prediction = predecir_estado_enfermedad(age,sex,
                                            temperature,
                                            itching,
                                            skin_rash,
                                            continuous_sneezing,
                                            shivering,
                                            joint_pain,
                                            stomach_pain)
        # --- Return the prediction as JSON ---
        return jsonify({'prediction': prediction})

    except Exception as e:
        # Handle any unexpected errors during processing
        print(f"Error during prediction: {e}") # Log the error on the server side
        return jsonify({'prediction': f'ERROR: Ocurrió un error interno. {str(e)}'}), 500 # Return a 500 Internal Server Error status



if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(debug=True, host='0.0.0.0',port=port)

