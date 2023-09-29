from flask import Flask,request,render_template,jsonify
from src.pipelines.prediction_pipleline import CustomData,PredictPipeline
from src.logger import logging

application=Flask(__name__)

app=application

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    
    else:
        logging.info('data being received')
        mean_radius1=float(request.form.get('mean_radius'))
        logging.info(f'mean_radius1 : {mean_radius1}')
        data=CustomData(
            mean_radius=float(request.form.get('mean_radius')),
            mean_texture = float(request.form.get('mean_texture')),
            mean_perimeter = float(request.form.get('mean_perimeter')),
            mean_area = float(request.form.get('mean_area')),
            mean_smoothness = float(request.form.get('mean_smoothness')),
            mean_compactness = float(request.form.get('mean_compactness')),
            mean_concavity = request.form.get('mean_concavity'),
            mean_concave_points= request.form.get('mean_concave_points'),
            mean_symmetry = request.form.get('mean_symmetry'),
            mean_fractal_dimension = request.form.get('mean_fractal_dimension'),
            radius_error = request.form.get('radius_error'),
            texture_error = request.form.get('texture_error'),
            perimeter_error = request.form.get('perimeter_error'),
            area_error = request.form.get('area_error'),
            smoothness_error = request.form.get('smoothness_error'),
            compactness_error = request.form.get('compactness_error'),
            concavity_error = request.form.get('concavity_error'),
            concave_points_error = request.form.get('concave_points_error'),
            symmetry_error = request.form.get('symmetry_error'),
            fractal_dimension_error = request.form.get('fractal_dimension_error'),
            worst_radius = request.form.get('worst_radius'),
            worst_texture = request.form.get('worst_texture'),
            worst_perimeter = request.form.get('worst_perimeter'),
            worst_area = request.form.get('worst_area'),
            worst_smoothness = request.form.get('worst_smoothness'),
            worst_compactness = request.form.get('worst_compactness'),
            worst_concavity = request.form.get('worst_concavity'),
            worst_concave_points = request.form.get('worst_concave_points'),
            worst_symmetry = request.form.get('worst_symmetry'),
            worst_fractal_dimension = request.form.get('worst_fractal_dimension')
        )
        logging.info(f'data : \n{data}')
        final_new_data=data.get_data_as_dataframe()
        logging.info(f'final_new_data : \n{final_new_data}')
        predict_pipeline=PredictPipeline()
        pred=predict_pipeline.predict(final_new_data)
        logging.info(f"Predicted result is {pred}")
        results=round(pred[0],2)

        return render_template('form.html',final_result=results)
    

if __name__=="__main__":
    # app.run(host='0.0.0.0',debug=True)
    app.run(port=5001)