from __future__ import annotations
from tuigpt.back.g4f        import models
from .Provider  import BaseProvider, AsyncProvider
from .typing    import Any, CreateResult, Union
import random

logging = False

def get_model_and_provider(model: Union[models.Model, str], provider: type[BaseProvider], stream: bool):
    # print(provider)

    if isinstance(model, str):
        if model in models.ModelUtils.convert:
            model = models.ModelUtils.convert[model]
        else:
            raise Exception(f'The model: {model} does not exist')

    if not provider:
        provider = model.best_provider

    if not provider:
        raise Exception(f'No provider found for model: {model}')
    
    if not provider.working:
        raise Exception(f'{provider.__name__} is not working')
    
    if not provider.supports_stream and stream:
        raise Exception(
                f'ValueError: {provider.__name__} does not support "stream" argument')
    
    if logging:
        print(f'Using {provider.__name__} provider')

    return model, provider

class ChatCompletion:
    @staticmethod
    def create(
        model    : Union[models.Model, str],
        messages : list[dict[str, str]],
        provider : Union[type[BaseProvider], None] = None,
        stream   : bool                            = False,
        auth     : Union[str, None]                = None,
        **kwargs
    ) -> Union[CreateResult, str]:

        model, provider = get_model_and_provider(model, provider, stream)

        if provider.needs_auth and not auth:
            raise Exception(
                f'ValueError: {provider.__name__} requires authentication (use auth=\'cookie or token or jwt ...\' param)')
            
        if provider.needs_auth:
            kwargs['auth'] = auth

        result = provider.create_completion(model.name, messages, stream, **kwargs)
        return result if stream else ''.join(result)

    @staticmethod
    async def create_async(
        model    : Union[models.Model, str],
        messages : list[dict[str, str]],
        provider : Union[type[BaseProvider], None] = None,
        **kwargs
    ) -> str:
        
        model, provider = get_model_and_provider(model, provider, False)

        provider_type = provider if isinstance(provider, type) else type(provider)
        if not issubclass(provider_type, AsyncProvider):
            raise Exception(f"Provider: {provider.__name__} doesn't support create_async")

        return await provider.create_async(model.name, messages, **kwargs)

class Completion:
    @staticmethod
    def create(
        model    : Union[models.Model, str],
        prompt   : str,
        provider : Union[type[BaseProvider], None] = None,
        stream   : bool                            = False, **kwargs) -> Union[CreateResult, str]:
        
        allowed_models = [
            'code-davinci-002',
            'text-ada-001',
            'text-babbage-001',
            'text-curie-001',
            'text-davinci-002',
            'text-davinci-003'
        ]
        
        if model not in allowed_models:
            raise Exception(f'ValueError: Can\'t use {model} with Completion.create()')
        
        model, provider = get_model_and_provider(model, provider, stream)

        result = provider.create_completion(model.name, 
                                            [{"role": "user", "content": prompt}], stream, **kwargs)

        return result if stream else ''.join(result)