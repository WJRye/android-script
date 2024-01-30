# 在 Android 开发中 使用 Python 脚本

## 引言

在日常的 Android 项目开发中，我们通常会使用 adb 命令来获取连接设备的内存、屏幕、CPU等信息，也会使用 gradle 命令来获取项目构建相关的
projects、tasks、dependencies等信息，还会使用 git 命令来获取代码 commit、log、diff 等信息。这些信息的获取，每次都在command
中输入相关命令进行操作（有时命令记不住，还需要查询一下），重复的操作让人感到厌倦和疲乏。现在，可以尝试使用 python
来简化这一部分工作，将常用的执行命令封装到 python 脚本中，每次想要获取某个信息时，就直接执行相关 python
脚本。这样就可以省去开发中的细碎工作。（将脚本一次写好，使用到退休:)）

## python 环境

Python 3.9.6

## adb

在日常的 Android 项目开发中，通常使用 adb 命令来获取屏幕、设备、应用程序等信息。

在 adb 目录下，是用 Python 封装的常用 adb 命令脚本。

### getprop

获取设备的属性信息：

```
python3 getprop.py

输出结果：
//.....省略
[dalvik.vm.dexopt.secondary]: [true]
[dalvik.vm.heapgrowthlimit]: [384m]
[dalvik.vm.heapmaxfree]: [8m]
[dalvik.vm.heapminfree]: [2m]
[dalvik.vm.heapsize]: [512m]
[dalvik.vm.heapstartsize]: [8m]
[dalvik.vm.heaptargetutilization]: [0.75]
//.....省略
[ro.system.build.version.release]: [10]
[ro.system.build.version.sdk]: [29]
//.....省略
[ro.product.vendor.device]: [kirin980]
[ro.product.vendor.manufacturer]: [HUAWEI]
[ro.product.vendor.model]: [kirin980]
[ro.product.vendor.name]: [kirin980]
//.....省略
```

### mainacitivity

获取设备三方应用程序的 main activity：

```
python3 mainactivity.py

输出结果：
Package: com.dianping.v1, Main Activity: com.dianping.v1/.NovaMainActivity 
Package: com.tencent.mm, Main Activity: com.tencent.mm/.ui.LauncherUI 
Package: com.baidu.searchbox, Main Activity: com.baidu.searchbox/.SplashActivity 
Package: com.ss.android.article.news, Main Activity: com.ss.android.article.news/.activity.SplashActivity 
Package: com.UCMobile, Main Activity: com.UCMobile/.main.UCMobile 
//.....省略
```

### pm

获取设备上的三方应用程序包名：

```
python3 pm.py

输出结果：
package:com.dianping.v1
package:com.tencent.mm
package:com.baidu.searchbox
package:com.ss.android.article.news
package:com.UCMobile
package:com.huawei.browser.fa
package:com.ss.android.ugc.aweme
package:com.tencent.mobileqq
package:com.netease.newsreader.activity
package:com.suning.mobile.ebuy
//.....省略
```

### proc

获取关于系统和进程的信息：

```
python3 proc.py

输出结果：
系统的版本信息：
Linux version 4.14.116 (HarmonyOS@localhost) (Android (5484270 based on r353983c) clang version 9.0.3 (https://android.googlesource.com/toolchain/clang 745b335211bb9eadfa6aa6301f84715cee4b37c5) (https://android.googlesource.com/toolchain/llvm 60cf23e54e46c807513f7a36d0a7b777920b5881) (based on LLVM 9.0.3svn)) #1 SMP PREEMPT Wed Apr 19 17:33:59 CST 2023

--------------------------------------------------
CPU 信息：
Processor	: AArch64 Processor rev 0 (aarch64)
processor	: 0
BogoMIPS	: 3.84
Features	: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm lrcpc dcpop asimddp
CPU implementer	: 0x41
CPU architecture: 8
CPU variant	: 0x1
CPU part	: 0xd05
CPU revision	: 0
//.....省略
--------------------------------------------------
内存信息：
MemTotal:        5765848 kB
MemFree:          326496 kB
MemAvailable:     775392 kB
Buffers:            1720 kB
Cached:           740196 kB
//.....省略
--------------------------------------------------
当前运行的进程信息：
Name:	cat
Umask:	0000
State:	R (running)
Tgid:	13681
Ngid:	0
Pid:	13681
PPid:	8617
//.....省略
--------------------------------------------------
文件系统信息：
37 24 253:7 / / ro,relatime shared:1 - erofs /dev/block/dm-7 ro,seclabel,user_xattr,lz4asm
38 37 0:18 / /dev rw,nosuid,relatime shared:2 - tmpfs tmpfs rw,seclabel,size=2850668k,nr_inodes=712667,mode=755
//.....省略
```

如果需要单独获取某一项信息，可以使用：

