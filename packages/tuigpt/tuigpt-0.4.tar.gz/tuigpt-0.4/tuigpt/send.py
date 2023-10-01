from tuigpt.back.g4f import ChatCompletion
# from tuigpt.back.g4f.Provider.base_provider import BaseProvider
from tuigpt.back.g4f.Provider.GptGo import GptGo

def request(messages:list[list], model:str ='gpt-3.5-turbo', provider=GptGo, stream:bool=False) -> str:
    response = ChatCompletion.create(model=model, stream=False, messages=messages, provider=provider)
    return response


