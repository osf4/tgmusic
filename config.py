from dotenv import dotenv_values
from argparse import ArgumentParser

class Config:
    """
    Config loads VK and Telegram tokens from .env file
    """
    
    vk_token: str
    tg_token: str

    def load(self, config_path: str = '.env'):
        config = dotenv_values(config_path)

        self.tg_token = config['TG_TOKEN']
        self.vk_token = config['VK_TOKEN']

    def try_load(self, config_path: str = '.env') -> bool:
        config = dotenv_values(config_path)

        self.tg_token = config.get('TG_TOKEN')
        self.vk_token = config.get('VK_TOKEN')

        return self.tg_token != None and self.vk_token != None
    
class CommandLinePaser:
    """
    CommandLineParser allows to set the path to .env file from console.
    Moreover, it provides the help message for new users.
    """
    
    __parser: ArgumentParser
    config_path: str

    def __init__(self):
        self.__parser = ArgumentParser(
            prog = 'tgmusic',
            description = 'tgmusic is a simple Telegram bot that downloads music from VK and sends to your Telegram chat.'              
        )

    def parse_args(self):
        self.__parser.add_argument('-c', '--config', help = 'Path to .env config file.')
        args = self.__parser.parse_args()

        self.config_path = args.config