<p align="center"><img src="images/banner.png" /></p>

# Dfunc-Bypasser
This is a tool that can be used by developers to check if exploitation using LD_PRELOAD is still possible given the current disable_functions in the php.ini file and taking into consideration the PHP modules installed on the server.

## Installation
`git clone https://github.com/UsifAraby/dfunc-bypasser-python3.git`

## Usage
There are two options to input the disable_functions list:
1. For help on the parameters:
`python3 dfunc-bypasser-python3.py -h`
2. Provide the phpinfo url:
`python3 dfunc-bypasser-python3.py --url https://example.com/phpinfo.php`
3. Provide the local phpinfo file:
`python3 dfunc-bypasser-python3.py --file dir/phpinfo`
4. Provide an additional header:
`python3 dfunc-bypasser-python3.py -H "Special-Header: dev"`

## Contributers
1. S Ashwin Shenoi
    * Github: [ashwinshenoi99](https://github.com/ashwinshenoi99)
    * Twitter: [c3rb3ru5](https://twitter.com/__c3rb3ru5__)
2. Tarunkant Gupta
    * Github: [tarunkant](https://github.com/tarunkant/)
    * Twitter: [TarunkantG](https://twitter.com/TarunkantG)

from team [bi0s](https://bi0s.in)

## Screenshots

<img width="1101" height="621" alt="Screenshot 2025-09-21 230651" src="https://github.com/user-attachments/assets/9db3e5d5-10d7-4163-b28a-85d9bd51f273" />

