from MaterialEdit.fun_素材下载.fun_插入素材 import fun_插入素材
from router_chrome_plugin.__class_new_tb import NewTbScrapy
from router_chrome_plugin.__class_old_tb import OldTbScrapy


class ChromeScrapy(NewTbScrapy, OldTbScrapy):
    def fun_insert_db(self):
        state = False

        if self.material_site in ["三老爹", "加油鸭素材铺", "漫语摄影"]:
            ma_list = self.fun_get_new_tb()
        elif self.material_site in ["青青草素材王国", "巴扎嘿"]:
            ma_list = self.fun_get_old_tb()

        for obj in ma_list:
            fun_插入素材(
                shop_name=self.shop_name,
                material_site=self.material_site,
                material_model=obj,
            )
            state = True

        return state
