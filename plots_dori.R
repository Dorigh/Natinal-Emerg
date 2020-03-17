library(sf)
library(maps)

# Tweet area
data_states <- read.csv("./files/States.csv")
sf_data<- st_as_sf(data_states, coords = c("Lon", "Lat"))
buffer <- st_buffer(sf_data, dist = 1.6) # unit 100km

par(mar = c(5,2,3,2))
map("state", plot = T, fill = TRUE, col = rainbow(50), lwd = 0.6)
plot(st_geometry(buffer), add = T, col = "snow", lwd = 0.7)
plot(st_geometry(sf_data), add = T, cex = 0.5, pch = 20)
title("Tweets Area", cex.main = 0.9)

# Analytical plots
data <- read.csv("./twitter_query.csv") # output of tweet.py
data <- data[-c(3,4)]
data <- data[order(data$state),]
data$num <- 1

data$day <- substr(data$date, 5, 10)
data <- data[!data$day %in% c("Mar 07","Mar 08"),]
data_st <- aggregate(data$num ~ data$state, FUN = sum)
colnames(data_st) <- c("state", "number")
data_st_less <- data_st[data_st$number < 700,]
data_st_less <- data_st_less[order(data_st_less$number),]
par(mar = c(7.5,4,4,2))
barplot(data_st$number, names.arg = data_st$state, col = terrain.colors(50), main = "State analysis \n(10 Mar - 16 Mar)", space = 0.75, las = 2)
barplot(data_st_less$number, ylim = c(0,800), names.arg = data_st_less$state, col = heat.colors(15), main = "State analysis \n(10 Mar - 16 Mar)", space = 0.75, las = 2)

data_day <- aggregate(data$num ~ data$day, FUN = sum)
colnames(data_day) <- c("day", "number")
par(mar = c(5,4,4,2))
barplot(data_day$number, ylim = c(4200,5100), names.arg = data_day$day, col = rainbow(10), main = "Number of Tweets per day", density = 40, las = 2, xpd = FALSE)

par(mfrow = c(2,2))
data_day_st <- aggregate(data$num ~ data$state + data$day, FUN = sum)
colnames(data_day_st) <- c("state", "day", "number")
dd <- data_day_st[data_day_st$state == "North Dakota",]
barplot(dd$number, names.arg = dd$day, col = heat.colors(7), main = "Number of Tweets per day \nin North Dakota", density = 50, las = 2)
dd <- data_day_st[data_day_st$state == "South Dakota",]
barplot(dd$number, names.arg = dd$day, col = heat.colors(7), main = "Number of Tweets per day \nin South Dakota", density = 50, las = 2)
dd <- data_day_st[data_day_st$state == "Montana",]
barplot(dd$number, names.arg = dd$day, col = heat.colors(7), main = "Number of Tweets per day \nin Montana", density = 50, las = 2)
dd <- data_day_st[data_day_st$state == "Idaho",]
barplot(dd$number, names.arg = dd$day, col = heat.colors(7), main = "Number of Tweets per day \nin Idaho", density = 50, las = 2)
