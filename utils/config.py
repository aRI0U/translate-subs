from typing import Any, Mapping, Sequence, Union

import yaml

import callbacks
from process import SubtitlesProcessor


def instantiate_callbacks(callbacks_config: Sequence[Union[Mapping[str, Any], str]]) -> Sequence[callbacks.Callback]:
    callbacks_list = []
    for callback_dict in callbacks_config:
        if isinstance(callback_dict, str):
            callback = getattr(callbacks, callback_dict)()
        elif isinstance(callback_dict, dict):
            callback = getattr(callbacks, callback_dict["callback_name"])(**callback_dict.get("callback_args", {}))
        else:
            raise TypeError("Invalid callback formatting in config file")
        callbacks_list.append(callback)

    return callbacks_list


def parse_config(config_file: str) -> SubtitlesProcessor:
    with open(config_file) as f:
        config = yaml.load(f, yaml.Loader)

    # eventually instantiate objects
    translator_args = config.get("translator")
    if translator_args is not None:
        from translate import Translator
        config["translator"] = Translator(**translator_args)

    splitter_args = config.get("splitter")
    if splitter_args is not None:
        from split.score import ClauseSplitter
        config["splitter"] = ClauseSplitter(**splitter_args)

    callbacks_config = config.get("callbacks")
    if callbacks_config is not None:
        config["callbacks"] = instantiate_callbacks(callbacks_config)

    return SubtitlesProcessor(**config)


if __name__ == "__main__":
    parse_config("config/default.yaml")
