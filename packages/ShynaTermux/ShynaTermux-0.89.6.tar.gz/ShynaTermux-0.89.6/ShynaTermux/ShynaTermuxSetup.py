import os


class ShynaTermuxSetup:
    """We need setup few things to make it work and test"""
    case_env = ''

    def set_env_variable(self):
        try:
            self.case_env = input("Want to add Environment (y/n)")
            if self.case_env.__contains__('yes') or self.case_env.__contains__('y'):
                dbpasswd = input("Enter the database password")
                dbhost_cmd = "echo 'export password=" + dbpasswd + "'>>~/.bash_profile;"
                os.popen(dbhost_cmd).readlines()
                dbhost_cmd = "echo 'export bossname=Shivam'>>~/.bash_profile;"
                os.popen(dbhost_cmd).readlines()
                dbhost_cmd = "echo 'export device_id=Termux'>>~/.bash_profile;"
                os.popen(dbhost_cmd).readlines()
            else:
                pass
            self.case_env = input("Want to install remaining (y/n)")
            if self.case_env.__contains__('yes') or self.case_env.__contains__('y'):
                os.popen("pkg install termux-api --assume-yes").readline()
                os.popen("pip install --upgrade ShynaTime ShynaTermux requests").readline()
                dbhost_cmd = """termux-notification --on-delete 'termux-tts-speak "hey Shivam"' -t 'Hey Shivam' """
                os.popen(dbhost_cmd)
            else:
                pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ShynaTermuxSetup().set_env_variable()
