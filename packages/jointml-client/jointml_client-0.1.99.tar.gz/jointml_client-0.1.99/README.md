# Joint-ml
 
Данный пакет помогает реализовать удобный интрерфейс для использования вашей модели
в федеративном обучении на нашей платформе. 

## Установка 

Устанавливаем joint-ml с помощью pip:
```sh
pip install jointml-client
```

## Создание клиента

### Требования
Для установки и запуска проекта, необходим Python>=3.8.0


### Шаг 1: Создаем модуль
Создайте python файл, который называется "client_methods.py" в корневом каталоге вашего git репозитория:
```sh
client_methods.py
```

### Шаг 2: В файле client_methods.py необходимо реализовать методы: load_model, get_dataset, train, test: 

#### Метод 1: load_model: 
*Метод для генерации модели*.   
На вход будут подаваться параметры, указанные на сервисе как Init Parameters.
Обязательные параметры, которые необходимо учитывать разработчику ML:  
**init_parameters** - параметры, которые разработчик ML указывает на сайте в разделе Init Parameters  
*Возвращает: (nn.Module) - модель*.

```python
def load_model(n_features, hidden_dim) -> nn.Module:
    model = Net(n_features, hidden_dim)
    return model
```

#### Метод 2: get_dataset: 
*Метод для чтения, предобработки и разбития датасета(with_split=True).*  
На вход будут подаваться dataset_path, with_split,
а также параметры, которые разработчик ML укажет в коде как необходимые(специфические для каждого отдельного пользователя)
Тут описывается вся логика предобработки датасета.
Обязательные параметры, которые необходимо учитывать разработчику ML:  
- **dataset_path(str)** - путь до csv-файла с датасетом;
- **with_split(bool)** - булева переменная, говорящая о необходимости разбития датасета на выборки(train, valid, test). 
Если True, тогда следует после предобработки данных разбить их на одну из следующих выборок - (train, test), (train, valid, test). 
Если False, тогда требуется лишь предобработка данных и возвращение лишь подготовленного датасета (
в дальнейшем будет использоваться для получения предсказаний модели на данных пользователя).

*Возвращает один из следующих кортежей:*  
- *(torch.utils.data.Dataset, torch.utils.data.Dataset, torch.utils.data.Dataset) - возвращается при with_split=True. В будущем используется как train_set, valid_set и test_set*  
- *(torch.utils.data.Dataset, torch.utils.data.Dataset) - возвращается при with_split=True. В будущем используется как train_set и test_set*  
- *(torch.utils.data.Dataset) - возвращается при with_split=False. В будущем используется как test_set(выборка для тестирования модели на весах)*  

```python
def get_dataset(dataset_path: str, with_split: bool, test_size: float, shuffle: bool) -> Union[
    Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset, torch.utils.data.Dataset],
    Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset], Tuple[torch.utils.data.Dataset]]:
    transactions, labels = load_dataset(dataset_path)
    if with_split:
        x_train, x_test, y_train, y_test = train_test_split(transactions, labels, test_size=test_size, shuffle=shuffle)
        x_train, x_test = preprocess_data(x_train, x_test)

        train_set = TransactionsDataset(x_train, y_train)
        test_set = TransactionsDataset(x_test, y_test)

        return train_set, test_set
    else:
        x_test = preprocess_set(transactions)
        test_set = TransactionsDataset(x_test, labels)
        return test_set
```

#### Метод 3: train:
*Метод для тренировки модели, полученной из метода load_model.*  
На вход будут подаваться: модель, сгенерированная методом load_model, train_set полученный из метода get_dataset, valid_set(опционально) полученный из
метода get_dataset(если возврат выборки предусмотрен разработчиком ML в методе get_dataset), а также
параметры, которые разработчик ML укажет в коде как необходимые(специфические для каждого отдельного пользователя).  
Обязательные параметры, которые необходимо учитывать разработчику ML:
- **model(nn.Module)** - модель, полученная из метода load_model;
- **train_set(torch.utils.data.Dataset)** - тренировочная выборка, полученная из метода get_dataset;
- **valid_set(torch.utils.data.Dataset)** - валидационная выборка, полученная из метода get_dataset; Подается на вход только если в методе
- **get_dataset предусмотрено получение** валидационной выборки и ее возврата;
- **train_parameters** - параметры, которые разработчик ML указывает на сайте в разделе Train Parameters.

