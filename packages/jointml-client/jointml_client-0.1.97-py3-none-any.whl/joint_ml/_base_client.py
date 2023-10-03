import torch
from torch import nn
import torch.utils.data

from joint_ml._utils import get_fn_parameters, save_output
from joint_ml._typing import WEIGHTS_TYPE

_get_dataset_fn_not_required_params = {
    'with_split': str
}

_train_fn_not_required_params = {
    'model': nn.Module,
    'train_set': torch.utils.data.Dataset,
    'valid_set': torch.utils.data.Dataset,
}

_test_fn_not_required_params = {
    'model': nn.Module,
    'test_set': torch.utils.data.Dataset,
    'return_output': bool
}


class Client:

    def __init__(self,
                 load_model_fn,
                 model_global_parameters=None,
                 dataset_global_parameters=None,
                 train_global_parameters=None,
                 test_global_parameters=None,
                 train_fn=None,
                 test_fn=None,
                 get_dataset_fn=None,
                 initial_weights_path=None,
                 output_folder=None):

        self.model_global_parameters = model_global_parameters
        self.dataset_global_parameters = dataset_global_parameters
        self.train_global_parameters = train_global_parameters
        self.test_global_parameters = test_global_parameters

        self.load_model_fn = load_model_fn
        self.get_dataset_fn = get_dataset_fn
        self.train_fn = train_fn
        self.test_fn = test_fn

        self.output_folder = output_folder

        if self.get_dataset_fn:
            self.get_dataset_user_required_parameters = get_fn_parameters(get_dataset_fn,
                                                                          [*list(
                                                                              _get_dataset_fn_not_required_params.keys()),
                                                                           *list(
                                                                               self.dataset_global_parameters.keys())])
        if self.train_fn:
            self.train_user_required_parameters = get_fn_parameters(train_fn,
                                                                    [*list(_train_fn_not_required_params.keys()),
                                                                     *list(self.train_global_parameters.keys())])

        if self.test_fn:
            self.test_user_required_parameters = get_fn_parameters(test_fn,
                                                                   [*list(_test_fn_not_required_params.keys()),
                                                                    *list(self.test_global_parameters.keys())])

        self.model = self.load_model_fn(
            **self.model_global_parameters) if self.model_global_parameters else self.load_model_fn()

        self.set_weights(weights=initial_weights_path)

        self.train_set, self.valid_set, self.test_set = None, None, None
        self.device = None

    def set_weights(self, weights: WEIGHTS_TYPE | None):
        if weights:
            weights = torch.load(weights)
            self.model.load_state_dict(weights)

    def get_weights(self):
        return self.model.state_dict()

    def fit(self, **kwargs):
        get_dataset_user_parameters = {}
        train_user_parameters = {}
        test_user_parameters = {}

        for arg, val in kwargs.items():
            if arg in [param['name'] for param in self.get_dataset_user_required_parameters]:
                get_dataset_user_parameters[arg] = val
            elif arg in [param['name'] for param in self.train_user_required_parameters]:
                train_user_parameters[arg] = val
            elif arg in [param['name'] for param in self.test_user_required_parameters]:
                test_user_parameters[arg] = val

        if self.device is None:
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        if self.train_set is None:
            sets = self.get_dataset_fn(with_split=True, **self.dataset_global_parameters, **get_dataset_user_parameters)
            if len(sets) == 3:
                self.train_set, self.valid_set, self.test_set = sets
            elif len(sets) == 2:
                self.train_set, self.test_set = sets
            elif len(sets) == 1:
                self.test_set = sets

        fit_metrics = []
        evaluate_metrics = []

        if self.train_set and self.valid_set:
            fit_metrics, self.model = self.train_fn(model=self.model, train_set=self.train_set,
                                                    valid_set=self.valid_set,
                                                    **self.train_global_parameters, **train_user_parameters)
        elif self.train_set:
            fit_metrics, self.model = self.train_fn(model=self.model, train_set=self.train_set,
                                                    **self.train_global_parameters, **train_user_parameters)

        if self.test_set:
            evaluate_metrics = self.test_fn(model=self.model, test_set=self.test_set, return_output=False,
                                            **self.test_global_parameters, **test_user_parameters)

        trained_weights = self.get_weights()
        metrics = [*fit_metrics, *evaluate_metrics]

        fit_additional_data = {
            'train_num_examples': [len(self.train_set)]
        }

        save_output(output_folder=self.output_folder, weights=trained_weights, metrics=metrics, additional_data=fit_additional_data)

    def evaluate(self, **kwargs):
        get_dataset_user_parameters = {}
        test_user_parameters = {}

        for arg, val in kwargs.items():
            if arg in [param['name'] for param in self.get_dataset_user_required_parameters]:
                get_dataset_user_parameters[arg] = val
            elif arg in [param['name'] for param in self.test_user_required_parameters]:
                test_user_parameters[arg] = val

        eval_set = self.test_set

        if 'dataset_path' in get_dataset_user_parameters:
            eval_set = self.get_dataset_fn(with_split=False, **self.dataset_global_parameters,
                                           **get_dataset_user_parameters)

        assert eval_set is not None

        eval_metrics, eval_output = None, None

        if 'return_output' in kwargs:
            eval_metrics, eval_output = self.test_fn(model=self.model, test_set=eval_set, return_output=True,
                                                     **self.test_global_parameters, **test_user_parameters)
        else:
            eval_metrics = self.test_fn(model=self.model, test_set=eval_set, return_output=False,
                                        **self.test_global_parameters, **test_user_parameters)

        if eval_output:
            save_output(output_folder=self.output_folder, metrics=eval_metrics, eval_output=eval_output)
        else:
            save_output(output_folder=self.output_folder, metrics=eval_metrics)
<<<<<<< Updated upstream
=======


def save_weights(weights, path):
    torch.save(weights, path)
>>>>>>> Stashed changes
