# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Yuri Luiz Kruger Torquato, Pedro Henrique Nascimento Souza
#    Matrícula: 202311567, 202310960
#    Turma: CC5N
#    Email: yuri.luizkt@gmail.com, pedrohenrique.nasci2020@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.
#


# Imports
import os
import pset1
import unittest

# Diretório
TEST_DIRECTORY = os.path.dirname(__file__)


# Classe para os testes de imagem:
class TestImagem(unittest.TestCase):
    def test_carregar(self):
        resultado = pset1.Imagem.carregar('test_images/centered_pixel.png')
        esperado = pset1.Imagem(11, 11,
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(resultado, esperado)
    

# Classe para os testes de inversão:
class TestInvertida(unittest.TestCase):
    def test_invertida_1(self):
        im = pset1.Imagem.carregar('test_images/centered_pixel.png')
        resultado = im.invertida()
        esperado = pset1.Imagem(11, 11,
                                [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
        self.assertEqual(resultado,  esperado)

    def test_invertida_2(self):
        # Escreva aqui o seu caso de teste
        im = pset1.Imagem(4,1, [29, 89, 136, 200])
        resultado = im.invertida()
        esperado = pset1.Imagem(4,1, [226, 166, 119, 55])
        self.assertEqual(resultado, esperado)
    
    def test_invertida_3(self):
        im = pset1.Imagem(5, 7, [0, 128, 255, 128, 0,
                                  0, 128, 255, 128, 0,
                                  0, 128, 255, 128, 0,
                                  0, 128, 255, 128, 0,
                                  0, 128, 255, 128, 0,
                                  0, 128, 255, 128, 0,
                                  0, 128, 255, 128, 0])
        resultado = im.invertida()
        esperado = pset1.Imagem(5, 7, [255, 127, 0, 127, 255,
                                       255, 127, 0, 127, 255,
                                       255, 127, 0, 127, 255,
                                       255, 127, 0, 127, 255,
                                       255, 127, 0, 127, 255,
                                       255, 127, 0, 127, 255,
                                       255, 127, 0, 127, 255])
        self.assertEqual(resultado, esperado)

    def test_invertida_4(self):
        im = pset1.Imagem(3, 3, [0, 50, 100,
                                  150, 200, 250,
                                  255, 128, 64])
        resultado = im.invertida()
        esperado = pset1.Imagem(3, 3, [255, 205, 155,
                                       105, 55, 5,
                                       0, 127, 191])
        self.assertEqual(resultado, esperado)

    def test_imagens_invertidas(self):
        for nome_arquivo in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=nome_arquivo):
                arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % nome_arquivo)
                resultado = pset1.Imagem.carregar(arquivo_entrada).invertida()
                esperado = pset1.Imagem.carregar(arquivo_saida)
                self.assertEqual(resultado,  esperado)


# Classe para os testes dos filtros:
class TestFiltros(unittest.TestCase):
    def test_borrada_1(self):
        # Teste simples com imagem pequena e kernel 3x3
        im = pset1.Imagem(3, 3, [0, 0, 0,
                                 0, 255, 0,
                                 0, 0, 0])
        resultado = im.borrada(3)
        esperado = pset1.Imagem(3, 3, [28, 28, 28,
                                       28, 28, 28,
                                       28, 28, 28])
        self.assertEqual(resultado, esperado)

    def test_borrada_2(self):
        # Teste scom imagem 9x9 e kernel 7x7
        im = pset1.Imagem(9, 9, [57, 12, 140, 125, 114, 71, 52, 44, 216,
                                 16, 15, 47, 111, 119, 13, 101, 214, 112,
                                 229, 142, 3, 81, 216, 174, 142, 79, 110,
                                 172, 52, 47, 194, 49, 183, 176, 135, 22,
                                 235, 63, 193, 40, 150, 185, 98, 35, 23,
                                 116, 148, 40, 119, 51, 194, 142, 232, 186,
                                 83, 189, 181, 107, 136, 36, 87, 125, 83,
                                 236, 194, 138, 112, 166, 28, 117, 16, 161,
                                 205, 137, 33, 108, 161, 108, 255, 202, 234])
        resultado = im.borrada(7)
        esperado = pset1.Imagem(9, 9, [89, 93, 94, 93, 92, 110, 119, 123, 129,
                                        104, 105, 104, 101, 97, 109, 113, 115, 116,
                                        110, 108, 109, 106, 104, 113, 119, 121, 122,
                                        116, 114, 113, 111, 110, 113, 115, 114, 113,
                                        134, 130, 124, 120, 115, 112, 113, 112, 108,
                                        152, 144, 137, 132, 122, 120, 124, 125, 123,
                                        151, 143, 135, 132, 126, 126, 132, 135, 137,
                                        153, 147, 136, 135, 129, 132, 143, 152, 155,
                                        150, 145, 133, 136, 134, 140, 158, 170, 178])
        self.assertEqual(resultado, esperado)

    def test_borrada(self):
        for tamanho_kernel in (1, 3, 7):
            for nome_arquivo in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=tamanho_kernel, f=nome_arquivo):
                    arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                    arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results',
                                                 '%s_blur_%02d.png' % (nome_arquivo, tamanho_kernel))
                    imagem_entrada = pset1.Imagem.carregar(arquivo_entrada)
                    imagem_entrada_copia = pset1.Imagem(imagem_entrada.largura, imagem_entrada.altura,
                                                        imagem_entrada.pixels)
                    resultado = imagem_entrada.borrada(tamanho_kernel)
                    esperado = pset1.Imagem.carregar(arquivo_saida)
                    self.assertEqual(imagem_entrada, imagem_entrada_copia,
                                     "Cuidado para não modificar a imagem original!")
                    self.assertEqual(resultado,  esperado)

    def test_focada(self):
        for tamanho_kernel in (1, 3, 9):
            for nome_arquivo in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=tamanho_kernel, f=nome_arquivo):
                    arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                    arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results',
                                                 '%s_sharp_%02d.png' % (nome_arquivo, tamanho_kernel))
                    imagem_entrada = pset1.Imagem.carregar(arquivo_entrada)
                    imagem_entrada_copia = pset1.Imagem(imagem_entrada.largura, imagem_entrada.altura,
                                                        imagem_entrada.pixels)
                    resultado = imagem_entrada.focada(tamanho_kernel)
                    esperado = pset1.Imagem.carregar(arquivo_saida)
                    self.assertEqual(imagem_entrada, imagem_entrada_copia,
                                     "Cuidado para não modificar a imagem original!")
                    self.assertEqual(resultado,  esperado)

    def test_bordas(self):
        for nome_arquivo in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=nome_arquivo):
                arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % nome_arquivo)
                imagem_entrada = pset1.Imagem.carregar(arquivo_entrada)
                imagem_entrada_copia = pset1.Imagem(imagem_entrada.largura, imagem_entrada.altura,
                                                    imagem_entrada.pixels)
                resultado = imagem_entrada.bordas()
                esperado = pset1.Imagem.carregar(arquivo_saida)
                self.assertEqual(imagem_entrada, imagem_entrada_copia,
                                 "Cuidado para não modificar a imagem original!")
                self.assertEqual(resultado,  esperado)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)

