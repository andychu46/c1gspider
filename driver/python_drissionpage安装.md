# Linux 安装drissionpage 和chrome

## drissionpage
DrissionPage® 是一个基于 Python 的网页自动化工具。读作 “拽神”。

既能控制浏览器，也能收发数据包，还能把两者合而为一。

可兼顾浏览器自动化的便利性和 requests 的高效率。

功能强大，语法简洁优雅，代码量少，对新手友好。


### Drissionpage 官网
https://drissionpage.cn/


### 最新版本：4.1.1.2

操作系统：Windows、Linux 和 Mac

Python 版本：3.6 及以上

支持：Chromium 内核浏览器（如 Chrome 和 Edge）、electron 应用

### 安装 DrissionPage
请使用 pip 安装：
```
pip install DrissionPage
```

### 升级最新稳定版
```
pip install DrissionPage --upgrade
```

### 指定版本升级
```
pip install DrissionPage==4.0.0b17
```

##  安装chrome
https://www.google.cn/chrome/?hl=zh-CN&standalone=1

在页面左下方选择其他平台，选择 Chrome Linux（64位）版本
uname -m
x86_64


### 在centos7.9上

在老系统安装最新版会出现依赖glibc，2.25版本以上的才支持
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
yum install -y google-chrome-stable_current_x86_64.rpm

Error: Package: google-chrome-stable-139.0.7258.127-1.x86_64 (/google-chrome-stable_current_x86_64)
           Requires: libc.so.6(GLIBC_2.25)(64bit)
Error: Package: google-chrome-stable-139.0.7258.127-1.x86_64 (/google-chrome-stable_current_x86_64)
           Requires: libc.so.6(GLIBC_2.18)(64bit)
```


找一个适合centos7的老版本chrome
http://dist.control.lth.se/public/CentOS-7/x86_64/google.x86_64/

```
https://docs.centos.org/en-US/centos-linux/7/system-administrators-guide/packages/https://www.google.com/chrome/index.htm
wget http://dist.control.lth.se/public/CentOS-7/x86_64/google.x86_64/google-chrome-stable-102.0.5005.61-1.x86_64.rpm
yum install google-chrome-stable-102.0.5005.61-1.x86_64.rpm 
```


```
=============================================================================================================
 Package                   Arch     Version             Repository                                      Size
=============================================================================================================
Installing:
 google-chrome-stable      x86_64   102.0.5005.61-1     /google-chrome-stable-102.0.5005.61-1.x86_64   264 M
Installing for dependencies:
 liberation-fonts          noarch   1:1.07.2-16.el7     base                                            13 k
 liberation-narrow-fonts   noarch   1:1.07.2-16.el7     base                                           202 k
 vulkan                    x86_64   1.1.97.0-1.el7      base                                           3.6 M
 vulkan-filesystem         noarch   1.1.97.0-1.el7      base                                           6.3 k

Transaction Summary
=============================================================================================================
Install  1 Package (+4 Dependent packages)


Total size: 268 M
Total download size: 3.8 M
Installed size: 286 M
Is this ok [y/d/N]: y
Downloading packages:
(1/4): liberation-fonts-1.07.2-16.el7.noarch.rpm                                      |  13 kB  00:00:00     
(2/4): liberation-narrow-fonts-1.07.2-16.el7.noarch.rpm                               | 202 kB  00:00:00     
(3/4): vulkan-filesystem-1.1.97.0-1.el7.noarch.rpm                                    | 6.3 kB  00:00:00     
(4/4): vulkan-1.1.97.0-1.el7.x86_64.rpm                                               | 3.6 MB  00:00:00     
-------------------------------------------------------------------------------------------------------------
Total                                                                        6.2 MB/s | 3.8 MB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : vulkan-filesystem-1.1.97.0-1.el7.noarch                                                   1/5 
  Installing : vulkan-1.1.97.0-1.el7.x86_64                                                              2/5 
  Installing : 1:liberation-narrow-fonts-1.07.2-16.el7.noarch                                            3/5 
  Installing : 1:liberation-fonts-1.07.2-16.el7.noarch                                                   4/5 
  Installing : google-chrome-stable-102.0.5005.61-1.x86_64                                               5/5 
  Verifying  : vulkan-1.1.97.0-1.el7.x86_64                                                              1/5 
  Verifying  : 1:liberation-narrow-fonts-1.07.2-16.el7.noarch                                            2/5 
  Verifying  : 1:liberation-fonts-1.07.2-16.el7.noarch                                                   3/5 
  Verifying  : google-chrome-stable-102.0.5005.61-1.x86_64                                               4/5 
  Verifying  : vulkan-filesystem-1.1.97.0-1.el7.noarch                                                   5/5 

