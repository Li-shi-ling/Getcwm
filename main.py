from UpDate.UpDate import Mymysql
from QQ_mailbox.QQ_mailbox import QQ_mailbox
from GetCwm.GetCwm import GetCwm
import yaml

def Getid_Updata(id_list,n,getcwm,mymysql,qq_mailbox,receiver):
    outputdata = []
    for id_data in id_list:
        for i in range(n):
            try:
                html_content = getcwm.Get_id(id_data)
                break
            except Exception as e:
                print(f"爬取阶段错误:{e}")
        else:
            return False
        outputdata.append(getcwm.Get_id_html_content(html_content))
        mymysql.Updata_id(outputdata[-1],f"id{id_data}")
    qq_mailbox.send_email(receiver = receiver,subject = "刺猬猫爬虫",content=qq_mailbox.fromcwm2(outputdata))

if __name__ == "__main__":
    init_data = yaml.load(open("./config/config.yaml","r").read(), Loader=yaml.FullLoader)
    Getid_Updata(
        id_list = init_data["id_list"],
        n = init_data["n"],
        getcwm = GetCwm(),
        mymysql = Mymysql(
            host = init_data["host"],
            user = init_data["user"],
            password = init_data["password"],
            port = init_data["port"],
            db_name = init_data["db_name"]
        ),
        qq_mailbox = QQ_mailbox(
            sender = init_data["sender"],
            password = init_data["QQ_password"]
        ),
        receiver = init_data["receiver"]
    )