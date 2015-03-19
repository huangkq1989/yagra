DEMO
=======
管理Avatar:
http://58.248.25.237:9090/  
账号： yagra_admin  
密码： yagra123A  

外站访问:  
http://58.248.25.237:9090/yagra/app.py/avatar/eda31c99d48062be48529a5cbf2fd654  
其中`eda31c99d48062be48529a5cbf2fd654`是注册邮箱的md5值  
md5值用hashlib.md5('yagra_admin@163.com').hexdigest()得到。  


设计说明
=======
---


###基本设计###

要求中说明无需过多考虑性能的问题，同时需求较为简单，主要需要考虑以下几个方面：  

1. 如何保存图片，是将图片存放到数据库中还是存储到文件系统中  

	> 本系统选择将图片保存到文件系统，然后由数据库的avatar_url字段指向图片路径，   
  	  原因是后期扩展可以通过将图片交由CDN处理，提高访问的速度。  
    > avatar的存储路径由用户id进行生成，`tmp = "%010d%" % id`，tmp[:3]为一级目录，  
      tmp[3:6]为二级，剩下的为文件名。分为多级是目录有文件数上限的。  
  
2. 如何保存会话，是存储到数据库中还是用文件来进行存储，或自实现一个基于内存的会话管理器   
   
	> 出于方便，本系统直接用标准库中的shelve来维护，保存到文件中。管理session时，
      除了在用户正常退出时销毁会话外，还有独立的回收session进程，将已过期的  
      session删除，保证断网等情况用户未能发送signout请求的情况下也能注销会话。   

3. 如何实现通过邮件发送的确认注册链接，伪代码如下：  

    > sep = "."
      hash = sha256(sep.join([base64_encode(email), base64_encode(time))])
      sign = hash.update(salt).digest()得到一个签名，  
      然后将 sep.join([base64(email), base64_encode(time),base64_encode(sign)])   
      得到一个字符串，用户确认时根据该字符串反解，看是否合法和未超时。  
      具体实现在application.utility.confirm_url_serializer中。  

4.  登录功能如何防止攻击：
    > 密码的存储与比较的安全问题参考Salted Password Hashing[1]。
    > 同时为防止在线暴力猜测密码，使用频率来控制错误账号密码登录，每一个M分钟内
      只能试N次，若完全用完则需要等待K分钟，其中M、N、K可配置。  

5. **HTTP的cache特性**：在用户重新上传avatar时，原来的avatar可能被浏览器所缓存，    
   导致新上传的avatar不会马上显示，因此在上传avatar后，再次请求avatar需要绕过  
   缓存功能。  
   HTTP缓存特性在RFC2616的第十四节[2]及stack overflow[3][4]有描述。
   在本系统中，有两类访问avatar的情况，一种是外站访问，一种是本站访问，外站  
   访问时通过MD5即可，因此，响应图片时应添加抑制缓存的HTTP头。考虑到兼容性，
   响应外站请求时，图片添加如下的HTTP头：

        Cache-Control: no-cache, no-store, must-revalidate  // for HTTP1.1
        Pragma: no-cache // for HTTP1.0
        Expires: 0 // for proxies

    而内站访问的链接都是本系统产生的，因此可以直接在访问链接加上一个随机参数，  
    如`<img id="image" src="/test/avatar/000/000/0001.jpg?1426752982.7" alt="Not found" class="photo">`    
    的?1426752982.7(时间戳)，浏览器发现带有不同的参数时也会再向服务器重新发出请求，  
    从而绕过缓存。这种方法的好处是图片会直接由HTTP服务器响应，无需CGI脚本  
    进行处理。 

6. 如何支持调试：支持调试和非调试两种模式，在调试模式下启动cgitb（cgitb.enable()），  
	错误数据通过sys.stderr写入apache日记后reraise异常，然后由cgitb显示；  
    非调试模式下，写入sys.stderr，向用户返回用户友好的提示。  
	
7. 对移动终端的兼容性：前端是基于Bootstrap框架实现的，这一响应式的CSS框架能很好的  
	兼容移动终端。  


