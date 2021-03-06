#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020 NXP
#
# SPDX-License-Identifier: BSD-3-Clause
""" Tests for key management (generating public/private key)
"""
from os import path

from spsdk.crypto.keys_management import generate_rsa_private_key, generate_rsa_public_key, \
    save_private_key, save_public_key


def test_keys_generation_2048(tmpdir):
    priv_key = generate_rsa_private_key()
    pub_key = generate_rsa_public_key(priv_key)
    save_private_key(priv_key, path.join(tmpdir, "priv_2048.pem"))
    save_public_key(pub_key, path.join(tmpdir, "pub_2048.pem"))
    assert path.isfile(path.join(tmpdir, "priv_2048.pem"))
    assert path.isfile(path.join(tmpdir, "pub_2048.pem"))


def test_keys_generation_3072(tmpdir):
    priv_key = generate_rsa_private_key(key_size=3072)
    pub_key = generate_rsa_public_key(priv_key)
    save_private_key(priv_key, path.join(tmpdir, "priv_3072.pem"))
    save_public_key(pub_key, path.join(tmpdir, "pub_3072.pem"))
    assert path.isfile(path.join(tmpdir, "priv_3072.pem"))
    assert path.isfile(path.join(tmpdir, "pub_3072.pem"))


def test_keys_generation_4096(tmpdir):
    priv_key = generate_rsa_private_key(key_size=4096)
    pub_key = generate_rsa_public_key(priv_key)
    save_private_key(priv_key, path.join(tmpdir, "priv_4096.pem"))
    save_public_key(pub_key, path.join(tmpdir, "pub_4096.pem"))
    assert path.isfile(path.join(tmpdir, "priv_4096.pem"))
    assert path.isfile(path.join(tmpdir, "pub_4096.pem"))