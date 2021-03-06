require(fpp)
data("elecequip")

#1
plot(elecequip, main = "Electrical equipment orders time series data")

#2
#Decomposing using stl()
decomp_stl <- stl(elecequip, s.window = "periodic")
plot(decomp_stl)

#3 
#Since, the data is seasonal plotting the seasonally adjusted data
seas_adj <- seasadj(decomp_stl)
plot(seas_adj)

#4
#Since, the time series data obtained from #3 has constant variance, no need to apply Box-Cox transformation.

#5
#The time series obtained is non-stationary due to the presence of seasonality.

#6
#Performing the unit root test to make the time series data stationary
ns <- nsdiffs(seas_adj)
if(ns > 0){
  seas_adjstar <- diff(seas_adj, lag = frequency(seas_adj), differences = ns)
} else{
  seas_adjstar <- seas_adj
}
nd <- ndiffs(seas_adjstar)
if(nd > 0){
  seas_adjstar <- diff(seas_adjstar, differences = nd)
}
plot(seas_adjstar)
acf(seas_adjstar)
#The plot obtained shows that the data is roughly horizontal and it lacks seasonality as well. Hence, it is a stationary data.

#7
# Applying auto.arima() on the tie series data obtained above to get the values of p,q and d.
arima_model <- auto.arima(seas_adjstar)
summary(arima_model)
# The values obtained are: (p,q,d) = (3,0,1) 

#8
arima1 <- Arima(seas_adjstar, order = c(4,0,0))
arima2 <- Arima(seas_adjstar, order = c(3,0,0)) 
arima3 <- Arima(seas_adjstar, order = c(2,0,0))
summary(arima1)
summary(arima2)
summary(arima3)
#Considering the AIC's generated by all the four models, the Arima(4,0,0) produces lowest AICc value. Hence, it is the better model.

#9
#Since, the best model is arima4, we exaine its residuals.
acf(arima4$residuals)
b.test <- Box.test(arima1$residuals)
b.test$p.value
#Since, the p-value obtained is equal to 0.998 meaning that it is insignificant proves that the null hypothesis stands correct.
#Hence, the residuals are white noise.

#10
#Since, the model is proper, we plot the forecast
plot(forecast(arima4))