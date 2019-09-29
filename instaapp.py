from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random


class InstagramBot():
    def __init__(self, email, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', options=self.browserProfile)
        self.email = email
        self.password = password
    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)
        emailInput = self.browser.find_element_by_name("username")
        passwordInput = self.browser.find_element_by_name("password")

        emailInput.send_keys(self.email)
        time.sleep(2)
        passwordInput.send_keys(self.password)
        time.sleep(3)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(3)

        notifInput = self.browser.find_element_by_css_selector('body div.RnEpo.Yx5HN div div div.mt3GC button.aOOlW.HoLwm').click()
    def getFollowerNum (self):
        followerCount = self.convert(self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(2) a span').get_attribute("title"))
    def getFollowingNum (self):
        followingCount = self.convert(self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(3) a span').text)
    def followWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(3)
        followButton = self.browser.find_element_by_css_selector("button")
        if (followButton.text != 'Following'):
            self.browser.find_element_by_class_name('BY3EC').click()
            time.sleep(2)
        else:
            print("You are already following this user")
    def unfollowWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Following'):
            followButton.click()
            time.sleep(2)
            confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following this user")
    def getUserFollowing(self, username):
        self.browser.get('https://www.instagram.com/' + username)
        followingLink = self.browser.find_element_by_css_selector('ul li:nth-child(3) a').click()
        time.sleep(2)

        followingList = self.browser.find_element_by_css_selector('body div.RnEpo.Yx5HN div div.isgrP ul div')
        numberOfFollowingInList = len(followingList.find_elements_by_css_selector('li'))

        followingList.click()

        followingCount = int(
            self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(3) a span').text)
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowingInList < followingCount):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)
            self.browser.find_element_by_css_selector('body div.RnEpo.Yx5HN div div.isgrP').click()
            numberOfFollowingInList = len(followingList.find_elements_by_css_selector('li'))
            print(numberOfFollowingInList)

        following = []
        for user in followingList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            following.append(userLink)
        return following
    def convert (self, text):
        text = text.replace(',','')
        return int(text)
    def getUserFollower(self, username):
        ranTime = random.randint(1, 3)
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a').click()
        time.sleep(3)
        users = []

        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')

        count = 0
        height = self.browser.find_element_by_css_selector('body div.RnEpo.Yx5HN div div.isgrP ul').value_of_css_property(
            "padding-top")
        match = False
        while match == False:
            previousCount = count

            # step 1
            elements = followersList.find_elements_by_css_selector('li')

            # step 2
            for user in followersList.find_elements_by_css_selector('li'):
                if user.find_element_by_css_selector('a').get_attribute('href') not in users:
                    userLink = user.find_element_by_css_selector('a').get_attribute('href')
                    users.append(userLink)
            # step 3
            self.browser.execute_script("return arguments[0].scrollIntoView();", elements[-1])
            time.sleep(ranTime)

            # step 4
            count = len(users)
            if count == previousCount:
                print("done")
                match = True

        return users
    def getUserFollowers(self, username):
        ranTime = random.randint(2, 4)
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a').click()
        time.sleep(2)

        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))

        followersList.click()

        followerCount = self.convert(self.browser.find_element_by_css_selector(
            '#react-root section main div ul li:nth-child(2) a span').get_attribute("title"))
        print(followerCount)
        actionChain = webdriver.ActionChains(self.browser)
        previousNum = 0
        while (numberOfFollowersInList < followerCount):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(ranTime)
            self.browser.find_element_by_css_selector('body div.RnEpo.Yx5HN div div.isgrP').click()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)
            if (numberOfFollowersInList == previousNum):
                break
            previousNum = numberOfFollowersInList
        followers = []
        print("retrieved")
        for user in followersList.find_elements_by_css_selector('li'):
            userTitle = user.find_element_by_css_selector('div.d7ByH a').get_attribute('title')
            followers.append(userTitle)
            print(userTitle)
        return followers
    def unfollowFollowing(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)
        followingLink = self.browser.find_element_by_css_selector('ul li:nth-child(3) a').click()
        time.sleep(2)

        followingList = self.browser.find_element_by_css_selector('body div.RnEpo.Yx5HN div div.isgrP ul div')
        numberOfFollowingInList = len(followingList.find_elements_by_css_selector('li'))

        followingList.click()

        followingCount = self.convert(
            self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(3) a span').text)
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowingInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)
            self.browser.find_element_by_css_selector('body div.RnEpo.Yx5HN div div.isgrP').click()
            numberOfFollowingInList = len(followingList.find_elements_by_css_selector('li'))
            print(numberOfFollowingInList)

        for user in followingList.find_elements_by_css_selector('li'):
            followButton = user.find_element_by_css_selector('button')
            if (followButton.text == 'Following'):
                followButton.click()
                print("unfollow")
                time.sleep(2)
                confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
                confirmButton.click()
    def getPostLikes (self, post):
        # Used to obtain all the likers on a specific post
        self.browser.get(post)
        time.sleep(1)
        likeLink = self.browser.find_element_by_css_selector(
            '#react-root section main div div article div.eo2As section.EDfFK.ygqzn div div button').click()
        time.sleep(2)

        users = []
        height = self.browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div").value_of_css_property(
            "padding-top")
        match = False
        while match == False:
            lastHeight = height

            # step 1
            elements = self.browser.find_elements_by_xpath("//*[@id]/div/a")

            # step 2
            for element in elements:
                if element.get_attribute('title') not in users:
                    users.append(element.get_attribute('title'))

            # step 3
            self.browser.execute_script("return arguments[0].scrollIntoView();", elements[-1])
            time.sleep(1)

            # step 4
            height = self.browser.find_element_by_xpath(
                "/html/body/div[3]/div/div[2]/div/div").value_of_css_property(
                "padding-top")
            if lastHeight == height:
                match = True

        return users
    def likersWNegativeRatio (self, post):
        self.browser.get(post)
        time.sleep(2)
        username = self.browser.find_element_by_css_selector('#react-root section main div div article header div.o-MQd div.PQo_0 div.e1e1d h2 a').get_attribute("title")
        # react-root > section > main > div > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > h2 > a
        time.sleep(1)
        likeLink = self.browser.find_element_by_css_selector(
            '#react-root section main div div article div.eo2As section.EDfFK.ygqzn div div button').click()
        time.sleep(2)

        users = []
        height = self.browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div").value_of_css_property(
            "padding-top")
        match = False
        while match == False:
            lastHeight = height

            # step 1
            elements = self.browser.find_elements_by_xpath("//*[@id]/div/a")

            # step 2
            for element in elements:
                if element.get_attribute('href') not in users:
                    users.append(element.get_attribute('href'))

            # step 3
            self.browser.execute_script("return arguments[0].scrollIntoView();", elements[-1])
            time.sleep(1)

            # step 4
            height = self.browser.find_element_by_xpath(
                "/html/body/div[3]/div/div[2]/div/div").value_of_css_property(
                "padding-top")
            if lastHeight == height:
                match = True
        counter = 0
        for a in range(0, len(users)):
            self.browser.get(users[a])
            time.sleep(1)
            try:
                followerCount = self.convert(self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(2) span span').text)
            except:
                try:
                    followerCount = self.convert(self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(2) a span').text)
                except:
                        try:
                            followerCount = self.convert(self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(2) span span').get_attribute("title"))
                        except:
                            followerCount = self.convert(self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(2) span').get_attribute("title"))
            try:
                followingCount = self.convert(self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(3) span').text)
            except:
                try:
                    followingCount = self.convert(self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(3) span span').text)
                except:
                    followingCount = self.convert(self.browser.find_element_by_css_selector('#react-root section main div ul li:nth-child(3) span span').text)
            if(followingCount > followerCount):
                counter = counter + 1
        print(username)
        print (counter/len(users))

    def likersWx2NegativeRatio (self, post):
        self.browser.get(post)
        time.sleep(2)
        username = self.browser.find_element_by_css_selector(
            '#react-root section main div div article header div.o-MQd div:nth-child(1) div h2 a').get_attribute("title")
        # react-root > section > main > div > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > h2 > a
        time.sleep(1)
        likeLink = self.browser.find_element_by_css_selector(
            '#react-root section main div div article div.eo2As section.EDfFK.ygqzn div div button').click()
        time.sleep(2)

        users = []
        height = self.browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div").value_of_css_property(
            "padding-top")
        match = False
        while match == False:
            lastHeight = height

            # step 1
            elements = self.browser.find_elements_by_xpath("//*[@id]/div/a")

            # step 2
            for element in elements:
                if element.get_attribute('href') not in users:
                    users.append(element.get_attribute('href'))

            # step 3
            self.browser.execute_script("return arguments[0].scrollIntoView();", elements[-1])
            time.sleep(1)

            # step 4
            height = self.browser.find_element_by_xpath(
                "/html/body/div[3]/div/div[2]/div/div").value_of_css_property(
                "padding-top")
            if lastHeight == height:
                match = True
        counter = 0
        print("complete")
        print (len(users))
        for a in range(0, len(users)):
            self.browser.get(users[a])
            time.sleep(1)
            try:
                followerCount = self.convert(self.browser.find_element_by_css_selector(
                    '#react-root section main div ul li:nth-child(2) span span').text)
            except:
                try:
                    followerCount = self.convert(self.browser.find_element_by_css_selector(
                        '#react-root section main div ul li:nth-child(2) a span').text)
                except:
                    try:
                        followerCount = self.convert(self.browser.find_element_by_css_selector(
                            '#react-root section main div ul li:nth-child(2) span span').get_attribute("title"))
                    except:
                        followerCount = self.convert(self.browser.find_element_by_css_selector(
                            '#react-root section main div ul li:nth-child(2) span').get_attribute("title"))
            try:
                followingCount = self.convert(self.browser.find_element_by_css_selector(
                    '#react-root section main div ul li:nth-child(3) span').text)
            except:
                try:
                    followingCount = self.convert(self.browser.find_element_by_css_selector(
                        '#react-root section main div ul li:nth-child(3) span span').text)
                except:
                    followingCount = self.convert(self.browser.find_element_by_css_selector(
                        '#react-root section main div ul li:nth-child(3) span span').text)
            followerCount = followerCount * 2
            if (followingCount > followerCount):
                counter = counter + 1
        print(username)
        print(counter / len(users))
    def likePercentage(self, username, post):
        followersList = instaBot.getUserFollower(username)
        likeList = instaBot.getPostLikes(post)
        count = 0
        for x in range(0, len(likeList)):
            if likeList[x] in followersList:
                count = count + 1
        print(count)
        print(count / len(likeList))
    def closeBrowser(self):
        self.browser.close()
    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()




