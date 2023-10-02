import requests
import os
from Shynatime import ShTime


class ShynaLocation:
    result = ""
    url = "https://shyna623.com/location/set_new_location/"
    s_time = ShTime.ClassTime()

    def get_location(self):
        self.result = "Empty location"
        new_dict = {}
        try:
            my_cmd = os.popen('termux-location -p network').read()
            if str(my_cmd) != '':
                new_dict = eval(my_cmd)
                new_dict.update(task_date=self.s_time.now_date)
                new_dict.update(task_time=self.s_time.now_time)
                new_dict.update(username='Shyna@623')
                new_dict.update(password=os.environ.get('password'))
                print(new_dict, type(new_dict))
                self.result = requests.request("POST", self.url, data=new_dict)
                print(self.result.text)
            else:
                self.result = "Empty location"
                print(self.result)
        except Exception as e:
            print(e)
            self.result = "Exceptions"
        finally:
            print(self.result)
            return self.result


if __name__ == '__main__':
    ShynaLocation().get_location()
