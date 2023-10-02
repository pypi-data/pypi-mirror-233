#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funçoes auxiliares.

pynad v3
Ipea - 2023
Rafael Guerreiro Osorio
"""

from time import sleep, time

# ANSI TERMINAL COLUNAS
TCOLS = 80
BARRA = '-' * 80
ARROW = '>>'

# ANSI TERMINAL ESCAPE SEQUENCES
CRCLR = '\r\033[K'  # CR + limpa linha
UPCLR = '\r\033[1A\033[K'  # CR + sobe uma linha + limpa linha

# ESTILOS
HEADER_F = '\033[1;38;5;193m'
HEADER_B = '\033[48;5;30m'
HEADER_W = '\033[1;38;5;210m'
COPIA_F = '\033[1;38;5;30m'
COPIA_B = '\033[48;5;193m'
COPIA_H = '\033[38;5;22m'
COPIA_W = '\033[38;5;160m'

# versão do 7 zip
A7Z = {'Windows': '7z', 'Linux': '7za', 'Darwin': '7z'}


def cli_main():
    """Prepara o terminal."""
    print('\033c', end='')  # limpa o terminal
    print(f'\033[8;24;{TCOLS}t', end='')  # formata linhas e colunas
    print(HEADER_B + HEADER_F, end='')
    for _linha in range(24):
        print(' ' * TCOLS, end='')
    print('\033[H', end='')
    print('\nPYNAD - MICRODADOS DA PNADC\n')


def continuar(pergunta='Continuar'):
    """Pergunta se é para continuar um processo."""
    sleep(0.05)
    resp = ''
    print()
    while resp not in ('s', 'y', 'n'):
        resp = input(f'{UPCLR}{pergunta}? s/n' +
                     f' {ARROW} ').lower()
    if resp == 'n':
        return False
    return True


def pausar():
    """Interrompe um processo, qualquer tecla continua."""
    sleep(0.05)
    input('Pressione ENTER para continuar')


def elapsed(start):
    """Retorna string com o tempo formatado desde start."""
    end = time()
    days = int((end - start) / 86400)
    hours = int((end - start) / 3600)
    mins = int(((end - start) - hours * 3600) / 60)
    segs = int((end - start) - hours * 3600 - mins * 60)
    mils = int(((end - start) - int(end - start)) * 1000)
    if days:
        result = f'{days:.0f} dias'
    elif hours:
        result = f'{hours:.0f}h {mins:0.0f}m {segs:0.0f}s'
    elif mins:
        result = f'{mins:0.0f}m {segs:0.0f}s'
    elif segs:
        result = f'{segs:0.0f}s'
    else:
        result = f'{mils:0.0f}ms'
    return result


def sizestr(size, lang='PT'):
    """Retorna string com o tamanho formatado."""
    if size > 10 ** 12:
        sizes = f'{size / 10 ** 12:.1f}TB'
    if size > 10 ** 9:
        sizes = f'{size / 10 ** 9:.1f}GB'
    elif size > 10 ** 6:
        sizes = f'{size / 10 ** 6:.1f}MB'
    elif size > 10 ** 3:
        sizes = f'{size / 10 ** 3:.1f}KB'
    else:
        sizes = f'{size:.1f} bytes'
    if lang == 'PT':
        sizes = sizes.replace('.', ',')
    return sizes
