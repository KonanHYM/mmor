setwd("/Users/Konan/Desktop/github/mmor/quant")
BTCUSDT<-read.csv("BTCUSDT.csv", stringsAsFactors =F)
BTCUSDT$Date<-as.Date(BTCUSDT$time)
str(BTCUSDT)
Return_p<-diff(log(BTCUSDT$close_price))

plot(Return_p)
Close.ts<-ts(BTCUSDT$close_price,start=c(2015),freq=250) 
Close.ts
Return.ts<-ts(Return_p,start=c(2015),freq=250)
par(mfrow=c(2,1))
plot(Close.ts,type="l",main="(a) Daily Closing Price of Bitcoin",xlab="Date", ylab="Price", cex.main=0.95,las=1)
plot(Return.ts,type="l",main="(b) Daily Rate of Return of Bitcoin",xlab="Date", ylab="Rate", cex.main=0.95, las=1)

library(tseries)
library(astsa)

summary(Return_p)
hist(Return_p)   ##直方图
n<-length(Return_p)
u<-sum(Return_p)/n   ### 求均值
e<-sqrt(sum((Return_p-u)^2)/(n-1))  # 求标准差
s<-sum((Return_p-u)^3)/((n-1)*e^3)  # 求偏度
k<-sum((Return_p-u)^4)/((n-1)*e^4)  # 求峰度
jarque.bera.test(Return_p)         # JB正态性检验（拒绝原假设：收益率是正态分布）

par(mfrow=c(2,1))   
acf(Return_p,main='',xlab='Lag (a)',ylab='ACF',las=1) #画自相关图 
title(main='(a) the ACF of Return',cex.main=0.95)  #为图形加标题，并设置标题大小
pacf(Return_p,main='',xlab='Lag (b)',ylab='PACF',las=1) #画偏自相关图   
title(main='(b) the PACF of Return',cex.main=0.95)

acf2(Return_p)
#两个图大部分函数值在置信区间内（图中蓝色虚线区域）上下跳跃,所以收益率序列自相关性很低,
#或者说具有很弱的自相关性，因此在条件期望模型中不需要引入自相关性部分，满足 GARCH 模型中的均值方程，
#收益率由一个常数项加上一个随机扰动项组成。
#虽然收益率序列基本不具有自相关性，但是要拟合 GARCH 模型，我们还需要考察收益率平方的自相关性。

par(mfrow=c(2,1))  
Return_p.square<-Return_p^2
acf(Return_p.square,main='',xlab='Lag (c)',ylab='ACF',las=1)               
title(main='(a) the ACF of Return Square',cex.main=0.95)
pacf(Return_p.square,main='',xlab='Lag (d)',ylab='PACF',las=1)    
title(main='(b) the PACF of Return Square',cex.main=0.95)
#acf2(Return_p.square)

#尽管股价收益率序列的 ACF 值揭示了其弱相关性,但收益率平方的 ACF 值 却表现出了一定的相关性和持续性，
#其大部分值都超过了置信区间（图中蓝色虚线）。
#注意到收益率平方的 ACF 值在滞后 3、10、21、30 期后都有缓慢衰退,
#说明了方差序列具有一定程度的序列相关性,因此采用 GARCH 模型来描述价格波动过程中的条件方差。


###ARCH 效应的检验
#收益率的时序图表明，在日收益率数据中可能存在 ARCH 效应，
#如果存在 ARCH 效应，则可以进行 GARCH 模型的拟合。反之，不能用 GARCH 模型拟合方程。

#ARCH 效应的检验，可以用FinTS包中的LM 检验
library(zoo)
library(tseries)