Installed:
  google-chrome-stable.x86_64 0:102.0.5005.61-1                                                              

Dependency Installed:
  liberation-fonts.noarch 1:1.07.2-16.el7           liberation-narrow-fonts.noarch 1:1.07.2-16.el7          
  vulkan.x86_64 0:1.1.97.0-1.el7                    vulkan-filesystem.noarch 0:1.1.97.0-1.el7    
```


### 在Rocky9上安装新版
yum install -y google-chrome-stable_current_x86_64.rpm

```
Dependencies resolved.
=============================================================================================================
 Package                                   Arch     Version                             Repository      Size
=============================================================================================================
Installing:
 google-chrome-stable                      x86_64   139.0.7258.127-1                    @commandline   115 M
Upgrading:
 llvm-libs                                 x86_64   19.1.7-1.el9                        appstream       57 M
Installing dependencies:
 ModemManager-glib                         x86_64   1.20.2-1.el9                        baseos         334 k
 adobe-source-code-pro-fonts               noarch   2.030.1.050-12.el9.1                baseos         831 k
 adwaita-cursor-theme                      noarch   40.1.1-3.el9                        appstream      623 k
 adwaita-icon-theme                        noarch   40.1.1-3.el9                        appstream       11 M
 alsa-lib                                  x86_64   1.2.13-2.el9                        appstream      506 k
 at-spi2-atk                               x86_64   2.38.0-4.el9                        appstream       86 k
 at-spi2-core                              x86_64   2.40.3-1.el9                        appstream      176 k
 atk                                       x86_64   2.36.0-5.el9                        appstream      270 k
 avahi-glib                                x86_64   0.8-22.el9_6.1                      appstream       14 k
 avahi-libs                                x86_64   0.8-22.el9_6.1                      baseos          66 k
 bluez-libs                                x86_64   5.72-4.el9                          baseos          81 k
 bubblewrap                                x86_64   0.4.1-8.el9_5                       baseos          49 k
 cairo                                     x86_64   1.17.4-7.el9                        appstream      659 k
 cairo-gobject                             x86_64   1.17.4-7.el9                        appstream       18 k
 colord-libs                               x86_64   1.4.5-6.el9_6                       appstream      228 k
 composefs-libs                            x86_64   1.0.8-1.el9                         appstream       53 k
 cups-libs                                 x86_64   1:2.3.3op2-33.el9                   baseos         261 k
 desktop-file-utils                        x86_64   0.26-6.el9                          appstream       72 k
 exempi                                    x86_64   2.6.0-0.2.20211007gite23c213.el9    appstream      523 k
 exiv2-libs                                x86_64   0.27.5-2.el9                        appstream      779 k
 fdk-aac-free                              x86_64   2.0.0-8.el9                         appstream      324 k
 flac-libs                                 x86_64   1.3.3-10.el9_2.1                    appstream      217 k
 flatpak-selinux                           noarch   1.12.9-4.el9_6                      appstream       20 k
 flatpak-session-helper                    x86_64   1.12.9-4.el9_6                      appstream       71 k
 fontconfig                                x86_64   2.14.0-2.el9_1                      appstream      274 k
 freetype                                  x86_64   2.10.4-10.el9_5                     baseos         386 k
 fribidi                                   x86_64   1.0.10-6.el9.2                      appstream       84 k
 fuse                                      x86_64   2.9.9-17.el9                        baseos          78 k
 gdk-pixbuf2                               x86_64   2.42.6-6.el9_6                      appstream      465 k
 gdk-pixbuf2-modules                       x86_64   2.42.6-6.el9_6                      appstream       83 k
 geoclue2                                  x86_64   2.6.0-8.el9_6.1                     appstream      122 k
 giflib                                    x86_64   5.2.1-9.el9                         appstream       48 k
 glib-networking                           x86_64   2.68.3-3.el9                        baseos         169 k
 graphene                                  x86_64   1.10.6-2.el9                        appstream       64 k
 graphite2                                 x86_64   1.3.14-9.el9                        baseos          94 k
 gsettings-desktop-schemas                 x86_64   40.0-6.el9                          baseos         667 k
 gsm                                       x86_64   1.0.19-6.el9                        appstream       33 k
 gstreamer1                                x86_64   1.22.12-3.el9                       appstream      1.4 M
 gstreamer1-plugins-base                   x86_64   1.22.12-4.el9                       appstream      2.2 M
 gtk-update-icon-cache                     x86_64   3.24.31-5.el9                       appstream       32 k
 gtk3                                      x86_64   3.24.31-5.el9                       appstream      4.8 M
 harfbuzz                                  x86_64   2.7.4-10.el9                        baseos         623 k
 hicolor-icon-theme                        noarch   0.17-13.el9                         appstream       66 k
 iso-codes                                 noarch   4.6.0-3.el9                         appstream      3.3 M
 jbigkit-libs                              x86_64   2.1-23.el9                          appstream       52 k
 json-glib                                 x86_64   1.6.6-1.el9                         baseos         151 k
 lcms2                                     x86_64   2.12-3.el9                          appstream      166 k
 libX11                                    x86_64   1.7.0-11.el9                        appstream      645 k
 libX11-common                             noarch   1.7.0-11.el9                        appstream      151 k
 libX11-xcb                                x86_64   1.7.0-11.el9                        appstream       10 k
 libXau                                    x86_64   1.0.9-8.el9                         appstream       30 k
 libXcomposite                             x86_64   0.4.5-7.el9                         appstream       23 k
 libXcursor                                x86_64   1.2.0-7.el9                         appstream       30 k
 libXdamage                                x86_64   1.1.5-7.el9                         appstream       22 k
 libXext                                   x86_64   1.3.4-8.el9                         appstream       39 k
 libXfixes                                 x86_64   5.0.3-16.el9                        appstream       19 k
 libXft                                    x86_64   2.3.3-8.el9                         appstream       61 k
 libXi                                     x86_64   1.7.10-8.el9                        appstream       39 k
 libXinerama                               x86_64   1.1.4-10.el9                        appstream       14 k
 libXrandr                                 x86_64   1.5.2-8.el9                         appstream       27 k
 libXrender                                x86_64   0.9.10-16.el9                       appstream       27 k
 libXtst                                   x86_64   1.2.3-16.el9                        appstream       20 k
 libXv                                     x86_64   1.0.11-16.el9                       appstream       18 k
 libXxf86vm                                x86_64   1.1.4-18.el9                        appstream       18 k
 libappstream-glib                         x86_64   0.7.18-5.el9_4                      appstream      386 k
 libasyncns                                x86_64   0.8-22.el9                          appstream       29 k
 libatomic                                 x86_64   11.5.0-5.el9_5                      baseos          25 k
 libcanberra                               x86_64   0.30-27.el9                         appstream       85 k
 libdrm                                    x86_64   2.4.123-2.el9                       appstream      158 k
 libepoxy                                  x86_64   1.5.5-4.el9                         appstream      244 k
 liberation-fonts                          noarch   1:2.1.3-5.el9                       appstream      6.7 k
 liberation-fonts-common                   noarch   1:2.1.3-5.el9                       appstream       13 k
 liberation-mono-fonts                     noarch   1:2.1.3-5.el9                       appstream      496 k
 liberation-sans-fonts                     noarch   1:2.1.3-5.el9                       appstream      600 k
 liberation-serif-fonts                    noarch   1:2.1.3-5.el9                       appstream      600 k
 libexif                                   x86_64   0.6.22-6.el9                        appstream      423 k
 libgexiv2                                 x86_64   0.12.3-1.el9                        appstream       81 k
 libglvnd                                  x86_64   1:1.3.4-1.el9                       appstream      133 k
 libglvnd-egl                              x86_64   1:1.3.4-1.el9                       appstream       36 k
 libglvnd-glx                              x86_64   1:1.3.4-1.el9                       appstream      140 k
 libgsf                                    x86_64   1.14.47-5.el9                       appstream      245 k
 libgudev                                  x86_64   237-1.el9                           baseos          35 k
 libgusb                                   x86_64   0.3.8-2.el9                         baseos          50 k
 libgxps                                   x86_64   0.3.2-3.el9                         appstream       78 k
 libicu                                    x86_64   67.1-10.el9_6                       baseos         9.6 M
 libiptcdata                               x86_64   1.0.5-10.el9                        appstream       60 k
 libjpeg-turbo                             x86_64   2.0.90-7.el9                        appstream      174 k
 libldac                                   x86_64   2.0.2.3-10.el9                      appstream       40 k
 libnotify                                 x86_64   0.7.9-8.el9                         appstream       43 k
 libogg                                    x86_64   2:1.3.4-6.el9                       appstream       32 k
 libosinfo                                 x86_64   1.10.0-1.el9                        appstream      312 k
 libpciaccess                              x86_64   0.16-7.el9                          baseos          26 k
 libproxy                                  x86_64   0.4.15-35.el9                       baseos          73 k
 librsvg2                                  x86_64   2.50.7-3.el9                        appstream      2.8 M
 libsbc                                    x86_64   1.4-9.el9                           appstream       44 k
 libsndfile                                x86_64   1.0.31-9.el9                        appstream      205 k
 libsoup                                   x86_64   2.72.0-10.el9_6.2                   appstream      388 k
 libstemmer                                x86_64   0-18.585svn.el9                     appstream       83 k
 libtheora                                 x86_64   1:1.1.1-31.el9                      appstream      163 k
 libtiff                                   x86_64   4.4.0-13.el9                        appstream      197 k
 libtool-ltdl                              x86_64   2.4.6-46.el9                        baseos          35 k
 libtracker-sparql                         x86_64   3.1.2-3.el9_1                       appstream      316 k
 libusbx                                   x86_64   1.0.26-1.el9                        baseos          75 k
 libvorbis                                 x86_64   1:1.3.7-5.el9                       appstream      192 k
 libwayland-client                         x86_64   1.21.0-1.el9                        appstream       33 k
 libwayland-cursor                         x86_64   1.21.0-1.el9                        appstream       18 k
 libwayland-egl                            x86_64   1.21.0-1.el9                        appstream       12 k
 libwayland-server                         x86_64   1.21.0-1.el9                        appstream       41 k
 libwebp                                   x86_64   1.2.0-8.el9                         appstream      276 k
 libxcb                                    x86_64   1.13.1-9.el9                        appstream      224 k
 libxkbcommon                              x86_64   1.0.3-4.el9                         appstream      132 k
 libxshmfence                              x86_64   1.3-10.el9                          appstream       12 k
 libxslt                                   x86_64   1.1.34-13.el9_6                     appstream      239 k
 low-memory-monitor                        x86_64   2.1-4.el9                           appstream       35 k
 mesa-dri-drivers                          x86_64   24.2.8-2.el9_6                      appstream      9.4 M
 mesa-filesystem                           x86_64   24.2.8-2.el9_6                      appstream       11 k
 mesa-libEGL                               x86_64   24.2.8-2.el9_6                      appstream      141 k
 mesa-libGL                                x86_64   24.2.8-2.el9_6                      appstream      169 k
 mesa-libgbm                               x86_64   24.2.8-2.el9_6                      appstream       36 k
 mesa-libglapi                             x86_64   24.2.8-2.el9_6                      appstream       44 k
 mesa-vulkan-drivers                       x86_64   24.2.8-2.el9_6                      appstream       11 M
 nspr                                      x86_64   4.35.0-17.el9_5                     appstream      134 k
 nss                                       x86_64   3.101.0-10.el9_5                    appstream      716 k
 nss-softokn                               x86_64   3.101.0-10.el9_5                    appstream      386 k
 nss-softokn-freebl                        x86_64   3.101.0-10.el9_5                    appstream      309 k
 nss-sysinit                               x86_64   3.101.0-10.el9_5                    appstream       18 k
 nss-util                                  x86_64   3.101.0-10.el9_5                    appstream       89 k
 openjpeg2                                 x86_64   2.4.0-8.el9                         appstream      161 k
 opus                                      x86_64   1.3.1-10.el9                        appstream      199 k
 orc                                       x86_64   0.4.31-8.el9                        appstream      182 k
 osinfo-db                                 noarch   20250124-2.el9.rocky.20250630       appstream      308 k
 osinfo-db-tools                           x86_64   1.10.0-1.el9                        appstream       68 k
 ostree-libs                               x86_64   2025.1-1.el9                        appstream      468 k
 pango                                     x86_64   1.48.7-3.el9                        appstream      297 k
 pipewire-jack-audio-connection-kit-libs   x86_64   1.0.1-1.el9                         appstream      134 k
 pipewire-libs                             x86_64   1.0.1-1.el9                         appstream      1.9 M
 pixman                                    x86_64   0.40.0-6.el9_3                      appstream      269 k
 polkit                                    x86_64   0.117-13.el9                        baseos         146 k
 polkit-libs                               x86_64   0.117-13.el9                        baseos         8.3 M
 poppler                                   x86_64   21.01.0-21.el9                      appstream      1.1 M
 poppler-data                              noarch   0.4.9-9.el9.0.1                     appstream      1.8 M
 poppler-glib                              x86_64   21.01.0-21.el9                      appstream      151 k
 pulseaudio-libs                           x86_64   15.0-3.el9                          appstream      663 k
 rtkit                                     x86_64   0.11-29.el9                         appstream       55 k
 shared-mime-info                          x86_64   2.1-5.el9                           baseos         372 k
 sound-theme-freedesktop                   noarch   0.8-17.el9                          appstream      377 k
 totem-pl-parser                           x86_64   3.26.6-2.el9                        appstream      130 k
 tracker                                   x86_64   3.1.2-3.el9_1                       appstream      538 k
 upower                                    x86_64   0.99.13-2.el9                       appstream      165 k
 vulkan-loader                             x86_64   1.4.304.0-1.el9                     appstream      149 k
 webkit2gtk3-jsc                           x86_64   2.48.5-1.el9_6                      appstream      8.5 M
 webrtc-audio-processing                   x86_64   0.3.1-8.el9.0.1                     appstream      303 k
 wireplumber                               x86_64   0.4.14-1.el9.0.1                    appstream       83 k
 wireplumber-libs                          x86_64   0.4.14-1.el9.0.1                    appstream      338 k
 xdg-dbus-proxy                            x86_64   0.1.3-1.el9                         appstream       41 k
 xdg-desktop-portal                        x86_64   1.12.6-1.el9                        appstream      367 k
 xdg-utils                                 noarch   1.1.3-13.el9_6                      appstream       71 k
 xkeyboard-config                          noarch   2.33-2.el9                          appstream      779 k
 xml-common                                noarch   0.6.3-58.el9                        appstream       31 k
