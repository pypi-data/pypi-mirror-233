文件夹管理(doFolder)
====================

.. code:: bash

   pip install doFolder

使用方法
--------

导入
~~~~

.. code:: python

   import doFolder

部分功能
~~~~~~~~

-  ``Folder`` 指一个文件夹

   -  *参数* ``path`` 文件夹路径:``str|doFolder.Path``
   -  *参数* ``onlisten`` 是否监听比同步文件夹变动:``bool``
   -  *参数* ``scan`` 是否在现在扫描(否则会在访问时进行扫描)
   -  *属性* ``files`` 文件夹中的文件列表:``FileList``
   -  *属性* ``subfolder`` 文件夹中的子文件夹:``FolderList``
   -  *方法* ``hasFolder,hasFile`` 是否包括某个文件/文件夹,参数为
      ``str``\ 时默认匹配 ``.name``\ 属性
   -  *方法* ``remove,copy,move`` 文件夹操作
   -  *方法* ``search`` 搜索文件夹的内容

      -  *参数* ``condition`` 搜索条件:``List[UnformattedMatching]``
      -  *参数* ``aim`` 目标: ``"file"|"folder"|"both"``
      -  *参数* ``threaded`` 是否线程化 ``bool``
      -  *参数* ``threaded`` 最大线程数:``int``
      -  *返回* 搜索结果:``SearchResult``

-  ``File`` 指一个文件

   -  *参数* ``path`` 文件路径:``str|doFolder.Path``
   -  *方法* ``remove,copy,move`` 文件操作
   -  *属性* ``mode,ino,dev,uid,gid...`` 参见 ``os.stat``

-  ``Path`` 指一个路径:来自specialStr的路径 ``(0.0.10之后)``

-  ``compare``\ 提供比较文件夹的API

   -  *函数* ``compare`` 比较两个文件夹

      -  *参数* ``folder1&folder2`` *比较的文件夹:``Folder``*
      -  *参数* ``compareContent``
         文件内容的比较方法:``str|Callable[[doFolder.File,doFolder.File],bool]``
      -  *参数* ``threaded`` 是否线程化 ``bool``
      -  *参数* ``threaded`` 最大线程数:``int``
      -  *返回* 比较结果:``CompareResult``

命令行使用
~~~~~~~~~~

.. code:: bash

   compare Folder1 Folder2 [-c ] [-t [-n num]]

具体作用参见

.. code:: bash

   compare -h

关于作者
--------

作者主页\ `宽宽2007 <https://kuankuan2007.gitee.io>`__

本项目在\ `苟浩铭/文件夹管理
(gitee.com) <https://gitee.com/kuankuan2007/do-folder>`__\ 上开源

帮助文档参见\ `宽宽的帮助文档
(gitee.io) <https://kuankuan2007.gitee.io/docs/do-folder/>`__

pypi官网项目地址\ `Pypi <https://pypi.org/project/doFolder/>`__
