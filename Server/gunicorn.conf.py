import multiprocessing

# 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1
# workers = 1
# 指定每个工作者的线程数
threads = 2
# 监听内网端口
bind = '0.0.0.0:8000'
# 还可以使用 gevent 模式，还可以使用sync模式，默认sync模式
worker_class = 'uvicorn.workers.UvicornWorker'
# 设置最大并发量
worker_connections = 2000
# 超过多少秒后工作将被杀掉，并重新启动。一般设置为30秒或更多
timeout = 30
# 设置进程文件目录
pidfile = '/Server/logs/gunicorn.pid'
# gunicorn要切换到的目的工作目录
chdir = '/Server'
# 设置访问日志和错误信息日志路径
accesslog = '/Server/logs/Server_gunicorn_access.log'
errorlog = '/Server/logs/Server_gunicorn_error.log'

