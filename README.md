# airmouse_pilot
## Webcam-Based Virtual Mouse using Computer Vision

This project allows users to control the computer mouse using hand gestures captured through a webcam. It leverages computer vision techniques to detect and track hand landmarks in real-time, translating movements into cursor control and click actions.

Built with Python and MediaPipe, the application processes live video input to create an intuitive and touchless interaction experience, eliminating the need for physical input devices.

This project demonstrates skills in real-time image processing, hardware integration, gesture recognition, and mapping visual inputs to system-level controls.

## Controle de Mouse com Webcam utilizando Visão Computacional

Projeto desenvolvido com o objetivo de controlar o cursor do mouse através de gestos das mãos capturados pela webcam. Utiliza técnicas de visão computacional para identificar pontos-chave da mão em tempo real e traduzir movimentos em ações como movimentação do cursor e cliques.

A aplicação foi construída utilizando Python e a biblioteca MediaPipe, permitindo o rastreamento preciso das mãos e oferecendo uma interface interativa sem necessidade de dispositivos físicos adicionais.

Este projeto demonstra conhecimentos em integração com hardware (webcam), processamento de imagem em tempo real e lógica para mapeamento de gestos em ações do sistema operacional.

# AirMouse Pilot

Controle o cursor do mouse com a webcam usando visão computacional, MediaPipe e PyAutoGUI.

## Requisitos
- Python 3.10 ou 3.11
- Webcam
- macOS, Windows ou Linux

## Bibliotecas usadas
- OpenCV
- MediaPipe
- PyAutoGUI

## Instalação
pip install -r requirements.txt

### 1. Clone o repositório
git clone https://github.com/gFreitasFerraz/airmouse_pilot.git

### 2. Entre na pasta do projeto
cd airmouse_pilot

### 3. Crie um ambiente virtual
python3 -m venv .venv

### 4. Ative o ambiente virtual

#### macOS/Linux
source .venv/bin/activate

#### Windows
.venv\Scripts\activate

### 5. Instale as dependências
pip install opencv-python mediapipe pyautogui

## Configuração

### 6. Baixe o modelo do MediaPipe
Baixe o arquivo `gesture_recognizer.task`.

### 7. Edite o caminho do modelo no código
No arquivo principal, altere esta linha:

MODEL_PATH = "/seu-caminho/para/gesture_recognizer.task"

para o caminho real do arquivo no seu computador.

Exemplo:
MODEL_PATH = "/Users/seunome/Desktop/airmouse_pilot/gesture_recognizer.task"

### 8. Ajuste a câmera, se necessário
Se a webcam não abrir, troque:

CAMERA_INDEX = 1

para:

CAMERA_INDEX = 0

## Como executar

### 9. Rode o projeto
python nome_do_arquivo.py

## Como usar
- Mova o dedo indicador para mover o cursor
- Junte polegar e indicador para clicar
- Pressione `q` para sair

## Observações
- O código usa suavização do cursor e clique por distância entre polegar e indicador :contentReference[oaicite:1]{index=1}
- A área ativa da câmera é reduzida para melhorar a precisão :contentReference[oaicite:2]{index=2}
- O projeto depende do arquivo de modelo do MediaPipe configurado em `MODEL_PATH` :contentReference[oaicite:3]{index=3}
