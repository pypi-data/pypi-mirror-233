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
    assert vigenere('abc', True, 'key') == 'kfa'
    assert vigenere('kfa', False, 'key') == 'abc'
    assert vigenere('ABC', True, 'KEY') == 'kfa'
    assert vigenere('123', True, 'key') == '123'
    assert vigenere('abc123', True, 'key') == 'kfa123'
    assert vigenere('!@#', True, 'key') == '!@#'


def test_playfair():
    assert playfair('Hide the gold', True, 'key') == 'COLDZOADIMGV'
    assert playfair('COLDZOADIMGV', False, 'key') == 'HIDETHEGOLDX'
    assert playfair('HELLO WORLD', True, 'key') == 'DBNVMIZMQMGV'
    assert playfair('DBNVMIZMQMGV', False, 'key') == 'HELXLOWORLDX'
    assert playfair('hello world', True, 'key') == 'DBNVMIZMQMGV'
    assert playfair('DBNVMIZMQMGV', False, 'key') == 'HELXLOWORLDX'
    assert playfair('hello there\n', True, 'key') == 'DBNVMIZOYQAV'
