from typing import Callable

from duodrone.data import OuterEvent

outer_request_callback: Callable[[OuterEvent], None] = lambda resp: print(f'Dummy get outer response: {resp}')
