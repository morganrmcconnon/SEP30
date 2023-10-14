#!/usr/bin/env python3
# @Zijian Wang

from random import shuffle
import json
import hashlib
import logging
import numpy as np
# # I could not install pycld2 or gcld3 into Windows 11, Python 3.11
# # so I used googletrans instead
# # Another option is https://github.com/pemistahl/lingua-py
# import pycld2 as cld2
# from lingua import Language, LanguageDetectorBuilder
from googletrans import Translator
import random
import re
import requests
import shutil
import tempfile
import torch
from torch.nn.utils.rnn import *
from tqdm import tqdm

from .consts import *
from .preprocess import download_resize_img

translator = Translator()

logger = logging.getLogger(__name__)


class DotDict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def set_seed(seed=0):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.device_count() > 0:
        torch.cuda.manual_seed_all(seed)


def pack_wrapper(sents, lengths):
    lengths_sorted, idx_sorted = lengths.sort(descending=True)
    sents_sorted = sents[idx_sorted]
    packed = pack_padded_sequence(sents_sorted, lengths_sorted.cpu(), batch_first=True)
    return packed, idx_sorted


def unpack_wrapper(sents, idx_unsort):
    h, _ = pad_packed_sequence(sents, batch_first=True)
    h = torch.zeros_like(h).scatter_(0, idx_unsort.unsqueeze(1).unsqueeze(1).expand(-1, h.shape[1], h.shape[2]), h)
    return h


def get_lang(sent):
    # lang = cld2.detect(''.join([i for i in sent if i.isprintable()]), bestEffort=True)[2][0][1]
    # lang = language_detector.detect_language_of(sent)
    # if(lang == None):
    #     return UNKNOWN_LANG
    # lang = lang.iso_code_639_1.name.lower()
    lang = translator.detect(sent).lang
    if(type(lang) == list):
        lang = lang[0] # Just temporary
    return UNKNOWN_LANG if lang not in LANGS else lang


def normalize_url(sent):
    return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '\u20CC', sent)


def normalize_space(sent):
    return sent.replace("\t", " ").replace("\n", " ").replace("\r", " ")


def fetch_pretrained_model(model_name, model_path):
    # Edited from https://github.com/huggingface/pytorch-pretrained-BERT/blob/68a889ee43916380f26a3c995e1638af41d75066/pytorch_pretrained_bert/file_utils.py
    # TODO: check whether the license from huggingface works with ours
    assert model_name in PRETRAINED_MODEL_ARCHIVE_MAP
    model_urls = PRETRAINED_MODEL_ARCHIVE_MAP[model_name]
    shuffle(model_urls)
    download_flag = False
    for idx, model_url in enumerate(model_urls):
        try:
            temp_file = tempfile.NamedTemporaryFile()
            logger.info(f'{model_path} not found in cache, downloading from {model_url} to {temp_file.name}')

            req = requests.get(model_url, stream=True)
            content_length = req.headers.get('Content-Length')
            total = int(content_length) if content_length is not None else None
            progress = tqdm(unit="KB", total=round(total / 1024), disable=logging.root.level>=logging.WARN)
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    progress.update(1)
                    temp_file.write(chunk)
            progress.close()
            temp_file.flush()
            temp_file.seek(0)
            download_flag = True
        except Exception as e:
            logger.warning(f'Download from {idx + 1}/{len(model_urls)} mirror failed with an exception of\n{str(e)}')
            try:
                temp_file.close()
            except Exception as e_file:
                logger.warning(f'temp_file failed with an exception of \n{str(e_file)}')
            continue

        if not download_flag:
            logging.warning(f'Download from all mirrors failed. Please retry.')
            return

        logger.info(f'Model {model_name} was downloaded to a tmp file.')
        logger.info(f'Copying tmp file to {model_path}.')
        with open(model_path, 'wb') as cache_file:
            shutil.copyfileobj(temp_file, cache_file)
        logger.info(f'Copied tmp model file to {model_path}.')
        temp_file.close()

        if download_flag and check_file_md5(model_name, model_path):
            break


def check_file_md5(model_name, model_path):
    assert model_name in PRETRAINED_MODEL_MD5_MAP
    logger.info(f'Checking MD5 for model {model_name} at {model_path}')
    correct_md5 = PRETRAINED_MODEL_MD5_MAP[model_name]
    downloaded_md5 = hashlib.md5(open(model_path, 'rb').read()).hexdigest()
    if correct_md5 == downloaded_md5:
        logger.info('MD5s match.')
        return True
    else:
        logger.error('MD5s mismatch. Consider clean your tmp dir (default: `./m3_tmp`) and retry,'
                     ' or download from the link in our github repo.')
        return False