Installing weak dependencies:
 abattis-cantarell-fonts                   noarch   0.301-4.el9                         appstream      364 k
 dconf                                     x86_64   0.40.0-6.el9                        appstream      109 k
 exiv2                                     x86_64   0.27.5-2.el9                        appstream      975 k
 flatpak                                   x86_64   1.12.9-4.el9_6                      appstream      1.7 M
 libcanberra-gtk3                          x86_64   0.30-27.el9                         appstream       31 k
 libproxy-webkitgtk4                       x86_64   0.4.15-35.el9                       appstream       21 k
 pipewire                                  x86_64   1.0.1-1.el9                         appstream      101 k
 pipewire-alsa                             x86_64   1.0.1-1.el9                         appstream       56 k
 pipewire-jack-audio-connection-kit        x86_64   1.0.1-1.el9                         appstream      8.1 k
 pipewire-pulseaudio                       x86_64   1.0.1-1.el9                         appstream      185 k
 polkit-pkla-compat                        x86_64   0.1-21.el9                          baseos          44 k
 tracker-miners                            x86_64   3.1.2-4.el9_3                       appstream      888 k
 xdg-desktop-portal-gtk                    x86_64   1.12.0-3.el9                        appstream      130 k

Transaction Summary
=============================================================================================================
Install  173 Packages
Upgrade    1 Package