*Возвращает (List[Metric], nn.Module) - кортеж состоящий из:*  
*1. Список метрик полученных в ходе обучения;*  
*2. Обученной модели.*

```python
def get_dataset(dataset_path: str, with_split: bool, test_size: float, shuffle: bool) -> Union[
    Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset, torch.utils.data.Dataset],
    Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset], Tuple[torch.utils.data.Dataset]]:
    transactions, labels = load_dataset(dataset_path)
    if with_split:
        x_train, x_test, y_train, y_test = train_test_split(transactions, labels, test_size=test_size, shuffle=shuffle)
        x_train, x_test = preprocess_data(x_train, x_test)

        train_set = TransactionsDataset(x_train, y_train)
        test_set = TransactionsDataset(x_test, y_test)

        return train_set, test_set
    else:
        x_test = preprocess_set(transactions)
        test_set = TransactionsDataset(x_test, labels)
        return test_set
```

#### Метод 4: test:
*Метод для тестирования модели на данных.*  
На вход подается model, полученная из load_model; return_output и булева переменная,
говорящая о необходимости возврата выхода из модели на данных;
test_set - тестировочная выборка, полученная из get_dataset, 
а также параметры, которые разработчик ML укажет в коде как необходимые(специфические для каждого отдельного пользователя).
Обязательные параметры, которые необходимо учитывать разработчику ML:
- **model(nn.Module)** - модель, полученный из метода load_model
- **test_set(torch.utils.data.Dataset)** - тестировочная выборка, полученная из метода get_dataset
- **return_output(bool)** - булева переменная, говорящая о необходимости возвращать ответы модели
- **test_parameters** - параметры, которые разработчик ML указывает на сайте в разделе Test Parameters

*Возвращает один из следующих кортежей:*  
- *(List[Metric]) - метрики полученные в ходе тестирования модели на данных;*
- *(List[Metric], list) - метрики и ответы модели полученные в ходе тестирования модели на данных(только если return_output=True).*

```python
def test(model: torch.nn.Module, test_set: torch.utils.data.Dataset, return_output: bool) -> Union[
    Tuple[List[Metric]], Tuple[List[Metric], list]]:
    test_loss = 0.0
    model.eval()
    loss_fn = BCELoss()

    test_dataloader = DataLoader(test_set)

    outputs = []
    labels = np.array([])

    for i, data in enumerate(test_dataloader):
        transactions, label = data['transaction'], data['label']

        transactions = transactions.reshape(transactions.shape[0], 1, transactions.shape[1])
        output = model(transactions)

        loss = loss_fn(output, label)

        test_loss += loss.item()

        outputs.append(output.cpu().detach().numpy().reshape(-1))
        labels = np.hstack([labels, label.cpu().reshape(-1)])

    test_loss /= len(test_dataloader)

    test_loss_metric = Metric(name="test_loss")
    test_loss_metric.log_value(test_loss)

    test_roc_auc_score = roc_auc_score(labels, np.array(outputs))

    test_roc_auc_score_metric = Metric(name="test_roc_auc_score")
    test_roc_auc_score_metric.log_value(test_roc_auc_score)


    if return_output:
        return ([test_loss_metric, test_roc_auc_score_metric], outputs)
    else:
        return ([test_loss_metric, test_roc_auc_score_metric])

```

## Выкладываем код с реализованным классом Сlient в GitHub
Необходимо выложить готовый клиент в открытый GitHub репозиторий в ветку с именем master
