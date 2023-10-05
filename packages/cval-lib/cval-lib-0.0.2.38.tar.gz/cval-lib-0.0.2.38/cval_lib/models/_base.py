from pydantic import BaseModel

from cval_lib.configs.main_config import MainConfig
from cval_lib.handlers._abstract_handler import AbstractHandler
from cval_lib.utils.base_conn import BaseConn



class Model(BaseModel):
    class Config:
        main_conn = MainConfig()

    def _send(self, user_api_key: str, url: str, sync: bool = True, method: str = 'post'):
        with BaseConn(user_api_key, sync=sync) as conn:
            handler = AbstractHandler(conn.session)
            getattr(handler, f'_{method}')(f'{self.Config.main_conn.main_url}{url}', json=self.dict())
            return handler.send().json()
