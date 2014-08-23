to install lxml on ubuntu run 'sudo apt-get install libxml2-dev libxslt-dev python-dev lib32z1-dev'

monitor
=======

`config.ini` example:

    [EmailConfigs]
    sender : someone@mail.com
    password : ********
    to : another@mail.com
    
    [URLS]
    urls : []
    
    [OTHER]
    secret_word: ******
    sch_period: 1
    
    [CONTENT_XPATH]
    xpath: //div[@id="confftent"]
