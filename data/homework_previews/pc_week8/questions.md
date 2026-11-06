# Extracted source text

Source: course_materials/过程控制工程/homework/1202067/作业.pdf

Extraction generated mechanically. Check formulas and images against page previews.

Pages: 2


## Page 1

      仿真练习


              汽氨
      氨冷却器                                                       Lsp 液氨冷却器的液位-温
                 度超弛控制方案如图所
 工艺介质                          Lm                               LT        LC 示，请在附件
                                      25          25  PIDAmmoniaCooler.mdl
    TT              文件的基础上，按照下
     31                   u          一页的结构，搭建超弛       RFB                 RFB
                      FC  Tm               控制方案，并分析超弛

    TC                 控制效果，设计时注意              LS     31           液氨           u1Tsp                  液氨液位不能超过90
             u2                   (百分比)。并实现抗积
                 分饱和功能。
                                   ,  u         u = min ( u1                                    2 )


## Page 2

氨冷却器超弛控制