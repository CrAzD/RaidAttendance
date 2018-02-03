import asyncio

class EventManager(object):
    events = {'counter':0, 'new':{}}

    def __init__(self):
        super().__init__()
        self.events = EventManager.events

    async def event_loop(self):
        if not len(self.events['new']) > 0:
            return

        tEvents = dict(self.events['new'])
        for event in tEvents:
            await self.event_fire(self.events['new'][event])
            del self.events['new'][event]

    async def event_fire(self, event):
        if event['async']:
            await event['function'](event['arguments'])
            return(True)
        else:
            event['function'](event['arguments'])
            return(False)