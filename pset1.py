# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Yuri Luiz Kruger Torquato
#    Matrícula: 202311567
#    Turma: CC5N
#    Email: yuri.luizkt@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        # Se tivermos um pixel fora da imagem, devolve o mais próximo possível na borda.
        # Se x ou y forem menores que zero, pega sempre o primeiro pixel da linha ou coluna.
        # Se x ou y forem grandes demais, pega o último pixel da linha ou coluna.
        
        if x < 0:
            x = 0
        elif x >= self.largura:
            x = self.largura - 1
        
        if y < 0:
            y = 0
        elif y >= self.altura:
            y = self.altura - 1
            
        # Utiliza a ordem por linhas na lista de pixels para facilitar o acesso e processamento 
        #rápido, pois pixels são armazenados em sequência por linha
        return self.pixels[y * self.largura + x]

    def set_pixel(self, x, y, c):
        # Utiliza a ordem por linhas na lista de pixels para facilitar o acesso e processamento rápido, pois pixels são armazenados em sequência por linha
        self.pixels[y * self.largura + x] = c

    def aplicar_por_pixel(self, func):
        # Gera uma nova imagem aplicando uma função a cada pixel individualmente.
        resultado = Imagem.nova(self.largura, self.altura)
        # Percorre cada pixel da imagem original
        for x in range(self.largura):
            for y in range(self.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)  # Aplica a função ao pixel
                resultado.set_pixel(x, y, nova_cor)  # Salva o resultado
        return resultado

    def aplicar_kernel(self, kernel):
        # Aplica o kernel: para cada pixel, multiplica os vizinhos pelos valores do kernel,
        # soma tudo e salva esse resultado na nova imagem. Se tentar acessar fora da imagem,
        # usa sempre o pixel mais próximo da borda.

        resultado = Imagem.nova(self.largura, self.altura)
        tamanho_kernel = len(kernel)
        deslocamento = tamanho_kernel // 2

        for y in range(self.altura):
            for x in range(self.largura):
                valor = 0
                for ky in range(tamanho_kernel):
                    for kx in range(tamanho_kernel):
                        px = x - deslocamento + kx
                        py = y - deslocamento + ky
                        pixel_valor = self.get_pixel(px, py)
                        valor += pixel_valor * kernel[ky][kx]
                valor = max(0, min(255, round(valor)))
                resultado.set_pixel(x, y, valor)
        return resultado
    
    def criar_kernel_borrado(self, n):
        # Cria um kernel que é um quadrado n × n de valores idênticos que somam 1
        kernel = valor = 1 / (n * n)
        kernel = [[valor for _ in range(n)] for _ in range(n)]
        return kernel

    # Função para inverter a imagem
    def invertida(self):
        # lambda c: 255 - c é uma função que recebe um pixel c e retorna o pixel invertido
        # Pois para invertermos uma imagem preto e branco, se subtrairmos cada pixel de 255, o preto se torna branco e o branco se torna preto
        return self.aplicar_por_pixel(lambda c: 255 - c)

    def borrada(self, n):
        # Cria um kernel chamando a função criar_kernel_borrado
        kernel = self.criar_kernel_borrado(n)
        return self.aplicar_kernel(kernel)

    def focada(self, n):
        # Cria um kernel de borrado n x n
        kernel_borrado = self.criar_kernel_borrado(n)

        # Cria o kernel nítido a partir do kernel de borrado
        # A lógica é (2 * Identidade) - Borrado
        # Começamos criando um kernel onde todos os valores são o negativo do valor do kernel de borrado
        valor_negativo = -kernel_borrado[0][0]
        kernel_nitido = [[valor_negativo for _ in range(n)] for _ in range(n)]

        # Encontra o a coordenada do centro do kernel
        centro = n // 2

        # Adiciona 2 no centro do kernel nítido
        # Isso corresponde a adicionar 2 * Identidade ao kernel (-Borrado)
        # O valor central se torna 2 - valor do kernel de borrado
        kernel_nitido[centro][centro] += 2

        
        return self.aplicar_kernel(kernel_nitido)

    def bordas(self):
        raise NotImplementedError

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    
    ## INVERTIDA
    # im = Imagem.carregar('test_images/Imagem colada.png')
    # im.mostrar()
    # im.invertida().mostrar()

    ## BORRADA
    # im = Imagem.carregar('test_images/Imagem colada.png')
    # im.mostrar()
    # im.borrada(7).mostrar()
    # img = Imagem.carregar('test_results/mushroom_blur_07.png')
    # img.mostrar()

    ## FOCADA
    im = Imagem.carregar('test_images/Imagem colada.png')
    im.mostrar()
    im.focada(11).mostrar()
    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
