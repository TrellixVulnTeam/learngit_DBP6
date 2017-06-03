# coding: utf-8
# https://github.com/tensorflow/models/tree/master/tutorials/rnn

'''
modes -> tutorials -> rnn
	ptb
		ptb_word_lm.py
		reader.py
		reader_test.py
	translate
		data_utils.py
		seq2seq_model.py
		translate.py
	build
'''




"""Libraries to build Recurrent Neural Networks"""
from __future__ import absolute_import, division, print_function





# data_utils.py

"""Utilities for downloading data from WMT, tokenizing, vocabularies."""
import gzip
import os
import re
import tarfile

from six.moves import urllib

from tensorflow.python.platform import gfile
import tensorflow as tf 

# Special vocabulary symbols - we always put them at the start.
_PAD = b"_PAD"
_GO = b"_GO"
_EOS = b"_EOS"
_UNK = b"_UNK"
_START_VOCAB = [_PAD, _GO, _EOS, _UNK]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3

# Regular expressions used to tokenize.
_WORD_SPLIT = re.compile(b"([.,!?\"':;)(])")
_DIGIT_RE = re.compile(br"\d")

# URLs for WMT data.
_WMT_ENFR_TRAIN_URL = "http://www.statmt.org/wmt10/training-giga-fren.tar"
_WMT_ENFR_DEV_URL = "http://www.statmt.org/wmt15/dev-v2.tgz"


def maybe_download(directory, filename, url):
	"""Download filename from url unless it's already in directory."""
	if not os.path.exists(directory):
		print("Creating directory %s" % directory)
		os.mkdir(directory)
	filepath = os.path.join(directory, filename)
	if not os.path.exists(filepath):
		print("Downloading %s to %s" % (url, filepath))
		filepath, _ = urllib.request.urlretrieve(url, filepath)
		statinfo = os.stat(filepath)
		print("Successfully downloaded", filename, statinfo.st_size, "bytes.")
	return filepath

def gunzip_file(gz_path, new_path):
	"""Unzips from gz_path into new_path."""
	print("Unpacking %s to %s" % (gz_path, new_path))
	with gzip.open(gz_path, "rb") as gz_file:
		with open(new_path, "wb") as new_file:
			for line in gz_file:
				new_file.write(line)

def get_wmt_enfr_train_set(directory):
	"""Download the WMT en-fr training corpus to directory unless it's there."""
	train_path = os.path.join(directory, "giga-fren.release2.fixed")
	if not (gfile.Exists(train_path+".fr") and gfile.Exists(train_path+".en")):
		corpus_file = maybe_download(directory, "training-giga-fren.tar", _WMT_ENFR_TRAIN_URL)
		print("Extracting tar file %s" % corpus_file)
		with tarfile.open(corpus_file, "r") as corpus_tar:
			corpus_tar.extractall(directory)
		gunzip_file(train_path + ".fr.gz", train_path + ".fr")
		gunzip_file(train_path + ".en.gz", train_path + ".en")
	return train_path

def get_wmt_enfr_dev_set(directory):
	"""Download the WMT en-fr training corpus to directory unless it's there."""
	dev_name = "newtest2013"
	dev_path = os.path.join(directory, dev_name)
	if not (gfile.Exists(dev_path+".fr") and gfile.Exists(dev_path+".en")):
		dev_file = maybe_download(directory, "dev-v2.tgz", _WMT_ENFR_DEV_URL)
		print("Extracting tgz file %s" % dev_file)
		with tarfile.open(dev_file, "r:gz") as dev_tar:
			fr_dev_file = dev_tar.getmember("dev/" + dev_name + ".fr")
			en_dev_file = dev_tar.getmember("dev/" + dev_name + ".en")
			fr_dev_file.name = dev_name + ".fr" # Extract without "dev/" prefix
			en_dev_file.name = dev_name + ".en"
			dev_tar.extract(fr_dev_file, directory)
			dev_tar.extract(en_dev_file, directory)
	return dev_paths










