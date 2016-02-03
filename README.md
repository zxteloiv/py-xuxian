# py-xuxian
A framework that helps to write scripts.

Xuxian is a man in an ancient Chinese legend who saved a python. He reincarnated a thousand years later, and married that very python who then turned into a beautiful woman. They opened a clinic selling medicines and saved a lot of people. People have extoled their love story in the long history.

Therefore, I hope this project can be close to the development of python scripts.

### Introduction

In my experience of writing scripts, I often get crazy about the robustness of my program. If the program is short and the execution takes only minutes, it may face no problem. However, if the goal of the program is to process a data file or is itself a service, the robustness may be important. If dead, the program should be restarted by itself or other tools like supervised and monit.

In addition, a script may use data parallelism to speed up the execution. So multiprocessing is useful. This brings new problem. As several processes are running concurrently, we have to monitor the status of all of them. All the logs, outputs, intermediate dumps and running status must be on their own way. Here I would like to use the logging module to do so.

Thus, all four aspects, robustness, speed, logging and monitoring, are focused on in this project.

### Usage

Refer to the example folder. Things are easy.

~~~shell
PYTHONPATH=../ python main.py
~~~

### Tools

There's a script to rotate log files in the tool directory. Add a line into the crontab then it will do the remaining.

### License

The Star And Thank Author License (SATA)