###代码设计###

由于不能使用现有的Web框架，而是需要通过CGI来实现各服务，因此代码设计应  
尽可能将框架(代码目录`framework`)和业务逻辑(代码目录`application`)划分开。

借鉴目前流行的MVC模型，本系统划分为以下三个部分：

1. Control层：负责请求派遣，借鉴Flask的路由实现模式，通过`python decorator`来完成，   
  代码在`framework/app_runner.py`中实现。  

2. View层：负责响应展示层数据。 

> 前端的代码在static目录下。  

> 由`framework/render_template.py`和`framework/jsonify.py`负责render, 实现了包括
  `redirect`，`render_template`，`jsonify`等方法。考虑到`DRY`，  
  `render_template`支持模板继承和变量功能，通过正则表达式来实现。  
  支持以下语法：

    # extends template
    {% extends template.html %}

    # block feature
    {% block blockname %}
    {% endblock %}

    # variable
    {variable}

3. Model层：

> 处理与Mysql的交互，通过`contextlib.contextmanager`来保证数据库的关闭。   

> 负责完成实际的业务操作，实现要求中所述的登录退出，上传和访问功能。  


###数据库设计###


####表的设计####

共存在两个表，分别为`users`和`access_control`。  

#####users#####

用户信息表，使用MyISAM引擎，原因是该表更新并不频繁，主要是读操作，无需支持事务，而
MyISAM有二进制可移植等优点，易于维护。

    +-------------+------------------+------+-----+---------+----------------+
    | Field       | Type             | Null | Key | Default | Extra          |
    +-------------+------------------+------+-----+---------+----------------+
    | id          | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
    | username    | varchar(20)      | NO   | UNI | NULL    |                |
    | email       | varchar(255)     | NO   |     | NULL    |                |
    | password    | char(32)         | NO   |     | NULL    |                |
    | salt        | char(32)         | NO   |     | NULL    |                |
    | avatar_key  | char(32)         | YES  | UNI | NULL    |                |
    | avatar_url  | varchar(20)      | YES  |     | NULL    |                |
    | register_on | datetime         | YES  |     | NULL    |                |
    | confirmed   | tinyint(1)       | YES  |     | 0       |                |
    +-------------+------------------+------+-----+---------+----------------+
说明：  
	1. email的长度：根据RFC5321， forward path最多为256，去除\r\n，则最多为254，这里取255；    
	2. 由于password、salt、avatar_url都是定长的，所以数据类型为char(32);  
	3. avatar_key是用户邮箱的MD5值，通过该值在其他网站引用用户的avatar;  
	4. confirmed用于记录用户是否已经确认邮箱，以反馈正确的信息给用户。  
	5. register_on记录用户注册的时间，若在超过指定时间后用户还未通过邮箱确认账号，  
	   则会通过MySQL 的Event功能将该信息删除；启用和创建Event的语句如下：  

        -- enable event.
        SET GLOBAL event_scheduler = ON; 

        -- create event.
        CREATE EVENT clearExpiredRegistration  
        ON SCHEDULE  
            EVERY 1 HOUR 
        DO 
            DELETE FROM yagra.users WHERE users.confirmed=0 and TIMESTAMPDIFF(SECOND, yagra.users.register_on, NOW()) > 3600;  
       

#####access_control#####

错误账号密码登录的频率控制，使用InnoDB引擎，原因是需要事务来保证并发不出错。  

    +-----------+--------------+------+-----+---------+----------------+
    | Field     | Type         | Null | Key | Default | Extra          |
    +-----------+--------------+------+-----+---------+----------------+
    | id        | int(11)      | NO   | PRI | NULL    | auto_increment |
    | username  | varchar(255) | YES  |     | NULL    |                |
    | last_time | double       | YES  |     | 0       |                |
    | allowance | int(11)      | YES  |     | 0       |                |
    +-----------+--------------+------+-----+---------+----------------+

