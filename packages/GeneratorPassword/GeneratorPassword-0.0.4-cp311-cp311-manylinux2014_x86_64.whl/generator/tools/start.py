import generator
from generator.exception import IsAuthorized


class Start:
    async def start(self: 'generator.Generator'):
        if self.is_authorize:
            raise IsAuthorized()
        
        await self.authorize()
        
        return self

