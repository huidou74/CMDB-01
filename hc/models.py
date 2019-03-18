from django.db import models

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=32,null=False,verbose_name='用户名')
    password = models.CharField(max_length=128,null=False,verbose_name='用户密码')
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural = "主机用户表"


class Host(models.Model):
    '''主机,阿里云eth0 内网网卡， eth1 公网网卡'''
      # 发布用到的两个字段
    # salt_id =  models.CharField(max_length=32, blank=True, null=True, verbose_name="salt_id")
    # ip = models.CharField(max_length=64, blank=True, null=True, verbose_name='IP')

    id_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='ID名')
    hostname = models.CharField(max_length=64, blank=True, null=True, verbose_name='主机名')
    ecsname = models.CharField(max_length=64, blank=True, null=True, verbose_name='实例名')

    login_port = models.CharField(max_length=16, default='22', blank=True, null=True, verbose_name='登录端口')
    cpu = models.CharField(max_length=8, blank=True, null=True, verbose_name='CPU')

    mem = models.CharField(max_length=8, blank=True, null=True, verbose_name='内存')
    speed = models.CharField(max_length=8, blank=True, default='5', null=True, verbose_name='带宽')

    eth1_network = models.CharField(max_length=32, blank=True, null=True, verbose_name='公网IP')
    eth0_network = models.CharField(max_length=32, verbose_name='私网IP')
    sn = models.CharField(max_length=64, blank=True, null=True, verbose_name='SN')

    kernel = models.CharField(max_length=64, blank=True, null=True, verbose_name='内核版本')  # 内核+版本号

    remarks = models.CharField(max_length=2048, blank=True, null=True, verbose_name='备注')
    createtime = models.CharField(max_length=32, blank=True, null=True, verbose_name='创建时间')
    expirytime = models.CharField(max_length=32, blank=True, null=True, verbose_name='到期时间')

    #ForeignKey

    lab = models.ForeignKey(to='Lable',default=1,blank=True, null=True, verbose_name='标签')
    os = models.ForeignKey(to='Os',default=1,blank=True, null=True, verbose_name='操作系统')  # os+版本号
    # the_upper = models.ForeignKey(to='Host', blank=True, null=True, verbose_name='宿主机', related_name='upper')
    source = models.ForeignKey(to='Source',default=1,blank=True, null=True, verbose_name='来源IP')
    region = models.ForeignKey(to='Region', blank=True, null=True, verbose_name='所属区域')


    #  ManyToManyField
    logining = models.ManyToManyField(to='Login',default=1,  verbose_name='所属用户')
    disks = models.ManyToManyField(to='Disk',default=1,  verbose_name='磁盘')

    state_choices    = (
        (1, 'Running'),
        (2, '下线'),
        (3, '关机'),
        (4, '删除'),
    )
    state = models.SmallIntegerField(verbose_name='主机状态', default=3, blank=True, null=True, choices=state_choices, )

    def __str__(self):
        return self.hostname
    class Meta:
        verbose_name_plural = "主机表"


class Region(models.Model):
    name = models.CharField(max_length=64,blank=True,null=True,verbose_name='区域')
    def __str__(self):
        return self.name
    class Meat:
        verbose_name_plural = '区域名'

class Source(models.Model):
    '''来源：阿里云、物理机（某机房等）'''
    name = models.CharField(max_length=16, blank=True, null=True, verbose_name='来源')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "主机来源表"


