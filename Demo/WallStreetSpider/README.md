# WallStreetSpider

(1)**多进程**：`multiprocessing.Process/multiprocessing.Pool`

(2)**多线程**：`threading.Thread`

全局变量由所有线程共享，多线程处理任务，
特别是对于全局变量修改的时候，我们往往要加线程锁，
保证在对某个全局变量修改的时候，只有一个线程接触到它。

`lock = threading.Lock()`

`lock.acquire() # 获取线程锁`                            

`xxxxxxxxxxx此处省略若干代码`

`lock.release() # 释放线程锁`

(3)**协程**：
Python能实现多个线程，但是实际上无法充分利用系统资源，
原因在于Python存在全局锁机制，即同一时刻在一个进程中只能有一个线程对数据进行操作。
所以实现并行效果，采用多进程方法，比较好。

协程在一定程度上解决了这个问题。
协程机制，即在运行某个任务的过程中，我们可以随时中断，去执行另一任务，也可能随时再回来执行老任务。这在网络传输，IO过程中很有用，特别是对于两个不相关的任务来说，使用协程能达到异步执行的效果。