ArchTest <- function (x, lags=12, demean = FALSE) 
{
  # Capture name of x for documentation in the output  
  xName <- deparse(substitute(x))
  # 
  x <- as.vector(x)
  if(demean) x <- scale(x, center = TRUE, scale = FALSE)
  #  
  lags <- lags + 1
  mat <- embed(x^2, lags)
  arch.lm <- summary(lm(mat[, 1] ~ mat[, -1]))
  STATISTIC <- arch.lm$r.squared * length(resid(arch.lm))
  names(STATISTIC) <- "Chi-squared"
  PARAMETER <- lags - 1
  names(PARAMETER) <- "df"
  PVAL <- 1 - pchisq(STATISTIC, df = PARAMETER)
  METHOD <- "ARCH LM-test;  Null hypothesis:  no ARCH effects"
  result <- list(statistic = STATISTIC, parameter = PARAMETER, 
                 p.value = PVAL, method = METHOD, data.name =
                   xName)
  class(result) <- "htest"
  return(result)
}

ArchTest(Return_p,lag=12)
#检验的原假设是：不存在 ARCH 效应。检验结果为卡方统计量的值为65.037，
#对应的 P 值几乎为0，也就是说在 1% 的显著性水平上拒绝原假设，
#从而拒绝不存在 ARCH 效应的假设，收益率序列存在 ARCH 效应，
#可以进行 GARCH 模型的拟合。


###GARCH 模型的估计

library(timeDate)
library(timeSeries)
library(fBasics)
library(fGarch)
library(forecast)

model.sel<-auto.arima(Return_p, trace = TRUE, ic="bic")#选取最优的ARMA模型 （0，0）
model.sel

m1<-garchFit(~arma(0,0)+garch(1,1),data=Return_p,trace=F) #拟合GARCH（1,1）模型
summary(m1)    #显示模型的详细拟合结果

predict_list = predict(m1, n.ahead = 10, plot = TRUE)
predict_list

m2<-garchFit(~arma(0,0)+garch(1,2),data=Return_p,trace=F) #拟合GARCH（1,2）模型
m3<-garchFit(~arma(0,0)+garch(2,1),data=Return_p,trace=F) #拟合GARCH（2,1）模型
m4<-garchFit(~arma(0,0)+garch(2,2),data=Return_p,trace=F) #拟合GARCH（2,2）模型

summary(m2)
summary(m3)
summary(m4)


####GARCH 模型的标准化残差分析
resi<-residuals(m1,standardize=T)   #获得标准化残差
res<-ts(resi,frequency=250,start=c(2000)) 

plot(res,xlab='Date',ylab='st.resi',type='l')
par(mfcol=c(2,2))

acf(resi,lag=24)
acf(resi^2,lag=24)

pacf(resi,lag=24)
pacf(resi^2,lag=24)


#Ljung-Box 自相关检验 不能拒绝原假设，原假设是不存在序列自相关，因而标准化残差平方不存在序列自相关性
Box.test(resi^2,lag=10,type='Ljung')  #残差平方的滞后10阶自相关检验
Box.test(resi^2,lag=15,type='Ljung')  #残差平方的滞后15阶自相关检验
Box.test(resi^2,lag=20,type='Ljung')  #残差平方的滞后20阶自相关检验

library(rugarch)

#SGARCH Model
spec1=ugarchspec(variance.model=list(model="sGARCH"), mean.model=list(armaOrder=c(1,1)))
fit1<-ugarchfit(data=Return_p,spec=spec1)
fit1

#对SGarch模型进行预测
forc_fit1 = ugarchforecast(fit1, n.head = 20)
forc_fit1



library(ggplot2)
p <- ggplot(forc_fit1, aes(x=time, y=price, colour=cyl)) +geom_point()
p



#SGARCH Model
spec2=ugarchspec(variance.model=list(model="sGARCH"), mean.model=list(armaOrder=c(1,1),archm=TRUE))
fit2=ugarchfit(data=Return_p,spec=spec2)
fit2

## Exponential GARCH models
spec3=ugarchspec(variance.model=list(model="eGARCH"), mean.model=list(armaOrder=c(1,1)))
fit3=ugarchfit(data=Return_p,spec=spec3)
fit3

## GJR-GARCH or TGARCH models
spec4=ugarchspec(variance.model=list(model="gjrGARCH"), mean.model=list(armaOrder=c(1,1)))
fit4=ugarchfit(data=Return_p,spec=spec4)
fit4
