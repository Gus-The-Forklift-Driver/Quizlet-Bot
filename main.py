from selenium import webdriver
from time import sleep
from Secret import id
from Secret import psw



class QuizletBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.dictionnary = {}
        self.reverse_dictionnary = {}

    def login(self, id = id, psw = psw):
        self.driver.get('https://quizlet.com/fr-fr')

        sleep(2)

        log_btn = self.driver.find_element_by_xpath(
            '//*[@id="SiteHeaderReactTarget"]/header/div[1]/div[1]/div[2]/span[2]/div/div[2]/div/button[1]')
        log_btn.click()
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(id)
        sleep(0.1)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(psw)
        self.driver.find_element_by_xpath('/html/body/div[8]/div/div[2]/form/button').click()

    # def go_to_last_list(self):
    #     brassart_btn = self.driver.find_element_by_xpath(
    #         '//*[@id="DashboardSidebarTarget"]/div/div[1]/div[2]/div[5]/div/span/a/span/div')
    #     brassart_btn.click()
    #     first_item = self.driver.find_element_by_xpath(
    #         '//*[@id="DashboardPageTarget"]/div/div[2]/div/div/div/div/div/div/div[1]/div[1]')
    #     first_item.click()

    def start_safe(self):
        self.driver.get('https://quizlet.com/fr-fr')

    def build_dictionnary(self, entries):
        items = []
        x = 1
        while x <= entries:
            value = """//*[@id="SetPageTarget"]/div/div/div[2]/div[2]/div/div/section/div/section/div[""" + str(
                x) + """]/div/div/div[1]/div/div[1]/div/a/span"""
            try:
                items.append(self.driver.find_element_by_xpath(value).text)
            except:
                items.append('err')
            x += 1

        translations = []
        x = 1
        while x <= entries:
            value = """//*[@id="SetPageTarget"]/div/div/div[2]/div[2]/div/div/section/div/section/div[""" + str(
                x) + """]/div/div/div[1]/div/div[2]/div/a/span"""
            try:
                translations.append(self.driver.find_element_by_xpath(value).text)
            except:
                translations.append('err')
            x += 1
        dictionnary = {}
        reverse_dictionnary = {}
        for i in range(len(items)):
            try:
                dictionnary[items[i]].append(translations[i])

            except KeyError:
                dictionnary[items[i]] = [translations[i]]

        self.dictionnary = dictionnary

        for i in range(len(items)):
            try:
                reverse_dictionnary[translations[i]].append(items[i])

            except KeyError:
                reverse_dictionnary[translations[i]] = [items[i]]


        self.reverse_dictionnary = reverse_dictionnary

    def answer_question(self, questionType, reverse=True):
        #cards question
        if questionType == 0:
            self.driver.find_element_by_xpath('//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[1]/div/div/div[1]/div[2]').click()
            sleep(0.1)
            self.driver.find_element_by_xpath('//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[2]/div/div/div[1]/div/button').click()

        #multiple choice questions
        if questionType == 1:
            if reverse:
                active_dictionnary = self.reverse_dictionnary
            else:
                active_dictionnary = self.dictionnary
            try:
                solution1 = self.driver.find_element_by_xpath(
                '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div')
                solution2 = self.driver.find_element_by_xpath(
                '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div')
                solution3 = self.driver.find_element_by_xpath(
                '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div/div[2]/div/div[2]/div/div[3]/div[2]/div/div')
                solution4 = self.driver.find_element_by_xpath(
                '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div/div[2]/div/div[2]/div/div[4]/div[2]/div/div')

                question = self.driver.find_element_by_xpath(
                '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div/div[2]/div/div[1]/div/div/div/div').text
                answer = active_dictionnary[question][0]
            except:
                print("Answer not found. Please answer mannualy")
                return

            if solution1.text == answer:
                solution1.click()
            elif solution2.text == answer:
                solution2.click()
            elif solution3.text == answer:
                solution3.click()
            elif solution4.text == answer:
                solution4.click()
            else:
                print(
                    solution1.text + " / " + solution2.text + " / " + solution3.text + " / " + solution4.text + " != " + answer + " = " + question)
        #text questions
        if questionType == 2:
            if reverse == False:
                question = self.driver.find_element_by_xpath(
                    '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[1]/div/div[2]/div/div/div/div/div').text
                answer = self.dictionnary[question][0]
                self.driver.find_element_by_xpath(
                    '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[2]/div/form/div[1]/div/label/div/div[1]/div[2]/textarea').click()
                self.driver.find_element_by_xpath(
                    '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[2]/div/form/div[1]/div/label/div/div[1]/div[2]/textarea').send_keys(
                    answer)
                self.driver.find_element_by_xpath('//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[2]/div/form/div[2]/button').click()
            else:
                question = self.driver.find_element_by_xpath(
                    '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[1]/div/div[2]/div/div/div/div/div').text
                answer = self.reverse_dictionnary[question][0]
                self.driver.find_element_by_xpath(
                    '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[2]/div/form/div[1]/div/label/div/div[1]/div[2]/textarea').click()
                self.driver.find_element_by_xpath(
                    '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[2]/div/form/div[1]/div/label/div/div[1]/div[2]/textarea').send_keys(
                    answer)
                self.driver.find_element_by_xpath('//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[2]/div/form/div[2]/button').click()

        #Test finnish
        if questionType == 3:
            self.driver.find_element_by_xpath('//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[1]/div/div/div[2]/div/button').click()


    def determine_question_type(self):
        card = False
        multiple_choice = False
        written = False
        questionType = -1

        try:
            self.driver.find_element_by_xpath(
                '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[1]/div/div/div[1]/div[2]')
        except:
            pass
        else:
            questionType = 0

        try:
            self.driver.find_element_by_xpath(
                '//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div')
        except:
            pass
        else:
            questionType = 1

        try:
            self.driver.find_element_by_xpath('//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[2]/div/div[2]/div/form/div[1]/div/label/div/div[1]/div[2]/textarea')
        except:
            pass
        else:
            questionType = 2

        try:
            self.driver.find_element_by_xpath('//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[1]/div/div/div[2]/div/button')
        except:
            pass
        else:
            questionType = 3

        if questionType != -1:
            return questionType
        else:
            print('Unable to determine question type')
            print('Please select one manualy :')
            print('0 = Card')
            print('1 = Multiple choice question')
            print('2 = Written answer')
            print('3 = Test finish')

            while True :

                try:
                    Input = int(input("Question type ? "))

                except ValueError:
                    print("Invalid value, try again")

                except KeyboardInterrupt:
                    print("returning 0 may cause errors")
                    return 0

                else:
                    return Input


    def simple_loop(self):
        if self.dictionnary == 0:
            print("build dictionnary with .build_dictionnary(#words amount)")
            return

        while True:
            try:
                self.driver.find_element_by_xpath('//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[1]/div/div/div[2]/div/button/span').click()
            except :
                wait = False
            if wait == True:
                sleep (1)
            wait = True
            self.answer_question(1)
            sleep(1)

    def prepare_dictionnary(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div/div[2]/div[2]/div/div/section/div/div/div/div/div/div/div/select/option[1]').click()
        except:
            pass
        try:
            self.driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div/div[2]/div[2]/div/div/section/div/div[2]/button').click()
        except:
            pass

    def loop(self):
        try :
            while True:
                sleep(0.5)
                self.answer_question(self.determine_question_type())
                sleep(1)
        except KeyboardInterrupt:
            print("stoping...")




bot = QuizletBot()
bot.login()