- 系统的版本信息：`python3 proc.py version`
- CPU 信息：`python3 proc.py cpuinfo`
- 内存信息：`python3 proc.py meminfo`
- 当前运行的进程信息：`python3 proc.py status`
- 文件系统信息：`python3 proc.py mountinfo`

### screenshot

获取截屏文件，并在电脑上打开：

```
python3 screenshot.py

输出结果：
From: /sdcard/Pictures/Screenshots/Screenshot_20240129_120423.png, To: /Users/wangjiang/Desktop/Screenshot_20240129_120423.png
```

这个就不展示具体操作结果了。

### topactivity

获取设备当前应用程序当前activity：

```
python3 topactivity.py

输出结果：
ACTIVITY com.petal.litegames/com.huawei.litegames.LiteGamesActivity 5e73dc2 pid=16955
```

### wm

获取设备屏幕信息：

```
python3 wm.py

输出结果：
Physical size: 1080x2244

Physical density: 480
```

### adb

使用 `python3 adb.py` 是上面脚本的汇总，可以在命令行执行：

- 获取设备的属性信息：`python3 adb.py getprop`
- 获取设备三方应用程序的 main activity：`python3 adb.py mainacitivity`
- 获取设备上的三方应用程序包名：`python3 adb.py pm`
- 获取关于系统和进程的信息：`python3 adb.py proc`
- 获取截屏文件，并在电脑上打开：`python3 adb.py screenshot`
- 获取设备当前应用程序当前activity：`python3 adb.py topactivity`
- 获取设备屏幕信息：`python3 adb.py wm`

## gradle

在日常的 Android 项目开发中，通常使用 gradle 命令来获取项目 tasks、projects、dependencies等信息，或执行自定义的 task。

在 gradle 目录下，是用 Python 封装的 gradle 命令脚本：

- dependencies.py：将项目依赖信息保存到文件，并在浏览器中打开
- dependencyinsight.py：将项目中特定依赖项的详细信息保存到文件，并在浏览器中打开
- native_libs.py：与 native_libs.gradle 对应，将项目 so 依赖信息保存到 html 报告文件，并在浏览器中打开

### dependencies

使用 `python3 dependencies.py android_project_path`，android_project_path 为项目路径：

```
python3 dependencies.py /Users/wangjiang/Public/software/android-workplace/Demo

输出结果：
Report File Path: /Users/wangjiang/Public/software/android-workplace/Demo/build/reports/app-dependencies.txt

```

### dependencies

使用 `python3 dependencyinsight.py android_project_path dependency`，android_project_path 为项目路径，dependency 为需要查找的依赖库，比如 io.reactivex.rxjava3:rxjava：

```
python3 dependencyinsight.py /Users/wangjiang/Public/software/android-workplace/Demo io.reactivex.rxjava3:rxjava

输出结果：
Report File Path: /Users/wangjiang/Public/software/android-workplace/Demo/build/reports/app-dependencyInsight.txt

> Task :app:dependencyInsight
io.reactivex.rxjava3:rxjava:3.0.4
   variant "runtime" [
      org.gradle.status                                               = release (not requested)
      org.gradle.usage                                                = java-runtime
      org.gradle.libraryelements                                      = jar (not requested)
      org.gradle.category                                             = library (not requested)

      Requested attributes not found in the selected variant:
         com.android.build.api.attributes.BuildTypeAttr                  = release
         com.android.build.api.attributes.ProductFlavor:type             = apink
         org.gradle.jvm.environment                                      = android
         com.android.build.api.attributes.AgpVersionAttr                 = 7.2.2
         org.jetbrains.kotlin.platform.type                              = androidJvm
   ]
   Selection reasons:
      - By conflict resolution : between versions 3.0.4, 3.0.0 and 3.0.2

io.reactivex.rxjava3:rxjava:3.0.4
+--- releaseRuntimeClasspath
//......省略
```

### native_libs

#### 准备
1. 把文件 `native_libs.gradle` 放到 app 的 `build.gradle` 文件所在同级目录下，并在项目 `build.gradle` 中添加依赖： `apply from: "./native_libs.gradle"`
2. 执行 `native_libs.py` 需要安装库 `numpy` 

注意：在 `native_libs.gradle` 中定义了 so 依赖信息的输出路径：`project.buildDir.path + "/reports/so" + "/native_libs.json"`，确保 `native_libs.py` 中能读到正确的 json 路径

---

使用 `python3 native_libs.py android_project_path`，android_project_path 为项目路径：

```
python3 native_libs.py /Users/wangjiang/Public/software/android-workplace/Demo

输出结果：
Report File Path: /Users/wangjiang/Public/software/android-workplace/Demo/build/report/so/native_libs.html
```
<img src="./assets/native_libs.png" alt="native_libs 信息">

## git
