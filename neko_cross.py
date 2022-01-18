import os
import argparse

import numpy as np
from sklearn.model_selection import KFold

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Flatten, Dense, Dropout, Input
from tensorflow.keras.optimizers import RMSprop, SGD
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.layers import Conv2D, MaxPooling2D
#from tensorflow.keras.applications.vgg16 import VGG16

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# 入力データの形状：画像の場合は画像サイズとチャネル数
INPUT_SHAPE = (150, 150, 3)


def read_data(data_file):
    return np.load(data_file, allow_pickle=True)


def build_model(num_categories):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=INPUT_SHAPE))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation="relu"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation="relu"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(256, activation="relu"))
    model.add(Dense(num_categories, activation="sigmoid"))

    model.compile(loss=categorical_crossentropy,
                  optimizer=RMSprop(learning_rate=1e-4),
                  metrics=["acc"])
    return model


def init_train_records(rec):
    # 学習経過記録用の配列を作成する
    records = []
    epochs = list(rec.history.values())[0]
    for _ in epochs:
        key_records = {}
        for k in rec.history.keys():
            key_records[k] = []
        records.append(key_records)
    return records


def store_train_record(records, rec):
    # foldごとの学習経過を記録する
    for k in rec.history.keys():
        for e, v in enumerate(rec.history[k]):
            records[e][k].append(v)


def calc_train_record_stats(records):
    # foldごとの学習経過記録の平均と標準偏差を計算
    train_stat_records = []
    for epoch_record in records:
        epoch_stats = {}
        for k in epoch_record.keys():
            epoch_stats[k] = {"ave": np.mean(epoch_record[k]),
                              "std": np.std(epoch_record[k])}
        train_stat_records.append(epoch_stats)
    return train_stat_records


def train(inputs, targets, num_categories, num_epochs, batch_size, num_folds=5, verbose=1):
    # kerasで扱えるようにcategoriesをベクトルに変換
    targets = to_categorical(targets, num_categories)

    # Define the K-fold Cross Validator
    kfold = KFold(n_splits=num_folds, shuffle=True)

    # 学習経過の記録
    train_records = None

    # K-fold Cross Validation model evaluation
    fold_no = 0
    for train, test in kfold.split(inputs, targets):
        # モデルの作成
        model = build_model(num_categories)

        # training
        record = model.fit(inputs[train], targets[train],
                           epochs=num_epochs, batch_size=batch_size,
                           validation_data=(inputs[test], targets[test]),
                           verbose=(1 < verbose))
        if train_records is None:  # 初回に学習経過記録用の配列を作成
            train_records = init_train_records(record)
        store_train_record(train_records, record)

        # 最後にテストして結果を表示
        s = model.evaluate(inputs[test], targets[test], verbose=0)
        if 0 < verbose:
            msg = "Fold {}: ".format(fold_no + 1)
            for idx, metrics_name in enumerate(model.metrics_names):
                msg = msg + " {} = {}".format(metrics_name, s[idx])
            print(msg)

        fold_no = fold_no + 1

    # foldごとの平均と標準偏差を計算
    train_stat_records = calc_train_record_stats(train_records)

    return train_stat_records


def parse_args():
    parser = argparse.ArgumentParser(description="Train model.")
    parser.add_argument("-d", "--data_file", type=str, nargs=1,
                        help="Data file.")
    parser.add_argument("-e", "--epochs", type=int, default=10,
                        help="Epochs.")
    parser.add_argument("-b", "--batch_size", type=int, default=20,
                        help="Batch size.")
    parser.add_argument("-f", "--num_folds", type=int, default=5,
                        help="# of folds in Cross Validation.")
    parser.add_argument("-r", "--results", type=str,
                        help="File to which results will be saved.")
    parser.add_argument("-v", "--verbose", type=int, default=1,
                        help="Set verbose level.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    inputs, targets, num_categories = read_data(args.data_file[0])
    train_stat_records = train(inputs,
                               targets,
                               num_categories,
                               args.epochs,
                               args.batch_size,
                               args.num_folds,
                               args.verbose)
    if args.results is not None:
        np.save(args.results, train_stat_records)
    else:
        # 学習経過の記録用ファイルが指定されていなければ画面に表示
        for epoch, epoch_stat in enumerate(train_stat_records):
            msg = "{}".format(epoch + 1)
            for metric in train_stat_records[0].keys():
                ave = epoch_stat[metric]["ave"]
                std = epoch_stat[metric]["std"]
                msg = msg + ", {}: {} ({})".format(metric, ave, std)
            print(msg)
