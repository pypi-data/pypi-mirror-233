import io
import os
import zipfile
from inspect import signature, Parameter

import pandas as pd
import torch


def get_fn_parameters(fn, excluded_parameters: list):
    sig = signature(fn)

    parameters = []

    for param_name, param in sig.parameters.items():
        if param_name not in excluded_parameters:
            parameters.append({
                'name': param_name,
                'type': param.annotation if param.annotation is not Parameter.empty else None,
                'default': param.default if param.default is not Parameter.empty else None
            })

    return parameters


def save_csv_in_zip(zipfile_path, csv_path, csv):
    with zipfile.ZipFile(zipfile_path, 'a') as zipf:
        zipf.writestr(csv_path, csv)


def save_metric_in_zip(zipfile_path, metric_path, metric):
    metric_df = metric.get_dataframe()
    csv_content = metric_df.to_csv(index=False)
    save_csv_in_zip(zipfile_path=zipfile_path, csv_path=metric_path, csv=csv_content)


def save_weights_in_zip(zipfile_path, weights_path, weights):
    with zipfile.ZipFile(zipfile_path, 'a') as zipf:
        weights_content = io.BytesIO()
        torch.save(weights, weights_content)
        zipf.writestr(weights_path, weights_content.getvalue())


def create_folders_in_zip(zipfile_path, folder_names):
    with zipfile.ZipFile(zipfile_path, 'a') as zipf:
        for folder_name in folder_names:
            zipf.writestr(f"{folder_name}/", '')


def count_experiments(output_folder):
    current_experiment = 0
    if os.path.isdir(output_folder):
        output_folder_files = os.listdir(output_folder)
        for file in output_folder_files:
            if file.startswith('experiment_') and file.endswith('.zip'):
                current_experiment += 1
    else:
        os.mkdir(output_folder)
        current_experiment = 1

    return current_experiment


def save_output(output_folder, weights=None, metrics=None, eval_output=None,
                additional_data=None):  # TODO: Decomposite for fit and eval output

    experiment_num = count_experiments(output_folder) + 1

    zipfile_path = os.path.join(output_folder, f'experiment_{experiment_num}.zip')

    folder_names = []

    if weights:
        folder_names.append("weights")

    if metrics:
        folder_names.append("metrics")

    if eval_output:
        folder_names.append("eval_output")

    if additional_data:
        folder_names.append("additional_data")

    create_folders_in_zip(zipfile_path=zipfile_path, folder_names=folder_names)

    if weights:
        weights_path = 'weights/weights.pth'
        save_weights_in_zip(zipfile_path=zipfile_path, weights_path=weights_path, weights=weights)

    if metrics:
        for metric in metrics:
            metric_path = 'metrics/' + metric.name + '.csv'
            save_metric_in_zip(zipfile_path=zipfile_path, metric_path=metric_path, metric=metric)

    if eval_output:
        eval_output_path = 'eval_output/output.csv'
        eval_output_df = pd.DataFrame(data={'value': eval_output})
        eval_output_csv = eval_output_df.to_csv(index=False)
        save_csv_in_zip(zipfile_path=zipfile_path, csv_path=eval_output_path, csv=eval_output_csv)

    if additional_data:
        additional_data_path = 'additional_data/' + "additional_data.csv"
        additional_data_df = pd.DataFrame(data=additional_data)
        additional_data_csv = additional_data_df.to_csv(index=False)
        save_csv_in_zip(zipfile_path=zipfile_path, csv_path=additional_data_path, csv=additional_data_csv)
