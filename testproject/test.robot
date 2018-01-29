*** Settings ***
Library    Selenium2Library
Resource    Pages/keywords.txt

*** Variables ***
${host}=    https://www.google.ru

*** Test Cases ***
Search Text
    Open Browser  ${host}  chrome
    Search  грокаем алгоритмы
    Close Browser