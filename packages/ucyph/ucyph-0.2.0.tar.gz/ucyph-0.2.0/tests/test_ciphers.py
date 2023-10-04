from src.ucyph.ciphers import *


def test_caesar():
    assert caesar('abc', True) == 'def'
    assert caesar('def', False) == 'abc'
    assert caesar('ABC', True) == 'def'
    assert caesar('123', True) == '123'
    assert caesar('abc123', True) == 'def123'
    assert caesar('!@#', True) == '!@#'


def test_rot13():
    assert rot13('abc') == 'nop'
    assert rot13('nop') == 'abc'
    assert rot13('ABC') == 'NOP'
    assert rot13('123') == '123'
    assert rot13('abc123') == 'nop123'


def test_rot47():
    assert rot47('abc') == '234'
    assert rot47('234') == 'abc'
    assert rot47('ABC') == 'pqr'
    assert rot47('123') == '`ab'
    assert rot47('abc123') == '234`ab'
    assert rot47('!@#') == 'PoR'


def test_vigenere():
    assert vigenere('abc', 'key', True) == 'kfa'
    assert vigenere('kfa', 'key', False) == 'abc'
    assert vigenere('ABC', 'KEY', True) == 'kfa'
    assert vigenere('123', 'key', True) == '123'
    assert vigenere('abc123', 'key', True) == 'kfa123'
    assert vigenere('!@#', 'key', True) == '!@#'


def test_playfair():
    assert playfair('Hide the gold', 'key', True) == 'COLDZOADIMGV'
    assert playfair('COLDZOADIMGV', 'key', False) == 'HIDETHEGOLDX'
    assert playfair('HELLO WORLD', 'key', True) == 'DBNVMIZMQMGV'
    assert playfair('DBNVMIZMQMGV', 'key', False) == 'HELXLOWORLDX'
    assert playfair('hello world', 'key', True) == 'DBNVMIZMQMGV'
    assert playfair('DBNVMIZMQMGV', 'key', False) == 'HELXLOWORLDX'
    assert playfair('hello there\n', 'key', True) == 'DBNVMIZOYQAV'