Total size: 280 M
Total download size: 165 M
```

### 查看浏览器版本
```
which google-chrome
/bin/google-chrome
google-chrome --version 
Google Chrome 139.0.7258.127 
```

### 激活 conda 虚拟环境
conda info --envs
```
# conda environments:
#
base                 * /data/miniconda3
py385                  /data/miniconda3/envs/py385
```

conda activate py385

### 安装DrissionPage
pip install DrissionPage

### 升级最新稳定版
pip install DrissionPage --upgrade

### 查看DrissionPage版
pip list|grep DrissionPage
DrissionPage       4.1.1.2



### 编写测试脚本
```
#!/usr/bin/env python3
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://www.baidu.com')
print(page.html)
```

### 编写测试脚本2
```
#!/usr/bin/env python3
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage._functions.keys import Keys

co = ChromiumOptions()
co.headless(True)
co.set_argument('--no-sandbox') 
co.set_argument("--disable-gpu") 
co.incognito(True)

# 1、设置无头模式：co.headless(True)
# 2、设置无痕模式：co.incognito(True)
# 3、设置访客模式：co.set_argument('--guest')
# 4、设置请求头user-agent：co.set_user_agent()
# 5、设置指定端口号：co.set_local_port(7890)
# 6、设置代理：co.set_proxy('http://localhost:2222')
page = ChromiumPage(co)
url = "https://cn.bing.com/"
page.get(url, retry=1, interval=1, timeout=5)

page.wait.load_start()  # 等待页面加载完成
#css定位,也可以用xpath

print(page.title)
print(page.url)
print(page.html)
```


测试浏览器信息
curl https://bot.sannysoft.com/
