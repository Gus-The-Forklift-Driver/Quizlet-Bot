x = 0
while x < 10:
    value = '//*[@id="SetPageTarget"]/div/div/div[2]/div[2]/div/div/section/div/section/div[' + str(x) + ']/div/div/div[1]/div/div[1]/div/a/span'
    print(value)
    x += 1