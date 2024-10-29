import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
import os
import string
import random
import datetime
import logging
import platform
class Learner:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_service = webdriver.ChromeService('C:\Program Files\Google\Chrome\Application\chrome.exe')
        webdriver_path = f"{os.path.dirname(__file__)}/chromedriver.exe"
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def create_folder(self, folder_name: str):
        self.current_path = os.path.dirname(__file__) #GET THE CURRENT PATH
        try:
            os.mkdir(f'{self.current_path}/transcriptions/{folder_name}')
            logging.info(f"Tentando criar um arquivo CSV para salvar os dados...")
        except Exception as e:
            logging.info(f"Erro ao criar pasta local.\nCódigo do ERRO: {e}")

    def get_youtube_videos(self, video_name: str, resultados: int):
        self.main_url_youtube_videos = "https://www.youtube.com/results?search_query="
        self.video_name_spaced = video_name.replace(" ", '+')
        full_url = f"{self.main_url_youtube_videos}{self.video_name_spaced}"
        try:    
            self.driver.get(full_url)
            self.titles = []
            self.href = []
            self.driver.execute_script(f"window.scroll(0, 10000)")
            sleep(1)
            self.driver.execute_script(f"window.scroll(0, 0)")
            video_titles = self.driver.find_elements(By.ID, 'video-title')
            for title in video_titles:
                self.titles.append(title.text)
                try:
                    links = title.get_attribute("href")
                    if "https://www.youtube.com/watch" in links:
                        self.href.append(links)
                    else:
                        pass
                except Exception as e:
                    pass
            with open ("links.csv", "a", encoding='UTF-8') as link_file:
                i = 0
                for links in self.href:
                    if i == resultados:
                        break
                    link_file.write(f"\n{i},{self.titles[i]},{links}")
                    logging.info(f"ADICIONANDO ITEM A LISTA - VALOR ATUALIZADO\n{self.titles[i]},{links}\n")
                    i+=1

        except Exception as e:
            logging.error(f"Erro para acessar URL, código do ERRO: {e}")

    def start(self):
        self.url_youtube = None
        with open ('links.csv', 'r', encoding='UTF-8') as urls_read:
            lines = urls_read.readlines()
            for line in lines:
                self.url_youtube = line.split(',')[2]
                self.youtube_title = line.split(',')[1]
                self.id = line.split(',')[0]
                logging.info(f"VIDEO URL: {self.url_youtube}")
                if "Titulo" in self.url_youtube:
                    pass
                else:
                    try:
                        self.driver.get(self.url_youtube)
                        sleep(2)
                        get_site_name = self.url_youtube.split("//")[1].split('.')[0] #GETTING ONLY THE SITE NAME
                        logging.info("Sucesso ao entrar no site: " + get_site_name)
                        try:
                            logging.info("Procurando pelo botão de mais itens...")
                            more_button = self.driver.find_element(By.XPATH, '//*[@id="expand"]')
                            try:
                                more_button.click()
                                logging.info("Sucesso ao abrir aba de mais descrição")
                                self.driver.execute_script('window.scroll(0, 800)')
                                sleep(1)
                                show_transcript = self.driver.find_element(By.XPATH, '//*[@id="primary-button"]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
                                logging.info("Tentando acesso a transcrição")
                                sleep(1)
                                scroll = 100
                                while True:
                                    try:
                                        show_transcript.click()
                                        self.driver.execute_script(f'window.scroll(0, {scroll})')
                                        break
                                    except Exception as e:
                                        scroll += 100
                                        pass
                                try:
                                    logging.info("Sucesso ao acessar transcrição...")
                                    sleep(1)
                                    logging.info("Salvando dados de transcrição: ")
                                    try:
                                        transcript_elements = self.driver.find_elements(By.CLASS_NAME, 'ytd-transcript-segment-renderer')
                                        logging.info("Sucesso ao acessar conteúdo de transcrição")

                                        fold_name = ''.join(random.choices(string.ascii_letters,k=7))

                                        self.create_folder(folder_name=fold_name)
                                        
                                        logging.info(f"Tentando adicionar dados ao arquivo CSV")
                                        line = 0
                                        for transcript_data in transcript_elements:
                                            transcript = transcript_data.text.split('\n')
                                            if len(transcript) > 1:
                                                try:
                                                    with open(f"./transcriptions/{fold_name}/ytb-{self.id}.csv", 'a', encoding='UTF-8') as csv:
                                                        if line == 0:
                                                            csv.write("TIME, DESCRIPT\n")
                                                        else:
                                                            csv.write(f"{transcript[0]},{transcript[1]}\n")
                                                except Exception as e:
                                                    logging.error(f"ERRO AO ACESSAR ARQUIVO CSV: {e}")
                                            else:
                                                pass
                                            line += 1
                                        logging.info("Processo - Finalizado!")
                                    except Exception as e:
                                        logging.error(f"Erro ao coletar dados de transcrição, código do ERRO: {e}")
                                except Exception as e:
                                    logging.error(f"Erro ao acessar transcrição, código do ERRO: {e}")
                            except Exception as e:
                                logging.error(f"Erro ao acessar descrição. Código do ERRO: {e}")
                        except Exception as e:
                            logging.error("Error to get the code...")
                    except Exception as e:
                        logging.error(f"Erro ao acessar URL\nCódigo do ERRO: {e}")


if __name__ == '__main__':
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    browser = Learner()
    while True:
        try:
            with open('links.csv', 'w', encoding='UTF-8') as deleter:
                deleter.write('ID,Titulo, URL')
            video_title = str(input("Insira o título do vídeo: "))
            result_quatity = int(input('Digite o total de resultados: '))
            break
        except Exception as e:
            pass
    browser.get_youtube_videos(video_title, result_quatity)
    browser.start()
    
