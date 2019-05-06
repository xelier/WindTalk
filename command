启动服务：nohup python -u webserver.py > server.log 2>&1 &
停止服务：lsof -i:8888   kill -9


nginx启动：/usr/local/nginx/sbin/nginx
重启：/usr/local/nginx/sbin/nginx –s reload
停止：/usr/local/nginx/sbin/nginx –s stop
测试配置文件是否正常：/usr/local/nginx/sbin/nginx –t
强制关闭：pkill nginx