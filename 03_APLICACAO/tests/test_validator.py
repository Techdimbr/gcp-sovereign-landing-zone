#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes unitários para o validador do GCP Sovereign Landing Zone.
"""

import unittest
from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from validator import validar_arquivo_terraform

class TestTerraformSecurityValidator(unittest.TestCase):
    def test_main_tf_e_conforme(self):
        main_tf = SRC_DIR / "main.tf"
        self.assertTrue(main_tf.exists())
        cheques = validar_arquivo_terraform(main_tf)
        for regra, sucesso, msg in cheques:
            self.assertTrue(sucesso, f"Falha na regra '{regra}': {msg}")

if __name__ == "__main__":
    unittest.main()