class Disk(models.Model):
    '''磁盘'''
    path = models.CharField(max_length=64, blank=True, null=True, verbose_name='挂载路径')
    size = models.CharField(max_length=16, blank=True, null=True, verbose_name='磁盘大小/G')
    type = models.CharField(max_length=128, blank=True, null=True, verbose_name='磁盘类型')
    id_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='实例ID')
    remarks = models.CharField(max_length=2048, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.size

    class Meta:
        verbose_name_plural = "磁盘表"


class Os(models.Model):
    '''系统'''
    name = models.CharField(max_length=16, blank=True, null=True, verbose_name='系统名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "操作系统表"



class Lable(models.Model):
    # 标签
    name = models.CharField(max_length=16, blank=True, null=True, verbose_name='标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "标签"

class Attr(models.Model):
    name = models.CharField(max_length=64,blank=False,null=False, verbose_name='属性')
    db_name = models.OneToOneField(to='Db_name',blank=True,null=True, verbose_name='数据库字段')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '属性'

class Db_name(models.Model):
    name = models.CharField(max_length=32,blank=False,null=False, verbose_name='数据库字段')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '数据库字段'



#  权限设置


class UserInfo(models.Model):    # 登录用户表
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='登录用户名')
    passwd = models.CharField(max_length=128, blank=True, null=True, verbose_name='登录密码')
    department = models.CharField(max_length=32,default='Diaoderyours组', verbose_name='所属部门')
    # img = models.CharField(max_length=16, blank=True,null=True,verbose_name='用户头像')
    img = models.ForeignKey(to='User_Img' ,blank=True,null=True,verbose_name='用户头像', related_name='userimg')
    # ForeignKey   # 一个岗位 对 多个用户 一对多， foreignkey 的 放在 对多的表里    # 用 related_name 反向查找方便
    pos = models.ForeignKey(to='Position', blank=True, null=True, verbose_name='权限', related_name='userpos')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '用户表'

class User_Img(models.Model):
    images = models.CharField(max_length=64,blank=True,null=True,verbose_name='用户头像')
    def __str__(self):
        return self.images
    class Meta:
        verbose_name_plural = '用户头像图片'

class Position(models.Model):    # 岗位，职位 表
    name = models.CharField(max_length=32,blank=True, null=True, verbose_name='职位名')
    # pos_user = models.ForeignKey(to='UserInfo', blank=True, null=True, verbose_name='职位用户账号', related_name='posuser')
    # ManyToMany  # 多个职位  对应 多个权限                          # 用 related_name 反向查找方便
    auth = models.ManyToManyField(to='Auth', blank=True, null=True, verbose_name='权限', related_name='posauth')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '职位表'



class Auth(models.Model):    # 权限表
    url = models.CharField(max_length=128, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='显示标识')

    # ForeignKey   # 一个组 对应多个 权限                     # 用 related_name 反向查找方便
    group = models.ForeignKey(to='AuthGroup', blank=True, null=True, verbose_name='组', related_name='authgroup')
    to_display = models.ForeignKey(to='Auth', blank=True, null=True, verbose_name='显示', related_name='authauth')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '权限表'



class AuthGroup(models.Model):     # 组表
    name = models.CharField(max_length=16, blank=True, null=True, verbose_name='组名')

    # ForeignKey    # 一个组 对应 多个菜单
    ti = models.ForeignKey(to='Menu', blank=True, null=True, verbose_name='菜单', related_name='groupmenu')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '组表'



class Menu(models.Model):     # 菜单表
    title = models.CharField(max_length=32, blank=True, null=True, verbose_name='菜单名')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '菜单栏'




#   发布系统使用的表
class Use_Env(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='环境名')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '环境表'

class Publishing_Host(models.Model):
    # 发布用到的两个字段
    hostname = models.CharField(max_length=32, blank=True, null=True, verbose_name="salt_id")
    ip = models.CharField(max_length=64, blank=True, null=True, verbose_name='IP')

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name_plural = "主机表"


class Record_Log(models.Model):
    timestamp = models.CharField(max_length=64, blank=True, null=True, verbose_name='时间')
    project = models.ForeignKey(to='App', blank=True, null=True, verbose_name='项目', related_name='proj')
    package = models.ManyToManyField(to='Package', blank=True, null=True, verbose_name='包', related_name='pack')
    env = models.ForeignKey(to='Use_Env', blank=True, null=True, verbose_name='环境', related_name='env')

    def __str__(self):
        return self.timestamp

    class Meta:
        verbose_name_plural = '记录日志'


class App(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='应用名')
    path = models.CharField(max_length=64, blank=True, null=True, verbose_name='应用路径')
    environment = models.ForeignKey(to='Use_Env', blank=True, null=True, verbose_name='环境')
    hosts = models.ManyToManyField(to='Publishing_Host', blank=True, null=True, verbose_name='对应主机', related_name='apphost')
    # _script = models.CharField(max_length=32, blank=True, null=True, verbose_name='部署脚本')
    package = models.ForeignKey(to='Package', blank=True, null=True, verbose_name='代码', related_name='apppack')
    _app = models.ForeignKey(to='App', blank=True, null=True, verbose_name='上级应用')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '项目表'


class Package(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='包名/版本号')
    pack_path = models.CharField(max_length=64, blank=True, null=True, verbose_name='代码路径/地址')
    # project = models.ForeignKey(to='App', blank=True, null=True, verbose_name='所属项目', related_name='packapp')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '代码'

