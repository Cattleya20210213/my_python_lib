"""ファイル操作モジュール

Todo:
    * 文字コード変換処理の実装
    * ファイル書き込み処理の実装
"""

__default_encoding__ = "utf-8"

import os
import errno
import shutil
import glob
import json


def get_file_list(src_dir: str, suffix: str = '', prefix: str = '') -> list:
    """ファイル一覧を取得します

    Args:
        src_dir (str): 読み込み先ディレクトリ
        suffix (str, optional): ファイル名の接頭語
        prefix (str, optional): ファイル名の接尾語

    Returns:
        list: [description]
    """
    return glob.glob('{}/{}*{}'.format(src_dir, suffix, prefix))


def read_file(filepath: str, encoding: str = __default_encoding__, is_binary: bool = False):
    """ファイルを読み込み、中身を文字列として応答します。

    Args:
        filepath (str): 読み込むファイルのパス
        encoding (str, optional): ファイルの文字コード デフォルト値:"utf-8".
        is_binary (bool, optional): バイナリモードで読み込むかどうか デフォルト値:"False".
    """

    with open(filepath, mode="rb" if is_binary else "r", encoding=encoding) as file_obj:
        context = file_obj.read()

    return context


def read_json_file(filepath: str, encoding: str = __default_encoding__) -> dict:
    """JSONファイルを読み込み、その内容をオブジェクトとして応答します。

    Args:
        filepath (str): ファイルのパス
        encoding (str, optional): ファイルの文字列

    Returns:
        dict: parseされたJSONのオブジェクトデフォルト値:"utf-8"
    """

    return json.loads(read_file(filepath, encoding=encoding))


def read_file_lines(filepath: str, encoding: str = __default_encoding__) -> list:
    """ファイルを読み込み、中身を文字列を行単位の配列として応答します。

    Args:
        filepath (str): 読み込むファイルのパス
        encoding (str, optional): 読み込むファイルの文字コード デフォルト値:"utf-8"
    """

    context = read_file(filepath, encoding=encoding)
    return context.split('\n')


def copy_file(src: str, dest: str):
    """指定のパスにファイルをコピーします。

    Args:
        src (str): コピー元ファイルのパス
        dest (str): 出力先のパス（ディレクトリ指定の場合、元のファイル名でコピーされます。）
    """

    if os.path.basename(dest):
        dest = os.path.join(dest, os.path.basename(src))

    shutil.copyfile(src, dest)


def copy_files(src_list: list, dest_dir: str, ignore_none_file: bool = False):
    """指定したディレクトリに指定した複数のファイルをコピーします。

    Args:
        src_list (list): コピー元ファイルの一覧
        dest_dir (str): コピー先ディレクトリ
        ignore_none_file (bool, optional): 存在しないファイルを無視するか. デフォルト値:False.
    """

    __validate_path_dir__(dest_dir)

    file_path_list = src_list.copy()  # 参照渡しなので浅いコピーをしておく
    none_exist_file_path_list = __pop_none_file_paths__(file_path_list)

    if(none_exist_file_path_list and not ignore_none_file):
        __raise_fnf_error__(', '.join(none_exist_file_path_list))
    del none_exist_file_path_list

    for src in file_path_list:
        # dest_dirはディレクトリだとわかりきっているのでcopy_file関数は使わない
        shutil.copyfile(src, os.path.join(dest_dir, os.path.basename(src)))


def convert_file_charset(src_path: str, dest_path: str, src_encoding: str, dest_encoding: str):
    """ファイルの文字コードを変換します。

    Args:
        src_path (str): 参照元ファイルのパス
        dest_path (str): 変換後のファイルパス
        src_encoding (str): 参照元ファイルの文字コード
        dest_encoding (str): 変換後のファイルの文字コード
    """
    with open(src_path, mode='r', encoding=src_encoding) as src_file_obj:
        with open(dest_path, mode='w', encoding=dest_encoding) as dest_file_obj:
            dest_file_obj.write(src_file_obj.read())


def __pop_none_file_paths__(file_path_list: list) -> list:
    """ファイルパスのリストから存在しないファイルの一覧を取得、削除します。

    Args:
        file_path_list (list): ファイルのパス一覧

    Returns:
        list: 存在しないファイルの一覧
    """
    none_file_idx_list = [i for i, item in enumerate(
        file_path_list) if not os.path.isfile(item)]
    none_file_idx_list.reverse()  # この後popするので降順にしておく。
    none_file_list = [file_path_list.pop(i)
                      for i in none_file_idx_list]  # 参照渡しを利用
    none_file_list.reverse()  # 降順をもう一度ひっくり返し戻す。
    return none_file_list


def __validate_path_dir__(path: str):
    """ディレクトリが存在するか確認します。

    Args:
        path (str): 確認するファイルパス
    """
    if not os.path.isdir(str):
        __raise_fnf_error__(path)


def __raise_fnf_error__(path: str):
    """ FileNotFoundErrorを出します。

    Args:
        path (str): ファイルパス

    Raises:
        __create_fnt_error__: 存在しないファイルやディレクトリが存在します。
    """
    # 一元化しておくことで関数内で呼び出している関数の変更に柔軟に対応できるようにする。
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
