from GalleryThief.mask import RobberMask
from .strategies import StealingStrategy


class Thief():
    '''
    Performer for executing given StealingStrategy.
    '''

    def __init__(self, strategy: StealingStrategy, mask: RobberMask):
        '''
        Initializes Thief with given StealingStrategy and RobberMask.

        StealingStrategy -> describes algorithm of getting images.
        RobberMask -> describes where to get fresh list of proxy servers.
        '''
        self._strategy: StealingStrategy = strategy
        self._strategy.mask = mask

    @property
    def strategy(self) -> StealingStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    @property
    def mask(self) -> RobberMask:
        return self._strategy._mask

    @mask.setter
    def mask(self, mask):
        self._strategy._mask = mask

    def get_images_list(self, *args):
        '''
        Takes prompts and returns dictionary of urls.

        Takes arguments in format "[<prompt>, <count>]" where
        <prompt> is your search requests and <count> is number
        of images you want to get from this search request.

        You can process several search requests like this:\n
        thief.get_images_list(\n
            [<prompt1>, <count1>],\n
            [<prompt2>, <count2>],\n
            [<prompt3>, <count3>],\n
            ...,\n
            [<promptN>, <countN>]\n
        )\n

        It will return dictionary in such format:\n
        {\n
            <prompt1>: [<url1>, <url2>, ..., <urlN>],\n
            <prompt2>: [<url1>, <url2>, ..., <urlN>],\n
            <prompt3>: [<url1>, <url2>, ..., <urlN>],\n
            ...,\n
            <promptN>: [<url1>, <url2>, ..., <urlN>]\n
        }
        '''
        result = {}
        for a in args:
            res = self._strategy.get_images(a[0], a[1])
            result[a[0]] = res
        return result