def get_extension(img_path):
    if '.' not in img_path.split('/')[-1]:
        return 'png'
    dotpos = img_path.rfind(".")
    extension = img_path[dotpos + 1:]
    if extension.lower() == "gif":
        return "png"
    return extension


def download_image_from_jsonl_object(input, cache_dir, img_path_key=None,  resize_img=True, keep_full_size_img=False):
        """
        A method to download image given the input jsonl object

        Parameters:
        -----------
        cache_dir: str
            The directory to store the downloaded images
        input: dict

            `input` is either a Twitter tweet object (https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object) or a Twitter user object (https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object)
            
            `input` can be a string in json format or a dictionary or an object

        img_path_key: str
            The key to the image path in the input object. If None, the function will try to find the image path in the input object.

        resize_img: bool
            Whether to resize the image to 224x224. Default: True

        keep_full_size_img: bool
            Whether to keep the full size image. Default: False

        Returns:
        --------
        """

        if isinstance(input, str): input = json.loads(input)

        # Detect user
        user = input["user"] if "user" in input else input

        if img_path_key != None and img_path_key in user:
            
            img_url = user[img_path_key]
            
            if resize_img:
                img_file_resize = f"{cache_dir}/{user['id_str']}_224x224.{get_extension(img_url)}"
                download_resize_img(img_url, img_file_resize)
            else:
                img_file_resize = img_url

        elif img_path_key != None and img_path_key in input:
            
            img_url = input[img_path_key]
            
            if resize_img:
                img_file_resize = f"{cache_dir}/{user['id_str']}_224x224.{get_extension(img_url)}"
                download_resize_img(img_url, img_file_resize)
            else:
                img_file_resize = img_url

        elif user["default_profile_image"]:
            # Default profile image
            img_file_resize = TW_DEFAULT_PROFILE_IMG

        else:
            img_url = user["profile_image_url_https"]
            img_url = img_url.replace("_normal", "_400x400")
            dotpos = img_url.rfind(".")
            img_file_full = f"{cache_dir}/{user['id_str']}.{img_url[dotpos + 1:]}"
            img_file_resize = f"{cache_dir}/{user['id_str']}_224x224.{get_extension(img_url)}"
            
            if not os.path.isfile(img_file_resize):
                if keep_full_size_img:
                    download_resize_img(img_url, img_file_resize, img_file_full)
                else:
                    download_resize_img(img_url, img_file_resize)
            
        # check if an error occurred and the image was not downloaded
        if not os.path.exists(img_file_resize):
            img_file_resize = TW_DEFAULT_PROFILE_IMG

        return img_file_resize


def transform_jsonl_object_for_m3inference_text_model(input, translate_description=False, use_language_detector=False, prioritize_language_detector=False):
        """
        A method to transform the input jsonl object to the format that can be used by the m3inference text model

        input is either a Twitter tweet object (https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object)
            or a Twitter user object (https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object)
        """
        if isinstance(input, str):
            input = json.loads(input)

        # Detect user
        user = input["user"] if "user" in input else input

        # Detect description
        description = user["description"]
        if description == None:
            description = ""

        # Detect language
        
        lang = None

        if translate_description:
            description = translator.translate(description).text
            lang = 'en'
            
        if lang == None and 'lang' in user:
            lang = user['lang']
        
        if lang == None and 'lang' in input:
            lang = input['lang']

        if not translate_description and prioritize_language_detector:
            detection = translator.detect(description)
            
            if(type(detection.lang) == list):
                # create a map of language to confidence
                confidence_map = dict(zip(detection.lang, detection.confidence))

                if lang in confidence_map:
                    confidence_map[lang] += 0.5
                # get the language with the highest confidence
                lang = max(confidence_map, key=confidence_map.get)
            else:
                lang = detection.lang

        if lang == None and description != "" and use_language_detector:
            lang = translator.detect(description).lang
        
        if lang not in LANGS:
            lang = UNKNOWN_LANG

        output = {
            "description": description,
            "id": user["id_str"],
            # "img_path": img_file_resize if download_img else TW_DEFAULT_PROFILE_IMG,
            "lang": lang,
            "name": user["name"],
            "screen_name": user["screen_name"]
        }

        return output