说明：  
	1. access_control用于控制错误账号密码登录的，为了表现出已存在的用户和未存在的用户名
        都有同样的表现(避免非法用户猜测用户名)，将access_control独立为一个表，不存在的用户
        也和存在的用户同样地处理。  
	2. last_time是用户上一次的访问时间，allowance是用户还有多少尝试机会的次数。  
    3. 这个表可以定期truncate一下，清理一下内存。
	

####索引设计####
	
#####users#####

通过username、avatar_key、id查询次数较多，因此对其建立索引。id字段为主键，进行自增。  

    +-------+------------+------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+
    | Table | Non_unique | Key_name   | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type |
    +-------+------------+------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+
    | users |          0 | PRIMARY    |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |
    | users |          0 | username   |            1 | username    | A         |           0 |     NULL | NULL   |      | BTREE      |
    | users |          0 | avatar_key |            1 | avatar_key  | A         |        NULL |     NULL | NULL   | YES  | BTREE      |
    +-------+------------+------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+

#####access_control#####

频率控制根据登录名进行，因此对username建立索引。id字段为主键，进行自增。 

    +----------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+
    | Table          | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type |
    +----------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+
    | access_control |          0 | PRIMARY  |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |
    | access_control |          0 | username |            1 | username    | A         |           0 |     NULL | NULL   | YES  | BTREE      |
    +----------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+


###安全问题###

网络程序中安全问题至关重要，本系统主要考虑的安全问题包括以下几方面：

1. SQL注入:  使用MySQL-python的MySQLdb模块，其paramstyle为format，  
    格式化标识不添加引号，通过将查询参数以元组的方式传入可避免常见的SQL注入。  

2. XSS：在网页上显示的用户提供的数据有用户名，因此将用户escape后再  
    响应浏览器。escape函数用的cgi.escape(name, quote=True)来完成。  

3. CSRF：应该没有这个问题。CSRF一般可通过在HTTP头部加可expire的token来预防。  

4. 会话管理：用户成功登录后，将一个cookie返回给用户，且维护一个session，
    后续请求会根据该cookie值结合session判断是否为合法请求。主要需要注意 
	的安全问题是在用户注销时必须合理地将会话失效。
	本系统一方面是在应用层保证用户退出（无论是点击退出按钮还是直接关闭
	窗口）都将会话注销，另一方面是管理session时，有独立的回收进程，将已
	过期的session删除，保证用户在断网等情况下未能发送signout请求也能注销  
    会话。  

5. 文件上传：文件上传需要注意webshell等问题，本系统的解决方案是对上传的文件
	名丢弃，用用户在数据库中id来为文件命名，避免攻击。同时上传的文件的mode
	不可有执行权限。  

6. 防止暴力破解密码：通过频率控制来防止。  


###TODO###

为防止机器自动注册，可以考虑添加验证码功能，不过不能用第三方库，所以本系统目前不实现。  


安装说明
========

###安装###

1. 将如下的Apache配置文件中的`/var/www/yagra/`替换为yagra的绝对路径   

    <VirtualHost *:9090>                             
        ServerAdmin yagra_admin@163.com
        DocumentRoot /var/www/yagra/
        ServerName *
        ErrorLog logs/yagra-error_log
        CustomLog logs/yagra-access_log common
        Alias /yagra "/var/www/yagra/"
        AddType text/html .py
        AddType image/x-icon .ico
        <Directory "/var/www/yagra/">
            Options +ExecCGI
            AddHandler cgi-script .py
            Order allow,deny
            Allow from all
        </Directory>
    </VirtualHost>

2. 若更改了Alias /yagra的别名为其他，则需要在index.html更改  
    <meta HTTP-EQUIV="REFRESH" content="0; url=/yagra/app.py/">  
    的`yagra`为Alias的内容

3. 在`yagra/config/config.py` 进行配置各参数，主要是数据库参数。  


###参考###

[1]: https://crackstation.net/hashing-security.htm "Salted Password Hashing"  
[2]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9 "RFC2616"
[3]: http://stackoverflow.com/questions/49547/making-sure-a-web-page-is-not-cached-across-all-browsers
[4]: http://stackoverflow.com/questions/3137934/how-to-clear-browser-cache-when-re-uploading-image-with-same-filename-in-php
