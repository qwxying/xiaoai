from selenium import webdriver  # 导入web驱动库
from time import sleep
from notify import send_email

# flag = 0
tasks = ['[群音]-人工转写-字幕时间戳任务', '[群音]-人工转写-纯字幕任务', ' ', '[群音]-人工转写-文稿任务', '[群音]-HYZX-快标']  # 已取得作业权限的任务列表
path = r'chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # 设置option
# options.add_argument('--disable-gpu')
print("正在初始化，请稍候……")
wd = webdriver.Chrome(executable_path=path)  # , options=options)  # 调用带参数的谷歌浏览器
wd.implicitly_wait(5)
wd.get('http://ainote.iflytek.com/open/login?http://ainote.iflytek.com/open/index/task')  # 登录界面


def login(slp_time=2):  # 登录
    print("【打开登录界面】completed")
    sleep(slp_time)  # 延时等待页面加载
    wd.find_element_by_tag_name('input').send_keys('18387410365\tzsr447121666\n')  # 输入账号密码
    print("【输入账户密码】completed")
    sleep(slp_time)  # 延时等待页面加载
    print("【已取得作业权限的任务列表】获取完成")


def quit_xa():
    wd.close()
    wd.quit()


def monitor(number_of_tasks=2, flag=0):  # 监测
    while flag == 0:
        sleep(0.2)
        for i in range(number_of_tasks):
            sleep(0.5)
            tsk = wd.find_elements_by_css_selector('.item_info')[i]  # 定位到指定任务
            get = wd.find_elements_by_css_selector('.right_info')[i].find_element_by_tag_name('a')  # 定位到当前任务的领取按钮
            title = tsk.find_element_by_css_selector('[href]').get_attribute('text')  # 定位到当前任务的任务标题
            jcpct = tsk.find_element_by_css_selector('.prop_jc > .prop >span').get_attribute('style')[
                    7:-1]  # 当前检查任务的剩余百分比
            bvpct = tsk.find_element_by_css_selector('.prop_bz > .prop >span').get_attribute('style')[
                    7:-1]  # 当前标注任务的剩余百分比
            jcl = tsk.find_element_by_css_selector('.prop_jc > .prop_sum').get_attribute('innerText')  # 当前检查任务的领取量
            bvl = tsk.find_element_by_css_selector('.prop_bz > .prop_sum').get_attribute('innerText')  # 当前标注任务的领取量

            print('----------------------\n' + title)
            print('标注任务量:  ' + bvpct + ' ' + bvl)

            if title in tasks[:number_of_tasks]:  # 判断当前任务是否有权限领取
                print('检查任务量:  ' + jcpct + ' ' + jcl)
                if (jcpct not in ['0%', '100%']) or (bvpct not in ['0%', '100%']):  # 判断当前任务领取量是否为100%或0%
                    print('Yes!!!当前可领取任务！')
                    get.click()  # 可领取任务时，点击当前任务右侧的领取按钮
                    sleep(0.15)
                    wd.find_element_by_css_selector('.yes').click()  # 确定领取按钮
                    sleep(0.15)
                    body = wd.find_element_by_tag_name('body').get_attribute('innerText')  # 定位到弹出框的body内的文本
                    if '错误信息' in body:  # 暂无可领取的任务时，关闭弹出框
                        flag = 0
                        print('oh，NO！没有抢到任务！')
                        sleep(1)
                        wd.find_element_by_css_selector('.poptitle').find_element_by_tag_name('i').click()
                    elif '立即执行' in body:  # 领取任务成功时，发送提醒邮件
                        flag = 1
                        wd.find_element_by_css_selector('.no').click()  # 点击暂不执行
                        print(title + '领取成功，正在发送邮件提醒……')
                        send_email(title)
                        wd.close()
                        wd.quit()
                        break
                    else:  # 除以上两种情况外，直接关闭弹出框
                        print('尚未加入该团队，点击关闭提示信息')
                        wd.find_element_by_css_selector('.poptitle').find_element_by_tag_name('i').click()
                else:
                    flag = 0
                    print('无可领任务，继续刷新')
            elif title in tasks[number_of_tasks + 1:]:
                if bvpct in ['0%', '100%']:
                    flag = 0
                    print('无可领任务，继续刷新')
                else:
                    print('Yes!!!当前可领取任务！')
                    get.click()
                    sleep(0.15)
                    wd.find_element_by_css_selector('.yes').click()
                    sleep(0.15)
                    body = wd.find_element_by_tag_name('body').get_attribute('innerText')
                    if '错误信息' in body:
                        flag = 0
                        print('oh，NO！没有抢到任务！')
                        wd.find_element_by_css_selector('.poptitle').find_element_by_tag_name('i').click()
                    elif '立即执行' in body:
                        flag = 1
                        send_email(title)
                        print(title + '领取成功，正在发送邮件提醒……')
                        wd.find_element_by_css_selector('.no').click()  # 点击暂不执行
                        quit_xa()
                        break
                    else:
                        print('无作业权限，点击关闭提示信息')
                        wd.find_element_by_css_selector('.poptitle').find_element_by_tag_name('i').click()
            else:
                print('无作业权限')
        wd.find_element_by_tag_name('input').send_keys('')  #
        wd.find_element_by_name('s_btn').click()  # 点击搜索按钮进行任务刷新


if __name__ == '__main__':
    login()
    monitor()

